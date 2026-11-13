#!/usr/bin/env bash
set -eo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/ros_env.sh"
cd "$AUTOPILOT_ROOT"
if [[ ! -f install/local_setup.bash ]]; then
  echo "Esegui prima: bash scripts/build.sh" >&2
  exit 1
fi
source install/local_setup.bash
exec ros2 launch zefiro_demo demo_fake_avoidance.launch.py "$@"
