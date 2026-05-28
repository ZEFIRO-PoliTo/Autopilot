# Install ROS 2 Jazzy on Ubuntu 24.04

These commands are a short install path for Ubuntu 24.04. If they fail, follow the official ROS 2 Jazzy Ubuntu installation documentation:

https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html

## Update Apt and Enable Universe

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository universe
```

## Install Basic Tools

```bash
sudo apt update
sudo apt install curl gnupg lsb-release software-properties-common
```

## Add the ROS 2 Apt Source

The current ROS 2 Jazzy documentation uses the `ros2-apt-source` package to configure ROS 2 apt sources and keys.

```bash
sudo apt update
sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

## Install ROS 2

For this demo, `ros-jazzy-ros-base` is enough:

```bash
sudo apt update
sudo apt install ros-jazzy-ros-base
```

If you also want RViz and desktop demos:

```bash
sudo apt install ros-jazzy-desktop
```

## Install Colcon and Rosdep

```bash
sudo apt install python3-colcon-common-extensions python3-rosdep
```

If this is a fresh machine and `rosdep` has not been initialized:

```bash
sudo rosdep init
rosdep update
```

## Source ROS 2

```bash
source /opt/ros/jazzy/setup.bash
```

To source ROS 2 automatically in new bash shells:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
```
