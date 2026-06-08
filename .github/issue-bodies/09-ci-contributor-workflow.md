## Target Effort

15 hours.

## Goal

Keep parallel work from breaking the shared baseline.

## Context

The repo already has a minimal CI workflow. This task turns it into a contributor workflow with clear local commands and PR expectations.

Reference: `zefiro_autonomy/docs/september_hardware_simulation_plan.md`, Task T8.

## Tasks

- [ ] Run local build/test and inspect current CI.
- [ ] Improve CI output or docs if needed.
- [ ] Write a PR checklist.
- [ ] Define local build, test, and test-result commands.
- [ ] Align package test expectations with the package boundary plan.

## Specification Fields

- Local build command:
- Local test command:
- CI status:
- Required PR evidence:
- Package test expectations:

## Expected Outputs

- CI/contributor workflow documentation.
- PR checklist.
- Clear package test expectations.

## Milestones

- 0-4h: local build/test and CI inspection.
- 4-8h: CI output or docs improvement.
- 8-12h: PR checklist.
- 12-15h: alignment with package plan.

## No Single Point Of Failure

Every contributor can run the same baseline command before pushing. CI catches shared breakage even when task owners work independently.

## Definition Of Done

- [ ] CI is documented.
- [ ] PR checklist exists.
- [ ] Local verification commands are clear.
