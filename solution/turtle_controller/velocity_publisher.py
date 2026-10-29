#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityPublisher(Node):
    """
    A ROS 2 node that publishes velocity commands to make the turtle move in a circle.
    
    This node demonstrates the publisher pattern in ROS 2, where messages are
    continuously sent to a topic that other nodes (like turtlesim) can subscribe to.
    """
    
    def __init__(self):
        # Initialize the node with a name
        super().__init__('velocity_publisher')
        
        # Create a publisher
        # - Topic: '/turtle1/cmd_vel' (turtlesim's velocity command topic)
        # - Message type: Twist (contains linear and angular velocity)
        # - Queue size: 10 (number of messages to buffer)
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Create a timer that calls timer_callback every 0.5 seconds
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.get_logger().info('Velocity Publisher has started!')
    
    def timer_callback(self):
        """
        This function is called every 0.5 seconds by the timer.
        It creates and publishes a Twist message to move the turtle.
        """
        # Create a new Twist message
        msg = Twist()
        
        # Set linear velocity (forward/backward movement)
        msg.linear.x = 2.0  # Move forward at 2.0 units/sec
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        
        # Set angular velocity (rotation)
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 1.0  # Rotate counter-clockwise at 1.0 rad/sec
        
        # Publish the message
        self.publisher_.publish(msg)
        
        # Log the action
        self.get_logger().info(f'Publishing: linear.x={msg.linear.x}, angular.z={msg.angular.z}')


def main(args=None):
    # Initialize the ROS 2 Python client library
    rclpy.init(args=args)
    
    # Create an instance of our node
    velocity_publisher = VelocityPublisher()
    
    # Keep the node running and processing callbacks
    # This will run until you press Ctrl+C
    rclpy.spin(velocity_publisher)
    
    # Cleanup
    velocity_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
