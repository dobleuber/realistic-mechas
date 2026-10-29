"""
Modelo de dimensionado de un mecha bípedo en función de su altura H.

Para cada altura se "diseña" el mecha y se resuelve su masa de forma
autoconsistente (la estructura y los actuadores dependen de la masa, que a su
vez depende de ellos). Se comparan tres conceptos estructurales para las
piernas:

  tubo          tubo de pared delgada de Ti-6Al-4V (monocasco, como un exoesqueleto)
  giroide       sección maciza rellena de giroide de Ti-6Al-4V (la propuesta del documento)
  tubo+giroide  tubo de pared delgada con núcleo de giroide que impide el pandeo local

Criterios que pueden limitar la altura:
  1. Espiral de masa: la masa no converge (estructura+actuadores+energía >= masa total).
  2. Encaje de actuadores: el cilindro hidráulico necesario no cabe en la pierna.
  3. Suelo: la presión bajo el pie supera la capacidad portante (ver soil.py).

Las cargas articulares salen de la simulación de MuJoCo de la marcha (sim/),
normalizadas por peso × altura, que son invariantes con similitud de Froude.
Todas las constantes y sus fuentes están en PARAMS y en docs/verificacion_fuentes.md.
"""
from __future__ import annotations

import json
import math
import os
import sys
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(__file__))
from soil import SOILS, bearing_capacity, equilibrium_sinkage  # noqa: E402

G = 9.81

# --------------------------------------------------------------------------
# Materiales (valores típicos; fuentes en docs/verificacion_fuentes.md)
# sigma_fat: resistencia a fatiga a ~1e7 ciclos (un mecha que camina años acumula ~1e7 pasos)
MATERIALS = {
    # Mahmud 2021 (INL): LPBF+HIP sy 928 MPa; fatiga LPBF+HIP+ataque químico ~450 MPa (R=0.1, 1e7)
    "Ti64": {"label": "Ti-6Al-4V (LPBF + HIP)", "rho": 4430, "E": 113.8e9, "sy": 928e6, "sfat": 450e6},
    # LPBF con alivio de tensiones: sy 1141 MPa; fatiga as-built ~210 MPa (rugosidad superficial)
    "Ti64_asbuilt": {"label": "Ti-6Al-4V (LPBF sin HIP)", "rho": 4430, "E": 113.8e9, "sy": 1141e6, "sfat": 210e6},
    "acero": {"label": "Acero 4340 templado y revenido", "rho": 7850, "E": 205e9, "sy": 1150e6, "sfat": 540e6},
    "Al7075": {"label": "Aluminio 7075-T6", "rho": 2810, "E": 71.7e9, "sy": 503e6, "sfat": 159e6},
    "CFRP": {"label": "CFRP cuasi-isótropo (IM7/8552)", "rho": 1580, "E": 57e9, "sy": 600e6, "sfat": 300e6},
}

# Gibson-Ashby para giroide tipo lámina (sheet) de Ti-6Al-4V LPBF (Naghavi et al. 2022):
#   E*/Es = 0.9 rho^1.58   ;   sy*/sys = 0.536 rho^1.45
# fatiga del giroide lámina en compresión ~45-50 % de su fluencia (Kelly 2021, Polley 2022): optimista.
# Nuestro FEA (gyroid_fea/) da E*/Es = 0.069 a rho = 0.2 frente a 0.071 de esta ley.
GYROID = {"C1": 0.9, "m": 1.58, "C2": 0.536, "n": 1.45, "r_fat": 0.45}


