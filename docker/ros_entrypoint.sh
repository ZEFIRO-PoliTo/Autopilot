#!/usr/bin/env bash
set -e

source "/opt/ros/${ROS_DISTRO:-jazzy}/setup.bash"

if [ -f "/workspace/autopilot/install/setup.bash" ]; then
  source /workspace/autopilot/install/setup.bash
elif [ -f "/workspace/autopilot/zefiro_autonomy/install/setup.bash" ]; then
  source /workspace/autopilot/zefiro_autonomy/install/setup.bash
fi

exec "$@"
