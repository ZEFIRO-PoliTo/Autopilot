## Goal

Make avoidance behavior testable and robust before connecting any vehicle-facing output.

## Context

The current `avoidance_node` mixes ROS I/O with decision logic. We need pure logic tests and stricter safety handling.

## Tasks

- [ ] Extract decision logic into a pure Python class/function.
- [ ] Add tests for clear, slowdown, stop, invalid input, timeout, and velocity saturation.
- [ ] Add acceleration/deceleration limiting.
- [ ] Preserve existing topic names and launch behavior.
- [ ] Document parameters and safety states.

## Expected Outputs

- Testable avoidance core.
- ROS wrapper node.
- Unit tests.
- Updated avoidance documentation.

## Milestones

- 0-4h: extract current logic without behavior changes.
- 4-12h: add tests for existing states.
- 12-20h: implement and test acceleration/deceleration limits.
- 20-28h: package split or prepare package split with stable topics.
- 28-36h: parameter docs and review with input/output owners.

## Definition of Done

- [ ] `colcon test --event-handlers console_direct+` passes.
- [ ] No invalid, stale, or too-close clearance can produce positive forward velocity.
- [ ] Safety-state behavior is documented.
