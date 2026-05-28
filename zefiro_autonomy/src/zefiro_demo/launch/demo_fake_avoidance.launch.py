from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='zefiro_demo',
            executable='fake_front_clearance_node',
            name='fake_front_clearance_node',
            output='screen',
        ),
        Node(
            package='zefiro_demo',
            executable='fake_goal_velocity_node',
            name='fake_goal_velocity_node',
            output='screen',
        ),
        Node(
            package='zefiro_demo',
            executable='avoidance_node',
            name='avoidance_node',
            output='screen',
        ),
        Node(
            package='zefiro_demo',
            executable='logger_node',
            name='logger_node',
            output='screen',
        ),
    ])
