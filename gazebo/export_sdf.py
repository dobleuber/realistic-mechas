"""
Exporta el mecha (mismas proporciones y masas que sim/mech_model.py) a SDF para
Gazebo Harmonic, junto con un mundo y la trayectoria articular de la marcha.

    python3 gazebo/export_sdf.py --H 20 --M 104500 --out gazebo/out_H20

Genera:
    <out>/mecha/model.sdf, <out>/mecha/model.config
    <out>/world.sdf
    <out>/trajectory.json   (tiempos y ángulos de la marcha planificada)

Después:  python3.12 gazebo/run_gazebo.py <out>     (servidor sin interfaz + registro)
o con interfaz gráfica:  gz sim <out>/world.sdf  y en otra terminal
                         python3.12 gazebo/run_gazebo.py <out> --no-server
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
from mech_model import (MechParams, M_HAT, M_THIGH, M_SHANK, M_FOOT, COM_THIGH, COM_SHANK,  # noqa: E402
                        COM_HAT, RG_THIGH, RG_SHANK, RG_HAT, JOINTS)
from gait import GaitParams, plan, H0  # noqa: E402


def inertial(m, pos, ixx, iyy, izz):
    return (f"<inertial><pose>{pos[0]:.6g} {pos[1]:.6g} {pos[2]:.6g} 0 0 0</pose><mass>{m:.6g}</mass>"
            f"<inertia><ixx>{ixx:.6g}</ixx><iyy>{iyy:.6g}</iyy><izz>{izz:.6g}</izz>"
            f"<ixy>0</ixy><ixz>0</ixz><iyz>0</iyz></inertia></inertial>")


def box(name, pos, size, rgba, collide=True):
    geo = f"<geometry><box><size>{size[0]:.6g} {size[1]:.6g} {size[2]:.6g}</size></box></geometry>"
    s = (f"<visual name='{name}_v'><pose>{pos[0]:.6g} {pos[1]:.6g} {pos[2]:.6g} 0 0 0</pose>{geo}"
         f"<material><ambient>{rgba}</ambient><diffuse>{rgba}</diffuse></material></visual>")
    if collide:
        s += (f"<collision name='{name}_c'><pose>{pos[0]:.6g} {pos[1]:.6g} {pos[2]:.6g} 0 0 0</pose>{geo}"
              "<surface><friction><ode><mu>1.2</mu><mu2>1.2</mu2></ode></friction></surface></collision>")
    return s


def cyl(name, pos, r, length, rgba):
    return (f"<visual name='{name}_v'><pose>{pos[0]:.6g} {pos[1]:.6g} {pos[2]:.6g} 0 0 0</pose>"
            f"<geometry><cylinder><radius>{r:.6g}</radius><length>{length:.6g}</length></cylinder></geometry>"
            f"<material><ambient>{rgba}</ambient><diffuse>{rgba}</diffuse></material></visual>")


def build_sdf(p: MechParams, torque: dict, kp: float, kd: float) -> str:
    H, M = p.H, p.M
    hip_h = p.thigh + p.shank + p.ankle_h
    m_hat, m_th, m_sh, m_ft = M * M_HAT, M * M_THIGH, M * M_SHANK, M * M_FOOT
    m_small = 0.002 * M
    I_small = m_small * (0.02 * H) ** 2
    # inercia reflejada del actuador ("armature" en MuJoCo: 0.001·M·H²), añadida al eslabón hijo
    # de cada articulación alrededor de su eje; además estabiliza la integración de DART
    arm = 0.001 * M * H * H
    hat_com = COM_HAT * 0.47 * H
    I_hat = m_hat * (RG_HAT * 0.47 * H) ** 2
    I_th = m_th * (RG_THIGH * p.thigh) ** 2
    I_sh = m_sh * (RG_SHANK * p.shank) ** 2
    fl, fw, fh = p.foot_len, p.foot_wid, p.ankle_h
    foot_x = fl * 0.25
    gray, dark, orange = "0.78 0.8 0.83 1", "0.55 0.58 0.62 1", "0.9 0.55 0.1 1"

    links = []
    joints = []
    links.append(f"""<link name='pelvis'><pose>0 0 {hip_h:.6g} 0 0 0</pose>
      {inertial(m_hat, (0, 0, hat_com), I_hat, I_hat, m_hat * (0.1 * H) ** 2)}
      {box('pelvis', (0, 0, 0.03 * H), (0.12 * H, 0.24 * H, 0.10 * H), dark)}
      {box('torso', (0, 0, 0.20 * H), (0.16 * H, 0.26 * H, 0.26 * H), gray)}
      {box('head', (0.01, 0, 0.42 * H), (0.12 * H, 0.12 * H, 0.12 * H), orange, collide=False)}
    </link>""")
    for side, sgn in (("L", 1), ("R", -1)):
        y = sgn * p.hip_w
        links.append(f"<link name='hip_{side}'><pose>0 {y:.6g} {hip_h:.6g} 0 0 0</pose>"
                     f"{inertial(m_small, (0, 0, 0), I_small + arm, I_small, I_small + arm)}</link>")
        links.append(f"""<link name='thigh_{side}'><pose>0 {y:.6g} {hip_h:.6g} 0 0 0</pose>
          {inertial(m_th, (0, 0, -COM_THIGH * p.thigh), I_th, I_th + arm, 0.2 * I_th + arm)}
          {cyl('thigh_' + side, (0, 0, -p.thigh / 2), 0.03 * H, p.thigh, gray)}</link>""")
        links.append(f"""<link name='shank_{side}'><pose>0 {y:.6g} {hip_h - p.thigh:.6g} 0 0 0</pose>
          {inertial(m_sh, (0, 0, -COM_SHANK * p.shank), I_sh, I_sh + arm, 0.2 * I_sh + arm)}
          {cyl('shank_' + side, (0, 0, -p.shank / 2), 0.021 * H, p.shank, dark)}</link>""")
        links.append(f"<link name='ankle_{side}'><pose>0 {y:.6g} {fh:.6g} 0 0 0</pose>"
                     f"{inertial(m_small, (0, 0, 0), I_small, I_small + arm, I_small + arm)}</link>")
        Ift = (m_ft * (fw ** 2 + fh ** 2) / 12 + arm, m_ft * (fl ** 2 + fh ** 2) / 12, m_ft * (fl ** 2 + fw ** 2) / 12 + arm)
        links.append(f"""<link name='foot_{side}'><pose>0 {y:.6g} {fh:.6g} 0 0 0</pose>
          {inertial(m_ft, (foot_x, 0, -fh / 2), *Ift)}
          {box('foot_' + side, (foot_x, 0, -fh / 2), (fl, fw, fh), '0.25 0.25 0.28 1')}</link>""")
        for jn, parent, child, axis, lo, hi in (
                (f"hip_roll_{side}", "pelvis", f"hip_{side}", "1 0 0", -0.6, 0.6),
                (f"hip_pitch_{side}", f"hip_{side}", f"thigh_{side}", "0 1 0", -2.0, 1.0),
                (f"knee_{side}", f"thigh_{side}", f"shank_{side}", "0 1 0", 0.0, 2.4),
                (f"ankle_pitch_{side}", f"shank_{side}", f"ankle_{side}", "0 1 0", -1.0, 1.0),
                (f"ankle_roll_{side}", f"ankle_{side}", f"foot_{side}", "1 0 0", -0.6, 0.6)):
            key = jn.rsplit("_", 1)[0].replace("_pitch", "")
            eff = torque.get(key, 1e15)
            joints.append(f"""<joint name='{jn}' type='revolute'><parent>{parent}</parent><child>{child}</child>
          <axis><xyz>{axis}</xyz><limit><lower>{lo}</lower><upper>{hi}</upper><effort>{eff:.6g}</effort></limit>
          <dynamics><damping>{0.001 * M * 9.81 * H * p.time_scale():.6g}</damping></dynamics></axis></joint>""")

    # JointTrajectoryController: ejecuta dentro de Gazebo la trayectoria completa (sin
    # latencia de comunicación) con un PD de par limitado por el par máximo de cada actuador
    ctrl = []
    for jn in JOINTS:
        key = jn.rsplit("_", 1)[0].replace("_pitch", "")
        eff = torque.get(key, 1e15)
        ctrl.append(f"<joint_name>{jn}</joint_name><initial_position>0</initial_position>"
                    f"<position_p_gain>{kp:.6g}</position_p_gain><position_d_gain>{kd:.6g}</position_d_gain>"
                    f"<position_i_gain>0</position_i_gain><position_cmd_max>{eff:.6g}</position_cmd_max>"
                    f"<position_cmd_min>{-eff:.6g}</position_cmd_min>")
    ctrl = ["<plugin filename='gz-sim-joint-trajectory-controller-system' "
            "name='gz::sim::systems::JointTrajectoryController'>" + "".join(ctrl) + "</plugin>"]
    return f"""<?xml version='1.0'?>
