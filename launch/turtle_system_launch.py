#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    Launch file to start the complete turtle control system.
    
    This will start:
    1. Turtlesim node
    2. Velocity publisher (makes turtle move)
    3. Pose subscriber (prints turtle position)
    4. Turtle status service (provides status checking service)
    """
    
    return LaunchDescription([
        # Start the turtlesim node
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen'
        ),
        
        # Start our velocity publisher
        Node(
            package='turtle_controller',
            executable='velocity_publisher',
            name='velocity_publisher',
            output='screen'
        ),
        
        # Start our pose subscriber
        Node(
            package='turtle_controller',
            executable='pose_subscriber',
            name='pose_subscriber',
            output='screen'
        ),
        
        # Start our turtle status service
        Node(
            package='turtle_controller',
            executable='turtle_status_service',
            name='turtle_status_service',
            output='screen'
        ),
    ])
