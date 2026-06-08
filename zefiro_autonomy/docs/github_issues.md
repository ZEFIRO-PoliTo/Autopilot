# GitHub Issues

This file lists the issue set for the 15-20 hour September hardware simulation readiness tasks. The detailed task descriptions live in [september_hardware_simulation_plan.md](september_hardware_simulation_plan.md).

Create the labels and issues automatically with:

```bash
scripts/create_github_issues.sh
```

Or create them manually from `.github/issue-bodies/`.

## Recommended Labels

- `area:setup`
- `area:input`
- `area:avoidance`
- `area:output`
- `area:bringup`
- `area:simulation`
- `area:hardware`
- `area:test`
- `area:docs`
- `area:integration`
- `priority:high`
- `priority:medium`

## Issue Set

| Issue | Labels | Target effort |
| --- | --- | --- |
| T0 Setup and acceptance checklist | `area:setup`, `area:docs`, `priority:high` | 15h |
| T1 Package boundaries and bringup | `area:bringup`, `priority:high` | 18h |
| T2 Synthetic perception node | `area:input`, `area:simulation`, `priority:high` | 18h |
| T3 Camera interface specification and replay path | `area:input`, `area:hardware`, `area:docs`, `priority:high` | 16h |
| T4 Avoidance core and safety tests | `area:avoidance`, `area:test`, `priority:high` | 20h |
| T5 PX4 output mock and micro XRCE-DDS study | `area:output`, `area:hardware`, `priority:high` | 18h |
| T6 Simulation scenario harness | `area:simulation`, `area:test`, `priority:medium` | 18h |
| T7 Observability and rosbag workflow | `area:docs`, `area:test`, `priority:medium` | 15h |
| T8 CI and contributor workflow | `area:test`, `area:setup`, `priority:medium` | 15h |
| T9 Integration rehearsal | `area:integration`, `area:simulation`, `priority:high` | 20h |

## Assignment Guidance

For 5 people, assign T0, T1, T2, T4, and T5 first. Then split T3, T6, T7, T8, and T9 after the first pull requests.

For 6 people, assign T7 immediately to the sixth person and keep T9 paired between bringup and one non-bringup owner.

Every issue includes specification fields that the owner must fill in during the work. This keeps task knowledge in GitHub instead of in private chats.
