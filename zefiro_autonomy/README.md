# zefiro_autonomy

A minimal ROS 2 demo for the Zefiro autonomy pipeline.

This repository demonstrates a toy laptop-only autonomy flow:

```text
fake clearance -> avoidance -> safe velocity -> logger
```

It publishes fake front clearance and fake mission velocity, runs a simple avoidance node, then prints the safe velocity setpoint and safety state.

## Core Idea

The demo separates the autonomy pipeline into small responsibilities:

- Perception publishes what the vehicle knows about free space ahead.
- Mission publishes what the vehicle would like to do.
- Avoidance decides whether the requested velocity is safe.
- Logging shows the result without connecting to real flight control.

The important behavior is that the mission request is not sent directly to a vehicle-facing output. It first passes through a safety layer.

## What This Is Not

This is not a full drone autonomy stack. It has no PX4, no Gazebo, no camera, no Jetson, no real control, and no planner.

## Demo Topics

| Topic | Type | Why it exists |
| --- | --- | --- |
| `/zefiro/perception/front_clearance` | `std_msgs/msg/Float32` | Minimal perception output: free distance in front of the drone, in meters. Negative values mean invalid sensor data. |
| `/zefiro/mission/goal_velocity` | `geometry_msgs/msg/TwistStamped` | What the mission layer wants before safety correction. In this demo it always asks for `1.0 m/s` forward. |
| `/zefiro/setpoint/velocity` | `geometry_msgs/msg/TwistStamped` | The safe velocity after avoidance has checked clearance, timeouts, invalid data, and velocity limits. |
| `/zefiro/safety/state` | `std_msgs/msg/String` | Human-readable safety state: `CLEAR`, `SLOWDOWN`, `STOP`, `INVALID_INPUT`, or `SENSOR_TIMEOUT`. |

## Prerequisites

- Ubuntu 24.04
- ROS 2 Jazzy
- Python 3
- `rclpy`
- `colcon`

If ROS 2 Jazzy is not installed, see [docs/INSTALL_ROS2_JAZZY.md](docs/INSTALL_ROS2_JAZZY.md).

## Build

From the repository root:

```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

Docker setup is available from the repository root:

```bash
docker compose build
docker compose run --rm autonomy
```

## Run

```bash
ros2 launch zefiro_demo demo_fake_avoidance.launch.py
```

## Expected Output

The logger prints one compact line per second. The state repeats through this sequence:

```text
CLEAR         | clearance=5.00 m | goal_vx=1.00 | cmd_vx=1.00
SLOWDOWN      | clearance=2.00 m | goal_vx=1.00 | cmd_vx=0.50
STOP          | clearance=0.70 m | goal_vx=1.00 | cmd_vx=0.00
INVALID_INPUT | clearance=-1.00 m | goal_vx=1.00 | cmd_vx=0.00
```

## Useful Inspection Commands

```bash
ros2 topic list
ros2 topic echo /zefiro/perception/front_clearance
ros2 topic echo /zefiro/mission/goal_velocity
ros2 topic echo /zefiro/setpoint/velocity
ros2 topic echo /zefiro/safety/state
```

## Future Evolution

- Replace `fake_front_clearance_node` with depth-camera perception.
- Replace logger-only output with a PX4 Offboard adapter.
- Later introduce custom messages.
- Later split into multiple packages.

For the development task plan, use [docs/task_plan.md](docs/task_plan.md).
