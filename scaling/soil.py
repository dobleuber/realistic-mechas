"""
Capacidad portante del suelo bajo el pie del mecha.

Fórmula general de Terzaghi con los factores de Vesić (capacidad), De Beer/Vesić
(forma) y Hansen (profundidad):

    q_ult = c·Nc·sc·dc + γ·D·Nq·sq·dq + 0.5·γ·B·Nγ·sγ·dγ

    Nq = e^(π tanφ) · tan²(45° + φ/2)
    Nc = (Nq − 1)·cot φ          (φ = 0  ->  Nc = π + 2 = 5.14)
    Nγ = 2·(Nq + 1)·tan φ        (Vesić 1973)

Puntos clave para el escalado:
  * Arcilla saturada (carga rápida, φ = 0): q_ult ≈ 5.14·cu·(1+0.2 B/L) — NO
    depende del tamaño del pie. La presión del mecha crece ∝ H, así que hay
    una altura máxima.
  * Arena/grava (c = 0): el término 0.5·γ·B·Nγ crece ∝ B. Si el pie crece en
    proporción, capacidad y presión crecen ambas ∝ H: el cociente se mantiene
    (lo que aumenta es el asentamiento absoluto, que también crece ∝ H).
  * Roca y pavimento: se usan valores de referencia (capacidad última aproximada
    = 3 × valor admisible de código; ver docs/verificacion_fuentes.md).

Los valores "admisibles" de código (IBC/CABO: 95–574 kPa) incluyen un factor de
seguridad de ~3 y están pensados para asentamientos de edificios, no para el
fallo instantáneo del terreno.
"""
from __future__ import annotations

import math

# γ en N/m³, c y cu en Pa, φ en grados.
SOILS = {
    "arcilla_blanda": {"label": "Arcilla blanda / barro", "c": 25e3, "phi": 0.0, "gamma": 17e3,
                       "allowable": 75e3},
    "arcilla_firme": {"label": "Arcilla firme", "c": 75e3, "phi": 0.0, "gamma": 18.5e3,
                      "allowable": 150e3},
    "arcilla_dura": {"label": "Arcilla dura", "c": 150e3, "phi": 0.0, "gamma": 19.5e3,
                     "allowable": 300e3},
    "arena_suelta": {"label": "Arena suelta (seca)", "c": 0.0, "phi": 30.0, "gamma": 16e3,
                     "allowable": 95.8e3},
    "arena_densa": {"label": "Arena densa", "c": 0.0, "phi": 38.0, "gamma": 19e3,
                    "allowable": 300e3},
    "grava_densa": {"label": "Grava densa", "c": 0.0, "phi": 40.0, "gamma": 20e3,
                    "allowable": 600e3},
    "pavimento": {"label": "Pavimento de hormigón (aeropuerto)", "fixed_ult": 3 * 1.75e6,
                  "allowable": 1.75e6},
    "roca_blanda": {"label": "Roca meteorizada / blanda", "fixed_ult": 3 * 766e3,
                    "allowable": 766e3},
    "granito": {"label": "Granito sano", "fixed_ult": 3 * 5.746e6, "allowable": 5.746e6},
}


def factors(phi_deg: float):
    phi = math.radians(phi_deg)
    if phi_deg < 1e-6:
        return 5.14, 1.0, 0.0
    Nq = math.exp(math.pi * math.tan(phi)) * math.tan(math.pi / 4 + phi / 2) ** 2
    Nc = (Nq - 1) / math.tan(phi)
    Ng = 2 * (Nq + 1) * math.tan(phi)
    return Nc, Nq, Ng


def bearing_capacity(soil: dict | str, B: float, L: float, D: float = 0.0) -> float:
    """Capacidad portante última [Pa] de una zapata rectangular B×L (B ≤ L) a profundidad D."""
    if isinstance(soil, str):
        soil = SOILS[soil]
    if "fixed_ult" in soil:
        return soil["fixed_ult"]
    B, L = min(B, L), max(B, L)
    c, phi_deg, g = soil["c"], soil["phi"], soil["gamma"]
    Nc, Nq, Ng = factors(phi_deg)
    phi = math.radians(phi_deg)
    r = B / L
    sc = 1 + r * Nq / Nc
    sq = 1 + r * math.tan(phi)
    sg = max(1 - 0.4 * r, 0.6)
    k = D / B if D <= B else math.atan(D / B)
    dc = 1 + 0.4 * k
    dq = 1 + 2 * math.tan(phi) * (1 - math.sin(phi)) ** 2 * k
    return c * Nc * sc * dc + g * D * Nq * sq * dq + 0.5 * g * B * Ng * sg


def equilibrium_sinkage(soil: dict | str, B: float, L: float, q: float, d_max: float = 50.0) -> float:
    """Profundidad D a la que la capacidad portante iguala la presión aplicada q (hundimiento)."""
    if bearing_capacity(soil, B, L, 0.0) >= q:
        return 0.0
    lo, hi = 0.0, d_max
    if bearing_capacity(soil, B, L, hi) < q:
        return float("inf")
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if bearing_capacity(soil, B, L, mid) < q:
            lo = mid
        else:
            hi = mid
    return hi


if __name__ == "__main__":
    # humano de 1.75 m apoyado en un pie (B = 0.096 m, L = 0.266 m, ~1.2 BW)
    B, L = 0.055 * 1.75, 0.152 * 1.75
    q = 1.2 * 70 * 9.81 / (B * L)
    print(f"humano: q = {q / 1e3:.1f} kPa")
    for k, s in SOILS.items():
        qu = bearing_capacity(s, B, L)
        print(f"  {s['label']:<35} q_ult = {qu / 1e3:8.1f} kPa  hundimiento = {equilibrium_sinkage(s, B, L, q) * 100:.1f} cm")
