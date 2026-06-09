# Contribution Workflow

This document defines how tasks should be handled in the Zefiro Autopilot repository.

## Task Ownership

- Work should start from a task in [tasks_plan.md](tasks_plan.md) or from a GitHub issue derived from that plan.
- Each task should have one primary owner.
- A task owner is responsible for documenting assumptions, expected inputs, expected outputs, and local verification.
- If a task changes a topic name, message type, launch name, or package boundary, the change must be discussed before implementation.

## Branches

Create one branch per task or small feature.

Branch naming:

```text
task/<task-id>-short-description
```

Examples:

```bash
git checkout -b task/t2-synthetic-perception
git checkout -b task/t4-avoidance-tests
git checkout -b task/t5-px4-output-mock
```

Keep branches focused. A branch for `T2` should not also refactor PX4 output or change unrelated documentation.

## Local Work

Before committing, run the checks that apply to the change.

Baseline commands:

```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
colcon test --event-handlers console_direct+
```

If the task adds or changes a launch file, also run that launch file and record the observed topics or logs.

Useful inspection commands:

```bash
ros2 topic list
ros2 topic echo /zefiro/perception/front_clearance
ros2 topic echo /zefiro/setpoint/velocity
ros2 topic echo /zefiro/safety/state
```

## Commits

Use clear commit messages that describe the actual change.

Examples:

```text
Add synthetic clearance publisher
Extract avoidance decision logic
Document PX4 micro XRCE-DDS output contract
```

Avoid mixing unrelated changes in the same commit. Documentation updates for the same task are fine in the same branch.

## Push And Pull Request

Push the feature branch:

```bash
git push origin task/t2-synthetic-perception
```

Open a pull request into `main`.

The pull request description must include:

- Task id, for example `T2`.
- What changed.
- Example input used for verification.
- Expected output or observed output.
- Commands run locally.
- Any known limitations or follow-up work.

Pull request description template:

```text
Task:

Summary:

Example input:

Expected or observed output:

Local verification:
- [ ] colcon build --symlink-install
- [ ] colcon test --event-handlers console_direct+
- [ ] Relevant launch command, if applicable:

Notes / limitations:
```

## Review

Every pull request should be reviewed before merging.

Review should check:

- The change matches the task scope.
- Topic names and message types are preserved or the change is clearly justified.
- Build and test commands are reported.
- The task has a concrete example input and expected output.
- Documentation was updated when behavior, launch files, or contracts changed.
- Real PX4 output is not enabled by default.

At least one reviewer should approve the pull request before merge. For changes touching PX4 output, safety behavior, or topic contracts, wait for review from the relevant task owner as well.

## Merge

Merge only after:

- Required review is complete.
- CI passes, if CI is enabled for the branch.
- Local verification is documented in the pull request.
- Open review comments are resolved.

Prefer squash merge for small task branches unless the branch history is intentionally structured.

After merge, delete the remote feature branch to keep the repository clean.

## Handling Blockers

If a task is blocked, document the blocker in the issue or pull request.

A useful blocker report includes:

- What command or scenario failed.
- Expected output.
- Actual output.
- Relevant logs or topic output.
- What dependency is missing.
- Suggested next step.

Do not keep blockers only in chat messages. They should be visible in GitHub or in the repository documentation.
