#!/usr/bin/env bash
set -e
source "/opt/ros/${ROS_DISTRO:-jazzy}/setup.bash"
exec "$@"
