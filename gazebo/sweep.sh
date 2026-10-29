#!/usr/bin/env bash
# Verificación cruzada en Gazebo de los casos clave de la simulación MuJoCo.
# Uso: PY=python3 GZPY=python3.12 bash gazebo/sweep.sh
set -euo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-python3}
GZPY=${GZPY:-python3.12}
OUT=${OUT:-results/gazebo}
mkdir -p "$OUT"
run() {  # nombre H M factor
  "$PY" gazebo/export_sdf.py --H "$2" --M "$3" --torque-factor "$4" --out "$OUT/$1" > /dev/null
  "$GZPY" gazebo/run_gazebo.py "$OUT/$1" --timeout 1500 | grep -v '^#' | tail -n 13 > "$OUT/$1.json"
  echo "$1: $(tr -d '\n ' < "$OUT/$1.json")"
}
# masas del diseño base (tubo de Ti) — ver scaling/mech_scaling.py
run humano_H1.75 1.75 70 1.5
run H20_diseno 20 9480 1.5
run H28_diseno 28 47200 1.5
run H20_par70 20 9480 0.7
