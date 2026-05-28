import rclpy
from geometry_msgs.msg import TwistStamped
from rclpy.node import Node
from std_msgs.msg import Float32, String


class LoggerNode(Node):
    def __init__(self):
        super().__init__('logger_node')

        self.clearance_m = None
        self.goal_vx = None
        self.cmd_vx = None
        self.state = None

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
        self.create_subscription(
            TwistStamped,
            '/zefiro/setpoint/velocity',
            self.on_velocity_setpoint,
            10,
        )
        self.create_subscription(
            String,
            '/zefiro/safety/state',
            self.on_safety_state,
            10,
        )

        self.timer = self.create_timer(1.0, self.log_status)

    def on_clearance(self, msg):
        self.clearance_m = msg.data

    def on_goal_velocity(self, msg):
        self.goal_vx = msg.twist.linear.x

    def on_velocity_setpoint(self, msg):
        self.cmd_vx = msg.twist.linear.x

    def on_safety_state(self, msg):
        self.state = msg.data

    def log_status(self):
        state = self.state if self.state is not None else 'n/a'
        clearance = self.format_clearance()
        goal_vx = self.format_number(self.goal_vx)
        cmd_vx = self.format_number(self.cmd_vx)

        self.get_logger().info(
            f'{state:<13} | clearance={clearance} | '
            f'goal_vx={goal_vx} | cmd_vx={cmd_vx}'
        )

    def format_clearance(self):
        if self.clearance_m is None:
            return 'n/a'
        return f'{self.clearance_m:.2f} m'

    @staticmethod
    def format_number(value):
        if value is None:
            return 'n/a'
        return f'{value:.2f}'


def main(args=None):
    rclpy.init(args=args)
    node = LoggerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
