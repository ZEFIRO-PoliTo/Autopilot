#!/usr/bin/env bash
set -eo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/ros_env.sh"
cd "$AUTOPILOT_ROOT"
echo "Repo: $AUTOPILOT_ROOT"
echo "ROS: $ROS_DISTRO; dominio: $ROS_DOMAIN_ID; discovery: $ROS_AUTOMATIC_DISCOVERY_RANGE"
for tool in python3 colcon ros2; do
  command -v "$tool" || exit 1
done
python3 -c 'import sys, pytest, rclpy, geometry_msgs, std_msgs, launch_ros; print("Python:", sys.executable); print("pytest:", pytest.__version__, pytest.__file__)'
if [[ -f install/local_setup.bash ]]; then
  source install/local_setup.bash
  ros2 pkg prefix zefiro_demo
else
  echo "Workspace da compilare: bash scripts/build.sh"
fi
echo "Diagnostica base OK. Verifica completa: bash scripts/check.sh"
