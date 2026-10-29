from glob import glob
import os

from setuptools import find_packages, setup

package_name = 'turtle_controller'

setup(
    name=package_name,
    version='1.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Install the launch files so `ros2 launch` can find them
        (os.path.join('share', package_name, 'launch'), glob('launch/*launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Angelos',
    maintainer_email='a.plastropoulos.229@cranfield.ac.uk',
    description='Reference solution for a beginner ROS 2 workshop using turtlesim',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'velocity_publisher = turtle_controller.velocity_publisher:main',
            'pose_subscriber = turtle_controller.pose_subscriber:main',
            'turtle_status_service = turtle_controller.turtle_status_service:main',
            'turtle_status_client = turtle_controller.turtle_status_client:main',
            'go_to_point = turtle_controller.go_to_point:main',
        ],
    },
)