@dataclass
class Design:
    concept: str = "tubo"            # tubo | giroide | tubo+giroide
    material: str = "Ti64"
    # cargas (de la simulación MuJoCo, par pico / (peso·altura)), marcha lenta tipo ZMP
    load_coeff: dict = field(default_factory=lambda: {"hip": 0.067, "knee": 0.126, "ankle": 0.091, "hip_roll": 0.054})
    grf_peak: float = 1.3            # GRF pico al caminar [× peso] (literatura: 1.0–1.5)
    dlf: float = 1.5                 # factor de carga de diseño (tropiezos, control, impactos)
    sf_static: float = 1.5           # factor de seguridad sobre fluencia
    sf_fatigue: float = 1.2          # factor de seguridad sobre fatiga
    # geometría
    r_thigh: float = 0.035           # radio exterior del tubo estructural del muslo [× H]
    r_shank: float = 0.025           # ídem pantorrilla [× H]
    lever: float = 0.035             # brazo de palanca del cilindro hidráulico [× H]
    bore_max: float = 0.6            # diámetro máximo del cilindro / diámetro del miembro
    joint_factor: float = 1.6        # masa extra por articulaciones, rodamientos, uniones
    t_min: float = 0.003             # espesor mínimo de pared por fabricación/daño [m]
    # actuación
    pressure: float = 21e6           # presión hidráulica [Pa] (Atlas/HyQ ~ 20.7 MPa)
    act_kg_per_J: float = 5.0e-4     # masa de cilindro por trabajo F·s [kg/J]; Enerpac 0.24–0.34 kg/kJ (gatos de carrera corta), IIT/Moog ISA 2–3 kg/kJ
    ranges: dict = field(default_factory=lambda: {"hip": 1.8, "knee": 2.2, "ankle": 1.2, "hip_roll": 0.8})
    # energía (diésel-hidráulico)
    p_peak_norm: float = 0.079       # potencia mecánica pico / (M g sqrt(g H)) (simulación MuJoCo)
    p_mean_norm: float = 0.0144       # potencia positiva media / (M g sqrt(g H)) (simulación MuJoCo)
    eff: float = 0.45                # eficiencia hidráulica (EHA típico 30–60 %; válvulas ~22 %)
    pd_power: float = 150.0          # grupo diésel + bomba completo [W/kg] (motores solos 270–310 W/kg)
    e_storage: float = 0.40 * 43e6   # energía útil del gasóleo con motor al 40 % [J/kg]
    t_op: float = 3600.0             # autonomía [s]
    # resto
    f_upper: float = 0.8             # estructura+actuadores de tronco y brazos / los de las piernas
    f_skin: float = 0.10             # blindaje, cableado, carenado [fracción de la masa total]
    m_fixed: float = 1000.0          # cabina, piloto, sensores, electrónica [kg]
    foot_scale: float = 1.0          # escala lineal de la huella respecto a la humana
    # cuadrúpedo (por defecto, bípedo): número de patas y cuerpo horizontal que trabaja como viga
    n_legs: int = 2
    trunk_span: float = 0.0          # luz de la viga del cuerpo entre caderas y hombros [× H]; 0 = tronco vertical
    trunk_radius: float = 0.08       # radio del tubo del cuerpo [× H] (canto 0.16 H)
    trunk_torsion_arm: float = 0.13  # semiancho de vía: brazo de la torsión cuando falta una pata [× H]


# --------------------------------------------------------------------------
def tube_section(N: float, M: float, R: float, l: float, mat: dict, d: Design, core: bool):
    """Espesor mínimo de un tubo de radio R para axial N y flexión M. Devuelve (masa/longitud, info)."""
    s_allow = min(mat["sy"] / d.sf_static, mat["sfat"] / d.sf_fatigue)
    E = mat["E"]

    def stress(t):
        A = 2 * math.pi * R * t
        Z = math.pi * R * R * t
        return N / A + M / Z

    def local_buckling(t):
        if core:
            return float("inf")
        # NASA SP-8007: sigma_cr = gamma 0.605 E t/R, gamma = 1 - 0.901(1 - exp(-sqrt(R/t)/16))
        phi = math.sqrt(R / t) / 16
        gamma = 1 - 0.901 * (1 - math.exp(-phi))
        return gamma * 0.605 * E * t / R

    lo, hi = 1e-7 * R, R
    if stress(hi) > s_allow or stress(hi) > local_buckling(hi):
        return None
    for _ in range(100):
        t = math.sqrt(lo * hi)
        ok = stress(t) <= s_allow and stress(t) <= local_buckling(t)
        lo, hi = (lo, t) if ok else (t, hi)
    t = max(hi, min(d.t_min, R))
    # pandeo global (Euler, extremos articulados)
    I = math.pi * R ** 3 * t
    euler = math.pi ** 2 * E * I / l ** 2
    m_per_l = mat["rho"] * 2 * math.pi * R * t
    governing = ("espesor mínimo" if t > hi * 1.0001 else
                 "fatiga/fluencia" if stress(t) >= 0.99 * s_allow else "pandeo local")
    if core:
        # núcleo de giroide al 10 % de densidad que estabiliza la pared (espesor 0.3 R)
        m_per_l += mat["rho"] * 0.10 * math.pi * (R ** 2 - (0.7 * R) ** 2)
    return m_per_l, {"t": t, "t_over_R": t / R, "governing": governing, "euler_margin": euler / max(N, 1)}


