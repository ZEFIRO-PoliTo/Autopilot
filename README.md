# Autopilot

The current codebase contains a minimal ROS 2 Jazzy demo that proves the first safety boundary:

```text
fake input -> avoidance -> safe velocity -> logger
```

The next development block should extend this into separate input, avoidance, output, bringup, and test responsibilities.

## Repository Layout

```text
zefiro_autonomy/
  docs/
    architecture.md
    tasks_plan.md
  src/
    zefiro_demo/
```

## Quick Start With Docker

Build the development image:

```bash
docker compose build
```

Start a shell inside the ROS 2 Jazzy environment:

```bash
docker compose run --rm autonomy
```

Inside the container:

```bash
colcon build --symlink-install
source install/setup.bash
ros2 launch zefiro_demo demo_fake_avoidance.launch.py
```

## Quick Start Natively

Install ROS 2 Jazzy on Ubuntu 24.04 using [zefiro_autonomy/docs/INSTALL_ROS2_JAZZY.md](zefiro_autonomy/docs/INSTALL_ROS2_JAZZY.md).

Then from the repository root:

```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch zefiro_demo demo_fake_avoidance.launch.py
```

## Project Docs

- [Architecture](zefiro_autonomy/docs/architecture.md)
- [Development tasks](zefiro_autonomy/docs/tasks_plan.md)
- [ROS 2 Jazzy install guide](zefiro_autonomy/docs/INSTALL_ROS2_JAZZY.md)

The repository also includes a minimal GitHub Actions workflow in `.github/workflows/ci.yml`.
