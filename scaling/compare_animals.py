"""
Tamaño máximo de mechas cuadrúpedos con proporciones de elefante, rinoceronte e
hipopótamo, con el mismo modelo de espiral de masa que el bípedo.

Toma los coeficientes medidos por dinámica inversa en sim/animal_experiments.py
(results/sim_animales.json). Para cada arquetipo:

- n_legs = 4, con los pares, la carga por pie y la potencia medidos;
- el cuerpo es una viga tubular entre caderas y hombros, con su luz, su canto y
  su semiancho de vía (torsión);
- el resto del cuerpo (cinturas, cabina) es 0.3 × la masa de las patas, igual
  que en la comparación bípedo-cuadrúpedo;
- el pie es el del arquetipo, que fija la presión sobre el suelo.

Escribe results/animales_compare.json y results/figures/animales.png.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sim"))
from mech_scaling import SCENARIOS, design, h_limits, make_design  # noqa: E402

ROOT = os.path.join(HERE, "..", "results")


def load():
    return json.load(open(os.path.join(ROOT, "sim_animales.json")))


def design_for(data, key, scenario="base"):
    c = data["casos"][key]
    lc = {k: c["par"][k] for k in ("hip", "knee", "ankle", "hip_roll")}
    kw = dict(load_coeff=lc, grf_peak=c["grf_pie"], p_peak_norm=c["p_pico"], p_mean_norm=c["p_media"])
    if c["patas"] == 4:
        a = data["arquetipos"][key]["arch"]
        DX, WY, depth = a.get("DX", 0.53), a.get("WY", 0.13), a.get("body_depth", 0.16)
        f_up = SCENARIOS[scenario].get("f_upper", 0.8)
        kw.update(n_legs=4, f_upper=f_up * 0.375, trunk_span=DX, trunk_radius=depth / 2, trunk_torsion_arm=WY,
                  foot_L=a.get("foot_L"), foot_W=a.get("foot_W"))
    d = make_design("tubo", scenario, **kw)

    def dims(H):
        if c["patas"] == 2:
            return {"pata": 0.53 * H, "lomo": H, "largo": 0.2 * H}
        z = c.get("z_rel", 0.95) * 0.53 * H
        return {"pata": 0.53 * H, "lomo": z + depth * H, "largo": 1.25 * DX * H}
    lim, soil, rs = h_limits(d, np.geomspace(1.5, 1000, 400))
    Hmax = lim["masa"]
    H_video = 0.8 * Hmax if Hmax else 20.0
    r = design(H_video, d)
    return d, {"H_max": Hmax, "H_video": H_video, "M_video": r["m"] if r["feasible"] else float("nan"),
               "dims": dims, "soil": soil}


def main():
    data = load()
    out = {}
    for key in data["casos"]:
        out[key] = {}
        for sc in ("optimista", "base", "pesimista"):
            d, info = design_for(data, key, sc)
            Hm = info["H_max"]
            dm = info["dims"](Hm) if Hm else None
            r80 = design(0.8 * Hm, d) if Hm else None
            out[key][sc] = {
                "H_max": Hm, "dims_limite": dm,
                "masa_80pct_t": r80["m"] / 1e3 if r80 and r80["feasible"] else None,
                "dims_80pct": info["dims"](0.8 * Hm) if Hm else None,
                "presion_pie_80pct_kPa": r80.get("q_foot_kPa") if r80 and r80["feasible"] else None,
            }
            if sc == "base":
                print(f"{key:14s} H_max={Hm:.1f}  límite: pata {dm['pata']:.1f} m, lomo {dm['lomo']:.1f} m, "
                      f"largo {dm['largo']:.1f} m | al 80 %: {out[key][sc]['masa_80pct_t']:.0f} t, "
                      f"presión {out[key][sc]['presion_pie_80pct_kPa']:.0f} kPa")
    json.dump(out, open(os.path.join(ROOT, "animales_compare.json"), "w"), indent=1, default=float)
    return out




NOMBRES = {"bipedo": "Bípedo (su velocidad)", "bipedo_lento": "Bípedo lento", "generico": "Cuadrúpedo genérico",
           "elefante": "Tipo elefante", "rinoceronte": "Tipo rinoceronte", "hipopotamo": "Tipo hipopótamo"}


def plot(out=None):
    """Dos paneles: demanda de actuadores a la misma velocidad y tamaño máximo (escenario base)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    data = load()
    out = out or json.load(open(os.path.join(ROOT, "animales_compare.json")))
    keys = list(NOMBRES)
    ink, ink2, grid = "#0b0b0b", "#52514e", "#e4e3df"
    c_pata, c_alto, c_largo = "#2a78d6", "#eb6834", "#1baf7a"
    plt.rcParams.update({"font.size": 9, "text.color": ink, "axes.labelcolor": ink2, "xtick.color": ink2,
                         "ytick.color": ink, "axes.edgecolor": grid})
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.4), gridspec_kw={"width_ratios": [1, 1.35]})
    y = np.arange(len(keys))[::-1]
    # panel 1: suma de par × recorrido de todos los actuadores (normalizada), menor es mejor
    ax = axs[0]
    vals = [data["casos"][k]["suma_par_recorrido"] for k in keys]
    ax.barh(y, vals, height=0.55, color="#8f8d86")
    for yi, v, k in zip(y, vals, keys):
        vel = data["casos"][k]["v"] / data["casos"]["bipedo"]["v"]
        ax.text(v + 0.02, yi, f"{v:.2f}  ({vel:.0%} de velocidad)", va="center", color=ink2, fontsize=8)
    ax.set_yticks(y, [NOMBRES[k] for k in keys])
    ax.set_xlim(0, max(vals) * 1.55)
    ax.set_xlabel("Σ par × recorrido de todos los actuadores (normalizado; menos es mejor)")
    ax.set_title("Lo que hay que construir en actuadores", loc="left", fontsize=10, color=ink)
    ax.grid(axis="x", color=grid, lw=0.8)
    ax.set_axisbelow(True)
    for s_ in ("top", "right", "left"):
        ax.spines[s_].set_visible(False)
    # panel 2: dimensiones en el límite de la espiral de masa (escenario base)
    ax = axs[1]
    h = 0.24
    series = (("pata", "Longitud de pata", c_pata), ("lomo", "Altura (cabeza o lomo)", c_alto),
              ("largo", "Largo del cuerpo", c_largo))
    for j, (campo, lab, col) in enumerate(series):
        vv = []
        for k in keys:
            d = out[k]["base"]["dims_limite"]
            vv.append(np.nan if (campo == "largo" and data["casos"][k]["patas"] == 2) else d[campo])
        yy = y + (1 - j) * (h + 0.02)
        ax.barh(yy, vv, height=h, color=col, label=lab)
        for yi, v in zip(yy, vv):
            if np.isfinite(v):
                ax.text(v + 0.6, yi, f"{v:.0f} m", va="center", color=ink2, fontsize=7.5)
    ax.set_yticks(y, ["" for _ in keys])
    ax.set_xlabel("metros, en el límite del escenario base")
    ax.set_title("Tamaño máximo", loc="left", fontsize=10, color=ink)
    ax.legend(frameon=False, loc="lower right", fontsize=8)
    ax.grid(axis="x", color=grid, lw=0.8)
    ax.set_axisbelow(True)
    for s_ in ("top", "right", "left"):
        ax.spines[s_].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(ROOT, "figures", "animales.png"), dpi=150, facecolor="#fcfcfb")


if __name__ == "__main__":
    plot(main())
