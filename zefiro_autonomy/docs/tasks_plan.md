# Autonomy Development Tasks

This document is the single public task plan for the Zefiro Autopilot repository. It describes the work needed to move from the current laptop-only ROS 2 demo toward a stack that can be exercised in simulation and later connected to hardware-facing components.

The current stable topic contracts are:

| Topic | Type | Meaning |
| --- | --- | --- |
| `/zefiro/perception/front_clearance` | `std_msgs/msg/Float32` | Estimated free distance in front of the vehicle, in meters. Negative values mean invalid input. |
| `/zefiro/mission/goal_velocity` | `geometry_msgs/msg/TwistStamped` | Desired velocity before safety correction. |
| `/zefiro/setpoint/velocity` | `geometry_msgs/msg/TwistStamped` | Safe velocity command after avoidance. |
| `/zefiro/safety/state` | `std_msgs/msg/String` | Human-readable safety state. |

## Common Rules

- Keep topic names stable unless the change is documented and reviewed.
- Prefer mocks, replay, and synthetic data before depending on hardware.
- Real PX4 output must stay disabled by default until SITL/HITL behavior is documented and reviewed.
- Each task must produce a repository artifact: code, test, launch file, documentation, recorded data, or checklist.
- Each pull request must include what was tested locally.

## Readiness Criteria

The stack is ready for hardware-facing simulation work when:

- `colcon build --symlink-install` passes from a clean checkout.
- `colcon test --event-handlers console_direct+` passes.
- The fake pipeline can be launched and inspected.
- Synthetic or replayed perception can drive the avoidance node.
- The PX4-facing path has a mock adapter and a documented real-output gate.
- Topic contracts and expected outputs are documented.
- Rosbag or equivalent replay/debug commands are available.

## Dependency Map

| Task | Can start now | Depends on |
| --- | --- | --- |
| T0 Setup and readiness checklist | Yes | Current repo |
| T1 Package boundaries and bringup | Yes | Current repo |
| T2 Synthetic perception node | Yes | Current perception topic contract |
| T3 Camera contract and replay path | Yes | Current perception topic contract |
| T4 Avoidance core and safety tests | Yes | Current avoidance behavior |
| T5 PX4 output mock and communication contract | Yes | Current safe setpoint topic contract |
| T6 Simulation scenario harness | Partly | Initial T2/T4/T5 interfaces |
| T7 Observability and rosbag workflow | Yes | Current topic list |
| T8 CI and contributor workflow | Yes | Current build/test commands |
| T9 Integration rehearsal | Later | T1/T2/T4/T5/T6/T7 outputs |

## T0: Setup and Readiness Checklist

Goal: provide a repeatable setup and validation path for contributors.

Inputs:

- Repository checkout.
- Native ROS 2 Jazzy environment or Docker.
- Existing fake avoidance demo.

Expected outputs:

- `zefiro_autonomy/docs/simulation_readiness_checklist.md`.
- Verified build, test, and launch commands.
- Troubleshooting notes for ROS 2 sourcing, stale build artifacts, Docker, and missing topics.

Task example:

Example input:

- A fresh clone of the repository on Ubuntu 24.04 with ROS 2 Jazzy installed.

Example expected output:

- A checklist section like:

```text
Setup validation:
- source /opt/ros/jazzy/setup.bash
- colcon build --symlink-install: PASS
- colcon test --event-handlers console_direct+: PASS
- ros2 launch zefiro_demo demo_fake_avoidance.launch.py: PASS

Observed topics:
- /zefiro/perception/front_clearance
- /zefiro/mission/goal_velocity
- /zefiro/setpoint/velocity
- /zefiro/safety/state
```

Definition of done:

- A new contributor can build, test, launch, and inspect the demo using repository documentation only.
- Known setup failures have direct fixes.

## T1: Package Boundaries and Bringup

Goal: define the package and launch structure used by future perception, avoidance, output, and simulation work.

Inputs:

- Existing `zefiro_demo` package.
- Topic contracts in `zefiro_autonomy/docs/architecture.md`.

Expected outputs:

- A documented package map.
- A bringup plan or `zefiro_bringup` package.
- Launch names for fake input, synthetic perception, PX4 mock, and integration scenarios.

Task example:

Example input:

- Current single-package demo with `demo_fake_avoidance.launch.py`.

Example expected output:

- A package/launch plan like:

