"""
Marcha de cuadrúpedo «tipo animal» para el mecha: cada pata sigue su propia fase
dentro del ciclo, como en los mamíferos, en lugar de mover una pata cada vez
con pausas (el paso de gateo de quad_walk.plan_quad).

- Temporización: factor de apoyo β (fracción del ciclo con la pata en el suelo)
  y desfases de cada pata; por defecto, secuencia lateral con desfases del 25 %,
  la del paso de los elefantes (Hutchinson et al. 2006). Con β < 0.75 hay fases
  con solo dos patas en el suelo y el equilibrio es dinámico.
- Pisadas: cada pata aterriza donde quedará bajo su cadera a mitad del apoyo
  (regla de Raibert con el avance nominal del cuerpo).
- ZMP: en cada intervalo con el mismo conjunto de patas apoyadas, el punto del
  polígono de apoyo (reducido en un margen) más cercano al avance nominal. Las
  transiciones terminan antes de cada despegue y empiezan después de cada
  aterrizaje, así que el ZMP de referencia nunca sale del polígono.
- Centro de masa: control predictivo del ZMP (Kajita et al. 2003), como el bípedo.
- Altura del cuerpo: la mayor que permite la pata apoyada más estirada con una
  flexión mínima de rodilla `knee_min`. Con knee_min pequeño las patas trabajan
  casi rectas (postura columnar, como el elefante) y el cuerpo sube y baja un
  poco en cada paso; con knee_min grande, la postura es flexionada.

Todo se planifica a escala humana (H0 = 1.75 m, pata L0 = 0.93 m) y se escala con
similitud de Froude.
"""
from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

import mujoco
import numpy as np
from scipy.signal import butter, filtfilt

sys.path.insert(0, os.path.dirname(__file__))
from gait import LegIK, min_jerk, zmp_preview  # noqa: E402
from quad_model import JOINTS, LEGS, QuadParams, build_quad_mjcf  # noqa: E402
from quad_walk import QuadPlan, leg_ik  # noqa: E402

H0 = 1.75
G = 9.81
LATERAL = (("LH", 0.0), ("LF", 0.25), ("RH", 0.5), ("RF", 0.75))


@dataclass
class AnimalGait:
    duty: float = 0.75              # factor de apoyo β
    froude: float = 0.0084          # v² / (g L), con L la longitud de la pata (0.53 H); 0.0084 = bípedo de E1
    stride: float = 0.8             # avance del cuerpo por ciclo [× L]
    phases: tuple = LATERAL         # (pata, fase de despegue en el ciclo)
    clearance: float = 0.06         # altura de levantamiento del pie [× L]
    knee_min: float = 0.25          # flexión mínima de rodilla en apoyo [rad]: postura
    n_cycles: int = 3               # ciclos a velocidad constante (más un ciclo de arranque y otro de parada)
    margin: float = 0.05            # margen del ZMP dentro del polígono de apoyo [× L]
    blend: float = 0.08             # duración de las transiciones del ZMP [× ciclo]
    w_ramp: float = 0.06            # rampa de carga y descarga de cada pata [× ciclo]
    z_smooth: float = 0.3           # escala de suavizado de la altura del cuerpo [× ciclo]
    t_init: float = 1.0
    t_end: float = 1.5
    dt: float = 0.005
    preview: float = 1.6


# --------------------------------------------------------------------------- geometría 2D
def _hull(P):
    P = sorted(map(tuple, P))
    if len(P) <= 2:
        return [np.array(p) for p in P]

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in P:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return [np.array(p) for p in lo[:-1] + up[:-1]]


def _cross2(a, b):
    return a[0] * b[1] - a[1] * b[0]


def _seg_closest(p, a, b):
    e = b - a
    den = float(np.dot(e, e))
    t = 0.0 if den == 0 else np.clip(np.dot(p - a, e) / den, 0, 1)
    return a + t * e


