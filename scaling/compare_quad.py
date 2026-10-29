"""
Bípedo frente a cuadrúpedo con el mismo modelo de dimensionado (espiral de masa).

Los coeficientes de carga y potencia salen de las simulaciones de MuJoCo
(sim/quad_experiments.py), medidos igual en los dos robots: pares y potencias
filtrados a 10 Hz (escala humana, con similitud de Froude), porque por encima de
eso solo hay vibración numérica de patas rígidas sobre suelo rígido, que un
actuador hidráulico no seguiría.

El cuadrúpedo usa cuatro patas idénticas a las del bípedo de altura equivalente H
(pata = 0.53 H) y un cuerpo horizontal que trabaja como viga entre caderas y
hombros. El resto del cuerpo (cinturas, cabina, cuello) se toma como 0.3 × la
masa de las patas frente al 0.8 del bípedo, que incluye tronco y brazos; también
se calcula el caso con la misma regla que el bípedo.

Escribe results/quad_compare.json y results/figures/bipedo_vs_cuadrupedo.png.
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mech_scaling import SCENARIOS, design, h_limits, make_design  # noqa: E402

ROOT = os.path.join(HERE, "..", "results")


def load_cases():
    sim = json.load(open(os.path.join(ROOT, "sim_quad.json")))
    return sim["casos"]


def make(case: dict, scenario: str, same_rule=False):
    lc = {k: case["par"][k] for k in ("hip", "knee", "ankle", "hip_roll")}
    kw = dict(load_coeff=lc, grf_peak=case["grf_pie"], p_peak_norm=case["p_pico"], p_mean_norm=case["p_media"])
    if case["patas"] == 4:
        f_up = SCENARIOS[scenario].get("f_upper", 0.8)
        kw.update(n_legs=4)
        if not same_rule:
            kw.update(f_upper=f_up * 0.375, trunk_span=0.53)
    return make_design("tubo", scenario, **kw)


def mass_at(d, H):
    r = design(H, d)
    return r["m"] if r["feasible"] else float("nan")


def main():
    cases = load_cases()
    Hs = np.geomspace(1.5, 1000, 300)
    out = {}
    for key, c in cases.items():
        for sc in ("optimista", "base", "pesimista"):
            for same in ((False, True) if c["patas"] == 4 else (False,)):
                d = make(c, sc, same)
                lim, soil, rs = h_limits(d, Hs)
                tag = f"{key}|{sc}" + ("|misma_regla" if same else "")
                Hmax = lim["masa"]
                feas = [r for r in rs if r["feasible"]]
                last = feas[-1] if feas else None
                out[tag] = {
                    "H_max": Hmax, "patas": c["patas"], "velocidad_rel": c["v_rel"],
                    "masa_cerca_del_limite_t": last["m"] / 1e3 if last else None,
                    "H_cerca_del_limite": last["H"] if last else None,
                    "masa_20m_t": mass_at(d, 20.0) / 1e3,
                    "presion_pie_20m_kPa": design(20.0, d).get("q_foot_kPa"),
                    "suelo": {k: v for k, v in soil.items()},
                }
                print(f"{tag:40s} H_max={Hmax and round(Hmax, 1)}  masa(20 m)={out[tag]['masa_20m_t']:.1f} t  "
                      f"q_pie(20 m)={out[tag]['presion_pie_20m_kPa'] or float('nan'):.0f} kPa")
    json.dump(out, open(os.path.join(ROOT, "quad_compare.json"), "w"), indent=1, default=float)
    plot(cases)


def plot(cases):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    Hs = np.geomspace(3, 120, 200)
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.6))
    styles = {"optimista": ":", "base": "-", "pesimista": "--"}
    colors = {"bipedo": "#2a6fdb", "bipedo_lento": "#7aa6ef", "cuadrupedo": "#d1495b", "cuadrupedo_rapido": "#f08a4b"}
    for key, c in cases.items():
        for sc, ls in styles.items():
            d = make(c, sc)
            m = np.array([mass_at(d, H) for H in Hs])
            lab = f"{c['nombre']}" if sc == "base" else None
            axs[0].plot(Hs, m / 1e3, ls, color=colors.get(key, "k"), label=lab, lw=1.8 if sc == "base" else 1.1)
            # altura real del punto más alto: bípedo H; cuadrúpedo, lomo/cabina a ~0.73 H
            hreal = Hs if c["patas"] == 2 else 0.73 * Hs
            axs[1].plot(m / 1e3, hreal, ls, color=colors.get(key, "k"), label=lab, lw=1.8 if sc == "base" else 1.1)
    for ax in axs:
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.grid(True, which="both", alpha=0.3)
    axs[0].set_xlabel("Altura equivalente H [m] (pata = 0.53 H)")
    axs[0].set_ylabel("Masa del mecha [t]")
    axs[0].set_title("Masa frente a tamaño (continua: base; punteada: optimista; discontinua: pesimista)", fontsize=9)
    axs[1].set_xlabel("Masa del mecha [t]")
    axs[1].set_ylabel("Altura del punto más alto [m]")
    axs[1].set_title("Para la misma masa, el cuadrúpedo es más bajo y más largo", fontsize=9)
    axs[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(ROOT, "figures", "bipedo_vs_cuadrupedo.png"), dpi=150)


if __name__ == "__main__":
    main()
