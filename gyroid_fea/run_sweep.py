"""
Barrido de densidades para giroides sheet y skeletal + ajuste de leyes de potencia
tipo Gibson-Ashby. Escribe results/gyroid_fea.csv, results/gyroid_fea_fit.json y
figuras en results/figures/.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from gyroid_homogenization import run  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)

N = int(os.environ.get("GYROID_N", 64))
RHOS = [0.10, 0.15, 0.20, 0.30, 0.40, 0.50]

rows = []
# convergencia de malla en un punto de referencia
for n in (32, 48, 64, 80):
    for kind in ("sheet", "skeletal"):
        r = run(kind, 0.2, n)
        r["study"] = "convergence"
        rows.append(r)
        print(kind, n, f"E={r['E100']:.4f} vm/σ={r['vm_p99_x']:.2f} t={r['seconds']:.0f}s", flush=True)

for kind in ("sheet", "skeletal"):
    for rho in RHOS:
        r = run(kind, rho, N)
        r["study"] = "sweep"
        rows.append(r)
        print(kind, rho, f"rho={r['rho']:.3f} E100={r['E100']:.4f} E111={r['E111']:.4f} "
              f"zener={r['zener']:.3f} vm99/σ={r['vm_p99_x']:.2f} t={r['seconds']:.0f}s", flush=True)

keys = ["study", "kind", "n", "rho", "E100", "E111", "zener", "nu12",
        "vm_mean_x", "vm_p99_x", "vm_p999_x", "vm_max_x", "vm_p99_111", "vm_max_111", "seconds"]
with open(os.path.join(ROOT, "gyroid_fea.csv"), "w") as f:
    f.write(",".join(keys) + "\n")
    for r in rows:
        f.write(",".join(str(r[k]) for k in keys) + "\n")

# Ajuste de leyes de potencia sobre el barrido
fits = {}
for kind in ("sheet", "skeletal"):
    sw = [r for r in rows if r["study"] == "sweep" and r["kind"] == kind]
    rho = np.array([r["rho"] for r in sw])
    E = np.array([r["E100"] for r in sw])
    # tensión macroscópica a la que el 1% más cargado del material alcanza la fluencia
    sy_first = 1.0 / np.array([r["vm_p99_x"] for r in sw])
    m, logC1 = np.polyfit(np.log(rho), np.log(E), 1)
    n_, logC2 = np.polyfit(np.log(rho), np.log(sy_first), 1)
    fits[kind] = {"E_exponent": m, "E_coeff": float(np.exp(logC1)),
                  "first_yield_exponent": n_, "first_yield_coeff": float(np.exp(logC2)),
                  "rho": rho.tolist(), "E": E.tolist(), "first_yield": sy_first.tolist()}
json.dump(fits, open(os.path.join(ROOT, "gyroid_fea_fit.json"), "w"), indent=1)
print(json.dumps({k: {kk: v for kk, v in d.items() if not isinstance(v, list)} for k, d in fits.items()}, indent=1))
