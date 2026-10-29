"""
Marcha estáticamente estable (paso de gateo, "crawl") del mecha cuadrúpedo y su
simulación en MuJoCo.

Secuencia lateral, como el paso de los mamíferos: trasera izquierda, delantera
izquierda, trasera derecha, delantera derecha. Siempre hay tres patas apoyadas
(factor de apoyo ≥ 0.75, McGhee y Frank 1968). Mientras vuela cada pata, el
punto de momento cero (ZMP) se coloca en el avance nominal del cuerpo proyectado
sobre el triángulo de apoyo de las otras tres, reducido en un margen de
seguridad: el cuerpo avanza de forma continua y solo se desplaza lo necesario.
El centro de masa sale del mismo control predictivo que usa el bípedo (Kajita et
al. 2003) y la cinemática inversa de cada pata es la del bípedo.

Valores por defecto: el «gateo lento» de la comparación (zancada 0.24 H por
ciclo, vuelo de 0.7 s a escala humana, 45 % de la velocidad del bípedo). Con
zancadas de 0.30 H o cuerpos más altos, la pata llega a estirarse del todo.
"""
from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

import mujoco
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from gait import LegIK, min_jerk, zmp_preview  # noqa: E402
from quad_model import DOFS, JOINTS, LEGS, QuadParams, build_quad_mjcf  # noqa: E402

H0 = 1.75
G = 9.81
SEQ = ("LH", "LF", "RH", "RF")


@dataclass
class QuadGait:
    stride: float = 0.24        # avance de cada pata por ciclo [× H]
    t_sw: float = 0.7           # vuelo de cada pata [s, escala humana]
    t_q: float = 0.15           # transferencia con cuatro apoyos antes de cada vuelo [s]
    n_cycles: int = 3            # ciclos completos, sin contar arranque y parada
    clearance: float = 0.035    # [× H]
    hip_drop: float = 0.06      # cuánto se agacha el cuerpo respecto a la pata estirada [× H]
    t_init: float = 1.0
    t_end: float = 1.5
    dt: float = 0.005
    preview: float = 1.6
    DX: float = 0.53
    WY: float = 0.13
    margin: float = 0.03        # margen de estabilidad estática: el ZMP queda a esta distancia de los bordes del triángulo [× H]


@dataclass
class QuadPlan:
    t: np.ndarray
    q: np.ndarray            # (N, 20) en el orden de JOINTS
    body: np.ndarray         # (N, 3)
    com: np.ndarray
    zmp: np.ndarray
    feet: np.ndarray         # (N, 4, 3) tobillos en el orden de LEGS
    swing: np.ndarray        # (N,) índice de la pata en vuelo, -1 si cuatro apoyos
    wload: np.ndarray        # (N, 4) peso de cada pata en el reparto de carga (0 = sin carga)
    dvec: np.ndarray         # (N, 4, 3) vector cadera -> tobillo de cada pata
    qd: np.ndarray           # (N, 20) velocidades articulares planificadas [rad/s, escala humana]
    speed: float
    duty: float


