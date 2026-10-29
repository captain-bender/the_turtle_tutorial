#!/usr/bin/env python3
"""Exercise 5 solution: call the turtle status service once and print the answer."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_srvs.srv import Trigger


class TurtleStatusClient(Node):
    """
    Call /check_turtle_status and log the response.

    Demonstrates the service client pattern: create a client, wait for the
    server to appear, send a request and wait for the response.
    """

    def __init__(self):
        super().__init__('turtle_status_client')

        # Create a client for the turtle status service
        self.client = self.create_client(Trigger, '/check_turtle_status')

    def check_status(self):
        """Wait for the server, send one request and log the response."""
        # Wait until the server is available, checking once per second
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /check_turtle_status service...')

        self.get_logger().info('Connected to turtle status service!')

        # Trigger requests have no fields, so the request is empty
        request = Trigger.Request()

        self.get_logger().info('Checking turtle status...')

        # Send the request without blocking; the future will hold the response
        future = self.client.call_async(request)

        # Process callbacks until the response arrives
        rclpy.spin_until_future_complete(self, future)

        response = future.result()
        if response is None:
            self.get_logger().error('Service call failed!')
        elif response.success:
            self.get_logger().info(f'✓ {response.message}')
        else:
            self.get_logger().info(f'✗ {response.message}')


def main(args=None):
    rclpy.init(args=args)
    node = TurtleStatusClient()
    try:
        # This node does one job and exits; no spin() loop needed
        node.check_status()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass  # Ctrl+C while waiting for the service or the response
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
