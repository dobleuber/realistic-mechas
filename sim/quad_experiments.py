"""
Bípedo frente a cuadrúpedo en MuJoCo, medidos igual.

Casos (a escala humana, H = 1.75 m; los resultados normalizados valen a
cualquier escala por similitud de Froude, comprobado a 20 y 50 m):

  bipedo              marcha ZMP del bípedo (la de los experimentos E1-E3), 0.276 m/s
  bipedo_lento        el mismo bípedo con apoyo simple de 1.2 s, 0.159 m/s
  cuadrupedo_rapido   paso de gateo con vuelo de 0.5 s, 0.162 m/s (misma velocidad que bipedo_lento)
  cuadrupedo          paso de gateo con vuelo de 0.7 s, 0.124 m/s

Métricas: pares pico por articulación (máximo de todas las patas) normalizados
por peso × H, fuerza vertical pico por pie, potencia mecánica pico y media
positiva normalizadas por peso × sqrt(g H). Se filtran a 10 Hz (escala humana)
con un Butterworth de orden 2 sin desfase; por encima solo hay vibración
numérica de patas rígidas sobre suelo rígido. También se guardan sin filtrar.

Uso:  python sim/quad_experiments.py [--video]
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
from scipy.signal import butter, filtfilt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "scaling"))
from gait import GaitParams  # noqa: E402
from mech_model import JOINTS as BJ  # noqa: E402
from quad_model import JOINTS as QJ, LEGS  # noqa: E402
from quad_walk import QuadGait, simulate_quad  # noqa: E402
from walk import simulate  # noqa: E402

ROOT = os.path.join(HERE, "..", "results")
VID = os.path.join(ROOT, "videos")
G = 9.81
FC = 10.0     # corte del filtro a escala humana [Hz]

CASES = {
    "bipedo": dict(nombre="Bípedo (marcha de E1)", patas=2, gp=GaitParams()),
    "bipedo_lento": dict(nombre="Bípedo lento", patas=2, gp=GaitParams(t_ss=1.2, t_ds=0.45)),
    "cuadrupedo_rapido": dict(nombre="Cuadrúpedo, gateo rápido", patas=4,
                              gp=QuadGait(stride=0.24, hip_drop=0.06, t_sw=0.5, t_q=0.15)),
    "cuadrupedo": dict(nombre="Cuadrúpedo, gateo lento", patas=4,
                       gp=QuadGait(stride=0.24, hip_drop=0.06, t_sw=0.7, t_q=0.15)),
}


def lp(x, dt, fc):
    b, a = butter(2, fc * 2 * dt)
    return filtfilt(b, a, x, axis=0)


def metrics(t, tau, qvel, fz, joints, W, H, filt=True):
    """fz: (N, n_pies) fuerzas verticales."""
    ts = math.sqrt(H / 1.75)
    dt = t[1] - t[0]
    m = t > 0.5 * ts
    if filt:
        tau, qvel, fz = lp(tau, dt, FC / ts), lp(qvel, dt, FC / ts), lp(fz, dt, FC / ts)
    P = tau * qvel
    peak = {}
    for d, key in (("hip_pitch", "hip"), ("knee", "knee"), ("ankle_pitch", "ankle"), ("hip_roll", "hip_roll"),
                   ("ankle_roll", "ankle_roll")):
        idx = [i for i, j in enumerate(joints) if j.startswith(d + "_")]
        peak[key] = float(np.abs(tau[m][:, idx]).max() / (W * H))
    return {
        "par": peak,
        "grf_pie": float(fz[m].max() / W),
        "p_pico": float(np.abs(P[m]).sum(1).max() / (W * math.sqrt(G * H))),
        "p_media": float(np.clip(P[m], 0, None).sum(1).mean() / (W * math.sqrt(G * H))),
    }


def run_case(key, H=1.75, M=None, video=None, label=""):
    c = CASES[key]
    if c["patas"] == 2:
        M = M or 70.0 * (H / 1.75) ** 3
        r = simulate(H, M, gp=c["gp"], record_every=1, video=video, label=label)
        fz = np.stack([r["F_L"][:, 2], r["F_R"][:, 2]], axis=1)
        out = {"fell": bool(r["fell"]), "v": r["speed_plan"]}
        joints, tau, qv, t = BJ, r["tau"], r["qvel"], r["t"]
    else:
        M = M or 100.0 * (H / 1.75) ** 3
        r, s = simulate_quad(H, M, gp=c["gp"], record_every=1, video=video, label=label)
        fz = r["F"][:, :, 2]
        out = {"fell": bool(s["fell"]), "v": s["speed_plan"], "duty": s["duty"]}
        joints, tau, qv, t = QJ, r["tau"], r["qvel"], r["t"]
    W = M * G
    out.update(metrics(t, tau, qv, fz, joints, W, H, filt=True))
    out["sin_filtrar"] = metrics(t, tau, qv, fz, joints, W, H, filt=False)
    out.update(nombre=c["nombre"], patas=c["patas"], H=H, M=M)
    return out


def main(video=False):
    res = {}
    for key in CASES:
        res[key] = run_case(key)
        res[key]["v_rel"] = res[key]["v"] / res["bipedo"]["v"]
        r = res[key]
        print(f"{key:18s} v={r['v']:.3f} m/s ({r['v_rel']:.0%})  par " +
              " ".join(f"{k} {v:.3f}" for k, v in r["par"].items()) +
              f"  GRF/pie {r['grf_pie']:.2f}  P pico {r['p_pico']:.3f}  P media {r['p_media']:.4f}  cae={r['fell']}")
    # similitud de Froude: el cuadrúpedo a 20 y 50 m
    check = {}
    for H in (20.0, 50.0):
        r = run_case("cuadrupedo", H=H)
        check[str(H)] = {k: r[k] for k in ("par", "grf_pie", "p_pico", "p_media", "fell")}
        print(f"cuadrupedo a {H:g} m: par " + " ".join(f"{k} {v:.3f}" for k, v in r["par"].items()))
    json.dump({"casos": res, "froude": check, "filtro_Hz": FC}, open(os.path.join(ROOT, "sim_quad.json"), "w"),
              indent=1, default=float)
    if video:
        make_videos()


def make_videos():
    sys.path.insert(0, os.path.join(HERE, "..", "scaling"))
    from compare_quad import make, load_cases
    from mech_scaling import design
    cases = load_cases()
    os.makedirs(VID, exist_ok=True)
    d = make(cases["cuadrupedo"], "base")
    jobs = [("cuadrupedo", 1.75, 100.0, "cuadrupedo_H1.75.mp4", "Cuadrúpedo de referencia: patas de 0.93 m, 100 kg"),
            ("cuadrupedo", 20.0, None, "cuadrupedo_H20.mp4", None),
            ("cuadrupedo", 40.0, None, "cuadrupedo_H40.mp4", None),
            ("cuadrupedo_rapido", 20.0, None, "cuadrupedo_rapido_H20.mp4", None)]
    for key, H, M, name, label in jobs:
        if M is None:
            dd = make(cases[key], "base")
            M = design(H, dd)["m"]
        if label is None:
            label = (f"{CASES[key]['nombre']}: patas de {0.53 * H:.1f} m, lomo a {0.645 * H:.1f} m, "
                     f"{M / 1e3:.0f} t")
        print("vídeo", name, label)
        run_case(key, H=H, M=M, video=os.path.join(VID, name), label=label)


if __name__ == "__main__":
    if "--solo-videos" in sys.argv:
        make_videos()
    else:
        main(video="--video" in sys.argv)
