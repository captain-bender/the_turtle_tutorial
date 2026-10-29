#!/usr/bin/env python3
"""Exercise 3 solution: subscribe to the turtle's pose and print it."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from turtlesim.msg import Pose


class PoseSubscriber(Node):
    """
    Subscribe to the turtle's pose and log it.

    Demonstrates the subscriber pattern: the node registers a callback, and
    ROS calls it every time a message arrives on the topic.
    """

    def __init__(self):
        super().__init__('pose_subscriber')

        # Create a subscriber
        # - Topic: '/turtle1/pose' (turtlesim publishes the pose here)
        # - Message type: Pose (x, y, theta, linear_velocity, angular_velocity)
        # - Callback: pose_callback (called for every message received)
        # - 10: queue depth, i.e. how many incoming messages to buffer
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self.get_logger().info('Pose Subscriber has started!')

    def pose_callback(self, msg):
        """
        Log the pose received on /turtle1/pose.

        Turtlesim publishes the pose about 60 times per second, which would
        flood the terminal. throttle_duration_sec limits this log line to at
        most once per second; the callback itself still runs for every message.
        In the Pose message, x and y are in turtlesim units and theta is in radians.
        """
        self.get_logger().info(
            f'Turtle Pose - X: {msg.x:.2f}, Y: {msg.y:.2f}, Theta: {msg.theta:.2f}',
            throttle_duration_sec=1.0
        )


def main(args=None):
    rclpy.init(args=args)
    node = PoseSubscriber()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
