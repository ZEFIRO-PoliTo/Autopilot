# Repository audit and onboarding preparation

Local audit performed on 12–13 November 2026. Repository: `ZEFIRO-PoliTo/Autopilot`; initial `main` baseline `f86a6bb`. Onboarding work was prepared on `chore/ros-team-onboarding`. The neighboring `zefiro/autopilot` directory and PX4 firmware checkout are separate projects. At the time of that audit, remote synchronization and GitHub settings were not verified.

## Findings and changes

| Priority | Baseline finding | Change |
| --- | --- | --- |
| High | Generated build/install/log copies were tracked | Removed generated files from Git; kept one root workspace and added a CI guard. |
| High | Tests covered only imports | Added decision tests, ROS publisher/subscriber tests, and a launch smoke check. |
| High | Invalid or non-finite inputs could pass through | Added explicit validation and `INVALID_INPUT` stop behavior. |
| High | The last goal could remain valid forever | Added a goal watchdog, `GOAL_TIMEOUT`, and recovery tests. |
| High | A large goal could override slowdown | Bound speed before applying the slowdown factor. |
| Medium | Bad parameters and a zero denominator were possible | Validated parameters at start-up and installed YAML with the package. |
| Medium | ROS time could hide stale inputs | Used local monotonic arrival time and a steady control timer. |
| Medium | Other axes and goal frame were ignored | Documented a forward-only contract and reject mismatches. |
| Medium | Docker mixed source and generated files | Separated build volumes and made startup explicit. |
| Medium | No common path for beginners | Added a guided exercise and five small contribution areas. |

## Validation at audit time

On Ubuntu 24.04, Python 3.12, ROS 2 Jazzy: workspace build passed; `colcon` ran 45 tests with zero failures/errors/skips; a clean source-only copy passed `doctor.sh`, `check.sh`, and the launch smoke covering all four states and clean shutdown. Syntax and local Markdown links passed. Docker and GitHub Actions were not executed locally during that audit. A global pytest conflict required system APT Python to take precedence; see [troubleshooting.md](troubleshooting.md). A setuptools `pytest-repeat` warning did not skip tests.

The demo remains one-dimensional, with no camera, PX4, physical simulator, dynamic braking, or external output watchdog. Fresh installation of APT dependencies was not repeated, as Jazzy was already present. No hardware test or flight certification is implied by the demo tests. Camera and PX4 contracts still require validation against actual devices and versions.

At audit time, no push, issue, PR, or branch protection change had been made. Names for P1–P5 were not supplied. This record describes the historical audit; check Git for current branch status.
