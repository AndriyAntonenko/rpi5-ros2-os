FROM ros:jazzy

RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-jazzy-demo-nodes-cpp \
        ros-jazzy-demo-nodes-py \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ros2_ws

COPY src/counter_demo/package.xml src/counter_demo/package.xml
RUN apt-get update \
    && (rosdep init 2>/dev/null || true) \
    && rosdep update \
    && rosdep install --from-paths src --ignore-src -y \
    && rm -rf /var/lib/apt/lists/*

COPY src/ src/
RUN . /opt/ros/jazzy/setup.sh && colcon build

COPY --chmod=755 docker/entrypoint.sh /entrypoint.sh
RUN echo 'source /opt/ros/jazzy/setup.bash && source /ros2_ws/install/setup.bash' >> /root/.bashrc

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
