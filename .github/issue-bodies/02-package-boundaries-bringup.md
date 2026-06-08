## Target Effort

18 hours.

## Goal

Prepare package and launch boundaries so input, avoidance, output, and simulation work can proceed independently.

## Context

This task should reduce parallel-edit conflicts. It does not need real camera or PX4 access.

Reference: `zefiro_autonomy/docs/september_hardware_simulation_plan.md`, Task T1.

## Tasks

- [ ] Write the target package map for `zefiro_perception`, `zefiro_avoidance`, `zefiro_px4_adapter`, `zefiro_bringup`, and optional `zefiro_msgs`.
- [ ] Define launch names and what each launch starts.
- [ ] Create or update `zefiro_bringup` if low-risk.
- [ ] Preserve current topic names unless a contract change is approved.
- [ ] Review topic names with input, avoidance, and output owners.

## Specification Fields

- Package names:
- Launch file names:
- Topics preserved:
- Topics proposed for change:
- Migration risk:

## Expected Outputs

- Package boundary document or migration PR.
- Bringup launch plan.
- Existing fake demo remains runnable.

## Milestones

- 0-4h: package map and dependency direction.
- 4-8h: launch names and launch responsibilities.
- 8-14h: low-risk bringup work or migration steps.
- 14-18h: cross-owner topic review.

## No Single Point Of Failure

If package splitting is delayed, the package map still lets owners work inside `zefiro_demo` temporarily. Topic contracts remain the shared interface.

## Definition Of Done

- [ ] Package boundaries are documented.
- [ ] Other owners know where their nodes should live.
- [ ] Existing fake demo still has a documented launch path.
