SUMMARY = "ROS 2 counter publisher/subscriber with a start/stop service"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

# Source lives in the same repository: <repo>/ros2_ws/src/counter_demo
FILESEXTRAPATHS:prepend := "${THISDIR}/../../../../ros2_ws/src:"
SRC_URI = "file://counter_demo"
S = "${WORKDIR}/counter_demo"

ROS_CN = "counter_demo"
ROS_BPN = "counter_demo"

# Runtime dependencies (mirror <depend>/<exec_depend> from package.xml)
RDEPENDS:${PN} += " \
    rclpy \
    std-msgs \
    std-srvs \
    rcl-interfaces \
    launch \
    launch-ros \
"

inherit ros_distro_jazzy
ROS_BUILD_TYPE = "ament_python"
inherit ros_${ROS_BUILD_TYPE}
