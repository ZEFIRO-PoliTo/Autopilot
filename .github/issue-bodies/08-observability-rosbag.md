## Target Effort

15 hours.

## Goal

Make debugging possible when multiple nodes and later hardware components are running.

## Context

This task gives the team shared inspection and replay commands, reducing dependence on the original node or hardware owner.

Reference: `zefiro_autonomy/docs/september_hardware_simulation_plan.md`, Task T7.

## Tasks

- [ ] Create `zefiro_autonomy/docs/observability.md`.
- [ ] List all current and planned core topics.
- [ ] Write `ros2 topic`, `ros2 node`, and `ros2 bag` commands.
- [ ] Improve logger/debug output if low-risk.
- [ ] Validate commands on the current fake demo.

## Specification Fields

- Topics to record:
- Replay command:
- Debug launch:
- Expected logger output:
- Known limitations:

## Expected Outputs

- Observability document.
- Rosbag record/replay workflow.
- Debug command checklist.

## Milestones

- 0-4h: topic list.
- 4-8h: inspection and rosbag commands.
- 8-12h: logger/debug improvement if low-risk.
- 12-15h: validation on current fake demo.

## No Single Point Of Failure

Recorded/replayed data lets other owners debug without the original hardware or node owner. Debug commands are committed to the repo.

## Definition Of Done

- [ ] A teammate can inspect the ROS graph from the docs.
- [ ] Core topics can be recorded or replayed.
- [ ] Debug output is readable enough for integration work.
