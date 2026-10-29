"""
Homogenización elástica por elementos finitos (vóxeles) de celdas giroides.

Qué calcula, para una celda unitaria periódica de giroide (tipo "sheet" o
"skeletal") a una densidad relativa dada:
  - la matriz de rigidez efectiva C^H (6x6) mediante condiciones de contorno
    periódicas (método estándar de homogenización asintótica),
  - el módulo de Young efectivo en [100] y [111] y la razón de Zener
    (anisotropía),
  - la concentración de tensiones: tensión de von Mises local máxima frente a
    la tensión macroscópica aplicada en compresión uniaxial. De ahí sale una
    estimación de la tensión a la que *empieza* a fluir el material (cota
    inferior; la meseta plástica real es mayor porque la carga se redistribuye).

Material base lineal elástico e isótropo (E=1, nu=0.3): los resultados son
relativos (E*/Es), así que valen para cualquier metal o polímero.

Uso:
    python gyroid_homogenization.py --kind sheet --rho 0.2 --n 48
"""
from __future__ import annotations

import argparse
import json
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

try:
    import pyamg
except ImportError:  # el solver funciona sin pyamg, solo más lento
    pyamg = None


# --------------------------------------------------------------------------
# Geometría
# --------------------------------------------------------------------------
def gyroid_field(n: int) -> np.ndarray:
    """Valor de la función giroide en el centro de cada vóxel (celda de lado 1)."""
    c = (np.arange(n) + 0.5) / n * 2 * np.pi
    X, Y, Z = np.meshgrid(c, c, c, indexing="ij")
    return np.sin(X) * np.cos(Y) + np.sin(Y) * np.cos(Z) + np.sin(Z) * np.cos(X)


def gyroid_voxels(n: int, kind: str, rho: float) -> tuple[np.ndarray, float]:
    """Máscara booleana de vóxeles sólidos con densidad relativa ~rho.

    sheet:    |f| <= t   (lámina de espesor uniforme sobre la superficie mínima)
    skeletal: f >= t     (una de las dos redes de "puntales" curvos)
    """
    f = gyroid_field(n)
    if kind == "sheet":
        lo, hi = 0.0, 1.5
        sel = lambda t: np.abs(f) <= t
    elif kind == "skeletal":
        lo, hi = -1.5, 1.5
        sel = lambda t: f >= t
    else:
        raise ValueError(kind)
    for _ in range(60):
        t = 0.5 * (lo + hi)
        frac = sel(t).mean()
        if kind == "sheet":
            lo, hi = (t, hi) if frac < rho else (lo, t)
        else:
            lo, hi = (lo, t) if frac < rho else (t, hi)
    mask = sel(t)
    return mask, float(mask.mean())


# --------------------------------------------------------------------------
# Elemento hexaédrico de 8 nodos (cubo unitario)
# --------------------------------------------------------------------------
LOCAL = np.array([[a, b, c] for c in (0, 1) for b in (0, 1) for a in (0, 1)], float)


def iso_C(E: float = 1.0, nu: float = 0.3) -> np.ndarray:
    lam = E * nu / ((1 + nu) * (1 - 2 * nu))
    mu = E / (2 * (1 + nu))
    C = np.zeros((6, 6))
    C[:3, :3] = lam
    C[np.arange(3), np.arange(3)] += 2 * mu
    C[np.arange(3, 6), np.arange(3, 6)] = mu
    return C


