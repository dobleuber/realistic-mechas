"""
Mechas cuadrúpedos con proporciones y postura de elefante, rinoceronte e
hipopótamo, comparados con el cuadrúpedo genérico y con el bípedo.

Todos los casos se miden igual, por dinámica inversa (sim/inverse_dynamics.py):
el par que necesita un mecha bien controlado para seguir el plan, con las
fuerzas de los pies dirigidas a lo largo de la pata. La simulación directa en
MuJoCo se usa para comprobar que cada diseño camina sin caerse y para los vídeos.

Las proporciones salen de docs/investigacion/elefante_rinoceronte_hipopotamo.md.

Uso:  python sim/animal_experiments.py [--video]
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
from gait import GaitParams, plan  # noqa: E402
from inverse_dynamics import biped_id, id_metrics, quad_id  # noqa: E402
from mech_model import JOINTS as BJ  # noqa: E402
from quad_gait import AnimalGait, plan_animal  # noqa: E402
from quad_model import JOINTS as QJ, LEGS  # noqa: E402
from quad_walk import simulate_quad  # noqa: E402

ROOT = os.path.join(HERE, "..", "results")
VID = os.path.join(ROOT, "videos")
H0 = 1.75
L0 = 0.53 * H0
G = 9.81

# Marcha común a los cuadrúpedos: paso estáticamente estable (factor de apoyo 0.79), zancada de 0.45 L
# por ciclo y número de Froude 0.0017 (0.124 m/s con patas de 0.93 m: el «gateo lento» de la comparación
# anterior). Con factores de apoyo menores de 0.75 el plan exige centros de presión fuera de la suela.
GAIT = dict(duty=0.794, stride=0.453, froude=0.00169)

# Bípedos de referencia: marcha de E1 y la misma marcha más lenta (0.119 m/s, la velocidad de los cuadrúpedos).
# Todos los casos usan el reparto de fuerzas que minimiza los pares (control de fuerza ideal).
BIPEDS = {
    "bipedo": dict(nombre="Bípedo (marcha de E1)", gp=dict(t_ss=0.7, t_ds=0.25)),
    "bipedo_lento": dict(nombre="Bípedo a la velocidad de los cuadrúpedos", gp=dict(t_ss=1.6, t_ds=0.6)),
}


def L_(x):
    """Longitud relativa a la pata L -> fracción de H (la pata mide 0.53 H)."""
    return 0.53 * x


# Arquetipos. Longitudes relativas a la longitud de pata L (altura de la cadera con la pata estirada).
#   D: distancia hombro-cadera; w: semiancho de vía; prof: canto del cuerpo; cruz: altura del lomo;
#   pie: área de la suela A/L². Fuentes y derivaciones en docs/investigacion/elefante_rinoceronte_hipopotamo.md.
TROTE = (("LH", 0.0), ("RF", 0.0), ("RH", 0.5), ("LF", 0.5))


def arch_from(D, w, prof, cruz, pie_L, pie_W, ankle_x, front, knee_front=1, hip_rel=0.95):
    """Parámetros del modelo (en fracciones de H = L / 0.53) a partir de proporciones relativas a L."""
    centro = cruz - prof / 2 - hip_rel          # centro del cuerpo sobre la cadera [× L]
    return dict(DX=L_(D), WY=L_(w), body_depth=L_(prof), body_z=L_(centro), foot_L=L_(pie_L), foot_W=L_(pie_W),
                ankle_x=ankle_x, front_share=front, knee_front=knee_front, knee_hind=1)


def disc(A):
    """Diámetro [× L] de un pie redondo de área A [× L²]."""
    return math.sqrt(4 * A / math.pi)


ARQUETIPOS = {
    "generico": dict(
        nombre="Cuadrúpedo genérico (patas del bípedo)",
        arch=dict(),
        gait=dict(knee_min=0.83)),
    # Elefante: tronco tan largo como la pata (GAD ≈ 0.95 L), vía estrecha (0.27 L), canto 0.59 L, cruz 1.44 L,
    # rodilla y codo flexionados solo 23-28° a mitad de apoyo (Ren et al. 2008), 60 % del peso delante,
    # pies redondos de A ≈ 0.04 L², secuencia lateral.
    "elefante": dict(
        nombre="Mecha tipo elefante",
        arch=arch_from(D=0.95, w=0.135, prof=0.59, cruz=1.44, pie_L=disc(0.04), pie_W=disc(0.04), ankle_x=0.0,
                       front=0.60),
        gait=dict(knee_min=0.42)),
    # Rinoceronte blanco: tronco largo (GAD ≈ 1.6 L), vía 0.30 L, canto ≈ 1.0 L, cruz ≈ 1.55 L, patas cortas
    # y flexionadas (huesos a 39-50° de la fuerza al trote, frente a 18-20° del elefante), 62 % delante,
    # pie de 0.29 × 0.23 L (A ≈ 0.035 L²), secuencia lateral.
    "rinoceronte": dict(
        nombre="Mecha tipo rinoceronte",
        arch=arch_from(D=1.6, w=0.15, prof=1.0, cruz=1.55, pie_L=0.29, pie_W=0.23, ankle_x=0.2, front=0.62),
        gait=dict(knee_min=0.8)),
    # Hipopótamo: tronco largo (GAD ≈ 1.5 L) y el más ancho (vía 0.39 L), canto 0.8 L, cruz ≈ 1.3 L, patas
    # flexionadas, ~60 % delante (supuesto), pies pequeños (A ≈ 0.02 L², sin dato publicado), y trota
    # siempre: diagonales sincronizadas (Hutchinson y Pringle 2024).
    "hipopotamo": dict(
        nombre="Mecha tipo hipopótamo",
        arch=arch_from(D=1.5, w=0.195, prof=0.8, cruz=1.3, pie_L=disc(0.02), pie_W=disc(0.02), ankle_x=0.1,
                       front=0.60),
        gait=dict(knee_min=0.8, phases=TROTE)),
}

# Variantes «fieles»: la pata delantera dobla como la del animal, con el codo hacia atrás. En el mecha sale
# peor (más par en la rodilla delantera), así que los arquetipos de arriba la doblan hacia delante.
for _k in ("elefante", "rinoceronte", "hipopotamo"):
    _a = ARQUETIPOS[_k]
    ARQUETIPOS[_k + "_codo_atras"] = dict(nombre=_a["nombre"] + ", codo hacia atrás",
                                          arch={**_a["arch"], "knee_front": -1}, gait=dict(_a["gait"]))


def plan_for(key):
    a = ARQUETIPOS[key]
    ag = AnimalGait(**{**GAIT, **a["gait"]})
    return plan_animal(ag, a["arch"]), a["arch"]


def run_id_quad(key):
    pl, arch = plan_for(key)
    m = id_metrics(quad_id(pl, arch), QJ)
    m.update(v=pl.speed, z_var=pl.z_var, patas=4, nombre=ARQUETIPOS[key]["nombre"],
             z_rel=float(np.mean(pl.body[:, 2]) / L0),
             knee_stance=float(np.abs(pl.q[:, [QJ.index(f"knee_{lg}") for lg in LEGS]]).min()))
    return m


def run_id_biped(key):
    pl = plan(GaitParams(**BIPEDS[key]["gp"]))
    m = id_metrics(biped_id(pl), BJ)
    m.update(v=pl.speed, patas=2, nombre=BIPEDS[key]["nombre"])
    return m


def rasgos(key="elefante"):
    """Efecto de cada rasgo del animal, partiendo del cuadrúpedo genérico: uno a uno y acumulados."""
    t_arch, t_gait = ARQUETIPOS[key]["arch"], ARQUETIPOS[key]["gait"]
    pasos = [("postura (patas más rectas)", {}, {"knee_min": t_gait["knee_min"]}),
             ("vía (ancho entre pies)", {"WY": t_arch["WY"]}, {}),
             ("largo del cuerpo", {"DX": t_arch["DX"]}, {}),
             ("canto y altura del cuerpo", {"body_depth": t_arch["body_depth"], "body_z": t_arch["body_z"]}, {}),
             ("reparto de peso delante", {"front_share": t_arch["front_share"]}, {}),
             ("pies", {"foot_L": t_arch["foot_L"], "foot_W": t_arch["foot_W"], "ankle_x": t_arch["ankle_x"]}, {}),
             ("codo hacia atrás", {"knee_front": -1}, {})]
    if "phases" in t_gait:
        pasos.insert(-1, ("trote", {}, {"phases": t_gait["phases"]}))

    def total(arch, gait):
        pl = plan_animal(AnimalGait(**{**GAIT, **gait}), arch)
        p = id_metrics(quad_id(pl, arch), QJ)["par"]
        return 4 * (p["hip"] * 1.8 + p["knee"] * 2.2 + p["ankle"] * 1.2 + p["hip_roll"] * 0.8)
    base_g = dict(ARQUETIPOS["generico"]["gait"])
    out = {"base": total({}, base_g), "solo": {}, "acumulado": {}}
    acc_a, acc_g = {}, dict(base_g)
    for name, da, dg in pasos:
        out["solo"][name] = total(da, {**base_g, **dg})
        acc_a.update(da)
        acc_g.update(dg)
        out["acumulado"][name] = total(dict(acc_a), dict(acc_g))
        print(f"  {key}: {name:28s} solo {out['solo'][name]:.2f}  acumulado {out['acumulado'][name]:.2f}", flush=True)
    return out


def run_forward(key, H=1.75, M=None, video=None, label=""):
    pl, arch = plan_for(key)
    M = M or 100.0 * (H / H0) ** 3
    _, s = simulate_quad(H, M, plan=pl, arch=arch, record_every=5, video=video, label=label)
    return {"cae": bool(s["fell"]), "avance_L": s["distance"] / (0.53 * H)}


def main(video=False):
    res = {}
    for key in BIPEDS:
        res[key] = run_id_biped(key)
    for key in ARQUETIPOS:
        res[key] = run_id_quad(key)
        res[key]["simulacion_directa"] = run_forward(key)
    for key, r in res.items():
        p = r["par"]
        r["suma_par_recorrido"] = r["patas"] * (p["hip"] * 1.8 + p["knee"] * 2.2 + p["ankle"] * 1.2 + p["hip_roll"] * 0.8)
        print(f"{key:24s} v={r['v']:.3f} Σ={r['suma_par_recorrido']:.2f} " + " ".join(f"{k} {v:.3f}" for k, v in r["par"].items()) +
              f" | GRF/pie {r['grf_pie']:.2f} Ppk {r['p_pico']:.3f} Pm {r['p_media']:.4f}" +
              (f" | CoP {r['cop_max']:.2f} roz {r['rozamiento_max']:.2f} camina={not r['simulacion_directa']['cae']}"
               if r["patas"] == 4 else ""), flush=True)
    print(f"rasgos del elefante (Σ par·recorrido; genérico = base)")
    efectos = {"elefante": rasgos("elefante")}
    json.dump({"casos": res, "marcha": GAIT, "rasgos": efectos, "arquetipos": {k: {kk: vv for kk, vv in a.items()}
                                                            for k, a in ARQUETIPOS.items()}},
              open(os.path.join(ROOT, "sim_animales.json"), "w"), indent=1, default=float)
    if video:
        make_videos()


def make_videos(only=None):
    from compare_animals import design_for, load
    os.makedirs(VID, exist_ok=True)
    data = load()
    for key in ARQUETIPOS:
        if key == "generico" or key.endswith("_codo_atras") or (only and key not in only):
            continue
        d, info = design_for(data, key, "base")
        H = info["H_video"]
        M = info["M_video"]
        dims = info["dims"](H)
        label = (f"{ARQUETIPOS[key]['nombre']}: patas de {dims['pata']:.0f} m, lomo a {dims['lomo']:.0f} m, "
                 f"{dims['largo']:.0f} m de largo, {M / 1e3:.0f} t")
        print("vídeo", key, label)
        run_forward(key, H=H, M=M, video=os.path.join(VID, f"animal_{key}.mp4"), label=label)


if __name__ == "__main__":
    if "--solo-videos" in sys.argv:
        make_videos()
    else:
        main(video="--video" in sys.argv)