def plan_quad(gp: QuadGait = QuadGait()) -> QuadPlan:
    p = QuadParams(H=H0, M=70.0, DX=gp.DX, WY=gp.WY)
    model = mujoco.MjModel.from_xml_string(build_quad_mjcf(p))
    data = mujoco.MjData(model)
    ik = LegIK(p)
    dt = gp.dt
    S = gp.stride * H0
    foot_cx = p.foot_len * 0.25
    hip_z = p.leg_len - gp.hip_drop * H0

    hips = {lg: np.array(p.hip_pos(lg)) for lg in LEGS}
    feet = {lg: np.array([hips[lg][0], hips[lg][1], 0.0]) for lg in LEGS}

    def sole(lg):
        return np.array([feet[lg][0] + foot_cx, feet[lg][1]])

    def tri_target(sw, x_sw_mid):
        """ZMP para el vuelo de `sw`: el avance nominal (centro de los cuatro pies, con el que vuela en la
        mitad de su recorrido) proyectado sobre el triángulo de apoyo reducido en `margin`. Así el cuerpo
        avanza de forma continua y solo se desplaza lo necesario para quedar dentro del triángulo."""
        pts = [sole(lg) for lg in LEGS if lg != sw]
        nom = np.mean([sole(lg) if lg != sw else np.array([x_sw_mid + foot_cx, feet[lg][1]]) for lg in LEGS], axis=0)
        return project_triangle(nom, *inset_triangle(*pts, gp.margin * H0))

    def all_center():
        return np.mean([sole(lg) for lg in LEGS], axis=0)

    zmp_l, feet_l, sw_l, w_l = [], [], [], []
    wl = {lg: 1.0 for lg in LEGS}

    def push(n, zfn, sw=-1, swing_fn=None, wfn=None):
        for k in range(n):
            tau = k / max(n - 1, 1)
            if swing_fn:
                swing_fn(tau)
            if wfn:
                wfn(tau)
            zmp_l.append(zfn(tau))
            feet_l.append([feet[lg].copy() for lg in LEGS])
            sw_l.append(sw)
            w_l.append([wl[lg] for lg in LEGS])

    push(int(gp.t_init / dt), lambda tau: all_center())
    prev = all_center()
    landed = None   # pata que acaba de apoyar y debe recuperar carga
    # arranque y parada: en el primer ciclo las patas avanzan 1/4, 2/4, 3/4 y 4/4 de zancada para
    # quedar escalonadas como en la marcha estacionaria; en el último se cierran con 3/4, 2/4, 1/4 y 0.
    cycles = [[(i + 1) / 4 for i in range(4)]] + [[1.0] * 4] * gp.n_cycles + [[(3 - i) / 4 for i in range(4)]]
    for frac in cycles:
        for lg, f in zip(SEQ, frac):
            if f == 0:
                continue
            a, b = prev.copy(), tri_target(lg, feet[lg][0] + 0.5 * f * S)

            def wfn(tau, lg=lg, landed=landed):
                # reparto de carga: la pata que va a despegar se descarga y la que acaba de apoyar se carga
                wl[lg] = 1 - min_jerk(tau)
                if landed and landed != lg:
                    wl[landed] = min_jerk(tau)

            push(int(gp.t_q / dt), lambda tau, a=a, b=b: a + (b - a) * min_jerk(tau), wfn=wfn)
            x0 = feet[lg][0]

            def swing_fn(tau, lg=lg, x0=x0, f=f):
                feet[lg][0] = x0 + f * S * min_jerk(tau)
                feet[lg][2] = gp.clearance * H0 * 0.5 * (1 - math.cos(2 * math.pi * tau))

            push(int(gp.t_sw / dt), lambda tau, b=b: b, LEGS.index(lg), swing_fn)
            feet[lg][2] = 0.0
            prev = b
            landed = lg
    a = prev.copy()

    def wfn_end(tau, landed=landed):
        wl[landed] = min_jerk(tau)

    push(int(2 * gp.t_q / dt), lambda tau, a=a: a + (all_center() - a) * min_jerk(tau), wfn=wfn_end)
    push(int(gp.t_end / dt), lambda tau: all_center())

    zmp = np.array(zmp_l)
    feet_arr = np.array(feet_l)
    N = len(zmp)
    t = np.arange(N) * dt

    jadr = [model.joint(j).qposadr[0] for j in JOINTS]

    def pose(body_xyz, k):
        qk = []
        for i, lg in enumerate(LEGS):
            hip = body_xyz + np.array([hips[lg][0], hips[lg][1], 0.0])
            ank = feet_arr[k, i] + np.array([0, 0, p.ankle_h])
            qk.append(ik.solve(ank - hip))
        return np.concatenate(qk)

    data.qpos[:3] = [0, 0, hip_z]
    data.qpos[3:7] = [1, 0, 0, 0]
    data.qpos[jadr] = pose(np.array([0, 0, hip_z]), 0)
    mujoco.mj_kinematics(model, data)
    mujoco.mj_comPos(model, data)
    zc = data.subtree_com[0][2]
    com = zmp_preview(zmp, zc, dt, gp.preview)

    q = np.zeros((N, len(JOINTS)))
    body = np.zeros((N, 3))
    dvec = np.zeros((N, 4, 3))
    offset = np.zeros(2)
    for k in range(N):
        target = com[k]
        pxy = target - offset
        for _ in range(4):
            bpos = np.array([pxy[0], pxy[1], hip_z])
            qk = pose(bpos, k)
            data.qpos[:3] = bpos
            data.qpos[3:7] = [1, 0, 0, 0]
            data.qpos[jadr] = qk
            mujoco.mj_kinematics(model, data)
            mujoco.mj_comPos(model, data)
            err = target - data.subtree_com[0][:2]
            pxy = pxy + err
            if np.linalg.norm(err) < 1e-6:
                break
        offset = target - pxy
        q[k] = qk
        body[k] = bpos
        for i, lg in enumerate(LEGS):
            dvec[k, i] = feet_arr[k, i] + np.array([0, 0, p.ankle_h]) - (bpos + np.array([hips[lg][0], hips[lg][1], 0.0]))

    cycle = 4 * (gp.t_sw + gp.t_q)
    return QuadPlan(t=t, q=q, body=body, com=com, zmp=zmp, feet=feet_arr, swing=np.array(sw_l),
                    wload=np.array(w_l), dvec=dvec, qd=np.gradient(q, dt, axis=0),
                    speed=S / cycle, duty=1 - gp.t_sw / cycle)


