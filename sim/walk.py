"""
Ejecuta la marcha planificada en MuJoCo para un mecha de altura H y masa M.

Registra: pares articulares, potencia, fuerza de reacción del suelo (GRF) y
centro de presión (CoP) de cada pie, presión media y presión efectiva sobre el
suelo (método del área efectiva de Meyerhof: B' = B - 2e), y si el mecha se cae.

Suelo opcional deformable: si se pasa `soil`, el terreno es un heightfield que
se hunde plásticamente cuando la presión bajo el pie supera la capacidad
portante última (Terzaghi/Vesić, ver scaling/soil.py), con la profundidad de
empotramiento ya alcanzada.
"""
from __future__ import annotations

import math
import os
import sys

import mujoco
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scaling"))
from mech_model import MechParams, build_mjcf, JOINTS  # noqa: E402
from gait import GaitParams, plan, H0  # noqa: E402

_PLAN_CACHE = {}


def get_plan(gp: GaitParams, foot_scale: float):
    key = (tuple(sorted(gp.__dict__.items())), foot_scale)
    if key not in _PLAN_CACHE:
        _PLAN_CACHE[key] = plan(gp, foot_scale)
    return _PLAN_CACHE[key]


def simulate(H: float, M: float, torque_limit: dict | None = None, foot_scale: float = 1.0,
             gp: GaitParams | None = None, soil=None, video: str | None = None,
             video_fps: int = 30, kp_scale: float = 1.0, record_every: int = 5, label: str = ""):
    gp = gp or GaitParams()
    pl = get_plan(gp, foot_scale)
    k = H / H0
    ts = math.sqrt(k)

    mp = MechParams(H=H, M=M, foot_scale=foot_scale, torque_limit=torque_limit or {},
                    kp_scale=kp_scale, hfield=soil is not None)
    model = mujoco.MjModel.from_xml_string(build_mjcf(mp))
    data = mujoco.MjData(model)
    dt = model.opt.timestep

    jadr = np.array([model.joint(j).qposadr[0] for j in JOINTS])
    vadr = np.array([model.joint(j).dofadr[0] for j in JOINTS])
    act_ids = np.array([model.actuator(j).id for j in JOINTS])
    foot_g = {"L": model.geom("foot_L").id, "R": model.geom("foot_R").id}
    floor_g = model.geom("floor").id

    # estado inicial = primera muestra del plan
    data.qpos[:3] = pl.pelvis[0] * k
    data.qpos[3:7] = [1, 0, 0, 0]
    data.qpos[jadr] = pl.q[0]
    data.ctrl[act_ids] = pl.q[0]

    hf = None
    if soil is not None:
        hf = SoilField(model, mp, soil)
        hf.reset()
    mujoco.mj_forward(model, data)

    T = pl.t[-1] * ts
    nsteps = int(T / dt)
    t_plan = pl.t * ts
    W = M * 9.81
    hip_z0 = pl.pelvis[0, 2] * k

    renderer = None
    frames = []
    if video:
        renderer = mujoco.Renderer(model, 540, 960)
        cam = mujoco.MjvCamera()
        cam.type = mujoco.mjtCamera.mjCAMERA_FREE
        cam.distance = 2.6 * H
        cam.elevation = -16
        cam.azimuth = 125
        if hf is not None:
            renderer._mjr_context  # noqa
        frame_dt = 1.0 / video_fps * ts  # vídeo con el tiempo "a escala humana"

    rec = {k_: [] for k_ in ("t", "tau", "qvel", "q", "q_ref", "F_L", "F_R", "cop_L", "cop_R",
                             "pelvis", "q_eff_L", "q_eff_R", "q_avg_L", "q_avg_R", "sink_L", "sink_R")}
    fell = False
    fall_t = None
    c6 = np.zeros(6)
    next_frame = 0.0
    fl, fw = mp.foot_len, mp.foot_wid
    for i in range(nsteps):
        t = i * dt
        qref = np.array([np.interp(t, t_plan, pl.q[:, j]) for j in range(10)])
        data.ctrl[act_ids] = qref
        mujoco.mj_step(model, data)

        # fuerzas de contacto por pie
        F = {"L": np.zeros(3), "R": np.zeros(3)}
        M_ = {"L": np.zeros(3), "R": np.zeros(3)}
        for c in range(data.ncon):
            con = data.contact[c]
            gs = {con.geom1, con.geom2}
            if floor_g not in gs:
                continue
            for side, gid in foot_g.items():
                if gid in gs:
                    mujoco.mj_contactForce(model, data, c, c6)
                    fr = con.frame.reshape(3, 3)
                    f_world = fr.T @ c6[:3]
                    if con.geom1 == gid:
                        f_world = -f_world   # fuerza del suelo sobre el pie
                    F[side] += f_world
                    M_[side] += np.cross(con.pos, f_world)
        q_eff, q_avg, cop = {}, {}, {}
        for side in ("L", "R"):
            fz = F[side][2]
            if fz > 0.2 * W:
                cx = -M_[side][1] / fz   # CoP en el plano: x = -My/Fz, y = Mx/Fz
                cy = M_[side][0] / fz
                cop[side] = np.array([cx, cy])
                # excentricidad respecto al centro de la suela
                sole = data.site(f"sole_{side}").xpos
                ex, ey = abs(cx - sole[0]), abs(cy - sole[1])
                Le, Be = max(fl - 2 * ex, 0.05 * fl), max(fw - 2 * ey, 0.05 * fw)
                q_eff[side] = fz / (Le * Be)
                q_avg[side] = fz / (fl * fw)
            else:
                cop[side] = np.array([np.nan, np.nan])
                q_eff[side] = 0.0
                q_avg[side] = 0.0
        if hf is not None:
            hf.update(data, F, q_avg, dt)

        if i % record_every == 0:
            rec["t"].append(t)
            rec["tau"].append(data.actuator_force[act_ids].copy())
            rec["qvel"].append(data.qvel[vadr].copy())
            rec["q"].append(data.qpos[jadr].copy())
            rec["q_ref"].append(qref)
            rec["F_L"].append(F["L"].copy())
            rec["F_R"].append(F["R"].copy())
            rec["cop_L"].append(cop["L"])
            rec["cop_R"].append(cop["R"])
            rec["pelvis"].append(data.qpos[:7].copy())
            rec["q_eff_L"].append(q_eff["L"])
            rec["q_eff_R"].append(q_eff["R"])
            rec["q_avg_L"].append(q_avg["L"])
            rec["q_avg_R"].append(q_avg["R"])
            rec["sink_L"].append(hf.sink["L"] if hf else 0.0)
            rec["sink_R"].append(hf.sink["R"] if hf else 0.0)

        if renderer is not None and t >= next_frame:
            cam.lookat[:] = [data.qpos[0], 0, 0.45 * H]
            if hf is not None and hf.dirty:
                mujoco.mjr_uploadHField(model, renderer._mjr_context, 0)
                hf.dirty = False
            renderer.update_scene(data, cam)
            frames.append(overlay(renderer.render().copy(), label, t / ts, data.qpos[0],
                                  hf.sink if hf is not None else None))
            next_frame += frame_dt

        # detección de caída
        quat = data.qpos[3:7]
        tilt = 2 * math.acos(min(1.0, abs(quat[0])))
        if data.qpos[2] < 0.6 * hip_z0 or tilt > 0.6:
            if not fell:
                fell, fall_t = True, t
            if renderer is None or t > (fall_t + 2.0 * ts):
                break

    if renderer is not None and frames:
        import imageio.v2 as imageio
        imageio.mimsave(video, frames, fps=video_fps, codec="libx264", quality=7)

    out = {k_: np.array(v) for k_, v in rec.items()}
    out.update(summarize(out, H, M, mp, torque_limit or {}, fell, fall_t, pl, ts))
    return out


