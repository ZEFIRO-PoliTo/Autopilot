# Exercise: understand and run the demo

By the end, each contributor should be able to start the demo, inspect a topic, stop an input, and explain why the output velocity becomes zero. Set aside a group practice session; initial installation may take additional time.

## 1. The ROS 2 concepts in this repository

| Concept | Meaning | Example |
| --- | --- | --- |
| Node | A ROS program with one responsibility | `avoidance_node` |
| Topic | A named channel for messages | `/zefiro/safety/state` |
| Message | Typed data sent on a topic | `std_msgs/msg/Float32` |
| Publisher / subscriber | Sender / receiver of topic messages | Synthetic sensor → avoidance |
| Package | Installable ROS unit | `zefiro_demo` |
| Launch file | Starts several nodes with configuration | `demo_fake_avoidance.launch.py` |

`colcon build` builds the package. `source` makes ROS and built packages available in the current shell. A **parameter** configures a node; a **callback** runs when a message arrives or a timer fires.

## 2. Get the project

You need access to the organization's GitHub repository. If cloning returns 403, ask the maintainer to add your GitHub account.

```bash
git clone https://github.com/ZEFIRO-PoliTo/Autopilot.git
cd Autopilot
```

Install ROS following [install_ros2_jazzy.md](install_ros2_jazzy.md), or use the container in the [main README](../../README.md). All commands below run from the `Autopilot/` root.

## 3. Build and run the pipeline

Terminal A:

```bash
bash scripts/doctor.sh
bash scripts/check.sh
bash scripts/demo.sh
```

Observe one full cycle:

| Approximate time | Front distance | State | Output velocity |
| --- | --- | --- | --- |
| 0–8 s | 5 m | CLEAR | 1 m/s |
| 8–14 s | 2 m | SLOWDOWN | 0.5 m/s |
| 14–20 s | 0.7 m | STOP | 0 m/s |
| 20–24 s | -1, invalid | INVALID_INPUT | 0 m/s |

An initial timeout before both inputs arrive is expected. The logger samples the latest values once per second; its lines are not atomic snapshots of all topics.

## 4. Inspect the ROS graph

Terminal B, in the same repository (or `docker exec` in the same container):

```bash
source scripts/ros_env.sh
source install/local_setup.bash
ros2 node list
ros2 node info /avoidance_node
ros2 topic list
ros2 topic info /zefiro/setpoint/velocity --verbose
ros2 interface show geometry_msgs/msg/TwistStamped
ros2 topic echo /zefiro/safety/state
```

Stop `echo` with Ctrl+C, then try:

```bash
ros2 topic hz /zefiro/setpoint/velocity
ros2 param get /avoidance_node stop_distance_m
```

Expect four application nodes, the four topics in [architecture.md](architecture.md), output near 20 Hz, and a 1.0 m stop threshold. ROS may also list `/rosout`, `/parameter_events`, and service nodes.

Every terminal in one exercise must use the same `ROS_DOMAIN_ID`. The scripts default to 41 and local discovery. If several people are working on one machine or network, use separate IDs such as 41–45; set the chosen ID in **every** terminal before launching anything:

```bash
export ROS_DOMAIN_ID=42
```

## 5. Stop an input and watch the timeout

Stop the full demo in Terminal A. Do not leave the synthetic publishers running beside the manual publishers. In each new terminal, first run:

```bash
source scripts/ros_env.sh
source install/local_setup.bash
```

Terminal A — avoidance only:

```bash
ros2 run zefiro_demo avoidance_node
```

Terminal B — synthetic distance:

```bash
ros2 topic pub -r 10 /zefiro/perception/front_clearance std_msgs/msg/Float32 "{data: 5.0}"
```

Terminal C — requested velocity:

```bash
ros2 topic pub -r 20 /zefiro/mission/goal_velocity geometry_msgs/msg/TwistStamped "{header: {frame_id: base_link}, twist: {linear: {x: 1.0}}}"
```

Terminal D — state:

```bash
ros2 topic echo /zefiro/safety/state
```

Try these cases in order:

1. Both inputs running → `CLEAR`.
2. Stop Terminal C → `GOAL_TIMEOUT` after about 0.5 s.
3. Restart C → back to `CLEAR`.
4. Stop Terminal B → `SENSOR_TIMEOUT` after about 0.5 s.
5. Restart B with `data: 0.7` → `STOP`.
6. Restart B with `data: -1.0` → `INVALID_INPUT`.

In another terminal, `ros2 topic echo /zefiro/setpoint/velocity` shows that `linear.x` is zero for each stop state. Timeouts use local arrival time, not the message timestamp.

## 6. Read and change a small piece of code

Read these files under `zefiro_autonomy/src/zefiro_demo/` in this order:

1. `zefiro_demo/fake_goal_velocity_node.py`: publisher, timer, message.
2. `zefiro_demo/fake_front_clearance_node.py`: timed distance sequence.
3. `zefiro_demo/avoidance_node.py`: subscribers and watchdog.
4. `zefiro_demo/avoidance_core.py`: decision independent of ROS.
5. `test/test_avoidance_core.py`: testable inputs and outputs.
6. `launch/demo_fake_avoidance.launch.py`: starts the pipeline.

In a personal branch, temporarily change `stop_distance_m` to 1.5 in `config/demo.yaml`. Restart the demo. Explain why a 2 m input now produces about 0.33 m/s. Restore 1.0 before running the standard smoke test. Avoidance parameters are read-only while the node runs.

An external configuration can be passed to the demo with:

```bash
bash scripts/demo.sh config:=/absolute/path/to/demo.yaml
```

## 7. Before the next session

Each contributor should be able to show a successful build, one topic and its message type, `GOAL_TIMEOUT` and `SENSOR_TIMEOUT`, and the files that decide and publish velocity. Then choose a small contribution from [task_plan.md](task_plan.md). You do not need to learn all of ROS 2 first.

Further reading: [ROS environment](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html), [CLI tutorials](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools.html), [colcon tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html).
