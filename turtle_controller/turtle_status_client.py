#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class TurtleStatusClient(Node):
    """
    A simple ROS 2 service client that checks the turtle's status.
    
    This node demonstrates how to create a service client that sends
    requests to a service and handles responses.
    """
    
    def __init__(self):
        super().__init__('turtle_status_client')
        
        # Create a client for the turtle status service
        self.client = self.create_client(Trigger, '/check_turtle_status')
        
        # Wait for the service to be available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /check_turtle_status service...')
        
        self.get_logger().info('Connected to turtle status service!')
    
    def check_status(self):
        """
        Call the service to check turtle status.
        """
        # Create a service request (Trigger has no request fields)
        request = Trigger.Request()
        
        self.get_logger().info('Checking turtle status...')
        
        # Call the service asynchronously
        future = self.client.call_async(request)
        
        # Wait for the response
        rclpy.spin_until_future_complete(self, future)
        
        if future.result() is not None:
            response = future.result()
            
            # Display the result
            if response.success:
                self.get_logger().info(f'✓ {response.message}')
            else:
                self.get_logger().info(f'✗ {response.message}')
        else:
            self.get_logger().error('Service call failed!')


def main(args=None):
    rclpy.init(args=args)
    
    # Create the client and check status
    status_client = TurtleStatusClient()
    status_client.check_status()
    
    status_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
