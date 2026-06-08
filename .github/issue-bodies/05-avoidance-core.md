## Target Effort

20 hours.

## Goal

Make the safety layer testable before simulation and hardware communication.

## Context

The current avoidance node mixes ROS I/O with decision logic. This task separates logic from ROS enough to test safety behavior directly.

Reference: `zefiro_autonomy/docs/september_hardware_simulation_plan.md`, Task T4.

## Tasks

- [ ] Extract pure decision logic with no behavior change.
- [ ] Add tests for `CLEAR`, `SLOWDOWN`, `STOP`, `INVALID_INPUT`, and `SENSOR_TIMEOUT`.
- [ ] Add velocity saturation tests.
- [ ] Add acceleration/deceleration tests or document why deferred.
- [ ] Document safety states and parameters.

## Specification Fields

- Inputs:
- Outputs:
- Safety states:
- Parameters:
- Test cases:
- Open edge cases:

## Expected Outputs

- Testable avoidance core.
- ROS wrapper preserved.
- Safety behavior tests.
- Updated documentation.

## Milestones

- 0-5h: pure decision logic extraction.
- 5-11h: tests for existing safety states.
- 11-16h: velocity and acceleration limit tests.
- 16-20h: docs and output-owner review.

## No Single Point Of Failure

Pure logic tests can run without ROS graph, camera, PX4, or simulation. Output work can continue from the documented `/zefiro/setpoint/velocity` contract.

## Definition Of Done

- [ ] `colcon test --event-handlers console_direct+` passes.
- [ ] Unsafe or stale perception input cannot produce positive forward velocity.
- [ ] Safety behavior is documented.