def leg_ik(ik: LegIK, d: np.ndarray, kdir: int) -> np.ndarray:
    """Cinemática inversa de una pata. kdir = -1: rodilla hacia atrás (imagen especular en el plano
    sagital: se resuelve el objetivo reflejado y se cambia el signo de los ángulos de cabeceo)."""
    if kdir > 0:
        return ik.solve(d)
    q = ik.solve(np.array([-d[0], d[1], d[2]]))
    return np.array([q[0], -q[1], -q[2], -q[3], q[4]])


def inset_triangle(A, B, C, m):
    """Triángulo con cada lado desplazado hacia dentro una distancia m (homotecia desde el incentro)."""
    a, b, c = np.linalg.norm(B - C), np.linalg.norm(C - A), np.linalg.norm(A - B)
    I = (a * A + b * B + c * C) / (a + b + c)
    area = 0.5 * abs((B - A)[0] * (C - A)[1] - (B - A)[1] * (C - A)[0])
    r = 2 * area / (a + b + c)
    f = max((r - m) / r, 0.05)
    return I + f * (A - I), I + f * (B - I), I + f * (C - I)


def project_triangle(p, A, B, C):
    """Punto del triángulo ABC más cercano a p."""
    def cross(o, u, v):
        return (u[0] - o[0]) * (v[1] - o[1]) - (u[1] - o[1]) * (v[0] - o[0])
    s1, s2, s3 = cross(A, B, p), cross(B, C, p), cross(C, A, p)
    if (s1 >= 0 and s2 >= 0 and s3 >= 0) or (s1 <= 0 and s2 <= 0 and s3 <= 0):
        return p.copy()
    best, bd = None, np.inf
    for u, v in ((A, B), (B, C), (C, A)):
        e = v - u
        t = np.clip(np.dot(p - u, e) / np.dot(e, e), 0, 1)
        q = u + t * e
        d = np.linalg.norm(p - q)
        if d < bd:
            best, bd = q, d
    return best


