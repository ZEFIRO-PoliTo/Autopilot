# Tasks After Demo

## Task 1: Split `zefiro_demo` Into Multiple Packages

Goal: Separate demo responsibilities once the single-package demo is validated.

Expected output:

- `zefiro_fake_inputs`
- `zefiro_avoidance`
- `zefiro_logging`
- `zefiro_bringup`

Local test command:

```bash
colcon build && source install/setup.bash && ros2 launch zefiro_bringup demo_fake_avoidance.launch.py
```

Definition of done: The same demo behavior works after package splitting, with no topic name changes.

## Task 2: Add Custom Messages

Goal: Replace generic demo messages with project-specific interfaces where they add clarity.

Expected output:

- `FrontClearance.msg`
- `SafetyState.msg`

Local test command:

```bash
colcon build && source install/setup.bash && ros2 interface show zefiro_msgs/msg/FrontClearance
```

Definition of done: The avoidance and logger nodes use the custom messages, and the message fields are documented.

## Task 3: Make Avoidance Robust

Goal: Improve avoidance behavior before connecting it to anything vehicle-facing.

Expected output:

- Timeout handling
- Invalid input handling
- Velocity saturation
- Acceleration/deceleration limiter
- Unit tests

Local test command:

```bash
colcon test --event-handlers console_direct+
```

Definition of done: Unit tests cover clear, slowdown, stop, invalid input, timeout, saturation, and acceleration limiting.

## Task 4: Add Synthetic Depth Perception

Goal: Add a synthetic perception step before using real camera hardware.

Expected output:

- `synthetic_depth_image_node`
- `simple_depth_clearance_node`
- Output on `/zefiro/perception/front_clearance`

Local test command:

```bash
ros2 launch zefiro_bringup demo_synthetic_depth.launch.py
```

Definition of done: Synthetic depth data produces the same clearance behavior expected by the avoidance node.

## Task 5: Add PX4 Mock Adapter

Goal: Introduce the adapter boundary without depending on PX4 yet.

Expected output:

- A node that subscribes to `/zefiro/setpoint/velocity`
- A log line that prints `would send to PX4`
- Later mapping notes for PX4 Offboard topics

Local test command:

```bash
ros2 launch zefiro_bringup demo_px4_mock.launch.py
```

Definition of done: The mock adapter receives safe velocity setpoints and clearly shows what would be forwarded to PX4 later.

## Task 6: Improve Logging and Test Documentation

Goal: Make the demo easier for new contributors to run and verify.

Expected output:

- Clearer logger output
- More topic inspection examples
- A short test checklist
- Troubleshooting notes

Local test command:

```bash
ros2 launch zefiro_bringup demo_fake_avoidance.launch.py
```

Definition of done: A new teammate can build, run, inspect, and validate the demo from the documentation alone.
