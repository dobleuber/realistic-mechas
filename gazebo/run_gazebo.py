"""
Lanza Gazebo (servidor sin interfaz), envía la trayectoria articular completa de
la marcha al JointTrajectoryController del mecha (que la ejecuta dentro de la
simulación, sin latencia) y registra la pose de la pelvis.

Requiere Gazebo Harmonic y sus bindings de Python (python3-gz-transport13,
python3-gz-msgs10), que en Ubuntu 24.04 se usan con python3.12:

    python3.12 gazebo/run_gazebo.py gazebo/out_H20
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time

import numpy as np
from gz.msgs10.clock_pb2 import Clock
from gz.msgs10.joint_trajectory_pb2 import JointTrajectory
from gz.msgs10.joint_trajectory_point_pb2 import JointTrajectoryPoint
from gz.msgs10.pose_v_pb2 import Pose_V
from gz.transport13 import Node


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--no-server", action="store_true", help="no lanzar gz sim (ya está abierto con GUI)")
    ap.add_argument("--timeout", type=float, default=900.0, help="tiempo máximo de reloj [s]")
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    traj = json.load(open(os.path.join(out, "trajectory.json")))
    H = traj["H"]
    T_end = traj["points"][-1]["t"] + 2.0 * traj["time_scale"]

    env = dict(os.environ)
    env["GZ_SIM_RESOURCE_PATH"] = out + ":" + env.get("GZ_SIM_RESOURCE_PATH", "")
    server = None
    if not a.no_server:
        server = subprocess.Popen(["gz", "sim", "-s", "-r", "-v", "2", os.path.join(out, "world.sdf")],
                                  env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    node = Node()
    log = []
    state = {"t": 0.0}
    clock = {"t": None}

    def on_pose(msg: Pose_V):
        t = None
        for p in msg.pose:
            if p.name == "mecha":
                t = clock["t"] if clock["t"] is not None else 0.0
                q = p.orientation
                tilt = 2 * math.acos(min(1.0, abs(q.w)))
                # la pose del modelo coincide con la pelvis desplazada pelvis_z0 hacia abajo
                log.append((t, p.position.x, p.position.y, p.position.z + traj["pelvis_z0"], tilt))
                state["t"] = t

    node.subscribe(Pose_V, "/world/mecha_world/pose/info", on_pose)

    def on_clock(msg: Clock):
        clock["t"] = msg.sim.sec + msg.sim.nsec * 1e-9

    node.subscribe(Clock, "/world/mecha_world/clock", on_clock)
    pub = node.advertise("/model/mecha/joint_trajectory", JointTrajectory)
    tp = np.array([p["t"] for p in traj["points"]])
    t0 = time.time()
    while (not log or clock["t"] is None) and time.time() - t0 < 120:
        time.sleep(0.2)
    if not log:
        print("Gazebo no publicó la pose del mecha (¿se cargó el modelo?)")
        if server:
            server.terminate()
            print(server.communicate(timeout=10)[0][-3000:])
        sys.exit(1)

    msg = JointTrajectory()
    msg.joint_names.extend(traj["joints"])
    for p in traj["points"]:
        pt = JointTrajectoryPoint()
        pt.positions.extend(p["q"])
        pt.time_from_start.sec = int(p["t"])
        pt.time_from_start.nsec = int((p["t"] - int(p["t"])) * 1e9)
        msg.points.append(pt)
    time.sleep(1.0)
    t_send = clock["t"]
    for _ in range(3):
        pub.publish(msg)
        time.sleep(0.05)
    hip0 = None
    fell = False
    while time.time() - t0 < a.timeout:
        time.sleep(0.05)
        tr = clock["t"] - t_send
        if not log:
            continue
        t, x, y, z, tilt = log[-1]
        if hip0 is None and tr > tp[40] + 0.5 * traj["time_scale"]:
            hip0 = z
        if hip0 and (z < 0.6 * hip0 or tilt > 0.6):
            fell = True
            break
        if tr > T_end:
            break
    if server:
        server.terminate()
        try:
            server.wait(timeout=10)
        except Exception:
            server.kill()
    t, x, y, z, tilt = log[-1]
    res = {"H": H, "M": traj["M"], "sim_time": t - t_send, "wall_time": time.time() - t0, "distance": x, "lateral": y,
           "pelvis_z": z, "tilt_rad": tilt, "fell": fell, "planned_distance": traj["planned_distance"]}
    json.dump({"result": res, "log": log}, open(os.path.join(out, "gazebo_log.json"), "w"))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
