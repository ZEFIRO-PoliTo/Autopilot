## Target Effort

16 hours.

## Goal

Prepare for real camera input without blocking on the physical camera being available every day.

## Context

This task defines the input contract and replay path. It can be completed even if the camera is not physically available yet.

Reference: `zefiro_autonomy/docs/september_hardware_simulation_plan.md`, Task T3.

## Tasks

- [ ] Create `zefiro_autonomy/docs/camera_input_contract.md`.
- [ ] Document expected camera/depth output format.
- [ ] Define ROS topic names, frame id, rate, encoding, and calibration assumptions.
- [ ] Document rosbag recording and replay commands.
- [ ] Align with synthetic perception assumptions where practical.

## Specification Fields

- Camera model:
- Expected topics:
- Encoding:
- Frame id:
- Rate:
- Calibration assumptions:
- Replay command:

## Expected Outputs

- Camera input contract.
- Replay workflow.
- Clear fallback when hardware is unavailable.

## Milestones

- 0-4h: expected camera/depth format.
- 4-8h: topic names and frame assumptions.
- 8-12h: recording and replay commands.
- 12-16h: alignment with synthetic data path.

## No Single Point Of Failure

If hardware is unavailable, complete the contract and replay path. Synthetic and replay paths let perception work continue without the camera.

## Definition Of Done

- [ ] Camera input assumptions are explicit.
- [ ] Replay workflow is documented.
- [ ] Perception work is not blocked by hardware access.
