FROM ros:jazzy-ros-base

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=jazzy
RUN apt-get update && apt-get install -y --no-install-recommends \
    git python3-colcon-common-extensions python3-pytest python3-rosdep \
    ros-jazzy-geometry-msgs ros-jazzy-launch-ros ros-jazzy-rclpy \
    ros-jazzy-rcl-interfaces ros-jazzy-std-msgs ros-jazzy-rosbag2 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace/autopilot
COPY zefiro_autonomy/src ./zefiro_autonomy/src
COPY scripts ./scripts
COPY docker/ros_entrypoint.sh /ros_entrypoint.sh
RUN chmod +x /ros_entrypoint.sh && bash scripts/build.sh
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
