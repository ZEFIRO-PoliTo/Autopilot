from glob import glob
from setuptools import find_packages, setup


package_name = 'zefiro_demo'


setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Zefiro Autonomy Team',
    maintainer_email='team@zefiro.local',
    description='Minimal ROS 2 demo for the Zefiro autonomy pipeline.',
    license='MIT',
    tests_require=['pytest'],
    test_suite='test.test_imports',
    entry_points={
        'console_scripts': [
            'avoidance_node = zefiro_demo.avoidance_node:main',
            'fake_front_clearance_node = zefiro_demo.fake_front_clearance_node:main',
            'fake_goal_velocity_node = zefiro_demo.fake_goal_velocity_node:main',
            'logger_node = zefiro_demo.logger_node:main',
        ],
    },
)
