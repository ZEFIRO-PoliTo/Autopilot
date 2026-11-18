# Inspect, record, and replay

Start the demo in one terminal. In another terminal at the `Autopilot/` root:

```bash
source scripts/ros_env.sh
source install/local_setup.bash
ros2 node info /avoidance_node
ros2 topic info /zefiro/setpoint/velocity --verbose
ros2 topic hz /zefiro/setpoint/velocity
```

## Record a case

Install `ros-jazzy-rosbag2` (already in the Docker image). Use a new output directory:

```bash
mkdir -p bags
ros2 bag record -o bags/demo_01 \
  /zefiro/perception/front_clearance \
  /zefiro/mission/goal_velocity \
  /zefiro/setpoint/velocity \
  /zefiro/safety/state
```

Record at least one 24-second cycle, then Ctrl+C. `ros2 bag info bags/demo_01` shows duration, types, and message counts. `bags/` is ignored by Git. Include commands and a short summary in the PR, not a large bag.

## Review or recompute

Stop the demo and manual publishers. `ros2 bag play bags/demo_01` republishes **recorded inputs and outputs**; it does not prove that the current code makes the same decisions.

To recompute outputs with current code, stop that playback, run `ros2 run zefiro_demo avoidance_node` in one shell and in another:

```bash
ros2 bag play bags/demo_01 --topics \
  /zefiro/perception/front_clearance \
  /zefiro/mission/goal_velocity
```

Do not run the synthetic publishers during this replay. After the bag ends, expect `SENSOR_TIMEOUT`. Watchdogs use local arrival time; slow or paused replay may itself cause timeouts.

Record evidence using this short template:

```text
Commit:
Environment and ROS_DOMAIN_ID:
Launch/commands:
Inputs or bag and replay speed:
Observed states and velocities:
Sensor/goal interruption and recovery:
Result and limits:
```

Output topics are not atomic or synchronized. Use tests for precise numerical comparisons; the logger is an inspection aid.
