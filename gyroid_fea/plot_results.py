"""Gráficas del FEA de giroides frente a la literatura y a lo que afirma el documento."""
import csv
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..", "results")
FIG = os.path.join(ROOT, "figures")
rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "gyroid_fea.csv"))) if r["study"] == "sweep"]
fit = json.load(open(os.path.join(ROOT, "gyroid_fea_fit.json")))

rho = np.linspace(0.08, 0.6, 100)
fig, axs = plt.subplots(1, 3, figsize=(14, 4.4))

# --- rigidez
ax = axs[0]
for kind, col, lab in (("sheet", "#2a6fdb", "lámina (sheet)"), ("skeletal", "#d9622b", "red (skeletal)")):
    pts = [(float(r["rho"]), float(r["E100"]), float(r["E111"])) for r in rows if r["kind"] == kind]
    pts.sort()
    ax.plot([p[0] for p in pts], [p[1] for p in pts], "o-", color=col, label=f"FEA {lab}, E[100]")
    ax.plot([p[0] for p in pts], [p[2] for p in pts], "s--", color=col, alpha=0.6, ms=4, label=f"FEA {lab}, E[111]")
ax.plot(rho, 0.9 * rho ** 1.58, "k-", lw=1, label="Naghavi 2022, Ti64 lámina (ensayo)")
ax.plot(rho, 1.11 * rho ** 2.0, "m:", lw=2, label="Documento: 1.11·ρ^2.0")
ax.plot(rho, rho, color="0.6", lw=1, label="Límite teórico (Voigt): ρ")
ax.set_xlabel("Densidad relativa ρ*/ρs"); ax.set_ylabel("E*/Es")
ax.set_title("Rigidez relativa", fontsize=10); ax.legend(fontsize=7); ax.grid(alpha=0.3)

# --- resistencia
ax = axs[1]
for kind, col, lab in (("sheet", "#2a6fdb", "lámina"), ("skeletal", "#d9622b", "red")):
    pts = sorted((float(r["rho"]), 1.0 / float(r["vm_p99_x"])) for r in rows if r["kind"] == kind)
    ax.plot([p[0] for p in pts], [p[1] for p in pts], "o-", color=col, label=f"FEA {lab}: inicio de fluencia (cota inferior)")
ax.plot(rho, 0.536 * rho ** 1.45, "k-", lw=1, label="Naghavi 2022, Ti64 lámina (ensayo)")
ax.plot(rho, 1.189 * rho ** 1.86, "k--", lw=1, label="Al-Ketan 2018, red (ensayo)")
ax.plot(rho, 0.197 * rho ** 1.5, "m:", lw=2, label="Documento: 0.197·ρ^1.5 (su tabla)")
ax.plot(rho, rho ** 1.5, "m-.", lw=1.2, label="Documento: ρ^1.5 (su cálculo del 8.9 %)")
ax.plot(rho, rho, color="0.6", lw=1, label="Límite teórico (Voigt): ρ")
ax.axvline(0.2, color="0.8", lw=0.8)
ax.set_xlabel("Densidad relativa ρ*/ρs"); ax.set_ylabel("σ*/σs")
ax.set_title("Resistencia relativa", fontsize=10); ax.legend(fontsize=6.5); ax.grid(alpha=0.3)

# --- resistencia específica
ax = axs[2]
for lab, f, ls in (("Naghavi 2022 (Ti64 lámina)", lambda r: 0.536 * r ** 1.45, "k-"),
                   ("Al-Ketan 2018 (red)", lambda r: 1.189 * r ** 1.86, "k--"),
                   ("Documento (ρ^1.5)", lambda r: r ** 1.5, "m-."),
                   ("Espuma clásica (0.3·ρ^1.5)", lambda r: 0.3 * r ** 1.5, "c:")):
    ax.plot(rho, f(rho) / rho, ls, label=lab)
ax.axhline(1.0, color="0.4", lw=1.5)
ax.text(0.1, 1.03, "material macizo = 1", fontsize=8)
ax.set_ylim(0, 1.15)
ax.set_xlabel("Densidad relativa ρ*/ρs"); ax.set_ylabel("(σ*/ρ*) / (σs/ρs)")
ax.set_title("Resistencia específica relativa al macizo\n(< 1: el giroide aguanta menos por kilo)", fontsize=10)
ax.legend(fontsize=7); ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "giroide_fea.png"), dpi=150)
print("ok", {k: {kk: round(v, 3) for kk, v in d.items() if not isinstance(v, list)} for k, d in fit.items()})
