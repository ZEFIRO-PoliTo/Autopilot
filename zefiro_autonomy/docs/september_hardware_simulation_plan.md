# September Hardware Simulation Readiness Plan

This plan is for parallel work before the team starts simulation with hardware in September. Each task is sized for about 15-20 hours and should be assignable as a GitHub issue.

The target is not a fully autonomous drone. The target is a reproducible ROS 2 stack that can run the autonomy pipeline in simulation, connect to selected hardware inputs or communication components, and prove that unsafe output paths remain controlled.

## Working Rules

- Each task must produce a repo artifact: code, launch file, test, document, recorded data, or checklist.
- No task can depend on one person being available. Every task must publish its assumptions in the task issue.
- Every owner must add a short "handoff notes" section to their PR.
- Keep topic names stable during this phase unless the team explicitly accepts a contract change.
- Use fake data, replay data, or mocks whenever real hardware is unavailable.
- Real vehicle-facing output stays disabled until PX4/SITL/HITL checks are reviewed.

## September Entry Criteria

The team is ready to start simulation with hardware when these are true:

- A clean checkout builds with `colcon build --symlink-install`.
- `colcon test --event-handlers console_direct+` passes.
- There is a launch file for the full fake pipeline.
- There is a launch file for synthetic or replayed perception data.
- There is a launch file for the PX4 output mock.
- Topic contracts are documented for perception input, mission input, safe setpoint output, and safety state.
- PX4/micro XRCE-DDS assumptions are documented separately from confirmed behavior.
- At least one teammate other than the task owner can run each documented demo.

## Parallel Task Map

| Task | Size | Primary area | Can run without |
| --- | --- | --- | --- |
| T0 Setup and acceptance checklist | 15h | Setup/docs | Camera, PX4, package split |
| T1 Package boundaries and bringup | 18h | Architecture/launch | Real camera, PX4 |
| T2 Synthetic perception node | 18h | Input/perception | Real camera, PX4 |
| T3 Camera interface specification and replay path | 16h | Input/hardware prep | Real camera online |
| T4 Avoidance core and safety tests | 20h | Safety | Camera, PX4 |
| T5 PX4 output mock and micro XRCE-DDS study | 18h | Output/communication | Real PX4 connection |
| T6 Simulation scenario harness | 18h | Simulation | Real camera, PX4 |
| T7 Observability and rosbag workflow | 15h | Debug/data | Package split complete |
| T8 CI and contributor workflow | 15h | Test/workflow | Hardware |
| T9 Integration rehearsal | 20h | Bringup/integration | Final hardware availability |

If there are 5 people, assign one task each and keep T7/T8/T9 as shared follow-up. If there are 6 people, assign T7 or T8 to the sixth person immediately. T9 should be run near the end by two people together.

## Task T0: Setup and Acceptance Checklist

Goal: make the baseline workflow reproducible and define exactly what "ready for September simulation" means.

Inputs:

- Current repo.
- Existing Dockerfile and native ROS 2 instructions.
- September entry criteria in this document.

Expected outputs:

- `docs/simulation_readiness_checklist.md`.
- A short troubleshooting section for ROS 2 sourcing, stale `build/install/log`, Docker, and missing topics.
- Verified commands for native build/test and Docker build/run.

Milestones:

- 0-4h: run native build/test and record exact commands.
- 4-8h: validate Docker instructions or document what could not be validated.
- 8-12h: write the readiness checklist.
- 12-15h: ask another teammate to run one checklist section and record feedback.

Specification fields to fill in the issue:

- Machine used:
- ROS 2 version:
- Docker available: yes/no
- Commands verified:
- Known failures:

No single point of failure:

- If Docker is not available, the owner still completes the native workflow and records the Docker gap.
- The checklist must be readable enough for another person to continue validation.

Definition of done:

- The checklist exists and includes exact commands.
- At least native build/test has been verified.
- One non-owner has enough information to reproduce the flow.

