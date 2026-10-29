"""
Análisis completo del modelo de escalado: escenarios, límites de altura y gráficas.
Escribe results/scaling_limits.json y figuras en results/figures/.
"""
import json
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, os.path.dirname(__file__))
from mech_scaling import make_design, h_limits, design, SCENARIOS, MATERIALS  # noqa: E402
from soil import SOILS, bearing_capacity, equilibrium_sinkage  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..", "results")
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)
CONCEPTS = {"tubo": "Tubo de Ti-6Al-4V", "tubo+giroide": "Tubo + núcleo giroide", "giroide": "Relleno de giroide (documento)"}
COLORS = {"tubo": "#2a6fdb", "tubo+giroide": "#2fa36b", "giroide": "#d9622b"}
Hs = np.geomspace(3.0, 200, 160)

out = {"limits": {}, "materials": {}}
for sc in SCENARIOS:
    for c in CONCEPTS:
        lim, soil, rs = h_limits(make_design(c, sc), Hs)
        out["limits"][f"{c}|{sc}"] = {"masa": lim["masa"], "actuador": lim["actuador"],
                                      "suelo": {k: v for k, v in soil.items()}}
        print(f"{sc:<10} {c:<14} H_max(masa) = {lim['masa']}")

# materiales en el escenario base, concepto tubo
for mk in MATERIALS:
    lim, _, _ = h_limits(make_design("tubo", "base", material=mk), Hs)
    out["materials"][mk] = lim["masa"]
    print(f"material {mk:<14} H_max = {lim['masa']}")

# ------------------------------------------------------------------ figura 1: masa vs H
fig, ax = plt.subplots(figsize=(7.5, 4.8))
for c, lab in CONCEPTS.items():
    for sc, ls in (("base", "-"), ("optimista", ":"), ("pesimista", "--")):
        rs = [design(float(H), make_design(c, sc)) for H in Hs]
        x = [r["H"] for r in rs if r["feasible"]]
        y = [r["m"] / 1e3 for r in rs if r["feasible"]]
        ax.plot(x, y, ls, color=COLORS[c], lw=2 if sc == "base" else 1.2,
                label=f"{lab} ({sc})" if sc == "base" else None)
ax.plot(Hs, 70 * (Hs / 1.75) ** 3 / 1e3, color="0.5", lw=1, label="Humano escalado (m ∝ H³)")
for name, H, m in (("LW Mononofu", 8.46, 7.3), ("Gundam Yokohama*", 18, 25), ("Tradinno (cuadrúpedo)", 8.2, 11),
                   ("Archax", 4.5, 3.5), ("Atlas hidráulico", 1.5, 0.08)):
    ax.scatter([H], [m], color="k", s=14, zorder=5)
    ax.annotate(name, (H, m), fontsize=7, xytext=(4, -3), textcoords="offset points")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("Altura H [m]"); ax.set_ylabel("Masa total [t]")
ax.set_title("Masa del mecha diseñado vs altura\n(línea continua: base; punteada: optimista; discontinua: pesimista)", fontsize=10)
ax.grid(True, which="both", alpha=0.25); ax.legend(fontsize=7, loc="upper left")
fig.text(0.01, 0.01, "* sostenido por una estructura, no camina", fontsize=7)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "masa_vs_altura.png"), dpi=150); plt.close(fig)

# ------------------------------------------------------------------ figura 2: desglose de masa
d = make_design("tubo", "base")
rs = [design(float(H), d) for H in Hs]
rs = [r for r in rs if r["feasible"]]
keys = ["estructura_piernas", "actuadores_piernas", "tronco_brazos", "energia", "blindaje_cables", "fijo"]
labs = ["Estructura piernas", "Actuadores piernas", "Tronco y brazos", "Energía (motor+bomba+combustible)", "Blindaje y cableado", "Cabina/piloto/electrónica"]
fr = np.array([[r["breakdown"][k] / r["m"] for k in keys] for r in rs]).T
fig, ax = plt.subplots(figsize=(7.5, 4.5))
ax.stackplot([r["H"] for r in rs], fr, labels=labs, alpha=0.85)
ax.set_xscale("log"); ax.set_xlim(3.0, rs[-1]["H"]); ax.set_ylim(0, 1)
ax.set_xlabel("Altura H [m]"); ax.set_ylabel("Fracción de la masa total")
ax.set_title("Desglose de masa (tubo de Ti, escenario base): al llegar a 100 % la masa diverge", fontsize=10)
ax.legend(fontsize=7, loc="upper left"); ax.grid(True, alpha=0.25)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "desglose_masa.png"), dpi=150); plt.close(fig)

