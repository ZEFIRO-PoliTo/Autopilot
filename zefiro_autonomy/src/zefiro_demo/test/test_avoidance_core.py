import math

import pytest

from zefiro_demo.avoidance_core import SafetyConfig, compute_command


@pytest.mark.parametrize('clearance,goal,velocity,state', [
    (5.0, 1.0, 1.0, 'CLEAR'),
    (3.0, 1.0, 1.0, 'CLEAR'),
    (2.0, 1.0, 0.5, 'SLOWDOWN'),
    (1.0, 1.0, 0.0, 'STOP'),
    (0.7, 1.0, 0.0, 'STOP'),
    (0.0, 1.0, 0.0, 'STOP'),
    (-1.0, 1.0, 0.0, 'INVALID_INPUT'),
    (math.nan, 1.0, 0.0, 'INVALID_INPUT'),
    (math.inf, 1.0, 0.0, 'INVALID_INPUT'),
    (-math.inf, 1.0, 0.0, 'INVALID_INPUT'),
    (None, 1.0, 0.0, 'INVALID_INPUT'),
    (5.0, math.nan, 0.0, 'INVALID_INPUT'),
    (5.0, math.inf, 0.0, 'INVALID_INPUT'),
    (5.0, -math.inf, 0.0, 'INVALID_INPUT'),
    (5.0, None, 0.0, 'INVALID_INPUT'),
    (5.0, -1.0, 0.0, 'INVALID_INPUT'),
    (5.0, 0.0, 0.0, 'CLEAR'),
    (5.0, 100.0, 1.5, 'CLEAR'),
    (2.0, 100.0, 0.75, 'SLOWDOWN'),
])
def test_decisions(clearance, goal, velocity, state):
    actual_velocity, actual_state = compute_command(
        clearance, goal, 0.1, 0.1, SafetyConfig())
    assert actual_velocity == pytest.approx(velocity)
    assert actual_state == state


@pytest.mark.parametrize('age', [None, 0.5001, -0.1, math.inf, math.nan])
@pytest.mark.parametrize('source,state', [('sensor', 'SENSOR_TIMEOUT'),
                                          ('goal', 'GOAL_TIMEOUT')])
def test_missing_or_stale_input_stops(age, source, state):
    sensor_age, goal_age = (age, 0.0) if source == 'sensor' else (0.0, age)
    assert compute_command(5.0, 1.0, sensor_age, goal_age, SafetyConfig()) == (0.0, state)


def test_timeout_boundary_and_precedence():
    cfg = SafetyConfig()
    assert compute_command(5.0, 1.0, 0.5, 0.5, cfg) == (1.0, 'CLEAR')
    assert compute_command(5.0, 1.0, None, None, cfg) == (0.0, 'SENSOR_TIMEOUT')
    assert compute_command(-1.0, 1.0, 0.0, None, cfg) == (0.0, 'INVALID_INPUT')


@pytest.mark.parametrize('changes', [
    {'stop_distance_m': -1.0}, {'slowdown_distance_m': 1.0},
    {'slowdown_distance_m': 0.5}, {'control_rate_hz': 0.0},
    {'control_rate_hz': -1.0}, {'sensor_timeout_s': 0.0},
    {'goal_timeout_s': -1.0}, {'max_velocity_mps': 0.0},
    {'max_velocity_mps': math.inf}, {'stop_distance_m': math.nan},
])
def test_invalid_configuration_is_rejected(changes):
    with pytest.raises(ValueError):
        SafetyConfig(**changes)


def test_output_is_finite_bounded_and_monotonic_with_clearance():
    cfg = SafetyConfig()
    for goal in (0.0, 0.2, 1.0, 1000.0):
        previous = 0.0
        for i in range(101):
            velocity, _ = compute_command(i / 20.0, goal, 0.0, 0.0, cfg)
            assert math.isfinite(velocity)
            assert previous <= velocity <= min(goal, cfg.max_velocity_mps)
            previous = velocity
