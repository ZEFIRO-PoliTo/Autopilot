## Target Effort

18 hours.

## Goal

Create a perception input that behaves like camera-derived clearance without needing the real camera.

## Context

This task gives avoidance and simulation owners a controllable input source while the real camera path is still being specified.

Reference: `zefiro_autonomy/docs/september_hardware_simulation_plan.md`, Task T2.

## Tasks

- [ ] Define generated data pattern and parameters.
- [ ] Implement a synthetic clearance or synthetic depth publisher.
- [ ] Publish `/zefiro/perception/front_clearance`.
- [ ] Add launch support that drives avoidance through clear, slowdown, stop, and invalid-input cases.
- [ ] Document expected `ros2 topic echo` and logger output.

## Specification Fields

- Published topic:
- Message type:
- Parameters:
- Scenario sequence:
- Expected safety states:

## Expected Outputs

- Synthetic perception node.
- Launch file or launch plan.
- Documentation for expected output.

## Milestones

- 0-4h: generated data pattern and parameters.
- 4-10h: synthetic publisher implementation.
- 10-14h: avoidance integration.
- 14-18h: expected output documentation.

## No Single Point Of Failure

If depth image generation takes too long, publish scalar clearance first and document the depth-image follow-up. Avoidance tests can still proceed.

## Definition Of Done

- [ ] Synthetic input can run without camera hardware.
- [ ] Avoidance receives the expected sequence.
- [ ] Expected outputs are documented.
