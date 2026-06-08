## Target Effort

18 hours.

## Goal

Define repeatable scenarios for simulation before hardware enters the loop.

## Context

This task can use fake or synthetic data. It should not wait for full simulation tooling or hardware.

Reference: `zefiro_autonomy/docs/september_hardware_simulation_plan.md`, Task T6.

## Tasks

- [ ] List scenarios for clear path, slowdown, stop, invalid sensor data, timeout, and command saturation.
- [ ] Create launch or script hooks using fake or synthetic nodes.
- [ ] Document expected topic/state output for each scenario.
- [ ] Run at least two scenarios with another task owner.

## Specification Fields

- Scenario names:
- Nodes started:
- Expected topics:
- Expected safety states:
- Pass/fail criteria:

## Expected Outputs

- Scenario list.
- Runnable hooks for at least two scenarios.
- Expected output documentation.

## Milestones

- 0-4h: scenario list and expected states.
- 4-10h: launch/script hooks.
- 10-15h: pass/fail documentation.
- 15-18h: two-scenario validation with another owner.

## No Single Point Of Failure

Scenarios can use fake or synthetic data if full simulation is not ready. The harness defines expected behavior independent of the person who wrote the nodes.

## Definition Of Done

- [ ] At least four scenarios are documented.
- [ ] At least two scenarios are runnable.
- [ ] Expected outputs are clear enough for another teammate to validate.
