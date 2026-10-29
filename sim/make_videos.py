"""Genera los vídeos de los casos representativos (MUJOCO_GL=osmesa en máquinas sin GPU)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "scaling"))
from walk import simulate  # noqa: E402
from experiments import torque_limits, VID  # noqa: E402
from mech_scaling import design, make_design  # noqa: E402
from soil import SOILS  # noqa: E402

d = make_design("tubo", "base")
cases = []
for H in (1.75, 20.0, 28.0):
    M = 70.0 if H == 1.75 else design(H, d)["m"]
    cases.append((f"e1_marcha_H{H:g}.mp4", dict(H=H, M=M, torque_limit=torque_limits(M, H, 1.5)),
                  f"Diseño base (tubo Ti): H = {H:g} m, M = {M / 1e3:.1f} t"))
M20 = design(20.0, d)["m"]
cases.append(("e2_par_60pct_H20.mp4", dict(H=20.0, M=M20, torque_limit=torque_limits(M20, 20.0, 0.6)),
              f"H = 20 m, M = {M20 / 1e3:.1f} t, actuadores al 60 % del par necesario"))
for H, soil in ((20.0, "arcilla_blanda"), (50.0, "arcilla_blanda"), (50.0, "arena_densa")):
    M = 13.06 * H ** 3
    cases.append((f"e3_{soil}_H{H:g}.mp4", dict(H=H, M=M, torque_limit=torque_limits(M, H, 1.5), soil=SOILS[soil]),
                  f"Densidad humana: H = {H:g} m, M = {M / 1e3:.0f} t, suelo: {SOILS[soil]['label']}"))
only = sys.argv[1:]
for fn, kw, label in cases:
    if only and not any(o in fn for o in only):
        continue
    r = simulate(**kw, video=os.path.join(VID, fn), label=label)
    print(fn, "cae" if r["fell"] else "camina", round(r["distance"], 1), flush=True)
