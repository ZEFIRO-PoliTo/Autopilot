# Architecture

## Current Demo Architecture

This repository is intentionally a toy ROS 2 pipeline with one Python package and standard ROS 2 messages only.

```text
fake_front_clearance_node
fake_goal_velocity_node
        -> avoidance_node
        -> logger_node
```

## Demo Idea

The demo shows the autonomy boundary between "desired motion" and "safe motion".

The mission input says: move forward at `1.0 m/s`.

The perception input says: this is how much free space exists in front of the vehicle.

The avoidance node combines those two inputs. If the path is clear, it passes the mission velocity through. If an obstacle is close, it slows down or stops. If the perception input is invalid or stale, it stops.

The logger is intentionally used instead of PX4, Gazebo, or hardware so the team can validate the software idea on a laptop.

## Topic Contracts

`/zefiro/perception/front_clearance`

- Type: `std_msgs/msg/Float32`
- Publisher: `fake_front_clearance_node`
- Subscriber: `avoidance_node`, `logger_node`
- Meaning: front free distance in meters
- Demo values: `5.0`, `2.0`, `0.7`, `-1.0`
- Why: this is the smallest possible placeholder for future depth-camera perception

`/zefiro/mission/goal_velocity`

- Type: `geometry_msgs/msg/TwistStamped`
- Publisher: `fake_goal_velocity_node`
- Subscriber: `avoidance_node`, `logger_node`
- Meaning: desired velocity before safety correction
- Demo value: `linear.x = 1.0`
- Why: this represents what a future mission layer, planner, or operator command would request

`/zefiro/setpoint/velocity`

- Type: `geometry_msgs/msg/TwistStamped`
- Publisher: `avoidance_node`
- Subscriber: `logger_node`
- Meaning: safe velocity command after avoidance
- Why: this is the output that could later feed a PX4 Offboard adapter

`/zefiro/safety/state`

- Type: `std_msgs/msg/String`
- Publisher: `avoidance_node`
- Subscriber: `logger_node`
- Meaning: compact explanation of the avoidance decision
- Values: `CLEAR`, `SLOWDOWN`, `STOP`, `INVALID_INPUT`, `SENSOR_TIMEOUT`
- Why: this makes the safety behavior visible during testing and demos

## Current Nodes

The fake clearance node publishes `/zefiro/perception/front_clearance` as a `std_msgs/msg/Float32`.

The fake goal velocity node publishes `/zefiro/mission/goal_velocity` as a `geometry_msgs/msg/TwistStamped`.

The avoidance node subscribes to both inputs and publishes:

- `/zefiro/setpoint/velocity` as a `geometry_msgs/msg/TwistStamped`
- `/zefiro/safety/state` as a `std_msgs/msg/String`

The logger subscribes to all demo topics and prints one compact status line per second.

## Future Architecture

The same idea can later be extended into a real vehicle pipeline:

```text
camera/depth
        -> perception/front_clearance
        -> avoidance
        -> PX4 offboard adapter
        -> PX4
```

In that future version, depth-camera perception would replace the fake clearance node, and a PX4 Offboard adapter would replace the logger-only output path. Custom messages and package splitting should wait until the minimal demo has been validated by the team.