<sdf version='1.9'>
  <model name='mecha'>
    {''.join(links)}
    {''.join(joints)}
    {''.join(ctrl)}
    <plugin filename='gz-sim-pose-publisher-system' name='gz::sim::systems::PosePublisher'>
      <publish_link_pose>true</publish_link_pose>
      <publish_nested_model_pose>false</publish_nested_model_pose>
      <use_pose_vector_msg>true</use_pose_vector_msg>
      <update_frequency>50</update_frequency>
    </plugin>
  </model>
</sdf>
"""


def build_world(p: MechParams, dt: float) -> str:
    H = p.H
    return f"""<?xml version='1.0'?>
<sdf version='1.9'>
  <world name='mecha_world'>
    <physics name='default' type='dart'>
      <max_step_size>{dt:.6g}</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>{1.0 / dt:.6g}</real_time_update_rate>
    </physics>
    <gravity>0 0 -9.81</gravity>
    <plugin filename='gz-sim-physics-system' name='gz::sim::systems::Physics'/>
    <plugin filename='gz-sim-user-commands-system' name='gz::sim::systems::UserCommands'/>
    <plugin filename='gz-sim-scene-broadcaster-system' name='gz::sim::systems::SceneBroadcaster'/>
    <light type='directional' name='sun'><cast_shadows>true</cast_shadows><pose>0 0 {10 * H:.6g} 0 0 0</pose>
      <diffuse>0.9 0.9 0.9 1</diffuse><direction>-0.5 0.2 -0.9</direction></light>
    <model name='ground'><static>true</static><link name='l'>
      <collision name='c'><geometry><plane><normal>0 0 1</normal><size>{200 * H:.6g} {200 * H:.6g}</size></plane></geometry>
        <surface><friction><ode><mu>1.2</mu><mu2>1.2</mu2></ode></friction></surface></collision>
      <visual name='v'><geometry><plane><normal>0 0 1</normal><size>{200 * H:.6g} {200 * H:.6g}</size></plane></geometry>
        <material><ambient>0.4 0.36 0.28 1</ambient><diffuse>0.4 0.36 0.28 1</diffuse></material></visual>
    </link></model>
    <include><uri>model://mecha</uri><name>mecha</name><pose>0 0 0 0 0 0</pose></include>
  </world>
