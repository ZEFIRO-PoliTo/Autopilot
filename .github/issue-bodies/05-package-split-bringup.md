## Goal

Move from one demo package to a package layout that lets 5-6 people work independently.

## Context

The current `zefiro_demo` package is useful for the first demo, but input, avoidance, output, logging, and bringup need separate ownership.

## Tasks

- [ ] Propose target package layout.
- [ ] Create `zefiro_bringup` for launch files.
- [ ] Split fake inputs, avoidance, logging, perception, and output mock where ready.
- [ ] Keep topic names stable during the migration.
- [ ] Decide whether custom messages are needed now or later.

## Expected Outputs

- Package split PR.
- Bringup launch files.
- Updated architecture docs.
- Package READMEs or concise package sections in the main docs.

## Milestones

- 0-4h: target package layout proposal.
- 4-12h: create bringup package and move launch files.
- 12-20h: split fake input/logging/avoidance packages.
- 20-28h: evaluate `zefiro_msgs`.
- 28-36h: docs and integration cleanup.

## Definition of Done

- [ ] Clean checkout builds with `colcon build`.
- [ ] Fake demo still runs through bringup.
- [ ] Package dependencies are explicit.