def gyroid_section(N: float, M: float, R: float, mat: dict, d: Design):
    """Sección maciza circular de radio R rellena de giroide: densidad relativa mínima necesaria."""
    A = math.pi * R * R
    Z = math.pi * R ** 3 / 4
    s_req = N / A + M / Z
    g = GYROID
    # resistencia admisible del giroide a densidad rho: min(fluencia, fatiga) / SF
    def allow(rho):
        sy = g["C2"] * rho ** g["n"] * mat["sy"]
        return min(sy / d.sf_static, g["r_fat"] * sy / d.sf_fatigue)
    if allow(1.0) < s_req:
        return None
    lo, hi = 1e-4, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if allow(mid) < s_req else (lo, mid)
    rho = hi
    return mat["rho"] * rho * A, {"rho_rel": rho}


def design(H: float, d: Design = Design(), verbose=False):
    mat = MATERIALS[d.material]
    l_th, l_sh = 0.245 * H, 0.246 * H
    R_th, R_sh = d.r_thigh * H, d.r_shank * H
    r = d.lever * H

    m = 70.0 * (H / 1.75) ** 3 + d.m_fixed  # semilla
    info = {}
    for it in range(200):
        W = m * G
        Mj = {k: d.dlf * c * W * H for k, c in d.load_coeff.items()}
        Fact = {k: v / r for k, v in Mj.items()}
        grf = d.dlf * d.grf_peak * W
        # cargas por segmento
        N_th = grf + max(Fact["hip"], Fact["knee"])
        M_th = max(Mj["hip"], Mj["knee"], Mj["hip_roll"])
        N_sh = grf + max(Fact["knee"], Fact["ankle"])
        M_sh = max(Mj["knee"], Mj["ankle"])
        segs = {}
        ok = True
        for name, N, Mb, R, l in (("muslo", N_th, M_th, R_th, l_th), ("pantorrilla", N_sh, M_sh, R_sh, l_sh)):
            if d.concept == "giroide":
                res = gyroid_section(N, Mb, R, mat, d)
            else:
                res = tube_section(N, Mb, R, l, mat, d, core=(d.concept == "tubo+giroide"))
            if res is None:
                ok = False
                break
            res[1]["governing"] = res[1].get("governing", "fatiga/fluencia (giroide)")
            mpl, sinfo = res
            segs[name] = {"mass": mpl * l * d.joint_factor, **sinfo}
        if not ok:
            reason = ("espiral de masa" if it > 3 else "estructura: la sección no resiste ni maciza")
            return {"H": H, "feasible": False, "reason": reason, "m": m}
        m_struct_leg = sum(s["mass"] for s in segs.values())
        # pie: placa ~ misma masa por área que la pantorrilla (aprox.) -> 30 % de la pantorrilla
        m_struct_leg += 0.3 * segs["pantorrilla"]["mass"]
        # actuadores: masa ∝ trabajo de carrera F·s = M_j·rango
        m_act_leg = sum(d.act_kg_per_J * Mj[k] * d.ranges[k] for k in Mj)
        m_legs = d.n_legs * (m_struct_leg + m_act_leg)
        m_upper = d.f_upper * m_legs
        m_trunk = 0.0
        if d.trunk_span > 0:
            # cuerpo horizontal apoyado en caderas y hombros: flexión de viga biapoyada con carga
            # repartida (W·D/8) más la torsión cuando una pata está en el aire (pie × semiancho de vía)
            span = d.trunk_span * H
            Mb = d.dlf * W * span / 8
            Tq = d.dlf * d.grf_peak * W * d.trunk_torsion_arm * H
            M_eq = math.sqrt(Mb ** 2 + 0.75 * Tq ** 2)
            res = tube_section(0.0, M_eq, d.trunk_radius * H, 1.25 * span, mat, d, core=False)
            if res is None:
                return {"H": H, "feasible": False, "reason": "espiral de masa", "m": m}
            m_trunk = res[0] * 1.25 * span * d.joint_factor
            m_upper += m_trunk
        # energía
        P_peak = d.p_peak_norm * m * G * math.sqrt(G * H) / d.eff   # potencia hidráulica pico
        P_mean = d.p_mean_norm * m * G * math.sqrt(G * H)            # potencia mecánica media
        m_power = P_peak / d.pd_power + (P_mean / d.eff) * d.t_op / d.e_storage
        m_new = (m_legs + m_upper + m_power + d.m_fixed) / (1 - d.f_skin)
        if m_new > 1e12 or not math.isfinite(m_new):
            return {"H": H, "feasible": False, "reason": "espiral de masa", "m": m}
        if abs(m_new - m) < 1e-6 * m:
            m = m_new
            break
        m = 0.5 * m + 0.5 * m_new
    else:
        return {"H": H, "feasible": False, "reason": "espiral de masa (no converge)", "m": m}

    W = m * G
    # cilindro hidráulico de rodilla: área y diámetro
    A_cyl = max(Fact.values()) / d.pressure
    bore = math.sqrt(4 * A_cyl / math.pi)
    limb_d = 2 * R_th / 0.7     # diámetro del miembro (el tubo ocupa ~70 %)
    fits = bore <= d.bore_max * limb_d

    # pie y suelo
    B = 0.055 * H * d.foot_scale
    L = 0.152 * H * d.foot_scale
    q = d.grf_peak * W / (B * L)
    ground = {}
    for k, s in SOILS.items():
        qu = bearing_capacity(s, B, L)
        ground[k] = {"q_ult_kPa": qu / 1e3, "ratio": q / qu,
                     "sink_m": equilibrium_sinkage(s, B, L, q)}
    fr_speed = math.sqrt(0.25 * G * 0.53 * H)
    return {
        "H": H, "feasible": True, "m": m, "m_over_H3": m / H ** 3,
        "breakdown": {"estructura_piernas": d.n_legs * m_struct_leg, "actuadores_piernas": d.n_legs * m_act_leg,
                      "tronco_brazos": m_upper, "energia": m_power, "fijo": d.m_fixed,
                      "blindaje_cables": d.f_skin * m},
        "segments": segs, "bore_m": bore, "limb_d_m": limb_d, "actuator_fits": fits,
        "knee_torque_Nm": Mj["knee"], "actuator_force_N": max(Fact.values()),
        "P_peak_W": P_peak, "P_mean_W": P_mean,
        "foot_B_m": B, "foot_L_m": L, "q_foot_kPa": q / 1e3, "ground": ground,
        "walk_speed_Fr025_ms": fr_speed,
    }


