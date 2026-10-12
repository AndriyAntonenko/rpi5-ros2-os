import rclpy
from rcl_interfaces.msg import ParameterDescriptor, SetParametersResult
from rclpy.node import Node
from std_msgs.msg import Int64
from std_srvs.srv import SetBool


class CounterPublisher(Node):
    def __init__(self):
        super().__init__("counter_publisher")

        self.declare_parameter(
            "period",
            1.0,
            ParameterDescriptor(description="Publish period in seconds (>0)"),
        )
        self.declare_parameter(
            "start_value",
            0,
            ParameterDescriptor(
                description="Counter starts from start_value + 1", read_only=True
            ),
        )
        self.declare_parameter(
            "start_running",
            True,
            ParameterDescriptor(description="Start counting immediatelly"),
        )

        period = self.get_parameter("period").value
        self.count = self.get_parameter("start_value").value
        self.running = self.get_parameter("start_running").value

        self.publisher = self.create_publisher(Int64, "counter", 10)
        self.timer = self.create_timer(period, self.tick)

        self.service = self.create_service(
            SetBool, "counter/set_running", self.on_set_running
        )
        self.add_on_set_parameters_callback(self.validate_params)
        self.add_post_set_parameters_callback(self.apply_params)

        self.get_logger().info("publishing on /counter every 1.0 s")

    def tick(self):
        if not self.running:
            return

        self.count += 1
        msg = Int64()
        msg.data = self.count
        self.publisher.publish(msg)
        self.get_logger().info(f"published {msg.data}")

    def on_set_running(self, request: SetBool.Request, response: SetBool.Response):
        self.running = request.data
        response.success = True
        response.message = (
            f"counter {'started' if self.running else 'stopped'} at {self.count}"
        )
        self.get_logger().info(response.message)
        return response

    def validate_params(self, params):
        for p in params:
            if p.name == "period" and p.value <= 0.0:
                return SetParametersResult(
                    successful=False, reason="period must be > 0"
                )
        return SetParametersResult(successful=True)

    def apply_params(self, params):
        for p in params:
            if p.name == "period":
                self.destroy_timer(self.timer)
                self.timer = self.create_timer(p.value, self.tick)
                self.get_logger().info(f"period changed to {p.value} s")


def main():
    rclpy.init()
    node = CounterPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