</sdf>
"""


def export(H: float, M: float, out: str, torque: dict | None = None, gp: GaitParams | None = None):
    # sin límite explícito: 0.4·peso·altura por articulación (~4 veces el pico de la marcha)
    lim = 0.4 * M * 9.81 * H
    torque = torque or {k: lim for k in ("hip", "hip_roll", "knee", "ankle", "ankle_roll")}
    p = MechParams(H=H, M=M)
    s = p.time_scale()
    kp = 60.0 * M * 9.81 * H      # N·m/rad (mismas ganancias que en MuJoCo)
    kd = kp * 0.04 * s            # N·m·s/rad (igual que en MuJoCo)
    os.makedirs(os.path.join(out, "mecha"), exist_ok=True)
    open(os.path.join(out, "mecha", "model.sdf"), "w").write(build_sdf(p, torque, kp, kd))
    open(os.path.join(out, "mecha", "model.config"), "w").write(
        f"<?xml version='1.0'?><model><name>mecha</name><version>1.0</version><sdf version='1.9'>model.sdf</sdf>"
        f"<description>Mecha bípedo H={H} m, M={M:.0f} kg</description></model>")
    dt = 0.00005 * s
    open(os.path.join(out, "world.sdf"), "w").write(build_world(p, dt))

    # trayectoria: rampa desde piernas rectas a la postura inicial + marcha planificada
    gp = gp or GaitParams()
    pl = plan(gp)
    t_ramp = 2.0
    pts = []
    for i in range(41):
        a = i / 40
        a = a * a * (3 - 2 * a)
        pts.append({"t": t_ramp * i / 40 * s, "q": (pl.q[0] * a).tolist()})
    step = 4  # submuestreo (20 ms a escala humana)
    k = H / H0
    for i in range(0, len(pl.t), step):
        pts.append({"t": (t_ramp + 1.0 + pl.t[i]) * s, "q": pl.q[i].tolist(),
                    "pelvis": (pl.pelvis[i] * k).tolist(),
                    "feet": [(pl.feet[i, j] * k + np.array([0, 0, p.ankle_h])).tolist() for j in (0, 1)]})
    json.dump({"H": H, "M": M, "time_scale": s, "joints": JOINTS, "points": pts,
               "pelvis_z0": p.thigh + p.shank + p.ankle_h,
               "leg": {"thigh": p.thigh, "shank": p.shank, "hip_w": p.hip_w}, "t_walk": (t_ramp + 1.0) * s,
               "planned_distance": float(pl.feet[-1, 0, 0] * H / H0)},
              open(os.path.join(out, "trajectory.json"), "w"))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--H", type=float, default=1.75)
    ap.add_argument("--M", type=float, default=None, help="masa [kg] (por defecto 70·(H/1.75)^3)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--torque-factor", type=float, default=None,
                    help="par máximo = factor × par pico de la marcha (por defecto 0.4·peso·altura)")
    a = ap.parse_args()
    M = a.M or 70.0 * (a.H / 1.75) ** 3
    out = a.out or os.path.join(os.path.dirname(__file__), f"out_H{a.H:g}")
    torque = None
    if a.torque_factor is not None:
        from experiments import torque_limits
        torque = torque_limits(M, a.H, a.torque_factor)
    print(export(a.H, M, out, torque=torque))
