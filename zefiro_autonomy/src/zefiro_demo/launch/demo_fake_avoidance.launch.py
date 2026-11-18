from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    default_config = PathJoinSubstitution([
        FindPackageShare('zefiro_demo'), 'config', 'demo.yaml'])
    nodes = [
        Node(package='zefiro_demo', executable=name, name=name, output='screen',
             parameters=[LaunchConfiguration('config')] if name == 'avoidance_node' else [])
        for name in ('fake_front_clearance_node', 'fake_goal_velocity_node',
                     'avoidance_node', 'logger_node')
    ]
    return LaunchDescription([
        DeclareLaunchArgument('config', default_value=default_config,
                              description='YAML configuration for avoidance'),
        *nodes,
    ])