def overlay(img, label, t_human, x, sink):
    """Rótulo con los datos del caso sobre el fotograma."""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.fromarray(img)
    d = ImageDraw.Draw(im)
    font = None
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                 "DejaVuSans.ttf", "Arial.ttf"):
        try:
            font = ImageFont.truetype(path, 20)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default()
    lines = [label] if label else []
    lines.append(f"avance: {x:5.1f} m")
    if sink is not None:
        lines.append(f"hundimiento máx.: {max(sink.values()):4.2f} m")
    lines.append("referencias: persona 1.75 m (roja), autobús 12 m (amarillo)")
    y = 10
    for ln in lines:
        d.text((12, y), ln, fill=(20, 20, 20), font=font)
        y += 28
    return np.asarray(im)


def summarize(r, H, M, mp, tl, fell, fall_t, pl, ts):
    W = M * 9.81
    tau = r["tau"]
    qv = r["qvel"]
    names = JOINTS
    peak_tau = {n: float(np.abs(tau[:, i]).max()) for i, n in enumerate(names)}
    power = np.abs(tau * qv)
    peak_pow = float(power.sum(axis=1).max()) if len(power) else 0.0
    pos_work_rate = float(np.clip(tau * qv, 0, None).sum(axis=1).mean()) if len(power) else 0.0
    grf = np.maximum(r["F_L"][:, 2], r["F_R"][:, 2]) if len(r["F_L"]) else np.zeros(1)
    qeff = np.maximum(r["q_eff_L"], r["q_eff_R"]) if len(r["q_eff_L"]) else np.zeros(1)
    qavg = np.maximum(r["q_avg_L"], r["q_avg_R"]) if len(r["q_avg_L"]) else np.zeros(1)
    track = np.abs(r["q"] - r["q_ref"]).max() if len(r["q"]) else 0.0
    sat = {}
    for i, n in enumerate(names):
        lim = tl.get(n.rsplit("_", 1)[0].replace("_pitch", ""), None)
        if lim:
            sat[n] = float((np.abs(tau[:, i]) > 0.98 * lim).mean())
    dist = float(r["pelvis"][-1, 0]) if len(r["pelvis"]) else 0.0
    return {
        "H": H, "M": M, "fell": fell, "fall_t": fall_t,
        "distance": dist,
        "duration": float(r["t"][-1]) if len(r["t"]) else 0.0,
        "speed_plan": pl.speed * math.sqrt(H / H0),
        "peak_tau": peak_tau,
        "peak_tau_norm": {n: v / (W * H) for n, v in peak_tau.items()},
        "peak_power_W": peak_pow,
        "mean_pos_power_W": pos_work_rate,
        "peak_grf_BW": float(grf.max() / W),
        "peak_q_avg_kPa": float(qavg.max() / 1e3),
        "peak_q_eff_kPa": float(qeff.max() / 1e3),
        "p95_q_eff_kPa": float(np.percentile(qeff[qeff > 0], 95) / 1e3) if (qeff > 0).any() else 0.0,
        "max_track_err_rad": float(track),
        "saturation": sat,
        "max_sink_m": float(max(r["sink_L"].max(), r["sink_R"].max())) if len(r["sink_L"]) else 0.0,
    }


