"""
Generador paramétrico del modelo MuJoCo (MJCF) de un mecha cuadrúpedo.

Para que la comparación con el bípedo sea justa, cada pata es exactamente una
pierna del bípedo de altura equivalente H (mismos segmentos, misma articulación
de 5 grados de libertad, mismos actuadores y el mismo pie), y el reparto de masa
es el mismo: las cuatro patas suman la misma fracción de la masa total que las
dos piernas del bípedo (32 %), y el cuerpo el 68 % restante.

    longitud de la pata  l = 0.53 H   (cadera -> suelo con la pierna estirada)
    distancia cadera-hombro D = DX · H (por defecto 0.53 H = l)
    semiancho de vía      w = WY · H  (por defecto 0.13 H)

Todas las magnitudes escalan con H, así que con similitud de Froude los pares
normalizados por peso × H no dependen del tamaño.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from mech_model import (ANKLE_HEIGHT, COM_SHANK, COM_THIGH, FOOT_LENGTH, FOOT_WIDTH, HIP_HEIGHT,
                        KNEE_HEIGHT, M_FOOT, M_SHANK, M_THIGH, RG_SHANK, RG_THIGH, _box_inertia)

LEGS = ("LF", "RF", "LH", "RH")          # izquierda/derecha, delantera/trasera (hind)
DOFS = ("hip_roll", "hip_pitch", "knee", "ankle_pitch", "ankle_roll")
JOINTS = [f"{j}_{leg}" for leg in LEGS for j in DOFS]

LEG_MASS_SHARE = 0.5     # cada pata pesa la mitad que una pierna del bípedo -> 4 patas = 2 piernas
M_BODY = 1.0 - 2 * (M_THIGH + M_SHANK + M_FOOT)   # 0.678, igual que el HAT del bípedo


@dataclass
class QuadParams:
    H: float = 1.75                 # altura del bípedo equivalente [m] (pata = 0.53 H)
    M: float = 70.0                 # masa total [kg]
    DX: float = 0.53                # distancia cadera-hombro [× H]
    WY: float = 0.13                # semiancho de vía [× H]
    body_depth: float = 0.16        # canto del cuerpo [× H]
    foot_scale: float = 1.0
    torque_limit: dict = field(default_factory=dict)
    kp_scale: float = 1.0
    refs: bool = True
    armature_share: float = 0.5     # inercia reflejada de cada actuador [× 0.001 M H²]; la mitad que en el
                                    # bípedo porque cada pata lleva la mitad de carga y sus actuadores son menores

    @property
    def thigh(self):
        return (HIP_HEIGHT - KNEE_HEIGHT) * self.H

    @property
    def shank(self):
        return (KNEE_HEIGHT - ANKLE_HEIGHT) * self.H

    @property
    def ankle_h(self):
        return ANKLE_HEIGHT * self.H

    @property
    def leg_len(self):
        return HIP_HEIGHT * self.H

    @property
    def foot_len(self):
        return FOOT_LENGTH * self.H * self.foot_scale

    @property
    def foot_wid(self):
        return FOOT_WIDTH * self.H * self.foot_scale

    def hip_pos(self, leg: str):
        x = 0.5 * self.DX * self.H * (1 if leg[1] == "F" else -1)
        y = self.WY * self.H * (1 if leg[0] == "L" else -1)
        return x, y

    def time_scale(self) -> float:
        return math.sqrt(self.H / 1.75)


def build_quad_mjcf(p: QuadParams, dt: float | None = None) -> str:
    H, M = p.H, p.M
    s = p.time_scale()
    if dt is None:
        dt = 0.001 * s
    g = 9.81
    W = M * g
    sh = LEG_MASS_SHARE
    m_body = M * M_BODY
    m_th, m_sh, m_ft = M * M_THIGH * sh, M * M_SHANK * sh, M * M_FOOT * sh
    I_th = m_th * (RG_THIGH * p.thigh) ** 2
    I_sh = m_sh * (RG_SHANK * p.shank) ** 2
    fl, fw, fh = p.foot_len, p.foot_wid, p.ankle_h
    I_ft = _box_inertia(m_ft, fl, fw, fh)
    Lb = p.DX * H * 1.25
    Bb = 2 * p.WY * H * 1.1
    Db = p.body_depth * H
    I_b = _box_inertia(m_body, Lb, Bb, Db)

    kp = 60.0 * W * H * p.kp_scale
    kv = kp * 0.04 * s
    tl = {"hip": 1e12, "hip_roll": 1e12, "knee": 1e12, "ankle": 1e12, "ankle_roll": 1e12}
    tl.update(p.torque_limit)
    r_th = 0.05 * H * 0.6
    r_sh = 0.035 * H * 0.6
    foot_x = fl * (0.5 - 0.25)

    def leg(name: str) -> str:
        x, y = p.hip_pos(name)
        return f"""
      <body name="thigh_{name}" pos="{x:.6g} {y:.6g} 0">
        <joint name="hip_roll_{name}" axis="1 0 0" range="-0.6 0.6"/>
        <joint name="hip_pitch_{name}" axis="0 1 0" range="-2.0 1.0"/>
        <inertial pos="0 0 {-COM_THIGH * p.thigh:.6g}" mass="{m_th:.6g}" diaginertia="{I_th:.6g} {I_th:.6g} {0.2 * I_th:.6g}"/>
        <geom name="thigh_{name}" type="capsule" fromto="0 0 0 0 0 {-p.thigh:.6g}" size="{r_th:.6g}" material="armor" contype="0" conaffinity="1" mass="0"/>
        <body name="shank_{name}" pos="0 0 {-p.thigh:.6g}">
          <joint name="knee_{name}" axis="0 1 0" range="0 2.4"/>
          <inertial pos="0 0 {-COM_SHANK * p.shank:.6g}" mass="{m_sh:.6g}" diaginertia="{I_sh:.6g} {I_sh:.6g} {0.2 * I_sh:.6g}"/>
          <geom name="shank_{name}" type="capsule" fromto="0 0 0 0 0 {-p.shank:.6g}" size="{r_sh:.6g}" material="armor2" contype="0" conaffinity="1" mass="0"/>
          <body name="foot_{name}" pos="0 0 {-p.shank:.6g}">
            <joint name="ankle_pitch_{name}" axis="0 1 0" range="-1.0 1.0"/>
            <joint name="ankle_roll_{name}" axis="1 0 0" range="-0.6 0.6"/>
            <inertial pos="{foot_x:.6g} 0 {-fh / 2:.6g}" mass="{m_ft:.6g}" diaginertia="{I_ft[0]:.6g} {I_ft[1]:.6g} {I_ft[2]:.6g}"/>
            <geom name="foot_{name}" type="box" pos="{foot_x:.6g} 0 {-fh / 2:.6g}" size="{fl / 2:.6g} {fw / 2:.6g} {fh / 2:.6g}" material="sole" contype="0" conaffinity="1" mass="0" condim="3" friction="0.9"/>
            <site name="sole_{name}" pos="{foot_x:.6g} 0 {-fh:.6g}" size="{0.01 * H:.6g}"/>
          </body>
        </body>
      </body>"""

    def act(name, joint, lim):
        return (f'<position name="{name}" joint="{joint}" kp="{kp:.6g}" kv="{kv:.6g}" '
                f'forcelimited="true" forcerange="{-lim:.6g} {lim:.6g}"/>')

    acts = []
    for lg in LEGS:
        acts += [act(f"hip_roll_{lg}", f"hip_roll_{lg}", tl["hip_roll"]),
                 act(f"hip_pitch_{lg}", f"hip_pitch_{lg}", tl["hip"]),
                 act(f"knee_{lg}", f"knee_{lg}", tl["knee"]),
                 act(f"ankle_pitch_{lg}", f"ankle_pitch_{lg}", tl["ankle"]),
                 act(f"ankle_roll_{lg}", f"ankle_roll_{lg}", tl["ankle_roll"])]

    refs_xml = ""
    if p.refs and H > 3.0:
        y_ref = -0.55 * H
        refs_xml = (f'<geom name="persona" type="capsule" fromto="{0.6 * H:.6g} {y_ref:.6g} 0.25 {0.6 * H:.6g} {y_ref:.6g} 1.5" '
                    f'size="0.25" material="person" contype="0" conaffinity="0"/>'
                    f'<geom name="persona_cabeza" type="sphere" pos="{0.6 * H:.6g} {y_ref:.6g} 1.62" size="0.13" material="person" contype="0" conaffinity="0"/>'
                    f'<geom name="autobus" type="box" pos="{0.6 * H + 9:.6g} {y_ref - 2:.6g} 1.6" size="6 1.25 1.6" material="bus" contype="0" conaffinity="0"/>')

    solref = f"{0.01 * s:.6g} 1"
    head_x = 0.5 * Lb + 0.06 * H
    return f"""<mujoco model="cuadrupedo_H{H:g}">
  <compiler angle="radian" autolimits="true"/>
  <option timestep="{dt:.6g}" gravity="0 0 {-g}" integrator="implicitfast" cone="elliptic" tolerance="1e-12" iterations="200"/>
  <size memory="200M"/>
  <visual>
    <global offwidth="1280" offheight="720"/>
    <map znear="0.01" zfar="{200 * H:.6g}"/>
    <headlight ambient="0.35 0.35 0.35" diffuse="0.6 0.6 0.6"/>
  </visual>
  <asset>
    <texture name="sky" type="skybox" builtin="gradient" rgb1="0.62 0.74 0.88" rgb2="0.95 0.95 0.97" width="512" height="512"/>
    <texture name="grid" type="2d" builtin="checker" rgb1="0.42 0.38 0.30" rgb2="0.36 0.32 0.25" width="512" height="512"/>
    <material name="ground" texture="grid" texrepeat="20 20" texuniform="false" reflectance="0"/>
    <material name="armor" rgba="0.78 0.80 0.83 1"/>
    <material name="armor2" rgba="0.55 0.58 0.62 1"/>
    <material name="sole" rgba="0.25 0.25 0.28 1"/>
    <material name="accent" rgba="0.90 0.55 0.10 1"/>
    <material name="person" rgba="0.85 0.15 0.15 1"/>
    <material name="bus" rgba="0.95 0.80 0.10 1"/>
  </asset>
  <default>
    <geom solref="{solref}" solimp="0.95 0.99 {0.001 * H / 1.75:.6g}"/>
    <joint damping="{0.002 * W * H * s:.6g}" armature="{0.001 * p.armature_share * M * H * H:.6g}" solreflimit="{0.02 * s:.6g} 1"/>
  </default>
  <worldbody>
    <light pos="0 0 {6 * H:.6g}" dir="0 0 -1" diffuse="0.5 0.5 0.5"/>
    <geom name="floor" type="plane" size="{20 * H:.6g} {20 * H:.6g} {0.1 * H:.6g}" material="ground" contype="1" conaffinity="1"/>
    {refs_xml}
    <body name="body" pos="0 0 {HIP_HEIGHT * H:.6g}">
      <freejoint name="root"/>
      <inertial pos="0 0 {0.5 * Db:.6g}" mass="{m_body:.6g}" diaginertia="{I_b[0]:.6g} {I_b[1]:.6g} {I_b[2]:.6g}"/>
      <geom name="body" type="box" pos="0 0 {0.5 * Db:.6g}" size="{Lb / 2:.6g} {Bb / 2:.6g} {Db / 2:.6g}" material="armor" contype="0" conaffinity="1" mass="0"/>
      <geom name="cabin" type="box" pos="{head_x - 0.04 * H:.6g} 0 {Db + 0.04 * H:.6g}" size="{0.07 * H:.6g} {0.06 * H:.6g} {0.04 * H:.6g}" material="accent" contype="0" conaffinity="1" mass="0"/>
      <site name="imu" pos="0 0 {0.5 * Db:.6g}"/>
      {"".join(leg(lg) for lg in LEGS)}
    </body>
  </worldbody>
  <actuator>
    {chr(10).join("    " + a for a in acts)}
  </actuator>
</mujoco>
"""