```text
Target packages:
- zefiro_perception: camera, replay, synthetic perception
- zefiro_avoidance: safety decision logic and ROS wrapper
- zefiro_px4_adapter: mock and future PX4 output adapter
- zefiro_bringup: launch files

Launch files:
- demo_fake_avoidance.launch.py
- demo_synthetic_perception.launch.py
- demo_px4_mock.launch.py
```

Definition of done:

- Contributors know where each future node should live.
- Existing demo behavior remains runnable.
- Package dependencies are explicit or documented.

## T2: Synthetic Perception Node

Goal: create a controllable perception source that can drive avoidance without real camera hardware.

Inputs:

- `/zefiro/perception/front_clearance`.
- Existing fake clearance behavior.
- Target package guidance from T1 if available.

Expected outputs:

- Synthetic clearance or synthetic depth publisher.
- Parameters for scenario pattern and publish rate.
- Launch file or launch instructions.
- Documentation for expected safety states.

Task example:

Example input:

- Configured clearance sequence: `[5.0, 2.0, 0.7, -1.0]`.

Example expected output:

- A node or launch file that produces:

```text
$ ros2 topic echo /zefiro/perception/front_clearance
data: 5.0
---
data: 2.0
---
data: 0.7
---
data: -1.0
---
```

- And drives these downstream states:

```text
5.0  -> CLEAR
2.0  -> SLOWDOWN
0.7  -> STOP
-1.0 -> INVALID_INPUT
```

Definition of done:

- The node runs without camera hardware.
- Avoidance consumes the published clearance values.
- Expected topic output is documented.

## T3: Camera Contract and Replay Path

Goal: define how real or recorded camera data enters the autonomy stack.

Inputs:

- Expected camera model, if known.
- ROS 2 image/depth conventions.
- Perception output contract from T2.

Expected outputs:

- `zefiro_autonomy/docs/camera_input_contract.md`.
- Expected camera topics, frame ids, message types, encoding, rate, and calibration assumptions.
- Rosbag record/replay commands.
- Fallback path using synthetic or recorded data.

Task example:

Example input:

- Depth camera or recorded depth stream publishing an image.

Example expected output:

- A camera contract section like:

```text
Camera input contract:
- Topic: /camera/depth/image_rect_raw
- Type: sensor_msgs/msg/Image
- Encoding: 32FC1 or 16UC1
- Frame: camera_depth_optical_frame
- Output topic after perception: /zefiro/perception/front_clearance
```

- Replay commands like:

```bash
ros2 bag record /camera/depth/image_rect_raw /camera/camera_info
ros2 bag play camera_depth_sample
```

Definition of done:

- Camera assumptions are explicit.
- Perception work can continue with replayed or synthetic data when hardware is unavailable.

## T4: Avoidance Core and Safety Tests

Goal: make the safety layer testable and robust before vehicle-facing output is enabled.

Inputs:

- `/zefiro/perception/front_clearance`.
- `/zefiro/mission/goal_velocity`.
- Existing `avoidance_node` behavior.

Expected outputs:

- Pure avoidance decision logic separated from ROS I/O.
- Tests for `CLEAR`, `SLOWDOWN`, `STOP`, `INVALID_INPUT`, `SENSOR_TIMEOUT`, saturation, and acceleration limiting where implemented.
- Documented safety parameters.

Task example:

Example input:

```text
clearance_m = 0.7
goal_velocity.linear.x = 1.0
stop_distance_m = 1.0
slowdown_distance_m = 3.0
```

Example expected output:

```text
state = STOP
cmd_velocity.linear.x = 0.0
```

Another expected output example:

```text
clearance_m = 2.0
goal_velocity.linear.x = 1.0
state = SLOWDOWN
cmd_velocity.linear.x = 0.5
```

Definition of done:

- `colcon test --event-handlers console_direct+` passes.
- Invalid, stale, or too-close perception input cannot produce positive forward velocity.
- Safety behavior is documented independently of ROS launch files.

## T5: PX4 Output Mock and Communication Contract

Goal: prepare the PX4-facing boundary while keeping real commands disabled by default.

Inputs:

- `/zefiro/setpoint/velocity`.
- `/zefiro/safety/state`.
- PX4 ROS 2 Offboard and micro XRCE-DDS information.

Expected outputs:

- PX4 output mock adapter.
- `zefiro_autonomy/docs/px4_microxrce_contract.md`.
- Mapping from safe Zefiro setpoints to future PX4 Offboard messages/topics.
- Conditions required before real output can be enabled.

Task example:

Example input:

```text
/zefiro/setpoint/velocity:
  frame_id: base_link
  linear.x: 0.5
  linear.y: 0.0
  linear.z: 0.0

/zefiro/safety/state:
  data: SLOWDOWN
```

Example expected output:

```text
PX4 MOCK: would send velocity setpoint vx=0.50 vy=0.00 vz=0.00, safety_state=SLOWDOWN
```

Definition of done:

- The mock adapter receives safe velocity setpoints.
- Real PX4 publishing is not enabled by default.
- Message, rate, frame, and failsafe assumptions are documented.

## T6: Simulation Scenario Harness

Goal: define repeatable scenarios for validating the autonomy pipeline before hardware is involved.

Inputs:

- Synthetic or fake perception.
- Avoidance safety states.
- Output mock.

Expected outputs:

- Scenario list for clear path, slowdown, stop, invalid sensor data, sensor timeout, and command saturation.
- Launch or script entry points for scenarios.
- Expected topic/state output for each scenario.

Task example:

Example input:

```text
Scenario: front obstacle approaches
clearance sequence: 5.0 -> 2.0 -> 0.7
goal velocity: 1.0 m/s forward
```

Example expected output:

```text
CLEAR    | clearance=5.00 | cmd_vx=1.00
SLOWDOWN | clearance=2.00 | cmd_vx=0.50
STOP     | clearance=0.70 | cmd_vx=0.00
```

Definition of done:

- Scenarios are documented with pass/fail criteria.
- At least one scenario can be run from a launch file or script.
- Expected outputs are clear enough for another contributor to validate.

## T7: Observability and Rosbag Workflow

Goal: make the ROS graph inspectable and replayable during integration.

Inputs:

- Current and planned core topics.
- Existing demo launch.

Expected outputs:

- `zefiro_autonomy/docs/observability.md`.
- Topic inspection commands.
- Rosbag record/replay commands.
- Logger or debug launch notes.

Task example:

Example input:

- Running fake avoidance demo.

Example expected output:

- An observability document section like:

```bash
ros2 topic list
ros2 topic echo /zefiro/safety/state
ros2 bag record \
  /zefiro/perception/front_clearance \
  /zefiro/mission/goal_velocity \
  /zefiro/setpoint/velocity \
  /zefiro/safety/state
```

- Replay command:

```bash
ros2 bag play zefiro_pipeline_bag
```

Definition of done:

- Contributors can inspect nodes and topics from documentation.
- Core topics can be recorded and replayed.
- Debug output is understandable during integration.

## T8: CI and Contributor Workflow

Goal: keep parallel work from breaking the shared baseline.

Inputs:

- Existing GitHub Actions workflow.
- Current build and test commands.
- Future package split from T1.

Expected outputs:

- Contributor checklist.
- Local build/test commands.
- CI expectations for pull requests.
- Package-level test expectations.

Task example:

Example input:

- Pull request changing `zefiro_demo`.

Example expected output:

- A contributor checklist like:

```text
Required PR evidence:
- colcon build --symlink-install: pass
- colcon test --event-handlers console_direct+: pass
- Relevant launch command tested or explicitly marked not applicable
```

Definition of done:

- CI behavior is documented.
- Contributors know the commands to run before opening a pull request.
- New packages have at least one test or documented smoke check expectation.

## T9: Integration Rehearsal

Goal: combine the pipeline pieces and record whether the stack is ready for hardware-facing simulation.

Inputs:

- Bringup launch path from T1.
- Synthetic or replayed perception from T2/T3.
- Avoidance tests from T4.
- Output mock from T5.
- Scenario and observability workflows from T6/T7.

Expected outputs:

- `zefiro_autonomy/docs/integration_rehearsal.md`.
- Recorded run or checklist result for the full fake/synthetic pipeline.
- List of blockers linked to follow-up issues.

Task example:

Example input:

```text
Launch: demo_synthetic_perception_px4_mock.launch.py
Scenario: front obstacle approaches
```

Example expected output:

```text
Build: PASS
Tests: PASS
Topics observed: PASS
Perception sequence: PASS
Avoidance states: CLEAR -> SLOWDOWN -> STOP
PX4 mock received safe setpoints: PASS
Real PX4 output enabled: NO
Blockers: camera replay contract missing calibration details
```

Definition of done:

- Full fake or synthetic pipeline has been rehearsed.
- Results are recorded in the repository.
- Remaining blockers are reproducible and linked to follow-up issues.