## Task T1: Package Boundaries and Bringup

Goal: prepare a package and launch structure that allows input, avoidance, output, and simulation work to proceed independently.

Inputs:

- Existing `zefiro_demo` package.
- Current topic contracts in `docs/architecture.md`.

Expected outputs:

- Proposed package map for `zefiro_perception`, `zefiro_avoidance`, `zefiro_px4_adapter`, `zefiro_bringup`, and optional `zefiro_msgs`.
- Bringup launch plan for fake, synthetic perception, PX4 mock, and integration rehearsal.
- Minimal migration PR if the team agrees the split should start now.

Milestones:

- 0-4h: write the target package map and dependency direction.
- 4-8h: define launch names and what each launch starts.
- 8-14h: create or update `zefiro_bringup` if low-risk; otherwise document exact migration steps.
- 14-18h: review topic names with T2, T4, and T5 owners.

Specification fields to fill in the issue:

- Package names:
- Launch file names:
- Topics preserved:
- Topics proposed for change:
- Migration risk:

No single point of failure:

- If package splitting is delayed, the launch and package map still lets other owners code inside `zefiro_demo` temporarily.
- Topic contracts remain the shared interface, not private knowledge.

Definition of done:

- Package boundaries are documented.
- Other task owners know where their nodes should live.
- Existing fake demo still has a documented launch path.

## Task T2: Synthetic Perception Node

Goal: create a perception input that behaves like camera-derived clearance without needing the real camera.

Inputs:

- `/zefiro/perception/front_clearance` contract.
- Existing fake clearance node.
- T1 package guidance.

Expected outputs:

- Synthetic depth or synthetic clearance source.
- Clearance publisher with configurable pattern.
- Launch file that drives avoidance through clear, slowdown, stop, and invalid-input cases.
- Node README or doc section.

Milestones:

- 0-4h: define generated data pattern and parameters.
- 4-10h: implement synthetic publisher.
- 10-14h: integrate with avoidance launch.
- 14-18h: document expected `ros2 topic echo` and logger output.

Specification fields to fill in the issue:

- Published topic:
- Message type:
- Parameters:
- Scenario sequence:
- Expected safety states:

No single point of failure:

- If depth image generation takes too long, publish scalar clearance first and document the depth-image follow-up.
- T4 can still test avoidance using scalar clearance.

Definition of done:

- The synthetic input can run without camera hardware.
- Avoidance receives the expected sequence.
- Expected outputs are documented.

## Task T3: Camera Interface Specification and Replay Path

Goal: prepare for real camera input without blocking on the physical camera being available every day.

Inputs:

- Expected camera model if known.
- ROS 2 image/depth message conventions.
- T2 synthetic perception assumptions.

Expected outputs:

- `docs/camera_input_contract.md`.
- Camera topic contract: raw image/depth topic, frame id, rate, encoding, calibration assumptions.
- Replay strategy using rosbag or a small documented sample.
- Fallback path for running perception from recorded or synthetic data.

Milestones:

- 0-4h: document the expected camera/depth output format.
- 4-8h: define the ROS topic names and frame assumptions.
- 8-12h: document recording and replay commands.
- 12-16h: align with T2 so synthetic data matches the same contract where practical.

Specification fields to fill in the issue:

- Camera model:
- Expected topics:
- Encoding:
- Frame id:
- Rate:
- Calibration assumptions:
- Replay command:

No single point of failure:

- If hardware is unavailable, the owner still completes the contract and replay path.
- Synthetic and replay paths let perception work continue without the camera.

Definition of done:

- Camera input assumptions are explicit.
- Replay workflow is documented.
- Perception work is not blocked by hardware access.

## Task T4: Avoidance Core and Safety Tests

Goal: make the safety layer testable before simulation and hardware communication.

Inputs:

- `/zefiro/perception/front_clearance`.
- `/zefiro/mission/goal_velocity`.
- Existing avoidance node behavior.

