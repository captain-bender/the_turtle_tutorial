#!/usr/bin/env python3
"""Exercise 4 solution: a service that reports whether the turtle is near the centre."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_srvs.srv import Trigger
from turtlesim.msg import Pose


class TurtleStatusService(Node):
    """
    Answer requests on /check_turtle_status with the turtle's position.

    Demonstrates the service server pattern: a client sends a request, the
    server runs a callback once and sends back a single response. The node
    also subscribes to the pose so it always knows where the turtle is.
    """

    def __init__(self):
        super().__init__('turtle_status_service')

        # Latest pose received; None until the first message arrives
        self.current_pose = None

        # Subscribe to the turtle's pose so the service can use it
        self.pose_subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # Create a service
        # - Service name: '/check_turtle_status'
        # - Service type: Trigger (empty request; response has success + message)
        # - Callback: handle_status_request (runs once per request)
        self.srv = self.create_service(
            Trigger,
            '/check_turtle_status',
            self.handle_status_request
        )

        self.get_logger().info('Turtle Status Service is ready!')

    def pose_callback(self, msg):
        """Store the turtle's latest pose."""
        self.current_pose = msg

    def handle_status_request(self, request, response):
        """
        Report whether the turtle is within 1 unit of the window centre.

        A Trigger request has no fields. The response has 'success' (bool) and
        'message' (str); fill them in and return the response.
        """
        # No pose yet: turtlesim is not running or has not published
        if self.current_pose is None:
            response.success = False
            response.message = 'No pose received yet. Is turtlesim running?'
            self.get_logger().warn(response.message)
            return response

        # The turtle starts at the centre of the window, about (5.54, 5.54)
        center_x = 5.5
        center_y = 5.5

        x = self.current_pose.x
        y = self.current_pose.y

        # "Near" means within 1 unit of the centre along both x and y
        # (a square region around the centre)
        near_center = abs(x - center_x) < 1.0 and abs(y - center_y) < 1.0

        response.success = near_center
        if near_center:
            response.message = f'Turtle is near center! Position: ({x:.2f}, {y:.2f})'
        else:
            response.message = f'Turtle is far from center. Position: ({x:.2f}, {y:.2f})'

        self.get_logger().info(response.message)
        return response


def main(args=None):
    rclpy.init(args=args)
    node = TurtleStatusService()
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