SCENARIOS = {
    "optimista": dict(act_kg_per_J=2.4e-4, pd_power=300.0, eff=0.60, dlf=1.3, sf_static=1.25,
                      sf_fatigue=1.0, f_upper=0.6, f_skin=0.05, m_fixed=500.0, joint_factor=1.3),
    "base": dict(),
    "pesimista": dict(act_kg_per_J=2.0e-3, pd_power=100.0, eff=0.30, dlf=2.0, f_upper=1.0,
                      f_skin=0.15, m_fixed=2000.0, joint_factor=2.0),
}


def make_design(concept="tubo", scenario="base", **kw) -> Design:
    params = dict(SCENARIOS[scenario])
    params.update(kw)
    return Design(concept=concept, **params)


def sweep(d: Design, Hs=None):
    import numpy as np
    Hs = Hs if Hs is not None else np.geomspace(1.5, 1000, 300)
    return [design(float(H), d) for H in Hs]


def h_limits(d: Design, Hs=None):
    """Altura máxima por criterio (la mayor altura factible antes del primer fallo)."""
    rs = sweep(d, Hs)
    feas = [r for r in rs if r["feasible"]]
    h_mass = None
    seen = False
    for r in rs:
        if r["feasible"]:
            seen = True
        elif seen:
            h_mass = r["H"]
            break
    h_act = next((r["H"] for r in feas if not r["actuator_fits"]), None)
    soil = {}
    for k in SOILS:
        ok = [r["H"] for r in feas if r["ground"][k]["ratio"] <= 1.0]
        soil[k] = (min(ok), max(ok)) if ok else None
    return {"masa": h_mass, "actuador": h_act}, soil, rs


if __name__ == "__main__":
    for concept in ("tubo", "tubo+giroide", "giroide"):
        d = Design(concept=concept)
        print(f"\n=== {concept} ===")
        for H in (2, 5, 10, 20, 50):
            r = design(H, d)
            if not r["feasible"]:
                print(H, r["reason"])
                continue
            b = r["breakdown"]
            print(f"H={H:>4} m  masa={r['m'] / 1e3:9.1f} t  (m/H³={r['m_over_H3']:.1f})  "
                  f"estr={b['estructura_piernas'] / r['m']:.2%} act={b['actuadores_piernas'] / r['m']:.2%} "
                  f"energía={b['energia'] / r['m']:.2%}  q_pie={r['q_foot_kPa']:.0f} kPa  "
                  f"seg={json.dumps({k: {kk: round(vv, 4) for kk, vv in v.items() if isinstance(vv, float)} for k, v in r['segments'].items()})}")
        lim, soil_lim, _ = h_limits(d)
        print("límites:", lim)
        print("suelo (rango de H en que q <= q_ult):", {k: (tuple(round(x, 1) for x in v) if v else None) for k, v in soil_lim.items()})
