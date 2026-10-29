#!/usr/bin/env python3
"""Exercise 6 solution: start turtlesim and the workshop nodes with one command."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    Describe the nodes to start.

    This launch file starts:
    1. turtlesim (the simulator window)
    2. velocity_publisher (makes the turtle drive in a circle)
    3. pose_subscriber (logs the turtle's position once per second)
    4. turtle_status_service (answers /check_turtle_status)

    The status client is left out on purpose: run it yourself from another
    terminal while the system is running.
    """
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen'
        ),
        Node(
            package='turtle_controller',
            executable='velocity_publisher',
            name='velocity_publisher',
            output='screen'
        ),
        Node(
            package='turtle_controller',
            executable='pose_subscriber',
            name='pose_subscriber',
            output='screen'
        ),
        Node(
            package='turtle_controller',
            executable='turtle_status_service',
            name='turtle_status_service',
            output='screen'
        ),
    ])
