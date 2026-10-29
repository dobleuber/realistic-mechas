"""
Pares articulares por dinámica inversa: lo que necesita un mecha bien controlado
para seguir un plan de marcha.

La simulación directa mide los pares que aplica un controlador concreto (servos
de posición rígidos). Con cuatro patas el reparto de fuerzas entre los pies es
indeterminado y, con patas casi rectas, un servo de posición rígido convierte
errores de milímetros en fuerzas enormes. Eso es un defecto del controlador, no
una exigencia de la máquina. Aquí se calcula el par necesario de forma ideal:

1. Con el plan (posiciones, velocidades y aceleraciones del cuerpo y de las
   articulaciones), mj_inverse da las fuerzas generalizadas necesarias.
2. Las fuerzas de los pies apoyados equilibran las 6 componentes de la base
   flotante. Entre todas las soluciones se elige la más cercana a un reparto
   preferido: el peso según el ZMP y cada fuerza apuntando a su cadera (la pata
   trabaja como un puntal). También hay momentos en cada pie, con penalización.
   Cada pie que se está descargando para despegar se penaliza en proporción.
3. El par de cada articulación es el resto: tau = qfrc_inverse - J^T f.

Se comprueba además que el centro de presiones de cada pie queda dentro de la
suela y que no hace falta más rozamiento que mu = 0.6.
"""
from __future__ import annotations

import math
import os
import sys

import mujoco
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from quad_model import JOINTS as QJ, LEGS, QuadParams, build_quad_mjcf  # noqa: E402
from quad_walk import load_share  # noqa: E402

G = 9.81


def _derivs(x, dt):
    v = np.gradient(x, dt, axis=0)
    return v, np.gradient(v, dt, axis=0)


def solve_contacts(Jb, rhs, f_pref, wts, n, w_m=30.0, w_xy=None):
    """min Σ wts_i |f_i - f_pref_i|² + w_m·Σ|m_i|²  s.a.  Jb·[f; m] = rhs  (6 ecuaciones de la base).

    Jb: (6, 6n) con columnas [f_1(3) .. f_n(3), m_1(3) .. m_n(3)]. w_xy: peso extra de las componentes
    horizontales de cada pie (para que un pie casi descargado no reciba fuerzas que el rozamiento no da)."""
    wf = np.repeat(wts, 3).astype(float)
    if w_xy is not None:
        wf = wf * np.repeat(np.column_stack([w_xy, w_xy, np.ones(n)]), 1, axis=0).ravel()
    Wd = np.concatenate([wf, np.full(3 * n, w_m)])
    x0 = np.concatenate([f_pref.ravel(), np.zeros(3 * n)])
    Winv = 1.0 / Wd
    A = Jb
    S = (A * Winv) @ A.T + 1e-12 * np.eye(6)
    lam = np.linalg.solve(S, rhs - A @ x0)
    return x0 + Winv * (A.T @ lam)


def solve_min_torque(Jb, rhs, G, qf_j, x0, R):
    """min |qf_j - G x|² + (x - x0)ᵀ R (x - x0)  s.a.  Jb x = rhs.

    Reparto de fuerzas de contacto que minimiza los pares articulares (lo que haría un control de fuerza
    de cuerpo entero), con una regularización R hacia el reparto preferido x0."""
    n = len(x0)
    K = np.zeros((n + 6, n + 6))
    K[:n, :n] = 2 * (G.T @ G + R)
    K[:n, n:] = Jb.T
    K[n:, :n] = Jb
    r = np.concatenate([2 * (G.T @ qf_j + R @ x0), rhs])
    return np.linalg.lstsq(K, r, rcond=None)[0][:n]


