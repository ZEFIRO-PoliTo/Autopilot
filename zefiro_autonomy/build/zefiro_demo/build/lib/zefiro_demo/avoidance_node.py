import rclpy
from geometry_msgs.msg import TwistStamped
from rclpy.node import Node
from std_msgs.msg import Float32, String


class AvoidanceNode(Node):
    def __init__(self):
        super().__init__('avoidance_node')

        self.declare_parameter('stop_distance_m', 1.0)
        self.declare_parameter('slowdown_distance_m', 3.0)
        self.declare_parameter('sensor_timeout_s', 0.5)
        self.declare_parameter('max_velocity_mps', 1.5)
        self.declare_parameter('control_rate_hz', 20.0)

        self.stop_distance_m = (
            self.get_parameter('stop_distance_m').get_parameter_value().double_value
        )
        self.slowdown_distance_m = (
            self.get_parameter('slowdown_distance_m').get_parameter_value().double_value
        )
        self.sensor_timeout_s = (
            self.get_parameter('sensor_timeout_s').get_parameter_value().double_value
        )
        self.max_velocity_mps = (
            self.get_parameter('max_velocity_mps').get_parameter_value().double_value
        )
        control_rate_hz = (
            self.get_parameter('control_rate_hz').get_parameter_value().double_value
        )

        self.latest_clearance_m = None
        self.latest_clearance_time = None
        self.goal_vx = 0.0

        self.create_subscription(
            Float32,
            '/zefiro/perception/front_clearance',
            self.on_clearance,
            10,
        )
        self.create_subscription(
            TwistStamped,
            '/zefiro/mission/goal_velocity',
            self.on_goal_velocity,
            10,
        )
        self.velocity_publisher = self.create_publisher(
            TwistStamped,
            '/zefiro/setpoint/velocity',
            10,
        )
        self.state_publisher = self.create_publisher(
            String,
            '/zefiro/safety/state',
            10,
        )

        self.timer = self.create_timer(1.0 / control_rate_hz, self.control_step)

    def on_clearance(self, msg):
        self.latest_clearance_m = msg.data
        self.latest_clearance_time = self.get_clock().now()

    def on_goal_velocity(self, msg):
        self.goal_vx = msg.twist.linear.x

    def control_step(self):
        cmd_vx, state = self.compute_command()
        cmd_vx = max(-self.max_velocity_mps, min(self.max_velocity_mps, cmd_vx))

        velocity_msg = TwistStamped()
        velocity_msg.header.stamp = self.get_clock().now().to_msg()
        velocity_msg.header.frame_id = 'base_link'
        velocity_msg.twist.linear.x = cmd_vx
        velocity_msg.twist.linear.y = 0.0
        velocity_msg.twist.linear.z = 0.0
        velocity_msg.twist.angular.x = 0.0
        velocity_msg.twist.angular.y = 0.0
        velocity_msg.twist.angular.z = 0.0
        self.velocity_publisher.publish(velocity_msg)

        state_msg = String()
        state_msg.data = state
        self.state_publisher.publish(state_msg)

    def compute_command(self):
        if self.latest_clearance_time is None:
            return 0.0, 'SENSOR_TIMEOUT'

        age_s = (self.get_clock().now() - self.latest_clearance_time).nanoseconds / 1e9
        clearance_m = self.latest_clearance_m

        if age_s > self.sensor_timeout_s:
            return 0.0, 'SENSOR_TIMEOUT'
        if clearance_m < 0.0:
            return 0.0, 'INVALID_INPUT'
        if clearance_m <= self.stop_distance_m:
            return 0.0, 'STOP'
        if clearance_m < self.slowdown_distance_m:
            scale = (
                (clearance_m - self.stop_distance_m)
                / (self.slowdown_distance_m - self.stop_distance_m)
            )
            return self.goal_vx * scale, 'SLOWDOWN'

        return self.goal_vx, 'CLEAR'


def main(args=None):
    rclpy.init(args=args)
    node = AvoidanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
