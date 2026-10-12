import sys

import rclpy
from rclpy.node import Node
from rclpy.utilities import remove_ros_args
from std_srvs.srv import SetBool


def main():
    args = remove_ros_args(sys.argv)[1:]
    if len(args) != 1 or args[0] not in ("start", "stop"):
        print("usage: ros2 run counter_demo counter_control start|stop")
        return

    rclpy.init()
    node = Node("counter_control")

    client = node.create_client(SetBool, "counter/set_running")
    if not client.wait_for_service(timeout_sec=5.0):
        node.get_logger().error("service counter/set_running is not available")
    else:
        request = SetBool.Request()
        request.data = args[0] == "start"
        future = client.call_async(request)

        rclpy.spin_until_future_complete(node, future)
        result = future.result()
        node.get_logger().info(f"success={result.success}: {result.message}")

    node.destroy_node()
    rclpy.try_shutdown()
