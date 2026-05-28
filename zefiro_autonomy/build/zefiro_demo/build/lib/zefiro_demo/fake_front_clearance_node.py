import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class FakeFrontClearanceNode(Node):
    def __init__(self):
        super().__init__('fake_front_clearance_node')
        self.publisher = self.create_publisher(
            Float32,
            '/zefiro/perception/front_clearance',
            10,
        )
        self.start_time = self.get_clock().now()
        self.timer = self.create_timer(0.1, self.publish_clearance)

    def publish_clearance(self):
        elapsed_s = (self.get_clock().now() - self.start_time).nanoseconds / 1e9
        phase_s = elapsed_s % 24.0

        if phase_s < 8.0:
            clearance_m = 5.0
        elif phase_s < 14.0:
            clearance_m = 2.0
        elif phase_s < 20.0:
            clearance_m = 0.7
        else:
            clearance_m = -1.0

        msg = Float32()
        msg.data = clearance_m
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = FakeFrontClearanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