def load_share(P: np.ndarray, zmp: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Reparto de la carga vertical entre los pies: mínima norma ponderada con el CoP en el ZMP.

    P (4, 2) posiciones de las suelas, w (4,) pesos (0 = pata que no debe cargar)."""
    w = np.maximum(w, 1e-6)
    A = np.vstack([P[:, 0], P[:, 1], np.ones(4)])
    b = np.array([zmp[0], zmp[1], 1.0])
    D = np.diag(w)
    lam = D @ A.T @ np.linalg.solve(A @ D @ A.T, b)
    lam = np.clip(lam, 0, None)
    return lam / max(lam.sum(), 1e-9)


_CACHE = {}


def simulate_quad(H: float, M: float, torque_limit: dict | None = None, gp: QuadGait | None = None,
                  video: str | None = None, video_fps: int = 30, label: str = "", record_every: int = 5,
                  adm: float = 0.03, vel_ff: bool = True, adm_xy: float = 0.03,
                  armature_share: float = 0.5, plan: "QuadPlan | None" = None, arch: dict | None = None):
    """adm: ganancia del control de reparto de carga (admitancia). Cada pata apoyada se acorta o se
    alarga en proporción a la diferencia entre la carga que lleva y la que le asigna el plan:
        d(dz)/dt = adm · sqrt(g H) · (F_medida - F_deseada) / W
    Sin esto, cuatro patas rígidas sobre suelo rígido son hiperestáticas y el peso acaba sobre una
    diagonal (la «mesa coja»). adm = 0 lo desactiva.

    adm_xy: lo mismo en horizontal. La fuerza deseada de cada pie apunta a su cadera (la pata trabaja
    como un puntal, como en los elefantes) y la resultante horizontal se conserva; sin esto, las patas
    se empujan entre sí en horizontal y aparecen pares de cadera que no hacen falta.

    plan / arch: plan ya calculado (por ejemplo, de quad_gait.plan_animal) y parámetros del modelo
    (QuadParams) que lo acompañan; si no se dan, se usa el paso de gateo de plan_quad(gp)."""
    if plan is None:
        gp = gp or QuadGait()
        key = tuple(sorted(gp.__dict__.items()))
        if key not in _CACHE:
            _CACHE[key] = plan_quad(gp)
        pl = _CACHE[key]
        arch = dict(DX=gp.DX, WY=gp.WY)
    else:
        pl = plan
        arch = dict(arch or {})
    k = H / H0
    ts = math.sqrt(k)
    qp = QuadParams(H=H, M=M, torque_limit=torque_limit or {}, armature_share=armature_share, **arch)
    kdir = [qp.knee_dir(lg) for lg in LEGS]
    model = mujoco.MjModel.from_xml_string(build_quad_mjcf(qp))
    data = mujoco.MjData(model)
    dt = model.opt.timestep
    jadr = np.array([model.joint(j).qposadr[0] for j in JOINTS])
    vadr = np.array([model.joint(j).dofadr[0] for j in JOINTS])
    act = np.array([model.actuator(j).id for j in JOINTS])
    foot_g = {model.geom(f"foot_{lg}").id: i for i, lg in enumerate(LEGS)}
    floor_g = model.geom("floor").id

    data.qpos[:3] = pl.body[0] * k
    data.qpos[3:7] = [1, 0, 0, 0]
    data.qpos[jadr] = pl.q[0]
    data.ctrl[act] = pl.q[0]
    mujoco.mj_forward(model, data)

    t_plan = pl.t * ts
    nsteps = int(t_plan[-1] / dt)
    W = M * G
    z0 = pl.body[0, 2] * k

    renderer = None
    frames = []
    if video:
        renderer = mujoco.Renderer(model, 540, 960)
        cam = mujoco.MjvCamera()
        cam.type = mujoco.mjtCamera.mjCAMERA_FREE
        cam.distance = 2.3 * H
        cam.elevation = -14
        cam.azimuth = 125
        frame_dt = 1.0 / video_fps * ts
    next_frame = 0.0

    rec = {n: [] for n in ("t", "tau", "qvel", "q", "q_ref", "F", "body", "dz", "F_des")}
    c6 = np.zeros(6)
    fell, fall_t = False, None
    ik = LegIK(qp)
    sole_ids = [model.site(f"sole_{lg}").id for lg in LEGS]
    dz = np.zeros((4, 3))
    F_des = np.zeros((4, 3))
    dtp = (pl.t[1] - pl.t[0]) * ts
    vel_scale = adm * math.sqrt(G * H) / W
    tau_leak_sw = 0.05 * ts
    tau_leak_st = 2.0 * ts
    dz_max = 0.03 * H

    def foot_forces():
        F = np.zeros((4, 3))
        for c in range(data.ncon):
            con = data.contact[c]
            g1, g2 = con.geom1, con.geom2
            if floor_g not in (g1, g2):
                continue
            gid = g2 if g1 == floor_g else g1
            if gid not in foot_g:
                continue
            mujoco.mj_contactForce(model, data, c, c6)
            f = con.frame.reshape(3, 3).T @ c6[:3]
            if g1 == gid:
                f = -f
            F[foot_g[gid]] += f
        return F

    F = np.zeros((4, 3))
    kvkp = 0.04 * ts if vel_ff else 0.0
    for i in range(nsteps):
        t = i * dt
        u = min(t / dtp, len(pl.t) - 1.000001)
        k0 = int(u)
        a_ = u - k0
        qref = pl.q[k0] * (1 - a_) + pl.q[k0 + 1] * a_
        if adm > 0:
            dv = (pl.dvec[k0] * (1 - a_) + pl.dvec[k0 + 1] * a_) * k
            w = pl.wload[k0] * (1 - a_) + pl.wload[k0 + 1] * a_
            zr = (pl.zmp[k0] * (1 - a_) + pl.zmp[k0 + 1] * a_) * k
            P = np.array([data.site_xpos[s_][:2] for s_ in sole_ids])
            Fz = F[:, 2]
            tot = Fz.sum()
            if tot > 0.3 * W:
                lam = load_share(P, zr, w)
                F_des[:, 2] = lam * tot
                if adm_xy > 0:
                    # dirección deseada: del pie a la cadera (dv apunta de la cadera al tobillo)
                    hor = -dv[:, :2] / np.maximum(-dv[:, 2:3], 1e-9)
                    Fxy = lam[:, None] * tot * hor
                    resid = F[:, :2].sum(0) - Fxy.sum(0)      # se respeta la resultante horizontal medida
                    F_des[:, :2] = Fxy + lam[:, None] * resid
                for j in range(4):
                    if w[j] > 1e-3:
                        dz[j, 2] += dt * (vel_scale * (Fz[j] - F_des[j, 2]) - dz[j, 2] / tau_leak_st)
                        if adm_xy > 0:
                            dz[j, :2] += dt * (adm_xy * math.sqrt(G * H) / W * (F[j, :2] - F_des[j, :2])
                                               - dz[j, :2] / tau_leak_st)
                    else:
                        dz[j] -= dt * dz[j] / tau_leak_sw
            dz = np.clip(dz, -dz_max, dz_max)
            qref = qref.copy()
            for j in range(4):
                qref[5 * j:5 * j + 5] = leg_ik(ik, dv[j] + dz[j], kdir[j])
        # prealimentación de velocidad: el servo de posición de MuJoCo amortigua la velocidad real
        # (-kv·qdot), lo que retrasa la pata en vuelo kv/kp·qdot; se compensa con kv/kp·qdot_ref.
        qd_ref = (pl.qd[k0] * (1 - a_) + pl.qd[k0 + 1] * a_) / ts
        data.ctrl[act] = qref + kvkp * qd_ref
        mujoco.mj_step(model, data)
        F = foot_forces()
        if i % record_every == 0:
            rec["dz"].append(dz.copy())
            rec["F_des"].append(F_des.copy())
            rec["t"].append(t)
            rec["tau"].append(data.actuator_force[act].copy())
            rec["qvel"].append(data.qvel[vadr].copy())
            rec["q"].append(data.qpos[jadr].copy())
            rec["q_ref"].append(qref)
            rec["F"].append(F)
            rec["body"].append(data.qpos[:7].copy())
        if renderer is not None and t >= next_frame:
            cam.lookat[:] = [data.qpos[0], 0, 0.30 * H]
            renderer.update_scene(data, cam)
            from walk import overlay
            frames.append(overlay(renderer.render().copy(), label, t / ts, data.qpos[0], None))
            next_frame += frame_dt
        quat = data.qpos[3:7]
        tilt = 2 * math.acos(min(1.0, abs(quat[0])))
        if data.qpos[2] < 0.6 * z0 or tilt > 0.6:
            if not fell:
                fell, fall_t = True, t
            if renderer is None or t > fall_t + 2.0 * ts:
                break
    if renderer is not None and frames:
        import imageio.v2 as imageio
        imageio.mimsave(video, frames, fps=video_fps, codec="libx264", quality=7)

    r = {n: np.array(v) for n, v in rec.items()}
    tau, qv = r["tau"], r["qvel"]
    peak = {n: float(np.abs(tau[:, i]).max()) for i, n in enumerate(JOINTS)}
    by_type = {}
    for d in DOFS:
        for end in ("F", "H"):
            by_type[f"{d}_{end}"] = max(peak[f"{d}_{lg}"] for lg in LEGS if lg[1] == end) / (W * H)
    pw = tau * qv
    vgrf = r["F"][:, :, 2]
    summary = {
        "H": H, "M": M, "fell": fell, "fall_t": fall_t,
        "distance": float(r["body"][-1, 0] - r["body"][0, 0]),
        "speed_plan": pl.speed * ts, "duty": pl.duty,
        "peak_tau_norm": by_type,
        "peak_power_norm": float(np.abs(pw).sum(axis=1).max() / (W * math.sqrt(G * H))),
        "mean_pos_power_norm": float(np.clip(pw, 0, None).sum(axis=1).mean() / (W * math.sqrt(G * H))),
        "peak_grf_foot_BW": {lg: float(vgrf[:, i].max() / W) for i, lg in enumerate(LEGS)},
        "min_feet_loaded": int((vgrf > 0.02 * W).sum(axis=1).min()),
        "max_track_err_rad": float(np.abs(r["q"] - r["q_ref"]).max()),
    }
    return r, summary


if __name__ == "__main__":
    import json
    for H, M in ((1.75, 100.0), (20.0, 20000.0)):
        _, s = simulate_quad(H, M)
        print(json.dumps(s, indent=1))
