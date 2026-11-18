# ROS 2 Jazzy development environment

Native setup: **Ubuntu 24.04, ROS 2 Jazzy, and system Python**. For other systems, see the Docker option in the [main README](../../README.md). Windows/macOS host integration has not been checked locally.

Follow the [official Jazzy Ubuntu installation guide](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html) for UTF-8 locale, Universe, `ros2-apt-source`, and ROS installation. `ros-jazzy-ros-base` is enough for this demo; the desktop variant is optional. APT setup changes over time, so use current official commands rather than old repository keys.

After installing ROS:

```bash
source /opt/ros/jazzy/setup.bash
sudo apt update
sudo apt install python3-colcon-common-extensions python3-rosdep python3-pytest ros-jazzy-rosbag2
```

Initialize rosdep once per machine:

```bash
sudo rosdep init
rosdep update --rosdistro jazzy
```

If `rosdep init` says `20-default.list` already exists, run update without deleting existing configuration.

From the `Autopilot/` root:

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths zefiro_autonomy/src --ignore-src --rosdistro jazzy -y
bash scripts/doctor.sh
bash scripts/check.sh
bash scripts/demo.sh
```

In every new inspection shell, run `source scripts/ros_env.sh` and `source install/local_setup.bash`. Build, test, and demo scripts set up their own environment.

Avoid `sudo pip` for pytest or ROS libraries. Deactivate conda/venv for these instructions. For a system-Python conflict observed on the audit machine, see [troubleshooting.md](troubleshooting.md).

Official references: [installation](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/Ubuntu-Install-Debs.rst), [colcon tutorial](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.rst).
