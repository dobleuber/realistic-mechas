"""
Generador paramétrico del modelo MuJoCo (MJCF) de un mecha bípedo humanoide.

Proporciones: tablas antropométricas de Winter (Biomechanics and Motor Control
of Human Movement, 4ª ed., tabla 4.1), expresadas como fracción de la altura H
y de la masa total M. Así el mismo modelo sirve para un humano de 1.75 m o para
un mecha de 50 m: solo cambian H, M, la huella del pie y los límites de los
actuadores.

Cuerpo:  pelvis + tronco/cabeza/brazos (HAT) como un solo sólido rígido con
         articulación libre, y dos piernas de 5 grados de libertad
         (cadera roll/pitch, rodilla, tobillo pitch/roll).
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math

# ---- Antropometría (Winter, tabla 4.1) -------------------------------------
# longitudes como fracción de H
HIP_HEIGHT = 0.530      # trocánter mayor
KNEE_HEIGHT = 0.285
ANKLE_HEIGHT = 0.039
FOOT_LENGTH = 0.152
FOOT_WIDTH = 0.055
HIP_HALF_WIDTH = 0.191 / 2 * 0.55   # separación de centros articulares de cadera (~0.105 H)
# masas como fracción de M
M_HAT = 0.678
M_THIGH = 0.100
M_SHANK = 0.0465
M_FOOT = 0.0145
# centro de masa del segmento desde el extremo proximal (fracción de longitud)
COM_THIGH = 0.433
COM_SHANK = 0.433
COM_HAT = 0.626          # desde el trocánter hacia arriba, sobre la longitud HAT
HAT_LENGTH = 0.818 - 0.530  # trocánter -> hombro (~0.288 H); el HAT real llega a la cabeza
# radios de giro respecto al CdM (fracción de longitud del segmento)
RG_THIGH = 0.323
RG_SHANK = 0.302
RG_FOOT = 0.475
RG_HAT = 0.496


@dataclass
class MechParams:
    H: float = 1.75                 # altura [m]
    M: float = 70.0                 # masa total [kg]
    foot_scale: float = 1.0         # multiplicador lineal de la huella del pie
    torque_limit: dict = field(default_factory=dict)   # Nm por articulación ("hip", "knee", "ankle", "hip_roll", "ankle_roll")
    kp_scale: float = 1.0
    hfield: bool = False            # suelo deformable (heightfield) en vez de plano rígido
    hfield_size: float = 0.0        # semi-lado del heightfield [m] (0 = automático)
    hfield_res: int = 384
    refs: bool = True               # objetos de referencia de escala (persona de 1.75 m, autobús de 12 m)

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
    def foot_len(self):
        return FOOT_LENGTH * self.H * self.foot_scale

    @property
    def foot_wid(self):
        return FOOT_WIDTH * self.H * self.foot_scale

    @property
    def hip_w(self):
        return HIP_HALF_WIDTH * self.H

    def time_scale(self) -> float:
        """Factor de escala de tiempo con similitud de Froude respecto a 1.75 m."""
        return math.sqrt(self.H / 1.75)


def _box_inertia(m, a, b, c):
    """Inercia diagonal de una caja de lados a,b,c."""
    return (m * (b * b + c * c) / 12, m * (a * a + c * c) / 12, m * (a * a + b * b) / 12)


def build_mjcf(p: MechParams, dt: float | None = None) -> str:
    H, M = p.H, p.M
    s = p.time_scale()
    if dt is None:
        dt = 0.001 * s
    g = 9.81
    W = M * g

    m_hat, m_th, m_sh, m_ft = M * M_HAT, M * M_THIGH, M * M_SHANK, M * M_FOOT
    L_hat = HAT_LENGTH * H
    hat_com_z = COM_HAT * (0.47 * H)      # CdM del HAT ~0.29 H sobre la cadera (Winter: HAT=0.47 H)
    # inercias por radio de giro
    I_th = m_th * (RG_THIGH * p.thigh) ** 2
    I_sh = m_sh * (RG_SHANK * p.shank) ** 2
    I_hat_pitch = m_hat * (RG_HAT * 0.47 * H) ** 2
    I_hat_yaw = m_hat * (0.1 * H) ** 2
    fl, fw, fh = p.foot_len, p.foot_wid, p.ankle_h
    I_ft = _box_inertia(m_ft, fl, fw, fh)

    # Ganancias PD escaladas con similitud dinámica: par ~ M g H, tiempo ~ sqrt(H)
    kp = 60.0 * W * H * p.kp_scale          # N·m/rad
    kv = kp * 0.04 * s                        # N·m·s/rad

    tl = {"hip": 1e12, "hip_roll": 1e12, "knee": 1e12, "ankle": 1e12, "ankle_roll": 1e12}
    tl.update(p.torque_limit)

    r_th = 0.05 * H * 0.6
    r_sh = 0.035 * H * 0.6
    foot_x = fl * (0.5 - 0.25)   # el tobillo está a ~25 % del talón

    if p.hfield:
        half = p.hfield_size or 4.0 * H
        floor_asset = (f'<hfield name="soil" nrow="{p.hfield_res}" ncol="{p.hfield_res}" '
                       f'size="{half} {half} {0.5 * H} {0.2 * H}"/>')
        floor_geom = (f'<geom name="floor" type="hfield" hfield="soil" pos="{half * 0.6} 0 {-0.5 * H}" '
                      f'material="ground" contype="1" conaffinity="1"/>')
    else:
        floor_asset = ""
        floor_geom = (f'<geom name="floor" type="plane" size="{20 * H} {20 * H} {0.1 * H}" '
                      f'material="ground" contype="1" conaffinity="1"/>')

    def leg(side: str, y: float) -> str:
        return f"""
      <body name="thigh_{side}" pos="0 {y:.6g} 0">
        <joint name="hip_roll_{side}" axis="1 0 0" range="-0.6 0.6"/>
        <joint name="hip_pitch_{side}" axis="0 1 0" range="-2.0 1.0"/>
        <inertial pos="0 0 {-COM_THIGH * p.thigh:.6g}" mass="{m_th:.6g}" diaginertia="{I_th:.6g} {I_th:.6g} {0.2 * I_th:.6g}"/>
        <geom name="thigh_{side}" type="capsule" fromto="0 0 0 0 0 {-p.thigh:.6g}" size="{r_th:.6g}" material="armor" contype="0" conaffinity="1" mass="0"/>
        <body name="shank_{side}" pos="0 0 {-p.thigh:.6g}">
          <joint name="knee_{side}" axis="0 1 0" range="0 2.4"/>
          <inertial pos="0 0 {-COM_SHANK * p.shank:.6g}" mass="{m_sh:.6g}" diaginertia="{I_sh:.6g} {I_sh:.6g} {0.2 * I_sh:.6g}"/>
          <geom name="shank_{side}" type="capsule" fromto="0 0 0 0 0 {-p.shank:.6g}" size="{r_sh:.6g}" material="armor2" contype="0" conaffinity="1" mass="0"/>
          <body name="foot_{side}" pos="0 0 {-p.shank:.6g}">
            <joint name="ankle_pitch_{side}" axis="0 1 0" range="-1.0 1.0"/>
            <joint name="ankle_roll_{side}" axis="1 0 0" range="-0.6 0.6"/>
            <inertial pos="{foot_x:.6g} 0 {-fh / 2:.6g}" mass="{m_ft:.6g}" diaginertia="{I_ft[0]:.6g} {I_ft[1]:.6g} {I_ft[2]:.6g}"/>
            <geom name="foot_{side}" type="box" pos="{foot_x:.6g} 0 {-fh / 2:.6g}" size="{fl / 2:.6g} {fw / 2:.6g} {fh / 2:.6g}" material="sole" contype="0" conaffinity="1" mass="0" condim="3" friction="0.9"/>
            <site name="sole_{side}" pos="{foot_x:.6g} 0 {-fh:.6g}" size="{0.01 * H:.6g}"/>
          </body>
        </body>
      </body>"""

    def act(name, joint, lim):
        return (f'<position name="{name}" joint="{joint}" kp="{kp:.6g}" kv="{kv:.6g}" '
                f'forcelimited="true" forcerange="{-lim:.6g} {lim:.6g}"/>')

    acts = []
    for side in ("L", "R"):
        acts += [act(f"hip_roll_{side}", f"hip_roll_{side}", tl["hip_roll"]),
                 act(f"hip_pitch_{side}", f"hip_pitch_{side}", tl["hip"]),
                 act(f"knee_{side}", f"knee_{side}", tl["knee"]),
                 act(f"ankle_pitch_{side}", f"ankle_pitch_{side}", tl["ankle"]),
                 act(f"ankle_roll_{side}", f"ankle_roll_{side}", tl["ankle_roll"])]

    # referencias de escala, solo visuales (no colisionan)
    refs_xml = ""
    if p.refs and H > 3.0:
        y_ref = -0.45 * H
        refs_xml = (f'<geom name="persona" type="capsule" fromto="{0.55 * H:.6g} {y_ref:.6g} 0.25 {0.55 * H:.6g} {y_ref:.6g} 1.5" '
                    f'size="0.25" material="person" contype="0" conaffinity="0"/>'
                    f'<geom name="persona_cabeza" type="sphere" pos="{0.55 * H:.6g} {y_ref:.6g} 1.62" size="0.13" material="person" contype="0" conaffinity="0"/>'
                    f'<geom name="autobus" type="box" pos="{0.55 * H + 9:.6g} {y_ref - 2:.6g} 1.6" size="6 1.25 1.6" material="bus" contype="0" conaffinity="0"/>')

    # rigidez de contacto: escala temporal con sqrt(H) para mantener similitud
    solref = f"{0.01 * s:.6g} 1"

    xml = f"""<mujoco model="mecha_H{H:g}">
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
    <material name="ground" texture="grid" texrepeat="{20:g} {20:g}" texuniform="false" reflectance="0"/>
    <material name="armor" rgba="0.78 0.80 0.83 1"/>
    <material name="armor2" rgba="0.55 0.58 0.62 1"/>
    <material name="sole" rgba="0.25 0.25 0.28 1"/>
    <material name="accent" rgba="0.90 0.55 0.10 1"/>
    <material name="person" rgba="0.85 0.15 0.15 1"/>
    <material name="bus" rgba="0.95 0.80 0.10 1"/>
    {floor_asset}
  </asset>
  <default>
    <geom solref="{solref}" solimp="0.95 0.99 {0.001 * H / 1.75:.6g}"/>
    <joint damping="{0.002 * W * H * s:.6g}" armature="{0.001 * M * H * H:.6g}" solreflimit="{0.02 * s:.6g} 1"/>
  </default>
  <worldbody>
    <light pos="0 0 {6 * H:.6g}" dir="0 0 -1" diffuse="0.5 0.5 0.5"/>
    {floor_geom}
    {refs_xml}
    <body name="pelvis" pos="0 0 {HIP_HEIGHT * H:.6g}">
      <freejoint name="root"/>
      <inertial pos="0 0 {hat_com_z:.6g}" mass="{m_hat:.6g}" diaginertia="{I_hat_pitch:.6g} {I_hat_pitch:.6g} {I_hat_yaw:.6g}"/>
      <geom name="pelvis" type="box" pos="0 0 {0.03 * H:.6g}" size="{0.06 * H:.6g} {0.12 * H:.6g} {0.05 * H:.6g}" material="armor2" contype="0" conaffinity="1" mass="0"/>
      <geom name="torso" type="box" pos="0 0 {0.20 * H:.6g}" size="{0.08 * H:.6g} {0.13 * H:.6g} {0.13 * H:.6g}" material="armor" contype="0" conaffinity="1" mass="0"/>
      <geom name="head" type="sphere" pos="0.01 0 {0.42 * H:.6g}" size="{0.06 * H:.6g}" material="accent" contype="0" conaffinity="1" mass="0"/>
      <geom name="arm_L" type="capsule" fromto="0 {0.17 * H:.6g} {0.30 * H:.6g} 0 {0.18 * H:.6g} {0.0 * H:.6g}" size="{0.03 * H:.6g}" material="armor2" contype="0" conaffinity="0" mass="0"/>
      <geom name="arm_R" type="capsule" fromto="0 {-0.17 * H:.6g} {0.30 * H:.6g} 0 {-0.18 * H:.6g} {0.0 * H:.6g}" size="{0.03 * H:.6g}" material="armor2" contype="0" conaffinity="0" mass="0"/>
      <site name="imu" pos="0 0 {0.2 * H:.6g}"/>
      {leg("L", p.hip_w)}
      {leg("R", -p.hip_w)}
    </body>
  </worldbody>
  <actuator>
    {chr(10).join("    " + a for a in acts)}
  </actuator>
</mujoco>
"""
    return xml


JOINTS = [f"{j}_{s}" for s in ("L", "R") for j in ("hip_roll", "hip_pitch", "knee", "ankle_pitch", "ankle_roll")]
