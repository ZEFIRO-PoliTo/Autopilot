"""ROS I/O for the laptop-only forward-velocity demo."""
from math import isfinite
from time import monotonic

import rclpy
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import TwistStamped
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.clock import Clock, ClockType
from rclpy.node import Node
from std_msgs.msg import Float32, String

from zefiro_demo.avoidance_core import SafetyConfig, compute_command


class AvoidanceNode(Node):
    def __init__(self, **kwargs):
        super().__init__('avoidance_node', **kwargs)
        # Parameters are startup-only: ros2 param set must not silently do nothing.
        defaults = SafetyConfig()
        values = {}
        for name, default in vars(defaults).items():
            values[name] = self.declare_parameter(
                name, default, ParameterDescriptor(read_only=True)
            ).value
        self.config = SafetyConfig(**values)
        self.latest_clearance_m = None
        self.latest_clearance_time = None
        self.goal_vx = None
        self.latest_goal_time = None
        self.create_subscription(
            Float32, '/zefiro/perception/front_clearance', self.on_clearance, 1)
        self.create_subscription(
            TwistStamped, '/zefiro/mission/goal_velocity', self.on_goal_velocity, 1)
        self.velocity_publisher = self.create_publisher(
            TwistStamped, '/zefiro/setpoint/velocity', 1)
        self.state_publisher = self.create_publisher(
            String, '/zefiro/safety/state', 1)
        # Watchdogs continue even if simulated ROS time is paused.
        self.steady_clock = Clock(clock_type=ClockType.STEADY_TIME)
        self.timer = self.create_timer(
            1.0 / self.config.control_rate_hz, self.control_step,
            clock=self.steady_clock)

    def on_clearance(self, msg):
        self.latest_clearance_m = msg.data
        self.latest_clearance_time = monotonic()

    def on_goal_velocity(self, msg):
        twist = msg.twist
        components = (twist.linear.x, twist.linear.y, twist.linear.z,
                      twist.angular.x, twist.angular.y, twist.angular.z)
        valid = (msg.header.frame_id == 'base_link'
                 and all(isfinite(value) for value in components)
                 and all(value == 0.0 for value in components[1:]))
        self.goal_vx = twist.linear.x if valid else float('nan')
        self.latest_goal_time = monotonic()

    def compute_command(self):
        now = monotonic()
        sensor_age = (None if self.latest_clearance_time is None
                      else now - self.latest_clearance_time)
        goal_age = (None if self.latest_goal_time is None
                    else now - self.latest_goal_time)
        return compute_command(self.latest_clearance_m, self.goal_vx,
                               sensor_age, goal_age, self.config)

    def control_step(self):
        cmd_vx, state = self.compute_command()
        velocity_msg = TwistStamped()
        velocity_msg.header.stamp = self.get_clock().now().to_msg()
        velocity_msg.header.frame_id = 'base_link'
        velocity_msg.twist.linear.x = cmd_vx
        self.velocity_publisher.publish(velocity_msg)
        self.state_publisher.publish(String(data=state))


def main(args=None):
    rclpy.init(args=args)
    node = AvoidanceNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