def B_matrix(xi: np.ndarray) -> np.ndarray:
    """Matriz deformación-desplazamiento (Voigt: xx,yy,zz,yz,xz,xy; corte ingenieril)."""
    s = 2 * LOCAL - 1  # signos de cada nodo
    # funciones de forma trilineales en [0,1]^3 -> derivadas
    dN = np.zeros((8, 3))
    for i in range(8):
        f = [(1 + s[i, d] * (2 * xi[d] - 1)) / 2 for d in range(3)]
        for d in range(3):
            g = list(f)
            g[d] = s[i, d]  # d/dx de (1 + s(2x-1))/2 = s
            dN[i, d] = g[0] * g[1] * g[2]
    B = np.zeros((6, 24))
    for i in range(8):
        dx, dy, dz = dN[i]
        B[0, 3 * i] = dx
        B[1, 3 * i + 1] = dy
        B[2, 3 * i + 2] = dz
        B[3, 3 * i + 1] = dz
        B[3, 3 * i + 2] = dy
        B[4, 3 * i] = dz
        B[4, 3 * i + 2] = dx
        B[5, 3 * i] = dy
        B[5, 3 * i + 1] = dx
    return B


def element_stiffness(C: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    g = 0.5 + np.array([-1, 1]) / (2 * np.sqrt(3))
    Ke = np.zeros((24, 24))
    for x in g:
        for y in g:
            for z in g:
                B = B_matrix(np.array([x, y, z]))
                Ke += B.T @ C @ B / 8.0
    B0 = B_matrix(np.array([0.5, 0.5, 0.5]))
    return Ke, B0


# --------------------------------------------------------------------------
# Homogenización periódica
# --------------------------------------------------------------------------
def homogenize(mask: np.ndarray, nu: float = 0.3, tol: float = 1e-8, verbose=False):
    n = mask.shape[0]
    Cs = iso_C(1.0, nu)
    Ke, B0 = element_stiffness(Cs)

    ei, ej, ek = np.nonzero(mask)
    nel = ei.size
    # nodos periódicos de cada elemento
    a, b, c = LOCAL[:, 0].astype(int), LOCAL[:, 1].astype(int), LOCAL[:, 2].astype(int)
    nodes = (((ei[:, None] + a) % n) + n * ((ej[:, None] + b) % n)
             + n * n * ((ek[:, None] + c) % n))  # (nel, 8)
    edof = (3 * nodes[:, :, None] + np.arange(3)).reshape(nel, 24)

    # renumerar solo los dof usados
    used, inv = np.unique(edof, return_inverse=True)
    edof_r = inv.reshape(nel, 24)
    ndof = used.size

    rows = np.repeat(edof_r, 24, axis=1).ravel()
    cols = np.tile(edof_r, (1, 24)).ravel()
    vals = np.tile(Ke.ravel(), nel)
    K = sp.coo_matrix((vals, (rows, cols)), shape=(ndof, ndof)).tocsr()

    # desplazamientos afines para las 6 deformaciones unitarias de prueba
    U0 = np.zeros((6, 24))
    for k in range(6):
        eps = np.zeros((3, 3))
        if k < 3:
            eps[k, k] = 1.0
        else:
            i, j = [(1, 2), (0, 2), (0, 1)][k - 3]
            eps[i, j] = eps[j, i] = 0.5  # corte ingenieril unitario
        U0[k] = (LOCAL @ eps.T).ravel()

    F = np.zeros((ndof, 6))
    for k in range(6):
        fe = np.tile(Ke @ U0[k], (nel, 1))
        np.add.at(F[:, k], edof_r.ravel(), fe.ravel())

    # fijar un nodo (3 traslaciones de cuerpo rígido)
    fixed = edof_r[0, :3]
    free = np.setdiff1d(np.arange(ndof), fixed)
    Kf = K[free][:, free]

    if pyamg is not None:
        Bns = np.zeros((free.size, 3))
        Bns[np.arange(free.size), used[free] % 3] = 1.0
        ml = pyamg.smoothed_aggregation_solver(Kf, B=Bns, max_coarse=2000)
        M = ml.aspreconditioner()
    else:
        d = Kf.diagonal()
        M = sp.diags(1.0 / d)

    chi = np.zeros((ndof, 6))
    iters = []
    for k in range(6):
        it = [0]

        def cb(_x):
            it[0] += 1

        x, info = spla.cg(Kf, F[free, k], rtol=tol, maxiter=5000, M=M, callback=cb)
        if info != 0:
            raise RuntimeError(f"CG no convergió (caso {k}, info={info})")
        chi[free, k] = x
        iters.append(it[0])
    if verbose:
        print("iteraciones CG:", iters)

    # matriz homogenizada
    Ue = np.empty((6, nel, 24))
    for k in range(6):
        Ue[k] = U0[k][None, :] - chi[edof_r, k]
    CH = np.zeros((6, 6))
    KUe = np.einsum("knj,ij->kni", Ue, Ke)
    for i in range(6):
        for j in range(6):
            CH[i, j] = np.einsum("ni,ni->", KUe[i], Ue[j]) / n**3
    CH = 0.5 * (CH + CH.T)

    return {"CH": CH, "Ue": Ue, "B0": B0, "Cs": Cs, "nel": nel, "ndof": ndof,
            "cg_iters": iters}


def analyse(mask: np.ndarray, res: dict) -> dict:
    CH, Ue, B0, Cs = res["CH"], res["Ue"], res["B0"], res["Cs"]
    S = np.linalg.inv(CH)
    E100 = 1.0 / S[0, 0]
    # módulo en dirección [111]
    d = np.ones(3) / np.sqrt(3)
    v = np.array([d[0] ** 2, d[1] ** 2, d[2] ** 2, 2 * d[1] * d[2], 2 * d[0] * d[2], 2 * d[0] * d[1]])
    # tensión uniaxial unitaria en d: sigma = d d^T -> Voigt [d0^2, d1^2, d2^2, d1d2, d0d2, d0d1]
    sig = np.array([d[0] ** 2, d[1] ** 2, d[2] ** 2, d[1] * d[2], d[0] * d[2], d[0] * d[1]])
    E111 = 1.0 / (sig @ S @ sig)
    zener = 2 * CH[3, 3] / (CH[0, 0] - CH[0, 1])

    out = {"E100": E100, "E111": E111, "zener": zener,
           "nu12": -S[0, 1] / S[0, 0]}
    # concentración de tensiones bajo compresión uniaxial macroscópica en x y en [111]
    for name, s_macro in (("x", np.array([1.0, 0, 0, 0, 0, 0])), ("111", sig)):
        eps_macro = S @ s_macro  # deformación macroscópica (corte ingenieril)
        u = np.einsum("k,knj->nj", eps_macro, Ue)
        strain = u @ B0.T
        stress = strain @ Cs.T
        sx, sy, sz, tyz, txz, txy = stress.T
        vm = np.sqrt(0.5 * ((sx - sy) ** 2 + (sy - sz) ** 2 + (sz - sx) ** 2)
                     + 3 * (tyz ** 2 + txz ** 2 + txy ** 2))
        out[f"vm_max_{name}"] = float(vm.max())
        out[f"vm_p99_{name}"] = float(np.percentile(vm, 99))
        out[f"vm_p999_{name}"] = float(np.percentile(vm, 99.9))
        out[f"vm_mean_{name}"] = float(vm.mean())
    return out


def run(kind: str, rho: float, n: int, verbose=False) -> dict:
    t0 = time.time()
    mask, rho_real = gyroid_voxels(n, kind, rho)
    res = homogenize(mask, verbose=verbose)
    out = analyse(mask, res)
    out.update({"kind": kind, "rho_target": rho, "rho": rho_real, "n": n,
                "nel": res["nel"], "ndof": res["ndof"], "seconds": time.time() - t0,
                "CH": res["CH"].round(6).tolist()})
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", default="sheet", choices=["sheet", "skeletal", "solid"])
    ap.add_argument("--rho", type=float, default=0.2)
    ap.add_argument("--n", type=int, default=40)
    a = ap.parse_args()
    if a.kind == "solid":
        mask = np.ones((a.n,) * 3, bool)
        res = homogenize(mask, verbose=True)
        print(json.dumps(analyse(mask, res), indent=1))
    else:
        print(json.dumps(run(a.kind, a.rho, a.n, verbose=True), indent=1))
