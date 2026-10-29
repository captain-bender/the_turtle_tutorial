#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from std_srvs.srv import Trigger


class TurtleStatusService(Node):
    """
    A simple ROS 2 service that reports if the turtle is near the center.
    
    This is a straightforward service example:
    - No cascading service calls
    - Simple logic (just checking position)
    - Turtle-related (stays on theme)
    - Easy to understand and test
    """
    
    def __init__(self):
        super().__init__('turtle_status_service')
        
        # Store the turtle's current position
        self.current_pose = Pose()
        
        # Subscribe to turtle's pose
        self.pose_subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        
        # Create a service
        # - Service name: '/check_turtle_status'
        # - Service type: Trigger (no request data, returns success + message)
        # - Callback: handle_status_request
        self.srv = self.create_service(
            Trigger,
            '/check_turtle_status',
            self.handle_status_request
        )
        
        self.get_logger().info('Turtle Status Service is ready!')
        self.get_logger().info('Call this service to check if turtle is near center')
    
    def pose_callback(self, msg):
        """Store the turtle's current pose whenever it updates."""
        self.current_pose = msg
    
    def handle_status_request(self, request, response):
        """
        Check if the turtle is near the center of the window.
        
        Args:
            request: Empty (Trigger service has no request fields)
            response: Contains 'success' (bool) and 'message' (string)
        
        Returns:
            response: Service response with turtle status
        """
        # Center of turtlesim window is approximately (5.5, 5.5)
        center_x = 5.5
        center_y = 5.5
        
        # Calculate how far turtle is from center
        distance_x = abs(self.current_pose.x - center_x)
        distance_y = abs(self.current_pose.y - center_y)
        
        # Check if turtle is near center (within 1 unit)
        if distance_x < 1.0 and distance_y < 1.0:
            response.success = True
            response.message = f'Turtle is near center! Position: ({self.current_pose.x:.2f}, {self.current_pose.y:.2f})'
        else:
            response.success = False
            response.message = f'Turtle is far from center. Position: ({self.current_pose.x:.2f}, {self.current_pose.y:.2f})'
        
        # Log the response
        self.get_logger().info(response.message)
        
        return response


def main(args=None):
    rclpy.init(args=args)
    turtle_status = TurtleStatusService()
    rclpy.spin(turtle_status)
    turtle_status.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
