## Target Effort

20 hours.

## Goal

Combine the completed pieces into a pre-September rehearsal that proves the team is ready to start hardware simulation.

## Context

This task should run near the end of the work block and should be paired. One person drives the run, another records and verifies results.

Reference: `zefiro_autonomy/docs/september_hardware_simulation_plan.md`, Task T9.

## Tasks

- [ ] Choose the integration launch and scenario.
- [ ] Run build/test.
- [ ] Launch the full fake or synthetic pipeline.
- [ ] Record outputs, logs, and failures.
- [ ] Write blockers for September hardware simulation and assign owners.

## Specification Fields

- Launch file:
- Scenario:
- Nodes observed:
- Topics observed:
- Passed checks:
- Failed checks:
- Blockers:

## Expected Outputs

- `zefiro_autonomy/docs/integration_rehearsal.md`.
- Recorded run or checklist result.
- Blocker list with owners.

## Milestones

- 0-4h: choose launch and scenario.
- 4-10h: build/test and run pipeline.
- 10-15h: record outputs and failures.
- 15-20h: blockers and next actions.

## No Single Point Of Failure

Any blocker must include enough detail for another owner to reproduce it. This task should be run by two people.

## Definition Of Done

- [ ] Full fake or synthetic pipeline has been rehearsed.
- [ ] September blockers are listed with owners.
- [ ] The team has a concrete next-step list.