# ------------------------------------------------------------------ figura 3: presión en el pie vs capacidad
fig, ax = plt.subplots(figsize=(7.5, 4.8))
Hh = np.geomspace(3.0, 100, 120)
for lab, mfun, col in (("Mecha con densidad humana (m = 13 kg/m³ · H³)", lambda H: 13.06 * H ** 3, "k"),):
    q = [1.3 * mfun(H) * 9.81 / ((0.055 * H) * (0.152 * H)) / 1e3 for H in Hh]
    ax.plot(Hh, q, color=col, lw=2.2, label=lab)
rs = [design(float(H), make_design("tubo", "base")) for H in Hh]
ax.plot([r["H"] for r in rs if r["feasible"]], [r["q_foot_kPa"] for r in rs if r["feasible"]],
        color=COLORS["tubo"], lw=2, label="Mecha diseñado (tubo Ti, base)")
for k, col in (("arcilla_blanda", "#8c564b"), ("arcilla_dura", "#c49c94"), ("arena_suelta", "#bcbd22"),
               ("arena_densa", "#dbdb8d"), ("pavimento", "#7f7f7f"), ("granito", "#17becf")):
    qu = [bearing_capacity(k, 0.055 * H, 0.152 * H) / 1e3 for H in Hh]
    ax.plot(Hh, qu, "--", color=col, lw=1.2, label=f"q_ult {SOILS[k]['label']}")
ax.axhline(574.6, color="r", lw=0.8, ls=":")
ax.text(3.1, 450, "574 kPa: valor admisible de código para roca (no es su resistencia)", fontsize=7, color="r")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_ylim(5, 5e4)
ax.set_xlabel("Altura H [m] (pie con proporciones humanas)"); ax.set_ylabel("Presión bajo un pie [kPa]")
ax.set_title("Presión bajo el pie (1.3 × peso en apoyo simple) frente a la capacidad portante última", fontsize=10)
ax.grid(True, which="both", alpha=0.25); ax.legend(fontsize=6.5, loc="upper left", ncol=2)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "presion_suelo.png"), dpi=150); plt.close(fig)

# ------------------------------------------------------------------ tabla: mecha de densidad humana sobre cada suelo
tab = {}
for H in (5, 10, 15, 20, 30, 50):
    m = 13.06 * H ** 3
    B, L = 0.055 * H, 0.152 * H
    q = 1.3 * m * 9.81 / (B * L)
    tab[H] = {"m_t": m / 1e3, "q_kPa": q / 1e3,
              "suelos": {k: {"q_ult_kPa": bearing_capacity(k, B, L) / 1e3,
                             "hundimiento_m": equilibrium_sinkage(k, B, L, q)} for k in SOILS}}
out["densidad_humana"] = tab
json.dump(out, open(os.path.join(ROOT, "scaling_limits.json"), "w"), indent=1, default=float)
print(json.dumps({H: {"m_t": round(v["m_t"], 1), "q_kPa": round(v["q_kPa"]),
                      "hund_m": {k: round(s["hundimiento_m"], 2) for k, s in v["suelos"].items()}} for H, v in tab.items()}, indent=0))

# ------------------------------------------------------------------ figura 4: altura máxima por escenario
fig, ax = plt.subplots(figsize=(7.5, 4.2))
scs = list(SCENARIOS)
w = 0.26
for i, (c, lab) in enumerate(CONCEPTS.items()):
    vals = [out["limits"][f"{c}|{sc}"]["masa"] or 0 for sc in scs]
    bars = ax.bar(np.arange(len(scs)) + (i - 1) * w, vals, w, color=COLORS[c], label=lab)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v * 1.05 if v else 2.3, f"{v:.0f} m" if v else "< 3 m",
                ha="center", fontsize=8)
ax.axhspan(15, 20, color="#d9622b", alpha=0.12)
ax.text(2.45, 16.2, "rango del\ndocumento", fontsize=7, color="#a04010", ha="right")
ax.set_yscale("log"); ax.set_ylim(2, 200)
ax.set_xticks(range(len(scs)), [s.capitalize() for s in scs])
ax.set_ylabel("Altura máxima antes de la espiral de masa [m]")
ax.set_title("Altura máxima de un mecha bípedo que camina, por concepto estructural y escenario", fontsize=10)
ax.legend(fontsize=8); ax.grid(True, axis="y", which="both", alpha=0.25)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "altura_maxima.png"), dpi=150); plt.close(fig)
