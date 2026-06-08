# Team Workplan

This plan is the larger work breakdown for the autonomy stack. For the first assignable 15-20 hour tasks aimed at starting simulation with hardware in September, use [september_hardware_simulation_plan.md](september_hardware_simulation_plan.md).

## Coordination Rules

- Work from issues, not from private notes.
- Every pull request must explain what was tested locally.
- Keep topic names stable unless the team agrees to change the contract.
- Prefer small ROS 2 packages with explicit responsibilities.
- Use fake or simulated data before connecting vehicle-facing output.
- Do not send any command to PX4 until the mock adapter and safety behavior are reviewed.

## Shared Milestones

| Milestone | Target | Expected repo state |
| --- | --- | --- |
| M0 | 2-4 hours | Everyone can build and run the existing demo locally or in Docker. |
| M1 | 8-12 hours | Package boundaries, topic contracts, and ownership are agreed. |
| M2 | 18-24 hours | Input, avoidance, output mock, and test work can run independently. |
| M3 | 30+ hours | Integration launch files and documentation let a new teammate reproduce the full fake pipeline. |

## Work Package 1: Input and Perception

Owner profile: teammate already assigned to camera input and first node.

Goal: replace the single fake clearance source with an input boundary that can accept synthetic depth first and a real camera later.

Main inputs:

- Existing `/zefiro/perception/front_clearance` contract.
- Current `fake_front_clearance_node`.
- ROS 2 image/depth conventions.

Expected outputs:

- A `zefiro_perception` package.
- A synthetic depth publisher.
- A depth-to-clearance node that publishes `/zefiro/perception/front_clearance`.
- Parameters for image size, field of view, center crop, minimum valid depth, maximum valid depth, and publish rate.
- A launch file that proves the perception output can drive the existing avoidance node.

Milestones:

- 0-4 hours: run the demo, inspect current topic contracts, document the desired camera/depth input format.
- 4-10 hours: create `zefiro_perception` with a synthetic depth image publisher and basic launch file.
- 10-18 hours: implement a depth-to-clearance node using a central image region and robust invalid-depth handling.
- 18-26 hours: add parameters, logging, and topic inspection documentation.
- 26-34 hours: integrate with avoidance and add a reproducible demo launch.

Definition of done:

- `colcon build` succeeds.
- Synthetic depth changes produce clear, slowdown, stop, and invalid-input behavior through avoidance.
- The README explains the node inputs, outputs, parameters, and expected topic echo results.

## Work Package 2: Safety and Avoidance Core

Goal: make the safety behavior testable before any real output adapter exists.

Main inputs:

- `/zefiro/perception/front_clearance`
- `/zefiro/mission/goal_velocity`

Expected outputs:

- A dedicated `zefiro_avoidance` package.
- Pure decision logic separated from ROS subscriptions/publishers.
- Unit tests for safety states and velocity limits.
- Parameters for stop distance, slowdown distance, timeout, velocity limits, and acceleration/deceleration limits.

Milestones:

- 0-4 hours: extract current avoidance behavior into a small pure-Python function/class.
- 4-12 hours: add unit tests for `CLEAR`, `SLOWDOWN`, `STOP`, `INVALID_INPUT`, `SENSOR_TIMEOUT`, and saturation.
- 12-20 hours: implement acceleration/deceleration limiting and test it.
- 20-28 hours: split the ROS wrapper into `zefiro_avoidance` while preserving topic names.
- 28-36 hours: review edge cases with the input and output owners and document parameters.

Definition of done:

- `colcon test --event-handlers console_direct+` passes.
- Safety behavior is testable without launching ROS.
- No unsafe input condition publishes nonzero forward velocity.

## Work Package 3: Output and micro XRCE-DDS / ROS 2 Communication

Owner profile: teammate assigned to output and micro XRCE-DDS / ROS 2 communication.

Goal: define and prove the vehicle-facing output boundary without sending real commands too early.

Main inputs:

- `/zefiro/setpoint/velocity`
- `/zefiro/safety/state`
- PX4 ROS 2 and micro XRCE-DDS documentation.

Expected outputs:

- A `zefiro_px4_adapter` package.
- A mock adapter that logs what would be sent to PX4.
- A design note mapping Zefiro setpoints to PX4 Offboard topics/messages.
- A launch file for output mock integration.
- A checklist of conditions required before enabling real PX4 output.

