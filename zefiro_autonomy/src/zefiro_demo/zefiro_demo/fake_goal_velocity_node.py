import rclpy
from geometry_msgs.msg import TwistStamped
from rclpy.node import Node


class FakeGoalVelocityNode(Node):
    def __init__(self):
        super().__init__('fake_goal_velocity_node')
        self.publisher = self.create_publisher(
            TwistStamped,
            '/zefiro/mission/goal_velocity',
            10,
        )
        self.timer = self.create_timer(0.05, self.publish_goal_velocity)

    def publish_goal_velocity(self):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.twist.linear.x = 1.0
        msg.twist.linear.y = 0.0
        msg.twist.linear.z = 0.0
        msg.twist.angular.x = 0.0
        msg.twist.angular.y = 0.0
        msg.twist.angular.z = 0.0
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = FakeGoalVelocityNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
