"""Gráficas de los experimentos de simulación (results/sim_e*.json)."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..", "results")
FIG = os.path.join(ROOT, "figures")
e1 = json.load(open(os.path.join(ROOT, "sim_e1.json")))
e2 = json.load(open(os.path.join(ROOT, "sim_e2.json")))
e3 = json.load(open(os.path.join(ROOT, "sim_e3.json")))

fig, axs = plt.subplots(1, 3, figsize=(14, 4.2))
ax = axs[0]
H = [r["H"] for r in e1]
for j, lab, col in (("knee_L", "rodilla", "#2a6fdb"), ("hip_pitch_L", "cadera", "#2fa36b"), ("ankle_pitch_L", "tobillo", "#d9622b")):
    ax.plot(H, [r["peak_tau_norm"][j] for r in e1], "o-", color=col, label=f"par pico {lab} / (peso·altura)")
ax.plot(H, [r["peak_grf_BW"] / 10 for r in e1], "ks--", label="fuerza en el suelo / peso (÷10)")
ax.set_xscale("log"); ax.set_ylim(0, 0.2)
ax.set_xlabel("Altura H [m]"); ax.set_title("E1: cargas normalizadas (similitud de Froude)", fontsize=10)
ax.legend(fontsize=7); ax.grid(alpha=0.3)

ax = axs[1]
f = [r["factor"] for r in e2]
ax.plot(f, [r["distance"] for r in e2], "o-", color="#2a6fdb")
for r in e2:
    ax.annotate("cae" if r["fell"] else "camina", (r["factor"], r["distance"]), fontsize=7,
                xytext=(0, 6), textcoords="offset points", ha="center", color="r" if r["fell"] else "g")
ax.axvline(1.0, color="0.5", ls=":")
ax.set_xlabel("Par máximo del actuador / par pico necesario"); ax.set_ylabel("Distancia recorrida [m] (plan: 21 m)")
ax.set_title("E2: mecha de 20 m con actuadores insuficientes", fontsize=10); ax.grid(alpha=0.3)

ax = axs[2]
labels = [f"{r['H']:.0f} m\n{r['soil'].replace('_', ' ')}" for r in e3]
cols = ["#c0392b" if r["fell"] else "#27ae60" for r in e3]
ax.bar(range(len(e3)), [max(r["max_sink_m"], 0.05) for r in e3], color=cols)
for i, r in enumerate(e3):
    ax.text(i, max(r["max_sink_m"], 0.05) * 1.1, "cae" if r["fell"] else "camina", ha="center", fontsize=7)
ax.set_yscale("log"); ax.set_ylim(0.03, 50)
ax.set_xticks(range(len(e3)), labels, fontsize=6.5)
ax.set_ylabel("Hundimiento máximo del pie [m]")
ax.set_title("E3: mecha con densidad humana sobre suelo deformable", fontsize=10); ax.grid(alpha=0.3, axis="y")
fig.tight_layout(); fig.savefig(os.path.join(FIG, "simulaciones.png"), dpi=150)
print("ok")
