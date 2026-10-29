"""
Planificador de marcha para el mecha.

1. Plan de pisadas y trayectoria de referencia del ZMP (punto de momento cero).
2. Trayectoria del centro de masa con control predictivo (preview control) sobre
   el péndulo invertido lineal (Kajita et al., ICRA 2003).
3. Cinemática inversa analítica de cada pierna de 5 GDL, con corrección
   iterativa para que el CdM real del modelo multicuerpo siga la referencia.

Todo se planifica a escala humana (H0 = 1.75 m). Con similitud de Froude, las
trayectorias articulares son idénticas a cualquier escala: las posiciones se
multiplican por k = H/H0 y los tiempos por sqrt(k).
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import mujoco
import numpy as np
import scipy.linalg as sla

from mech_model import MechParams, build_mjcf, JOINTS

H0 = 1.75
G = 9.81


@dataclass
class GaitParams:
    step_len: float = 0.15       # avance por paso [fracción de H]
    t_ss: float = 0.70           # apoyo simple [s, escala humana]
    t_ds: float = 0.25           # doble apoyo [s, escala humana]
    n_steps: int = 8
    clearance: float = 0.035     # altura de levantamiento del pie [fracción de H]
    hip_drop: float = 0.045      # cuánto se agacha la pelvis para no estirar la rodilla [fracción de H]
    t_init: float = 1.0
    t_end: float = 1.5
    dt: float = 0.005            # paso de planificación [s, escala humana]
    preview: float = 1.6         # horizonte de previsión [s]


# --------------------------------------------------------------------------
def preview_gains(zc: float, dt: float, n_prev: int, Qe=1.0, R=1e-6):
    A = np.array([[1, dt, dt * dt / 2], [0, 1, dt], [0, 0, 1]])
    B = np.array([[dt ** 3 / 6], [dt * dt / 2], [dt]])
    C = np.array([[1, 0, -zc / G]])
    Aa = np.block([[np.eye(1), C @ A], [np.zeros((3, 1)), A]])
    Ba = np.vstack([C @ B, B])
    Q = np.zeros((4, 4))
    Q[0, 0] = Qe
    P = sla.solve_discrete_are(Aa, Ba, Q, np.array([[R]]))
    S = R + (Ba.T @ P @ Ba)[0, 0]
    K = (Ba.T @ P @ Aa) / S
    Gi, Gx = K[0, 0], K[0, 1:]
    Ac = Aa - Ba @ K
    I1 = np.array([[1.0], [0], [0], [0]])
    X = -Ac.T @ P @ I1
    Gd = np.zeros(n_prev)
    Gd[0] = -Gi
    for j in range(1, n_prev):
        Gd[j] = (Ba.T @ X)[0, 0] / S
        X = Ac.T @ X
    return A, B, C, Gi, Gx, Gd


def zmp_preview(zmp_ref: np.ndarray, zc: float, dt: float, preview_t: float):
    n_prev = int(preview_t / dt)
    A, B, C, Gi, Gx, Gd = preview_gains(zc, dt, n_prev)
    N = len(zmp_ref)
    ref = np.concatenate([zmp_ref, np.repeat(zmp_ref[-1:], n_prev, axis=0)])
    out = np.zeros((N, 3))
    for d in range(2):
        x = np.array([ref[0, d], 0.0, 0.0])
        e = 0.0
        for k in range(N):
            out[k, d] = x[0]
            p = (C @ x)[0]
            e += p - ref[k, d]
            u = -Gi * e - Gx @ x - Gd @ ref[k + 1:k + 1 + n_prev, d]
            x = A @ x + B[:, 0] * u
    return out[:, :2]


def min_jerk(t):
    t = np.clip(t, 0, 1)
    return 10 * t ** 3 - 15 * t ** 4 + 6 * t ** 5


# --------------------------------------------------------------------------
class LegIK:
    def __init__(self, p: MechParams):
        self.l1, self.l2 = p.thigh, p.shank

    def solve(self, d: np.ndarray):
        """d = tobillo - cadera (marco de la pelvis, vertical). Devuelve 5 ángulos."""
        l1, l2 = self.l1, self.l2
        roll = math.atan2(d[1], -d[2])
        dr = math.hypot(d[1], d[2])
        L2 = d[0] ** 2 + dr ** 2
        ck = (L2 - l1 * l1 - l2 * l2) / (2 * l1 * l2)
        ck = min(1.0, max(-1.0, ck))
        knee = math.acos(ck)
        alpha = math.atan2(-d[0], dr)
        beta = math.atan2(l2 * math.sin(knee), l1 + l2 * math.cos(knee))
        hip = alpha - beta
        ankle = -(hip + knee)
        return np.array([roll, hip, knee, ankle, -roll])


@dataclass
class GaitPlan:
    t: np.ndarray            # tiempo [s] a escala humana
    q: np.ndarray            # (N, 10) ángulos articulares en el orden de JOINTS
    pelvis: np.ndarray       # (N, 3) posición de la pelvis a escala humana
    com: np.ndarray          # (N, 2) CdM de referencia
    zmp: np.ndarray          # (N, 2)
    feet: np.ndarray         # (N, 2, 3) tobillos L, R
    support: np.ndarray      # (N,) 0 doble, 1 izq, 2 der
    speed: float             # velocidad media [m/s] a escala humana


def plan(gp: GaitParams = GaitParams(), foot_scale: float = 1.0) -> GaitPlan:
    p = MechParams(H=H0, M=70.0, foot_scale=foot_scale)
    model = mujoco.MjModel.from_xml_string(build_mjcf(p))
    data = mujoco.MjData(model)
    ik = LegIK(p)
    dt = gp.dt
    s = gp.step_len * H0
    w = p.hip_w
    foot_cx = p.foot_len * 0.25   # centro de la suela respecto al tobillo
    hip_z = (p.thigh + p.shank + p.ankle_h) - gp.hip_drop * H0

    # ---- plan de pisadas ------------------------------------------------------
    # eventos: (pie que se mueve, x_inicial, x_final)
    feet_x = {"L": 0.0, "R": 0.0}
    steps = []
    swing = "R"
    for i in range(gp.n_steps):
        if i == 0:
            target = s
        elif i == gp.n_steps - 1:
            target = feet_x["L" if swing == "R" else "R"]  # juntar pies
        else:
            target = feet_x["L" if swing == "R" else "R"] + s
        steps.append((swing, feet_x[swing], target))
        feet_x[swing] = target
        swing = "L" if swing == "R" else "R"

    t_list, zmp_list, feet_list, sup_list = [], [], [], []
    fx = {"L": 0.0, "R": 0.0}
    fz = {"L": 0.0, "R": 0.0}
    yoff = {"L": w, "R": -w}

    def center(side):
        return np.array([fx[side] + foot_cx, yoff[side]])

    def push(n, zmp_fn, sup, swing_fn=None):
        for k in range(n):
            tau = k / max(n - 1, 1)
            if swing_fn:
                swing_fn(tau)
            zmp_list.append(zmp_fn(tau))
            feet_list.append([[fx["L"], yoff["L"], fz["L"]], [fx["R"], yoff["R"], fz["R"]]])
            sup_list.append(sup)

    mid = lambda: 0.5 * (center("L") + center("R"))
    push(int(gp.t_init / dt), lambda tau: mid(), 0)
    prev = mid()
    for (sw, x0, x1) in steps:
        st = "L" if sw == "R" else "R"
        a = prev.copy()
        b = center(st)
        push(int(gp.t_ds / dt), lambda tau, a=a, b=b: a + (b - a) * min_jerk(tau), 0)

        def swing_fn(tau, sw=sw, x0=x0, x1=x1):
            fx[sw] = x0 + (x1 - x0) * min_jerk(tau)
            fz[sw] = gp.clearance * H0 * 0.5 * (1 - math.cos(2 * math.pi * tau))

        push(int(gp.t_ss / dt), lambda tau, b=b: b, 1 if st == "L" else 2, swing_fn)
        fz[sw] = 0.0
        prev = b
    a = prev.copy()
    push(int(gp.t_ds / dt), lambda tau, a=a: a + (mid() - a) * min_jerk(tau), 0)
    push(int(gp.t_end / dt), lambda tau: mid(), 0)

    zmp = np.array(zmp_list)
    feet = np.array(feet_list)
    N = len(zmp)
    t = np.arange(N) * dt

    # altura del CdM en la postura agachada
    qpos0 = np.zeros(model.nq)
    qpos0[2] = hip_z
    qpos0[3] = 1.0
    data.qpos[:] = qpos0
    d0 = np.array([0.0, 0.0, -(hip_z - p.ankle_h)])
    qleg = ik.solve(d0)
    for side, sgn in (("L", 1), ("R", -1)):
        for j, name in enumerate(["hip_roll", "hip_pitch", "knee", "ankle_pitch", "ankle_roll"]):
            data.qpos[model.joint(f"{name}_{side}").qposadr] = qleg[j]
    mujoco.mj_kinematics(model, data)
    mujoco.mj_comPos(model, data)
    zc = data.subtree_com[0][2]

    com = zmp_preview(zmp, zc, dt, gp.preview)

    # ---- IK con corrección de CdM ---------------------------------------------
    q = np.zeros((N, 10))
    pel = np.zeros((N, 3))
    offset = np.zeros(2)
    jadr = [model.joint(j).qposadr[0] for j in JOINTS]
    for k in range(N):
        target = com[k]
        pxy = target - offset
        for _ in range(3):
            pelvis = np.array([pxy[0], pxy[1], hip_z])
            qk = []
            for side, sgn in (("L", 1), ("R", -1)):
                hip = pelvis + np.array([0, sgn * w, 0])
                ank = np.array(feet[k, 0 if side == "L" else 1]) + np.array([0, 0, p.ankle_h])
                qk.append(ik.solve(ank - hip))
            qk = np.concatenate(qk)
            data.qpos[:3] = pelvis
            data.qpos[3:7] = [1, 0, 0, 0]
            data.qpos[jadr] = qk
            mujoco.mj_kinematics(model, data)
            mujoco.mj_comPos(model, data)
            err = target - data.subtree_com[0][:2]
            pxy = pxy + err
            if np.linalg.norm(err) < 1e-5:
                break
        offset = target - pxy
        q[k] = qk
        pel[k] = pelvis

    speed = (steps[-2][2] if len(steps) > 1 else s) / (gp.t_ds + gp.t_ss) / max(len(steps) - 1, 1)
    return GaitPlan(t=t, q=q, pelvis=pel, com=com, zmp=zmp, feet=feet,
                    support=np.array(sup_list), speed=speed)


if __name__ == "__main__":
    gp = plan()
    print("muestras", len(gp.t), "duración", gp.t[-1], "s; velocidad media", round(gp.speed, 3), "m/s")
    print("rodilla max (deg)", np.degrees(gp.q[:, 2].max()))