Milestones:

- 0-6 hours: study PX4 ROS 2 Offboard examples and micro XRCE-DDS Agent role; document the data path.
- 6-12 hours: create the mock adapter subscribing to `/zefiro/setpoint/velocity`.
- 12-20 hours: write the mapping note for future PX4 messages, rates, frames, arming/offboard constraints, and failsafe assumptions.
- 20-28 hours: add launch files and logs that make command forwarding visible without hardware.
- 28-38 hours: prepare the first real-adapter skeleton behind a disabled-by-default parameter or separate launch file.

Definition of done:

- Mock output works with the current fake pipeline.
- No real PX4 command path is enabled by default.
- The design note clearly states what still needs validation on SITL/hardware.

## Work Package 4: Interfaces, Package Split, and Bringup

Goal: turn the toy package into a repo layout the team can extend in parallel.

Main inputs:

- Current `zefiro_demo` package.
- Topic contracts in `docs/architecture.md`.

Expected outputs:

- `zefiro_bringup` package containing launch files.
- Optional `zefiro_msgs` package only where custom messages add value.
- Package split plan and migration PR.
- Launch files for fake, synthetic perception, and output mock demos.

Milestones:

- 0-4 hours: propose target package layout and dependencies.
- 4-12 hours: create `zefiro_bringup` and move launch files there.
- 12-20 hours: split fake inputs, avoidance, logging, and output mock into packages without changing topics.
- 20-28 hours: evaluate whether `zefiro_msgs` is needed now or should wait.
- 28-36 hours: clean docs so every package has a short README and test command.

Definition of done:

- A clean checkout builds with `colcon build`.
- The existing demo still runs through a bringup launch file.
- Package dependencies are explicit in `package.xml` files.

## Work Package 5: Simulation, Test, and CI

Goal: make regressions visible early and give every contributor a reliable local workflow.

Main inputs:

- Current demo launch.
- Future package split.
- Docker environment.

Expected outputs:

- Test checklist for manual ROS graph verification.
- Unit tests for pure logic.
- Launch/integration smoke tests where practical.
- GitHub Actions workflow for build and tests.
- Documentation for local Docker and native ROS 2 workflows.

Milestones:

- 0-4 hours: verify native and Docker setup instructions.
- 4-12 hours: add first CI workflow for `colcon build` and `colcon test`.
- 12-20 hours: add test documentation and a manual smoke-test checklist.
- 20-28 hours: add lint/test conventions for Python packages.
- 28-36 hours: work with each owner to add at least one meaningful test or smoke check per package.

Definition of done:

- CI runs on pull requests.
- The team has one documented command for local build and one for local tests.
- At least the avoidance core has automated behavioral coverage.

## Optional Work Package 6: Logging, Demo, and Documentation

Use this package if there are 6 contributors. If there are 5, split this work between package owners.

Goal: make the system observable and easy to demo.

Expected outputs:

- Improved logger output.
- A compact demo checklist.
- Topic inspection commands.
- Troubleshooting notes for ROS 2 sourcing, Docker, missing topics, and stale builds.
- Diagrams kept in plain Markdown or Mermaid.

Milestones:

- 0-6 hours: run the current demo and collect confusing points.
- 6-14 hours: improve logger readability without changing core behavior.
- 14-22 hours: write demo and troubleshooting docs.
- 22-30 hours: validate docs on a clean checkout or with a teammate.

Definition of done:

- A new teammate can run the fake demo using docs only.
- Expected output is documented for each launch file.
- Common setup failures have direct fixes.

## Suggested First Sprint Assignment

For 5 people:

- Person A: Work Package 1, input and perception.
- Person B: Work Package 3, output and micro XRCE-DDS / ROS 2 communication.
- Person C: Work Package 2, safety and avoidance core.
- Person D: Work Package 4, package split and bringup.
- Person E: Work Package 5 plus documentation support.

For 6 people:

- Add Person F on Work Package 6.

## Integration Order

1. Stabilize setup and current fake demo.
2. Split packages only after the current behavior is covered by a simple test or checklist.
3. Add synthetic perception before real camera input.
4. Add output mock before any real PX4 adapter.
5. Integrate fake input, synthetic input, avoidance, logger, and output mock in bringup launch files.
6. Move toward PX4 SITL only after mock output and safety tests are reviewed.