def quad_id(pl, arch: dict | None = None, H: float = 1.75, M: float = 100.0, mu: float = 0.6, strut: bool = True,
            w_m: float = 10.0, mode: str = "min_torque"):
    """Dinámica inversa del cuadrúpedo para un QuadPlan (a escala humana, H = 1.75 m).

    mode = "min_torque": reparto de fuerzas que minimiza los pares (por defecto).
    mode = "strut": reparto más cercano al preferido (peso según el ZMP, fuerzas hacia la cadera)."""
    arch = dict(arch or {})
    qp = QuadParams(H=H, M=M, **arch)
    model = mujoco.MjModel.from_xml_string(build_quad_mjcf(qp))
    data = mujoco.MjData(model)
    dt = pl.t[1] - pl.t[0]
    N = len(pl.t)
    jadr = np.array([model.joint(j).qposadr[0] for j in QJ])
    vadr = np.array([model.joint(j).dofadr[0] for j in QJ])
    qpos = np.zeros((N, model.nq))
    qpos[:, :3] = pl.body
    qpos[:, 3] = 1.0
    qpos[:, jadr] = pl.q
    vb, ab = _derivs(pl.body, dt)
    vq, aq = _derivs(pl.q, dt)
    sole = [model.site(f"sole_{lg}").id for lg in LEGS]
    foot_body = [model.body(f"foot_{lg}").id for lg in LEGS]
    thigh_body = [model.body(f"thigh_{lg}").id for lg in LEGS]
    W = M * G
    fl, fw = qp.foot_len, qp.foot_wid
    tau = np.zeros((N, len(QJ)))
    F = np.zeros((N, 4, 3))
    cop_ratio = np.zeros(N)
    fric_ratio = np.zeros(N)
    jacp = np.zeros((3, model.nv))
    jacr = np.zeros((3, model.nv))
    for k in range(N):
        data.qpos[:] = qpos[k]
        data.qvel[:] = 0
        data.qvel[0:3] = vb[k]
        data.qvel[vadr] = vq[k]
        data.qacc[:] = 0
        data.qacc[0:3] = ab[k]
        data.qacc[vadr] = aq[k]
        mujoco.mj_inverse(model, data)
        qf = data.qfrc_inverse.copy()
        w = pl.wload[k].copy()
        sw = pl.swing4[k] if hasattr(pl, "swing4") else np.array([pl.swing[k] == i for i in range(4)])
        st = [i for i in range(4) if not sw[i] and w[i] > 1e-4]
        if not st:
            continue
        n = len(st)
        P = np.array([data.site_xpos[sole[i]][:2] for i in range(4)])
        lam = load_share(P, pl.zmp[k], np.where([i in st for i in range(4)], np.maximum(w, 1e-3), 0.0))
        Fz_tot = qf[2]
        f_pref = np.zeros((n, 3))
        Jcols = []
        for j, i in enumerate(st):
            hip = data.xpos[thigh_body[i]]
            ps = data.site_xpos[sole[i]]
            d = hip - ps
            f_pref[j, 2] = lam[i] * Fz_tot
            if strut and d[2] > 1e-9:
                f_pref[j, :2] = f_pref[j, 2] * d[:2] / d[2]
            mujoco.mj_jac(model, data, jacp, jacr, ps, foot_body[i])
            Jcols.append((jacp.copy(), jacr.copy()))
        Jb = np.zeros((6, 6 * n))
        for j, (Jp, Jr) in enumerate(Jcols):
            Jb[:, 3 * j:3 * j + 3] = Jp[:, :6].T
            Jb[:, 3 * n + 3 * j:3 * n + 3 * j + 3] = Jr[:, :6].T
        wts = np.array([1.0 / max(w[i], 1e-3) for i in st])
        # un momento en el pie equivale a desplazar el centro de presiones; se encarece en proporción al
        # tamaño de la suela para que el reparto se haga con fuerzas y no con momentos imposibles
        w_xy = (0.25 * Fz_tot / np.maximum(f_pref[:, 2], 0.05 * abs(Fz_tot))) ** 2
        if mode == "strut":
            x = solve_contacts(Jb, qf[:6], f_pref, wts, n, w_m=w_m / (0.5 * fl) ** 2, w_xy=w_xy)
        else:
            # matriz que lleva fuerzas y momentos de contacto a pares articulares
            Gm = np.zeros((len(vadr), 6 * n))
            for j, (Jp, Jr) in enumerate(Jcols):
                Gm[:, 3 * j:3 * j + 3] = Jp[:, vadr].T
                Gm[:, 3 * n + 3 * j:3 * n + 3 * j + 3] = Jr[:, vadr].T
            # regularización (en unidades de par: fuerza × L, momento × L/(media suela)): mantiene el
            # reparto cerca del preferido, encarece los momentos en el pie y las fuerzas horizontales en
            # pies poco cargados, y evita cargar los pies que se están descargando
            Lr = qp.leg_len
            reg_f = 1e-2 * Lr ** 2 * np.concatenate([np.repeat(wts, 3) * np.repeat(np.column_stack(
                [w_xy, w_xy, np.ones(n)]), 1, axis=0).ravel()])
            reg_m = w_m * (Lr / (0.5 * fl)) ** 2 * np.ones(3 * n)
            R = np.diag(np.concatenate([reg_f, reg_m]))
            x0 = np.concatenate([f_pref.ravel(), np.zeros(3 * n)])
            x = solve_min_torque(Jb, qf[:6], Gm, qf[vadr], x0, R)
        gen = np.zeros(model.nv)
        for j, (Jp, Jr) in enumerate(Jcols):
            f = x[3 * j:3 * j + 3]
            m = x[3 * n + 3 * j:3 * n + 3 * j + 3]
            gen += Jp.T @ f + Jr.T @ m
            F[k, st[j]] = f
            if f[2] > 0.1 * W:
                cop_ratio[k] = max(cop_ratio[k], abs(m[1]) / (f[2] * fl / 2), abs(m[0]) / (f[2] * fw / 2))
                fric_ratio[k] = max(fric_ratio[k], np.hypot(f[0], f[1]) / (mu * f[2]))
        tau[k] = (qf - gen)[vadr]
    return {"t": pl.t, "tau": tau, "qvel": vq, "F": F, "cop_ratio": cop_ratio, "fric_ratio": fric_ratio,
            "W": W, "H": H}


