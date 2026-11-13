"""Decisione 1D della demo, indipendente da ROS e verificabile con pytest."""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class SafetyConfig:
    stop_distance_m: float = 1.0
    slowdown_distance_m: float = 3.0
    sensor_timeout_s: float = 0.5
    goal_timeout_s: float = 0.5
    max_velocity_mps: float = 1.5
    control_rate_hz: float = 20.0

    def __post_init__(self):
        if not all(isfinite(value) for value in vars(self).values()):
            raise ValueError('All safety parameters must be finite')
        if not 0.0 <= self.stop_distance_m < self.slowdown_distance_m:
            raise ValueError('Require 0 <= stop_distance_m < slowdown_distance_m')
        for name in ('sensor_timeout_s', 'goal_timeout_s', 'max_velocity_mps',
                     'control_rate_hz'):
            if getattr(self, name) <= 0.0:
                raise ValueError(f'{name} must be positive')


def stale(age_s, timeout_s):
    return age_s is None or not isfinite(age_s) or age_s < 0.0 or age_s > timeout_s


def compute_command(clearance_m, goal_vx, sensor_age_s, goal_age_s, config):
    """Return (forward velocity in m/s, state); ages use local monotonic time.

    This front-only demo accepts forward motion. Reverse motion requires another
    sensing contract and is rejected. Limit the goal BEFORE applying slowdown.
    """
    if stale(sensor_age_s, config.sensor_timeout_s):
        return 0.0, 'SENSOR_TIMEOUT'
    if clearance_m is None or not isfinite(clearance_m) or clearance_m < 0.0:
        return 0.0, 'INVALID_INPUT'
    if stale(goal_age_s, config.goal_timeout_s):
        return 0.0, 'GOAL_TIMEOUT'
    if goal_vx is None or not isfinite(goal_vx) or goal_vx < 0.0:
        return 0.0, 'INVALID_INPUT'
    if clearance_m <= config.stop_distance_m:
        return 0.0, 'STOP'
    limited_vx = min(goal_vx, config.max_velocity_mps)
    if clearance_m < config.slowdown_distance_m:
        scale = ((clearance_m - config.stop_distance_m)
                 / (config.slowdown_distance_m - config.stop_distance_m))
        return limited_vx * scale, 'SLOWDOWN'
    return limited_vx, 'CLEAR'
