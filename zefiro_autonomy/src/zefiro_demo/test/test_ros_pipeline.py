"""Exercise real DDS publishers, subscriptions, timer and watchdog recovery."""
import time

import pytest
import rclpy
from geometry_msgs.msg import TwistStamped
from rclpy.context import Context
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.parameter import Parameter
from std_msgs.msg import Float32, String

from zefiro_demo.avoidance_node import AvoidanceNode


@pytest.fixture
def pipeline():
    context = Context()
    rclpy.init(context=context)
    avoidance = AvoidanceNode(context=context)
    probe = Node('test_probe', context=context)
    executor = SingleThreadedExecutor(context=context)
    executor.add_node(avoidance)
    executor.add_node(probe)
    clearance = probe.create_publisher(Float32, '/zefiro/perception/front_clearance', 1)
    goal = probe.create_publisher(TwistStamped, '/zefiro/mission/goal_velocity', 1)
    received = {'velocity': [], 'state': []}
    probe.create_subscription(TwistStamped, '/zefiro/setpoint/velocity',
                              lambda msg: received['velocity'].append(msg), 10)
    probe.create_subscription(String, '/zefiro/safety/state',
                              lambda msg: received['state'].append(msg.data), 10)

    def expect(state, vx, distance=5.0, send_goal=True, frame='base_link',
               goal_vx=1.0, lateral=0.0):
        received['velocity'].clear()
        received['state'].clear()
        started = time.monotonic()
        deadline = started + 4.0
        while time.monotonic() < deadline:
            if distance is not None:
                clearance.publish(Float32(data=distance))
            if send_goal:
                msg = TwistStamped()
                msg.header.frame_id = frame
                msg.header.stamp = probe.get_clock().now().to_msg()
                msg.twist.linear.x = goal_vx
                msg.twist.linear.y = lateral
                goal.publish(msg)
            executor.spin_once(timeout_sec=0.01)
            if (time.monotonic() - started > 0.15
                    and len(received['state']) >= 3
                    and len(received['velocity']) >= 3):
                msg = received['velocity'][-1]
                if (all(s == state for s in received['state'][-3:])
                        and msg.twist.linear.x == pytest.approx(vx)):
                    assert msg.header.frame_id == 'base_link'
                    assert (msg.twist.linear.y, msg.twist.linear.z,
                            msg.twist.angular.x, msg.twist.angular.y,
                            msg.twist.angular.z) == (0.0,) * 5
                    return
        pytest.fail(f'Expected {state}/{vx}; last states: {received["state"][-5:]}')

    try:
        yield expect, avoidance
    finally:
        executor.shutdown()
        probe.destroy_node()
        avoidance.destroy_node()
        context.shutdown()


def test_pipeline_states_timeouts_and_recovery(pipeline):
    expect, _ = pipeline
    expect('SENSOR_TIMEOUT', 0.0, distance=None, send_goal=False)
    expect('GOAL_TIMEOUT', 0.0, send_goal=False)
    expect('CLEAR', 1.0)
    expect('SLOWDOWN', 0.5, distance=2.0)
    expect('STOP', 0.0, distance=0.7)
    expect('INVALID_INPUT', 0.0, distance=-1.0)
    expect('INVALID_INPUT', 0.0, distance=float('nan'))
    expect('INVALID_INPUT', 0.0, goal_vx=float('nan'))
    expect('INVALID_INPUT', 0.0, frame='map')
    expect('INVALID_INPUT', 0.0, lateral=0.1)
    expect('SLOWDOWN', 0.75, distance=2.0, goal_vx=100.0)
    expect('CLEAR', 1.0)
    expect('GOAL_TIMEOUT', 0.0, send_goal=False)
    expect('CLEAR', 1.0)
    expect('SENSOR_TIMEOUT', 0.0, distance=None)
    expect('CLEAR', 1.0)


def test_startup_parameters_cannot_silently_change(pipeline):
    _, node = pipeline
    result = node.set_parameters([
        Parameter('stop_distance_m', value=2.0)])[0]
    assert not result.successful
    assert node.config.stop_distance_m == 1.0


def test_watchdog_runs_when_simulated_clock_is_paused(pipeline):
    expect, node = pipeline
    node.set_parameters([Parameter('use_sim_time', value=True)])
    expect('CLEAR', 1.0)
    expect('GOAL_TIMEOUT', 0.0, send_goal=False)
    expect('CLEAR', 1.0)
    expect('SENSOR_TIMEOUT', 0.0, distance=None)
