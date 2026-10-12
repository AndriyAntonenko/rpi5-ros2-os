from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    params_file = LaunchConfiguration("params_file")
    period = LaunchConfiguration("period")
    namespace = LaunchConfiguration("namespace")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "params_file",
                default_value=PathJoinSubstitution(
                    [FindPackageShare("counter_demo"), "config", "params.yaml"]
                ),
                description="YAML file with node parameters",
            ),
            DeclareLaunchArgument(
                "period",
                default_value="1.0",
                description="Publish period in seconds (overrides the YAML value)",
            ),
            DeclareLaunchArgument(
                "namespace",
                default_value="",
                description="Namespace for all nodes, e.g. robot1",
            ),
            Node(
                package="counter_demo",
                executable="counter_publisher",
                name="counter_publisher",
                namespace=namespace,
                parameters=[params_file, {"period": period}],
                output="screen",
                respawn=True,
                respawn_delay=2.0,
            ),
            Node(
                package="counter_demo",
                executable="counter_subscriber",
                name="counter_subscriber",
                namespace=namespace,
                output="screen",
            ),
        ]
    )
