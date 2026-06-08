## Goal

Define the vehicle-facing output boundary and prove it with a mock adapter before enabling real PX4 communication.

## Context

The output owner is studying micro XRCE-DDS / ROS 2 communication. The first implementation should not send real commands to PX4; it should make the mapping and safety assumptions explicit.

## Tasks

- [ ] Study PX4 ROS 2 Offboard and micro XRCE-DDS Agent data path.
- [ ] Create a `zefiro_px4_adapter` package or a temporary output package.
- [ ] Add a mock adapter subscribing to `/zefiro/setpoint/velocity`.
- [ ] Log the command that would be forwarded to PX4.
- [ ] Write a design note mapping Zefiro setpoints to future PX4 messages/topics.
- [ ] Add a disabled-by-default skeleton or checklist for real PX4 output.

## Expected Outputs

- Output mock node.
- Launch file for fake pipeline plus output mock.
- PX4/micro XRCE-DDS design note.
- Safety checklist before real output.

## Milestones

- 0-6h: research and document PX4/micro XRCE-DDS path.
- 6-12h: mock adapter package and subscriber.
- 12-20h: mapping note covering topics, rates, frames, and failsafe assumptions.
- 20-28h: integration launch and logging.
- 28-38h: reviewed real-output checklist or disabled skeleton.

## Definition of Done

- [ ] Mock adapter receives safe velocity setpoints from avoidance.
- [ ] Real PX4 output is not enabled by default.
- [ ] Documentation clearly separates confirmed behavior from assumptions requiring SITL/hardware validation.