def support_target(points, p, m):
    """Punto del polígono de apoyo (envolvente convexa de `points`, reducida en m) más cercano a p."""
    V = _hull(points)
    if len(V) == 1:
        return V[0].copy()
    if len(V) == 2:
        a, b = V
        L = np.linalg.norm(b - a)
        if L > 2 * m:
            u = (b - a) / L
            a, b = a + m * u, b - m * u
        return _seg_closest(p, a, b)
    c = np.mean(V, axis=0)
    dmin = min(abs(_cross2(V[(i + 1) % len(V)] - V[i], c - V[i])) / np.linalg.norm(V[(i + 1) % len(V)] - V[i])
               for i in range(len(V)))
    f = max((dmin - m) / dmin, 0.05)
    V = [c + f * (v - c) for v in V]
    inside = all(_cross2(V[(i + 1) % len(V)] - V[i], p - V[i]) >= 0 for i in range(len(V)))
    if inside:
        return p.copy()
    cands = [_seg_closest(p, V[i], V[(i + 1) % len(V)]) for i in range(len(V))]
    return min(cands, key=lambda q: np.linalg.norm(q - p))


# --------------------------------------------------------------------------- plan
def plan_animal(ag: AnimalGait, arch: dict | None = None) -> QuadPlan:
    arch = dict(arch or {})
    p = QuadParams(H=H0, M=70.0, **arch)
    model = mujoco.MjModel.from_xml_string(build_quad_mjcf(p))
    data = mujoco.MjData(model)
    ik = LegIK(p)
    kdir = [p.knee_dir(lg) for lg in LEGS]
    dt = ag.dt
    L0 = p.leg_len
    ah = p.ankle_h
    l1, l2 = p.thigh, p.shank
    d_max = math.sqrt(l1 * l1 + l2 * l2 + 2 * l1 * l2 * math.cos(ag.knee_min))
    v = math.sqrt(ag.froude * G * L0)
    T = ag.stride * L0 / v
    beta = ag.duty
    foot_cx = p.foot_len * p.ankle_x
    hips = {lg: np.array(p.hip_pos(lg)) for lg in LEGS}

    # avance nominal del cuerpo: arranque y parada de un ciclo con velocidad de mínimo tirón
    t0 = ag.t_init
    t_walk = (ag.n_cycles + 2) * T
    t_last = t0 + t_walk + 1.0 * T          # margen para que las patas se recoloquen
    t_total = t_last + ag.t_end
    t = np.arange(0.0, t_total, dt)
    N = len(t)

    def vel(tt):
        u = tt - t0
        if u <= 0 or u >= t_walk:
            return 0.0
        if u < T:
            return v * min_jerk(u / T)
        if u > t_walk - T:
            return v * min_jerk((t_walk - u) / T)
        return v
    vv = np.array([vel(x) for x in t])
    x_nom = np.concatenate([[0.0], np.cumsum(0.5 * (vv[1:] + vv[:-1]) * dt)])

    def xnom(tt):
        return float(np.interp(tt, t, x_nom))

    # pisadas
    feet = {lg: np.array([hips[lg][0], hips[lg][1], 0.0]) for lg in LEGS}
    swings = []      # (pata, t_lo, t_td, x0, x1)
    for lg, ph in ag.phases:
        x = feet[lg][0]
        k = 0
        while True:
            t_lo = t0 + (k + ph) * T
            if t_lo > t_last:
                break
            t_td = t_lo + (1 - beta) * T
            x1 = xnom(t_td + 0.5 * beta * T) + hips[lg][0]
            if abs(x1 - x) > 0.01 * L0:
                swings.append((lg, t_lo, t_td, x, x1))
                x = x1
            k += 1
    feet_arr = np.zeros((N, 4, 3))
    sw4 = np.zeros((N, 4), bool)
    for i, lg in enumerate(LEGS):
        feet_arr[:, i, 0] = hips[lg][0]
        feet_arr[:, i, 1] = hips[lg][1]
    for lg, t_lo, t_td, x0, x1 in sorted(swings, key=lambda s: s[1]):
        i = LEGS.index(lg)
        m_sw = (t >= t_lo) & (t < t_td)
        tau = (t[m_sw] - t_lo) / (t_td - t_lo)
        feet_arr[m_sw, i, 0] = x0 + (x1 - x0) * min_jerk(tau)
        feet_arr[m_sw, i, 2] = ag.clearance * L0 * 0.5 * (1 - np.cos(2 * np.pi * tau))
        feet_arr[t >= t_td, i, 0] = x1
        sw4[m_sw, i] = True

    # postura de partida: altura del CdM y su posición respecto al origen del cuerpo
    jadr = [model.joint(j).qposadr[0] for j in JOINTS]

    def pose(bpos, k):
        qk = []
        for i, lg in enumerate(LEGS):
            hip = bpos + np.array([hips[lg][0], hips[lg][1], 0.0])
            ank = feet_arr[k, i] + np.array([0, 0, ah])
            qk.append(leg_ik(ik, ank - hip, kdir[i]))
        return np.concatenate(qk)

    z_stand = ah + d_max
    data.qpos[:3] = [0, 0, z_stand]
    data.qpos[3:7] = [1, 0, 0, 0]
    data.qpos[jadr] = pose(np.array([0, 0, z_stand]), 0)
    mujoco.mj_kinematics(model, data)
    mujoco.mj_comPos(model, data)
    zc = data.subtree_com[0][2]
    com_off = data.subtree_com[0][:2].copy()     # CdM respecto al origen del cuerpo

    # intervalos con el mismo conjunto de apoyos y objetivo del ZMP en cada uno
    # Se recorren los eventos en orden (a igual tiempo, primero el despegue) llevando la cuenta de qué
    # pies están en el aire y dónde está apoyado cada uno. Los intervalos de duración nula se conservan:
    # si un pie aterriza en el mismo instante en que otro despega, el ZMP pasa por la recta entre los
    # dos pies que siguen apoyados.
    events = sorted([(s_[1], 0, "lo", s_[0], s_[4]) for s_ in swings] +
                    [(s_[2], 1, "td", s_[0], s_[4]) for s_ in swings])
    planted = {lg: hips[lg].copy() for lg in LEGS}
    in_air = set()
    ints = []
    prev_t, prev_e = 0.0, "td"
    for (te, _, kind, lg, x1) in events + [(t_total, 2, "fin", None, None)]:
        tm = 0.5 * (prev_t + te)
        pts = [np.array([planted[l_][0] + foot_cx, planted[l_][1]]) for l_ in LEGS if l_ not in in_air]
        # avance nominal: centro de los cuatro pies, con los que vuelan en la mitad de su recorrido
        rep_x = []
        for l_ in LEGS:
            if l_ in in_air:
                sw_ = [s_ for s_ in swings if s_[0] == l_ and s_[1] <= tm <= s_[2]]
                rep_x.append(0.5 * (sw_[0][3] + sw_[0][4]) if sw_ else planted[l_][0])
            else:
                rep_x.append(planted[l_][0])
        nom = np.array([np.mean(rep_x) + foot_cx, 0.0])
        ints.append([prev_t, te, prev_e, kind, support_target(pts, nom, ag.margin * L0)])
        if kind == "lo":
            in_air.add(lg)
        elif kind == "td":
            in_air.discard(lg)
            planted[lg] = np.array([x1, hips[lg][1]])
        prev_t, prev_e = te, kind
    zmp = np.zeros((N, 2))
    keys = []
    for ta, tb, ea, eb, pk in ints:
        bl = min(ag.blend * T, 0.5 * (tb - ta))
        a = ta if ea == "lo" else ta + bl
        d = tb - bl if eb == "lo" else tb
        if d < a:
            a = d = 0.5 * (ta + tb)
        keys.append((a, d, pk))
    for j, (a, d, pk) in enumerate(keys):
        zmp[(t >= a) & (t <= d)] = pk
        if j + 1 < len(keys):
            a2, _, pk2 = keys[j + 1]
            m_tr = (t > d) & (t < a2)
            if m_tr.any():
                tau = (t[m_tr] - d) / (a2 - d)
                zmp[m_tr] = pk + (pk2 - pk) * min_jerk(tau)[:, None]
    first = keys[0]
    zmp[t < first[0]] = first[2]

    com = zmp_preview(zmp, zc, dt, ag.preview)

    # altura del cuerpo: la que permite la pata apoyada más estirada
    bxy = com - com_off
    z_raw = np.full(N, z_stand)
    for i, lg in enumerate(LEGS):
        # vale también para la pata en vuelo, con su pie levantado: tiene que poder alcanzar su pisada
        r = np.hypot(bxy[:, 0] + hips[lg][0] - feet_arr[:, i, 0], bxy[:, 1] + hips[lg][1] - feet_arr[:, i, 1])
        lim = ah + feet_arr[:, i, 2] + np.sqrt(np.clip(d_max ** 2 - r ** 2, 1e-6, None))
        z_raw = np.minimum(z_raw, lim)
    b, a_ = butter(2, min(0.99, 2 * dt / (ag.z_smooth * T)))
    z = z_raw.copy()
    for _ in range(25):
        z = filtfilt(b, a_, np.minimum(z, z_raw))
    z = np.minimum(z, z_raw)

    # cinemática inversa con corrección del CdM
    q = np.zeros((N, len(JOINTS)))
    body = np.zeros((N, 3))
    dvec = np.zeros((N, 4, 3))
    offset = com_off.copy()
    for k in range(N):
        target = com[k]
        pxy = target - offset
        for _ in range(4):
            bpos = np.array([pxy[0], pxy[1], z[k]])
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
            dvec[k, i] = feet_arr[k, i] + np.array([0, 0, ah]) - (bpos + np.array([hips[lg][0], hips[lg][1], 0.0]))

    # pesos de reparto de carga: rampas antes del despegue y después del aterrizaje
    wl = np.ones((N, 4))
    rw = ag.w_ramp * T
    for lg, t_lo, t_td, _, _ in swings:
        i = LEGS.index(lg)
        m1 = (t > t_lo - rw) & (t < t_lo)
        wl[m1, i] = np.minimum(wl[m1, i], 1 - min_jerk((t[m1] - (t_lo - rw)) / rw))
        wl[sw4[:, i], i] = 0.0
        m2 = (t >= t_td) & (t < t_td + rw)
        wl[m2, i] = np.minimum(wl[m2, i], min_jerk((t[m2] - t_td) / rw))
    swing = np.where(sw4.any(1), sw4.argmax(1), -1)
    out = QuadPlan(t=t, q=q, body=body, com=com, zmp=zmp, feet=feet_arr, swing=swing,
                   wload=wl, dvec=dvec, qd=np.gradient(q, dt, axis=0), speed=v, duty=beta)
    out.swing4 = sw4
    out.z_var = float((z[t > t0 + T].max() - z[t > t0 + T].min()) / L0)
    out.cycle = T
    return out


if __name__ == "__main__":
    pl = plan_animal(AnimalGait())
    kn = pl.q[:, [JOINTS.index(f"knee_{lg}") for lg in LEGS]]
    i, j = np.unravel_index(np.abs(kn).argmin(), kn.shape)
    print("rodilla mínima en t", round(pl.t[i], 3), "pata", LEGS[j], "en vuelo" if pl.swing4[i, j] else "apoyada")
    print("duración", round(pl.t[-1], 2), "s; v", round(pl.speed, 3), "m/s; ciclo", round(pl.cycle, 2),
          "s; variación de altura", round(pl.z_var, 4), "L; rodilla mín/máx", np.round(np.abs(kn).min(), 3),
          np.round(np.abs(kn).max(), 3))
