# GitHub Issues

This file contains ready-to-create issues for the first development block. Create them with `gh issue create` or copy them into GitHub manually.

Recommended labels:

- `area:setup`
- `area:input`
- `area:avoidance`
- `area:output`
- `area:bringup`
- `area:test`
- `area:docs`
- `priority:high`
- `priority:medium`

## Create Labels

```bash
gh label create "area:setup" --color "5319e7" --description "Development environment and repo workflow"
gh label create "area:input" --color "1d76db" --description "Camera, synthetic depth, and perception input"
gh label create "area:avoidance" --color "d93f0b" --description "Safety and avoidance behavior"
gh label create "area:output" --color "0052cc" --description "PX4, micro XRCE-DDS, and output adapters"
gh label create "area:bringup" --color "0e8a16" --description "ROS 2 package layout and launch files"
gh label create "area:test" --color "fbca04" --description "Automated tests, smoke tests, and CI"
gh label create "area:docs" --color "006b75" --description "Documentation and demo instructions"
gh label create "priority:high" --color "b60205" --description "Must be handled in the first work block"
gh label create "priority:medium" --color "fbca04" --description "Important but can follow high-priority work"
```

## Issue 1: Stabilize Local and Docker Setup

Labels: `area:setup`, `area:docs`, `priority:high`

```text
Goal
Make the repo buildable by every teammate using either native ROS 2 Jazzy or Docker.

Context
The repo currently contains a minimal ROS 2 demo. Before splitting work, every contributor needs a repeatable setup and a known-good command sequence.

Tasks
- Test native setup on Ubuntu 24.04 with ROS 2 Jazzy.
- Test Docker setup from the repository root.
- Document build, run, and test commands.
- Add troubleshooting notes for missing ROS setup, stale build folders, and missing topics.

Expected outputs
- Updated setup documentation.
- Verified Docker workflow.
- Verified native workflow.
- A short demo checklist.

Milestones
- 0-4h: run current demo and record exact commands.
- 4-10h: validate Docker build/run workflow.
- 10-18h: improve docs and troubleshooting.
- 18-30h: validate with at least one teammate or clean checkout.

Definition of done
- `colcon build --symlink-install` succeeds.
- `ros2 launch zefiro_demo demo_fake_avoidance.launch.py` runs.
- A new teammate can reproduce the demo from docs only.
```

## Issue 2: Implement Synthetic Depth Input and Clearance Node

Labels: `area:input`, `priority:high`

```text
Goal
Create the first real input boundary for the autonomy stack using synthetic depth data before using camera hardware.

Context
The current demo publishes `/zefiro/perception/front_clearance` directly from a fake scalar node. We need a perception package that can later be connected to a camera/depth stream.

Tasks
- Create a `zefiro_perception` ROS 2 package.
- Add a synthetic depth image publisher.
- Add a depth-to-clearance node.
- Keep publishing `/zefiro/perception/front_clearance`.
- Add parameters for image size, central crop, valid depth range, and publish rate.
- Add a launch file for synthetic perception plus avoidance.

Expected outputs
- `zefiro_perception` package.
- Synthetic depth publisher node.
- Depth clearance node.
- Launch file and README.

Milestones
- 0-4h: document expected camera/depth input and current topic contract.
- 4-10h: package and synthetic publisher skeleton.
- 10-18h: depth-to-clearance computation with invalid-depth handling.
- 18-26h: parameters, logging, and docs.
- 26-34h: integration launch and manual verification.

Definition of done
- Synthetic depth drives `CLEAR`, `SLOWDOWN`, `STOP`, and `INVALID_INPUT` states.
- `ros2 topic echo /zefiro/perception/front_clearance` shows expected values.
- Existing avoidance node consumes the output without topic changes.
```

## Issue 3: Refactor and Test Avoidance Core

Labels: `area:avoidance`, `area:test`, `priority:high`

```text
Goal
Make avoidance behavior testable and robust before connecting any vehicle-facing output.

Context
The current `avoidance_node` mixes ROS I/O with decision logic. We need pure logic tests and stricter safety handling.

Tasks
- Extract decision logic into a pure Python class/function.
- Add tests for clear, slowdown, stop, invalid input, timeout, and velocity saturation.
- Add acceleration/deceleration limiting.
- Preserve existing topic names and launch behavior.
- Document parameters and safety states.

Expected outputs
- Testable avoidance core.
- ROS wrapper node.
- Unit tests.
- Updated avoidance documentation.

Milestones
- 0-4h: extract current logic without behavior changes.
- 4-12h: add tests for existing states.
- 12-20h: implement and test acceleration/deceleration limits.
- 20-28h: package split or prepare package split with stable topics.
- 28-36h: parameter docs and review with input/output owners.

Definition of done
- `colcon test --event-handlers console_direct+` passes.
- No invalid, stale, or too-close clearance can produce positive forward velocity.
- Safety-state behavior is documented.
```

