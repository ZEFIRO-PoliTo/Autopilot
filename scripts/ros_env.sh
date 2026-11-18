#!/usr/bin/env bash
# Shared environment; source this file from the other scripts.
if [[ -n "${ROS_DISTRO:-}" && "${ROS_DISTRO}" != jazzy ]]; then
  echo "Apri un terminale senza altre distro ROS: serve Jazzy." >&2
  return 1
fi
if [[ ! -f /opt/ros/jazzy/setup.bash ]]; then
  echo "ROS 2 Jazzy is missing. Read zefiro_autonomy/docs/install_ros2_jazzy.md" >&2
  return 1
fi
source /opt/ros/jazzy/setup.bash
AUTOPILOT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-41}"
export ROS_AUTOMATIC_DISCOVERY_RANGE="${ROS_AUTOMATIC_DISCOVERY_RANGE:-LOCALHOST}"
