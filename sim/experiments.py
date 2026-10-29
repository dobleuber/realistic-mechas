"""
Experimentos de simulación (MuJoCo) del mecha. Escribe results/sim_*.json,
figuras en results/figures/ y vídeos en results/videos/.

  E1  Marcha a varias alturas con la masa del diseño (tubo de Ti, escenario base)
      y actuadores limitados al par de diseño. Comprueba que las cargas
      normalizadas son invariantes (similitud de Froude) y mide GRF, presión y potencia.
  E2  Actuadores insuficientes: par máximo = f × par pico necesario. ¿Desde qué f se cae?
  E3  Suelo deformable (heightfield que se hunde plásticamente según Terzaghi/Vesić):
      mecha con densidad humana a 20 y 50 m sobre arcilla blanda, arena densa y roca.

Uso:  MUJOCO_GL=osmesa python sim/experiments.py [e1|e2|e3|all] [--video]
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "scaling"))
from walk import simulate  # noqa: E402
from mech_scaling import design, make_design  # noqa: E402
from soil import SOILS  # noqa: E402

ROOT = os.path.join(HERE, "..", "results")
FIG = os.path.join(ROOT, "figures")
VID = os.path.join(ROOT, "videos")
os.makedirs(FIG, exist_ok=True)
os.makedirs(VID, exist_ok=True)

# par pico normalizado de la marcha (par / (peso·altura)), medido en la simulación a escala humana
PEAK = {"hip": 0.067, "knee": 0.126, "ankle": 0.091, "hip_roll": 0.054, "ankle_roll": 0.026}


def torque_limits(M, H, factor):
    W = M * 9.81
    return {k: factor * c * W * H for k, c in PEAK.items()}


def clean(r):
    return {k: v for k, v in r.items() if not isinstance(v, np.ndarray)}


def e1(video=False):
    d = make_design("tubo", "base")
    res = []
    for H in (1.75, 5.0, 10.0, 20.0, 28.0):
        if H == 1.75:
            M = 70.0
        else:
            M = design(H, d)["m"]
        tl = torque_limits(M, H, d.dlf)   # actuadores dimensionados con el factor de diseño
        vid = os.path.join(VID, f"e1_marcha_H{H:g}.mp4") if (video and H in (1.75, 20.0, 28.0)) else None
        r = simulate(H, M, tl, video=vid)
        c = clean(r)
        c["torque_limit"] = tl
        res.append(c)
        print(f"E1 H={H:5.1f} M={M / 1e3:8.2f} t  cae={r['fell']}  dist={r['distance']:.2f} m  "
              f"v={r['speed_plan']:.2f} m/s  GRF={r['peak_grf_BW']:.2f}  q_pie={r['peak_q_avg_kPa']:.0f} kPa  "
              f"rodilla={r['peak_tau_norm']['knee_L']:.3f}  P_pico={r['peak_power_W'] / 1e3:.1f} kW", flush=True)
    json.dump(res, open(os.path.join(ROOT, "sim_e1.json"), "w"), indent=1, default=float)
    return res


def e2(video=False):
    H, M = 20.0, design(20.0, make_design("tubo", "base"))["m"]
    res = []
    for f in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5):
        vid = os.path.join(VID, f"e2_par_{int(f * 100)}pct_H20.mp4") if (video and f in (0.6,)) else None
        r = simulate(H, M, torque_limits(M, H, f), video=vid)
        c = clean(r)
        c["factor"] = f
        res.append(c)
        print(f"E2 factor={f:.1f}  cae={r['fell']}  t_caida={r['fall_t']}  dist={r['distance']:.2f} m  "
              f"sat={max(r['saturation'].values()) if r['saturation'] else 0:.2f}", flush=True)
    json.dump(res, open(os.path.join(ROOT, "sim_e2.json"), "w"), indent=1, default=float)
    return res


def e3(video=False):
    res = []
    cases = [(20.0, "arcilla_blanda"), (20.0, "arcilla_firme"), (20.0, "arena_densa"),
             (50.0, "arcilla_blanda"), (50.0, "arcilla_dura"), (50.0, "arena_densa"), (50.0, "granito")]
    for H, soil in cases:
        M = 13.06 * H ** 3   # densidad humana, como la hipótesis del documento
        tl = torque_limits(M, H, 1.5)
        vid = os.path.join(VID, f"e3_{soil}_H{H:g}.mp4") if (video and (H, soil) in ((50.0, "arcilla_blanda"), (50.0, "arena_densa"))) else None
        r = simulate(H, M, tl, soil=SOILS[soil], video=vid)
        c = clean(r)
        c["soil"] = soil
        res.append(c)
        print(f"E3 H={H:4.0f} {soil:<15} M={M / 1e3:7.0f} t  cae={r['fell']}  dist={r['distance']:.1f} m  "
              f"hundimiento={r['max_sink_m']:.2f} m  q_pie={r['peak_q_avg_kPa']:.0f} kPa", flush=True)
    json.dump(res, open(os.path.join(ROOT, "sim_e3.json"), "w"), indent=1, default=float)
    return res


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    video = "--video" in sys.argv
    if which in ("e1", "all"):
        e1(video)
    if which in ("e2", "all"):
        e2(video)
    if which in ("e3", "all"):
        e3(video)
