#!/usr/bin/env bash
set -eo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/ros_env.sh"
cd "$AUTOPILOT_ROOT"
bash scripts/build.sh
source install/local_setup.bash
result=0
colcon test --event-handlers console_direct+ --return-code-on-test-failure || result=$?
colcon test-result --verbose || result=$?
exit "$result"
