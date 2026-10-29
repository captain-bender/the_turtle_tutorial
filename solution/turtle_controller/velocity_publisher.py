#!/usr/bin/env python3
"""Exercise 2 solution: publish velocity commands so the turtle drives in a circle."""

from geometry_msgs.msg import Twist
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class VelocityPublisher(Node):
    """
    Publish velocity commands that make the turtle move in a circle.

    Demonstrates the publisher pattern: a timer fires at a fixed rate and each
    time it fires the node sends a message on a topic. Turtlesim subscribes to
    that topic and moves the turtle.
    """

    def __init__(self):
        # Initialise the node with a name (shown by `ros2 node list`)
        super().__init__('velocity_publisher')

        # Create a publisher
        # - Topic: '/turtle1/cmd_vel' (turtlesim's velocity command topic)
        # - Message type: Twist (linear and angular velocity)
        # - 10: queue depth, i.e. how many outgoing messages to buffer
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # Call timer_callback every 0.5 seconds.
        # Turtlesim stops the turtle if it receives no command for 1 second,
        # so the period must stay below 1.0 for smooth motion.
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.get_logger().info('Velocity Publisher has started!')

    def timer_callback(self):
        """Build a Twist message and publish it (runs every 0.5 seconds)."""
        msg = Twist()

        # Linear velocity: forward/backward along the turtle's own x axis
        msg.linear.x = 2.0  # units per second

        # Angular velocity: rotation about the vertical (z) axis
        msg.angular.z = 1.0  # radians per second, positive = counter-clockwise

        # All other fields (linear.y, linear.z, angular.x, angular.y) stay 0.0

        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Publishing: linear.x={msg.linear.x}, angular.z={msg.angular.z}')


def main(args=None):
    # Initialise the ROS 2 Python client library
    rclpy.init(args=args)
    node = VelocityPublisher()
    try:
        # Process callbacks until the node is stopped with Ctrl+C
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass  # Ctrl+C is the normal way to stop a node, so no error message
    finally:
        node.destroy_node()
        # Ctrl+C may already have shut ROS down, so only shut down if needed
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
