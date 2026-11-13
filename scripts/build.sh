#!/usr/bin/env bash
set -eo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/ros_env.sh"
cd "$AUTOPILOT_ROOT"
colcon build --base-paths zefiro_autonomy/src --symlink-install --event-handlers console_direct+