Expected outputs:

- Pure avoidance logic separated from ROS I/O.
- Tests for `CLEAR`, `SLOWDOWN`, `STOP`, `INVALID_INPUT`, `SENSOR_TIMEOUT`, and velocity saturation.
- Parameters documented for stop distance, slowdown distance, timeout, max velocity, and acceleration limits.

Milestones:

- 0-5h: extract pure decision logic with no behavior change.
- 5-11h: add tests for existing safety states.
- 11-16h: add velocity saturation and acceleration/deceleration tests or document why deferred.
- 16-20h: update docs and review outputs with T5 owner.

Specification fields to fill in the issue:

- Inputs:
- Outputs:
- Safety states:
- Parameters:
- Test cases:
- Open edge cases:

No single point of failure:

- The pure logic tests can run without ROS graph, camera, PX4, or simulation.
- T5 can use the documented output contract even if refactor work is still in progress.

Definition of done:

- `colcon test --event-handlers console_direct+` passes.
- Unsafe or stale perception input cannot produce positive forward velocity.
- Safety behavior is documented.

## Task T5: PX4 Output Mock and micro XRCE-DDS Study

Goal: prepare the output communication boundary while keeping real vehicle commands disabled.

Inputs:

- `/zefiro/setpoint/velocity`.
- `/zefiro/safety/state`.
- PX4 ROS 2 Offboard and micro XRCE-DDS references.

Expected outputs:

- Output mock adapter.
- `docs/px4_microxrce_contract.md`.
- Mapping from safe velocity setpoint to future PX4 Offboard messages.
- Startup checklist for micro XRCE-DDS Agent, PX4 SITL, and later hardware.

Milestones:

- 0-5h: document PX4/micro XRCE-DDS data path.
- 5-10h: implement mock subscriber and visible log output.
- 10-15h: write mapping and rate/frame assumptions.
- 15-18h: define what must be proven before enabling real PX4 output.

Specification fields to fill in the issue:

- Subscribed topics:
- Future PX4 topics/messages:
- Expected rates:
- Frame assumptions:
- Real-output enable condition:
- Unknowns requiring SITL/hardware:

No single point of failure:

- Mock adapter can be integrated without PX4.
- The design note separates confirmed facts from assumptions so another owner can continue the research.

Definition of done:

- Mock adapter receives safe velocity setpoints.
- Real PX4 output is disabled by default.
- Communication assumptions are documented for September simulation.

## Task T6: Simulation Scenario Harness

Goal: define repeatable scenarios for simulation before hardware enters the loop.

Inputs:

- Synthetic perception from T2.
- Avoidance states from T4.
- Output mock from T5.

Expected outputs:

- Scenario list for clear path, obstacle slowdown, obstacle stop, invalid sensor data, sensor timeout, and command saturation.
- Launch or script entry points for running scenarios.
- Expected topic/state output for each scenario.

Milestones:

- 0-4h: list scenarios and expected states.
- 4-10h: create launch/script hooks using existing fake or synthetic nodes.
- 10-15h: document expected outputs and pass/fail criteria.
- 15-18h: run at least two scenarios with another task owner.

Specification fields to fill in the issue:

- Scenario names:
- Nodes started:
- Expected topics:
- Expected safety states:
- Pass/fail criteria:

No single point of failure:

- Scenarios can use fake or synthetic data if full simulation is not ready.
- The harness defines expected behavior independent of the person who wrote the nodes.

Definition of done:

- At least four scenarios are documented.
- At least two scenarios are runnable.
- Expected outputs are clear enough for another teammate to validate.

## Task T7: Observability and Rosbag Workflow

Goal: make debugging possible when multiple nodes and later hardware components are running.

Inputs:

- Current demo topics.
- Planned perception, avoidance, and output topics.

Expected outputs:

- `docs/observability.md`.
- Topic inspection commands.
- Rosbag record/replay commands for the core pipeline.
- Logger improvements or a documented debug launch.