## Issue 4: Design and Implement PX4 Output Mock Adapter

Labels: `area:output`, `priority:high`

```text
Goal
Define the vehicle-facing output boundary and prove it with a mock adapter before enabling real PX4 communication.

Context
The output owner is studying micro XRCE-DDS / ROS 2 communication. The first implementation should not send real commands to PX4; it should make the mapping and safety assumptions explicit.

Tasks
- Study PX4 ROS 2 Offboard and micro XRCE-DDS Agent data path.
- Create a `zefiro_px4_adapter` package or a temporary output package.
- Add a mock adapter subscribing to `/zefiro/setpoint/velocity`.
- Log the command that would be forwarded to PX4.
- Write a design note mapping Zefiro setpoints to future PX4 messages/topics.
- Add a disabled-by-default skeleton or checklist for real PX4 output.

Expected outputs
- Output mock node.
- Launch file for fake pipeline plus output mock.
- PX4/micro XRCE-DDS design note.
- Safety checklist before real output.

Milestones
- 0-6h: research and document PX4/micro XRCE-DDS path.
- 6-12h: mock adapter package and subscriber.
- 12-20h: mapping note covering topics, rates, frames, and failsafe assumptions.
- 20-28h: integration launch and logging.
- 28-38h: reviewed real-output checklist or disabled skeleton.

Definition of done
- Mock adapter receives safe velocity setpoints from avoidance.
- Real PX4 output is not enabled by default.
- Documentation clearly separates confirmed behavior from assumptions requiring SITL/hardware validation.
```

## Issue 5: Split Packages and Create Bringup Launches

Labels: `area:bringup`, `priority:high`

```text
Goal
Move from one demo package to a package layout that lets 5-6 people work independently.

Context
The current `zefiro_demo` package is useful for the first demo, but input, avoidance, output, logging, and bringup need separate ownership.

Tasks
- Propose target package layout.
- Create `zefiro_bringup` for launch files.
- Split fake inputs, avoidance, logging, perception, and output mock where ready.
- Keep topic names stable during the migration.
- Decide whether custom messages are needed now or later.

Expected outputs
- Package split PR.
- Bringup launch files.
- Updated architecture docs.
- Package READMEs or concise package sections in the main docs.

Milestones
- 0-4h: target package layout proposal.
- 4-12h: create bringup package and move launch files.
- 12-20h: split fake input/logging/avoidance packages.
- 20-28h: evaluate `zefiro_msgs`.
- 28-36h: docs and integration cleanup.

Definition of done
- Clean checkout builds with `colcon build`.
- Fake demo still runs through bringup.
- Package dependencies are explicit.
```

## Issue 6: Harden CI and Test Workflow

Labels: `area:test`, `area:setup`, `priority:medium`

```text
Goal
Make build and test failures more useful on pull requests.

Context
A minimal GitHub Actions workflow already builds the workspace and runs `colcon test`. As multiple people start contributing, it should be extended with package-specific tests and clearer failure output.

Tasks
- Review the existing GitHub Actions workflow.
- Keep building the workspace with `colcon build --symlink-install`.
- Keep running tests with `colcon test`.
- Upload or print test results in a useful way.
- Add meaningful tests as package owners add logic.
- Document the local equivalent commands.

Expected outputs
- Reviewed or improved `.github/workflows/ci.yml`.
- Updated setup/test docs.
- Passing CI on the default branch.

Milestones
- 0-6h: review the minimal CI build.
- 6-12h: improve test result output if needed.
- 12-20h: align CI with Docker/native docs.
- 20-30h: add package-specific tests as they appear.

Definition of done
- Pull requests run CI automatically.
- CI catches build failures.
- Contributors know the matching local commands.
```

## Issue 7: Improve Demo Logging and Troubleshooting

Labels: `area:docs`, `priority:medium`

```text
Goal
Make demos and debugging easier for new contributors.

Context
The current logger is intentionally minimal. As the system grows, the team needs clearer output and troubleshooting notes.

Tasks
- Improve logger readability while keeping output compact.
- Add a manual smoke-test checklist.
- Add topic inspection examples for every launch file.
- Document common ROS 2 setup and stale-build problems.
- Keep the documentation synchronized with package split work.

Expected outputs
- Improved logger output.
- Demo checklist.
- Troubleshooting guide.
- Updated README references.

Milestones
- 0-6h: run current demo and collect confusing points.
- 6-14h: improve logger output.
- 14-22h: write docs and checklist.
- 22-30h: validate instructions on clean checkout or with teammate.

Definition of done
- A new teammate can build, run, inspect topics, and understand expected output.
- Docs cover both Docker and native setup.
```
