#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose


class PoseSubscriber(Node):
    """
    A ROS 2 node that subscribes to the turtle's pose and prints it.
    
    This node demonstrates the subscriber pattern in ROS 2, where a node
    listens to messages published on a topic and processes them in a callback.
    """
    
    def __init__(self):
        # Initialize the node
        super().__init__('pose_subscriber')
        
        # Create a subscriber
        # - Topic: '/turtle1/pose' (turtlesim publishes pose here)
        # - Message type: Pose (contains x, y, theta, linear_velocity, angular_velocity)
        # - Callback function: pose_callback (called when a message is received)
        # - Queue size: 10
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        
        self.get_logger().info('Pose Subscriber has started!')
    
    def pose_callback(self, msg):
        """
        This function is called automatically whenever a message is received on /turtle1/pose.
        
        Args:
            msg (Pose): The received pose message containing x, y, theta, and velocities
        """
        # Log the turtle's position and orientation
        self.get_logger().info(
            f'Turtle Pose - X: {msg.x:.2f}, Y: {msg.y:.2f}, Theta: {msg.theta:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    pose_subscriber = PoseSubscriber()
    
    # Keep the node running and processing incoming messages
    rclpy.spin(pose_subscriber)
    
    pose_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