Milestones:

- 0-4h: list all current and planned topics.
- 4-8h: write `ros2 topic`, `ros2 node`, and `ros2 bag` commands.
- 8-12h: improve logger/debug output if low-risk.
- 12-15h: validate commands on current fake demo.

Specification fields to fill in the issue:

- Topics to record:
- Replay command:
- Debug launch:
- Expected logger output:
- Known limitations:

No single point of failure:

- Recorded/replayed data lets other owners debug without the original hardware or node owner.
- Debug commands are committed to the repo, not held privately.

Definition of done:

- A teammate can inspect the ROS graph from the docs.
- Core topics can be recorded or replayed.
- Debug output is readable enough for integration work.

## Task T8: CI and Contributor Workflow

Goal: keep parallel work from breaking the shared baseline.

Inputs:

- Existing GitHub Actions workflow.
- Current package tests.
- Planned package split.

Expected outputs:

- CI workflow reviewed and adjusted if needed.
- Contributor checklist for PRs.
- Local commands for build, test, and test-result inspection.
- At least one meaningful test requirement for each new package.

Milestones:

- 0-4h: run local build/test and inspect current CI.
- 4-8h: improve CI output or docs if needed.
- 8-12h: write PR checklist.
- 12-15h: align checklist with T1 package plan.

Specification fields to fill in the issue:

- Local build command:
- Local test command:
- CI status:
- Required PR evidence:
- Package test expectations:

No single point of failure:

- Every contributor can run the same baseline command before pushing.
- CI catches shared breakage even when task owners work independently.

Definition of done:

- CI is documented.
- PR checklist exists.
- Local verification commands are clear.

## Task T9: Integration Rehearsal

Goal: combine the completed pieces into a pre-September rehearsal that proves the team is ready to start hardware simulation.

Inputs:

- T0 checklist.
- T1 bringup plan.
- T2/T3 input path.
- T4 avoidance tests.
- T5 output mock.
- T6 scenarios.
- T7 observability workflow.

Expected outputs:

- `docs/integration_rehearsal.md`.
- A recorded run or checklist results for the full fake/synthetic pipeline.
- List of blockers for September hardware simulation.
- Owners assigned for each blocker.

Milestones:

- 0-4h: choose the integration launch and scenario.
- 4-10h: run build/test and launch the pipeline.
- 10-15h: record outputs, logs, and failures.
- 15-20h: write blockers and next actions.

Specification fields to fill in the issue:

- Launch file:
- Scenario:
- Nodes observed:
- Topics observed:
- Passed checks:
- Failed checks:
- Blockers:

No single point of failure:

- Run this task as a pair: one person drives, one records and verifies.
- Any blocker must include enough detail for another owner to reproduce it.

Definition of done:

- Full fake or synthetic pipeline has been rehearsed.
- September blockers are listed with owners.
- The team has a concrete next-step list.

## Suggested Assignment

For 5 people:

- Person A: T2 synthetic perception, then support T3.
- Person B: T5 PX4 output mock and micro XRCE-DDS study.
- Person C: T4 avoidance core and safety tests.
- Person D: T1 package boundaries and bringup, then T9 integration.
- Person E: T0 setup checklist and T8 CI workflow.
- Shared: T6 simulation scenarios and T7 observability, split after first PRs.

For 6 people:

- Person F owns T7 observability and helps T6.
- T9 is still paired between bringup and one non-bringup owner.

## Minimum First Assignment Set

Start these in parallel immediately:

- T0 because everyone depends on clear setup.
- T1 because package boundaries avoid messy parallel edits.
- T2 because input can be developed without camera hardware.
- T4 because safety tests are independent.
- T5 because output communication research can proceed without PX4.

Start these once the first five tasks have initial PRs:

- T3 camera contract.
- T6 simulation scenarios.
- T7 observability.
- T8 CI hardening.
- T9 integration rehearsal.
