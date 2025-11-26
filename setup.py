from setuptools import setup
import os
from glob import glob

package_name = 'turtle_controller'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your_email@example.com',
    description='A beginner-friendly ROS 2 package demonstrating publishers, subscribers, services, and launch files using turtlesim',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'velocity_publisher = turtle_controller.velocity_publisher:main',
            'pose_subscriber = turtle_controller.pose_subscriber:main',
            'turtle_status_service = turtle_controller.turtle_status_service:main',
            'turtle_status_client = turtle_controller.turtle_status_client:main',
        ],
    },
)
