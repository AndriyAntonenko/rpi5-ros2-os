import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64


class CounterSubscriber(Node):
    def __init__(self):
        super().__init__("counter_subscriber")
        self.subscription = self.create_subscription(Int64, "counter", self.on_msg, 10)
        self.get_logger().info("listening on /counter")

    def on_msg(self, msg: Int64):
        self.get_logger().info(f"received {msg.data}")


def main():
    rclpy.init()
    node = CounterSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