def biped_id(pl, H: float = 1.75, M: float = 70.0, mode: str = "min_torque", w_m: float = 1.0):
    """Lo mismo para el bípedo (GaitPlan de gait.plan). En doble apoyo el reparto es el que deja el CoP
    de cada pie lo más centrado posible."""
    from mech_model import JOINTS as BJ, MechParams, build_mjcf
    mp = MechParams(H=H, M=M)
    model = mujoco.MjModel.from_xml_string(build_mjcf(mp))
    data = mujoco.MjData(model)
    dt = pl.t[1] - pl.t[0]
    N = len(pl.t)
    jadr = np.array([model.joint(j).qposadr[0] for j in BJ])
    vadr = np.array([model.joint(j).dofadr[0] for j in BJ])
    vb, ab = _derivs(pl.pelvis, dt)
    vq, aq = _derivs(pl.q, dt)
    sole = [model.site("sole_L").id, model.site("sole_R").id]
    fb = [model.body("foot_L").id, model.body("foot_R").id]
    W = M * G
    tau = np.zeros((N, len(BJ)))
    F = np.zeros((N, 2, 3))
    jacp = np.zeros((3, model.nv))
    jacr = np.zeros((3, model.nv))
    for k in range(N):
        data.qpos[:] = 0
        data.qpos[:3] = pl.pelvis[k]
        data.qpos[3] = 1.0
        data.qpos[jadr] = pl.q[k]
        data.qvel[:] = 0
        data.qvel[:3] = vb[k]
        data.qvel[vadr] = vq[k]
        data.qacc[:] = 0
        data.qacc[:3] = ab[k]
        data.qacc[vadr] = aq[k]
        mujoco.mj_inverse(model, data)
        qf = data.qfrc_inverse.copy()
        sup = pl.support[k]
        st = [0, 1] if sup == 0 else ([0] if sup == 1 else [1])
        # pies que de verdad tocan el suelo: el pie en vuelo levantado no
        st = [i for i in st if pl.feet[k, i, 2] < 1e-6]
        n = len(st)
        f_pref = np.zeros((n, 3))
        if n == 2:
            P = np.array([data.site_xpos[sole[i]][:2] for i in st])
            e = P[1] - P[0]
            s_ = np.clip(np.dot(pl.zmp[k] - P[0], e) / max(np.dot(e, e), 1e-12), 0, 1)
            f_pref[:, 2] = qf[2] * np.array([1 - s_, s_])
        else:
            f_pref[0, 2] = qf[2]
        Jcols = []
        for i in st:
            mujoco.mj_jac(model, data, jacp, jacr, data.site_xpos[sole[i]], fb[i])
            Jcols.append((jacp.copy(), jacr.copy()))
        Jb = np.zeros((6, 6 * n))
        for j, (Jp, Jr) in enumerate(Jcols):
            Jb[:, 3 * j:3 * j + 3] = Jp[:, :6].T
            Jb[:, 3 * n + 3 * j:3 * n + 3 * j + 3] = Jr[:, :6].T
        if mode == "min_torque" and n == 2:
            Gm = np.zeros((len(vadr), 6 * n))
            for j, (Jp, Jr) in enumerate(Jcols):
                Gm[:, 3 * j:3 * j + 3] = Jp[:, vadr].T
                Gm[:, 3 * n + 3 * j:3 * n + 3 * j + 3] = Jr[:, vadr].T
            Lr = mp.thigh + mp.shank
            fl = mp.foot_len
            R = np.diag(np.concatenate([1e-2 * Lr ** 2 * np.ones(3 * n), w_m * (Lr / (0.5 * fl)) ** 2 * np.ones(3 * n)]))
            x0 = np.concatenate([f_pref.ravel(), np.zeros(3 * n)])
            x = solve_min_torque(Jb, qf[:6], Gm, qf[vadr], x0, R)
        else:
            x = solve_contacts(Jb, qf[:6], f_pref, np.ones(n), n, w_m=1.0)
        gen = np.zeros(model.nv)
        for j, (Jp, Jr) in enumerate(Jcols):
            f = x[3 * j:3 * j + 3]
            m = x[3 * n + 3 * j:3 * n + 3 * j + 3]
            gen += Jp.T @ f + Jr.T @ m
            F[k, st[j]] = f
        tau[k] = (qf - gen)[vadr]
    return {"t": pl.t, "tau": tau, "qvel": vq, "F": F, "W": W, "H": H}


def id_metrics(r, joints, t_from=0.5):
    """Pares pico normalizados (× peso · H), carga pico por pie y potencias, como en quad_experiments."""
    W, H = r["W"], r["H"]
    m = r["t"] > t_from
    tau, qv = r["tau"][m], r["qvel"][m]
    peak = {}
    for d, key in (("hip_pitch", "hip"), ("knee", "knee"), ("ankle_pitch", "ankle"), ("hip_roll", "hip_roll"),
                   ("ankle_roll", "ankle_roll")):
        idx = [i for i, j in enumerate(joints) if j.startswith(d + "_")]
        peak[key] = float(np.abs(tau[:, idx]).max() / (W * H))
    P = tau * qv
    out = {"par": peak, "grf_pie": float(r["F"][m][:, :, 2].max() / W),
           "p_pico": float(np.abs(P).sum(1).max() / (W * math.sqrt(G * H))),
           "p_media": float(np.clip(P, 0, None).sum(1).mean() / (W * math.sqrt(G * H)))}
    if "cop_ratio" in r:
        out["cop_max"] = float(r["cop_ratio"][m].max())
        out["rozamiento_max"] = float(r["fric_ratio"][m].max())
    return out
