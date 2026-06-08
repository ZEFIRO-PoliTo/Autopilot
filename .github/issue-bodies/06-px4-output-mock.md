## Target Effort

18 hours.

## Goal

Prepare the PX4 communication boundary while keeping real vehicle commands disabled.

## Context

This task lets the output owner study micro XRCE-DDS / ROS 2 communication and produce a mock adapter usable by integration work.

Reference: `zefiro_autonomy/docs/september_hardware_simulation_plan.md`, Task T5.

## Tasks

- [ ] Create `zefiro_autonomy/docs/px4_microxrce_contract.md`.
- [ ] Document PX4/micro XRCE-DDS data path.
- [ ] Implement a mock subscriber for `/zefiro/setpoint/velocity`.
- [ ] Log what would be sent to PX4.
- [ ] Map safe velocity setpoint to future PX4 Offboard messages/topics.
- [ ] Define conditions required before real PX4 output is enabled.

## Specification Fields

- Subscribed topics:
- Future PX4 topics/messages:
- Expected rates:
- Frame assumptions:
- Real-output enable condition:
- Unknowns requiring SITL/hardware:

## Expected Outputs

- PX4 output mock.
- micro XRCE-DDS/PX4 contract document.
- Real-output safety checklist.

## Milestones

- 0-5h: PX4/micro XRCE-DDS data path.
- 5-10h: mock subscriber and logs.
- 10-15h: mapping and assumptions.
- 15-18h: real-output enable checklist.

## No Single Point Of Failure

Mock adapter can be integrated without PX4. The design note separates confirmed facts from assumptions so another owner can continue the research.

## Definition Of Done

- [ ] Mock adapter receives safe velocity setpoints.
- [ ] Real PX4 output is disabled by default.
- [ ] Communication assumptions are documented for September simulation.