# --------------------------------------------------------------------------
class SoilField:
    """Terreno que se hunde plásticamente bajo el pie (modelo cuasi-estático de punzonamiento).

    Para la presión media bajo cada pie (filtrada para no reaccionar a picos de
    impacto de un paso de integración) se calcula la profundidad de equilibrio
    D* a la que la capacidad portante última q_ult(B, L, D) iguala a la presión
    (Terzaghi/Vesić con factores de profundidad: el empotramiento aumenta la
    capacidad). El terreno bajo la huella baja hacia D* con una velocidad
    máxima limitada. Es una aproximación ingenieril, no un modelo continuo de suelo.
    """

    def __init__(self, model, mp: MechParams, soil):
        from soil import equilibrium_sinkage
        self.m = model
        self.mp = mp
        self.soil = soil
        self.nr = model.hfield_nrow[0]
        self.nc = model.hfield_ncol[0]
        sx, sy, sz, base = model.hfield_size[0]
        self.size = (sx, sy, sz, base)
        gid = model.geom("floor").id
        self.origin = model.geom_pos[gid].copy()
        self.sink = {"L": 0.0, "R": 0.0}
        self.qf = {"L": 0.0, "R": 0.0}
        self.dirty = True
        self.e0 = -self.origin[2] / sz
        self.tau = 0.05 * mp.time_scale()
        self.vmax = 0.2 * math.sqrt(9.81 * mp.H)
        # tabla presión -> profundidad de equilibrio para esta huella
        B, L = mp.foot_wid, mp.foot_len
        self.q_tab = np.geomspace(1e3, 1e8, 400)
        self.d_tab = np.array([min(equilibrium_sinkage(soil, B, L, q, d_max=0.45 * mp.H), 0.45 * mp.H)
                               for q in self.q_tab])

    def reset(self):
        adr = self.m.hfield_adr[0]
        self.m.hfield_data[adr:adr + self.nr * self.nc] = self.e0
        self.dirty = True

    def _cells(self, cx, cy, hl, hw):
        sx, sy = self.size[0], self.size[1]
        ox, oy = self.origin[0], self.origin[1]
        c0 = int(np.floor((cx - hl - ox + sx) / (2 * sx) * (self.nc - 1)))
        c1 = int(np.ceil((cx + hl - ox + sx) / (2 * sx) * (self.nc - 1)))
        r0 = int(np.floor((cy - hw - oy + sy) / (2 * sy) * (self.nr - 1)))
        r1 = int(np.ceil((cy + hw - oy + sy) / (2 * sy) * (self.nr - 1)))
        return max(r0, 0), min(r1, self.nr - 1), max(c0, 0), min(c1, self.nc - 1)

    def update(self, data, F, q_avg, dt):
        adr = self.m.hfield_adr[0]
        grid = self.m.hfield_data[adr:adr + self.nr * self.nc].reshape(self.nr, self.nc)
        sz = self.size[2]
        a = min(1.0, dt / self.tau)
        for side in ("L", "R"):
            q = q_avg[side]
            self.qf[side] += (q - self.qf[side]) * a
            if q <= 0:
                continue
            sole = data.site(f"sole_{side}").xpos
            r0, r1, c0, c1 = self._cells(sole[0], sole[1], self.mp.foot_len / 2, self.mp.foot_wid / 2)
            cells = grid[r0:r1 + 1, c0:c1 + 1]
            depth = max(0.0, -(self.origin[2] + cells.max() * sz))
            target = float(np.interp(self.qf[side], self.q_tab, self.d_tab))
            if target > depth + 1e-6 * self.mp.H:
                new_depth = min(target, depth + self.vmax * dt)
                new = (-new_depth - self.origin[2]) / sz
                grid[r0:r1 + 1, c0:c1 + 1] = np.minimum(cells, new)
                self.dirty = True
                depth = new_depth
            self.sink[side] = max(self.sink[side], depth)
        self.m.hfield_data[adr:adr + self.nr * self.nc] = grid.ravel()


if __name__ == "__main__":
    r = simulate(1.75, 70.0)
    import json
    print(json.dumps({k: v for k, v in r.items() if not isinstance(v, np.ndarray)}, indent=1, default=float))
