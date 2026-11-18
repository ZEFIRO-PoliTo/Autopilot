# First work cycle for five contributors

Assign names to P1–P5 together. These are responsibilities, not skill levels. Everyone first completes the [exercise](getting_started.md). The baseline already has a build, tests, four nodes, YAML configuration, and input watchdogs. Start with small extensions; the current package can remain intact while interfaces are tested.

Paths below are relative to `zefiro_autonomy/src/zefiro_demo/`.

| Role | Responsibility | First PR and check | Reviewer |
| --- | --- | --- | --- |
| P1 | Mission input (`fake_goal_velocity_node.py`) | Add a `goal_vx_mps` start-up parameter, default 1.0. Verify that 0.4 publishes 0.4; reject negative, NaN, and infinity. | P3 |
| P2 | Synthetic perception (`fake_front_clearance_node.py`) | Add a configurable constant-distance mode. Keep the current cycle as the default; 2.0 m must cause slowdown. | P1 |
| P3 | Decision and robustness (`avoidance_core.py`) | Test a non-default configuration: stop 1.5, slowdown 3.0, distance 2.0, goal 1.0 → 1/3 m/s. Document state priority. | P4 |
| P4 | Mock output receiver (new `output_mock_node.py`) | Read only `/zefiro/setpoint/velocity`; report a received, missing, or stale command, including loss of the publisher. Do not send to PX4. | P2 |
| P5 | Integration (`launch/`, `config/`, `scripts/`) | Add an exercise launch that can disable each input. Keep the standard launch working and document a timeout test without source edits. | P1 and affected owner |

A first PR should cover one behavior, a relevant test, and a short usage example. Each author updates the documentation for their own change.

## Shared contracts

- Keep topic names and types in [architecture.md](architecture.md).
- Velocity is m/s, distance is metres, frame is `base_link`, and only forward x is accepted.
- Negative/non-finite distance is invalid. Missing sensor or mission input produces `SENSOR_TIMEOUT` or `GOAL_TIMEOUT`.
- The mock consumes the filtered output, not the requested goal as a command.
- Validate parameters before creating timers; stop nodes cleanly; add meaningful tests.
- P5 coordinates changes to shared setup and launch files to avoid conflicting PRs.

## Suggested sequence

1. Run the exercise together; everyone reproduces the demo and inspects a topic.
2. Read the code, choose P1–P5, open a branch, and write the expected input/output for the first PR.
3. Review each other's work and fix issues.
4. Integrate one PR at a time; run the checks after each merge.
5. Show the group demo, record limits, and choose the next cycle.

Rotate roles next cycle. Someone who finishes early can help reproduce or review another PR.

## Second activity by area

- **P1:** test zero goal, publisher interruption, and recovery.
- **P2:** configure a distance sequence and a publication pause; keep camera-free tests.
- **P3:** propose hysteresis near thresholds, with a clear expected input/output; review any change to stopping behavior with the group.
- **P4:** draft a PX4 interface contract covering frames, timestamps, rates, and receiver watchdog; no unvalidated arm/disarm implementation.
- **P5:** build a scenario matrix and record/replay walkthrough using [observability.md](observability.md).

## First integration checklist

- [ ] All five environments have a recorded OS, native/Docker path, and check result.
- [ ] `bash scripts/check.sh` and `python3 scripts/smoke_demo.py` pass.
- [ ] Distance 5 / 2 / 0.7 / -1 produces CLEAR / SLOWDOWN / STOP / INVALID_INPUT.
- [ ] Stopping the sensor and goal stops output; resuming restores behavior.
- [ ] The mock receives setpoints and detects lost avoidance output.
- [ ] Another contributor reproduces the change using only documented commands.
- [ ] No generated data, credential, or bag is committed.
- [ ] Limitations appear in the PR.

## Later backlog

The previous T0–T9 plan covered setup, packages, synthetic and camera perception, avoidance, PX4 output, scenarios, observability, CI, and integration. Setup, CI, and part of avoidance/scenarios are prepared; packages, camera, output, and integration remain future work.

The earlier camera candidate was **Orbbec Gemini 336L**. Before implementing it, confirm the actual device, driver version, topics, encoding, units, frames, and calibration. Old range/default assumptions are not measurements. PX4/SITL follows a reproducible synthetic pipeline and a mock receiver with a watchdog. Frame, failsafe, and hardware limits require separate testing. This demo is not a flight controller.
