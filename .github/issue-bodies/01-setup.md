## Goal

Make the repo buildable by every teammate using either native ROS 2 Jazzy or Docker.

## Context

The repo currently contains a minimal ROS 2 demo. Before splitting work, every contributor needs a repeatable setup and a known-good command sequence.

## Tasks

- [ ] Test native setup on Ubuntu 24.04 with ROS 2 Jazzy.
- [ ] Test Docker setup from the repository root.
- [ ] Document build, run, and test commands.
- [ ] Add troubleshooting notes for missing ROS setup, stale build folders, and missing topics.

## Expected Outputs

- Updated setup documentation.
- Verified Docker workflow.
- Verified native workflow.
- A short demo checklist.

## Milestones

- 0-4h: run current demo and record exact commands.
- 4-10h: validate Docker build/run workflow.
- 10-18h: improve docs and troubleshooting.
- 18-30h: validate with at least one teammate or clean checkout.

## Definition of Done

- [ ] `colcon build --symlink-install` succeeds.
- [ ] `ros2 launch zefiro_demo demo_fake_avoidance.launch.py` runs.
- [ ] A new teammate can reproduce the demo from docs only.
