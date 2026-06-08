## Target Effort

15 hours.

## Goal

Make the baseline workflow reproducible and define exactly what "ready for September simulation" means.

## Context

This task supports all other tasks. It should not wait for camera, PX4, package split, or simulation work.

Reference: `zefiro_autonomy/docs/september_hardware_simulation_plan.md`, Task T0.

## Tasks

- [ ] Run native build/test and record exact commands.
- [ ] Validate Docker instructions or document why Docker could not be validated.
- [ ] Create `zefiro_autonomy/docs/simulation_readiness_checklist.md`.
- [ ] Add troubleshooting notes for ROS 2 sourcing, stale `build/install/log`, Docker, and missing topics.
- [ ] Ask another teammate to run one checklist section and record feedback.

## Specification Fields

- Machine used:
- ROS 2 version:
- Docker available: yes/no
- Commands verified:
- Known failures:

## Expected Outputs

- Simulation readiness checklist.
- Verified native workflow.
- Docker status clearly documented.
- Troubleshooting notes.

## Milestones

- 0-4h: run native build/test and record exact commands.
- 4-8h: validate Docker instructions or document the gap.
- 8-12h: write the readiness checklist.
- 12-15h: non-owner validation pass.

## No Single Point Of Failure

If Docker is not available, complete the native workflow and record the Docker gap. The checklist must be readable enough for another person to continue validation.

## Definition Of Done

- [ ] Checklist exists and includes exact commands.
- [ ] Native build/test has been verified.
- [ ] One non-owner has enough information to reproduce the flow.
