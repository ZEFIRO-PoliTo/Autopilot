## Goal

Create the first real input boundary for the autonomy stack using synthetic depth data before using camera hardware.

## Context

The current demo publishes `/zefiro/perception/front_clearance` directly from a fake scalar node. We need a perception package that can later be connected to a camera/depth stream.

## Tasks

- [ ] Create a `zefiro_perception` ROS 2 package.
- [ ] Add a synthetic depth image publisher.
- [ ] Add a depth-to-clearance node.
- [ ] Keep publishing `/zefiro/perception/front_clearance`.
- [ ] Add parameters for image size, central crop, valid depth range, and publish rate.
- [ ] Add a launch file for synthetic perception plus avoidance.

## Expected Outputs

- `zefiro_perception` package.
- Synthetic depth publisher node.
- Depth clearance node.
- Launch file and README.

## Milestones

- 0-4h: document expected camera/depth input and current topic contract.
- 4-10h: package and synthetic publisher skeleton.
- 10-18h: depth-to-clearance computation with invalid-depth handling.
- 18-26h: parameters, logging, and docs.
- 26-34h: integration launch and manual verification.

## Definition of Done

- [ ] Synthetic depth drives `CLEAR`, `SLOWDOWN`, `STOP`, and `INVALID_INPUT` states.
- [ ] `ros2 topic echo /zefiro/perception/front_clearance` shows expected values.
- [ ] Existing avoidance node consumes the output without topic changes.
