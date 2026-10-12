require rpi5-base-image.bb
SUMMARY = "Custom Raspberry Pi 5 image with SSH and ROS 2 Jazzy"

IMAGE_INSTALL:append = " \
    ros-core \
    demo-nodes-cpp \
    demo-nodes-py \
    counter-demo \
"
