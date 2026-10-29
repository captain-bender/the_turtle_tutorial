#!/usr/bin/env python3
"""
Example: Different Turtle Movement Patterns

This example shows how to create different movement patterns by modifying
the velocity commands. You can experiment with these values to learn
how linear and angular velocities combine to create different motions.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class MovementPatternExample(Node):
    def __init__(self):
        super().__init__('movement_pattern_example')
        
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Pattern selection: 'circle', 'square', 'forward', 'spin'
        self.pattern = 'circle'
        self.step = 0
        
        # Timer for pattern execution
        self.timer = self.create_timer(0.5, self.execute_pattern)
        
        self.get_logger().info(f'Starting pattern: {self.pattern}')
    
    def execute_pattern(self):
        msg = Twist()
        
        if self.pattern == 'circle':
            # Circular motion: constant forward + constant rotation
            msg.linear.x = 2.0
            msg.angular.z = 1.0
            
        elif self.pattern == 'square':
            # Square pattern: alternate between forward and turn
            if self.step < 4:  # Move forward
                msg.linear.x = 2.0
                msg.angular.z = 0.0
            else:  # Turn 90 degrees
                msg.linear.x = 0.0
                msg.angular.z = 1.57  # ~90 degrees
            
            self.step += 1
            if self.step >= 8:  # Complete one side
                self.step = 0
                
        elif self.pattern == 'forward':
            # Straight line
            msg.linear.x = 2.0
            msg.angular.z = 0.0
            
        elif self.pattern == 'spin':
            # Spin in place
            msg.linear.x = 0.0
            msg.angular.z = 2.0
        
        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Pattern: {self.pattern}, linear: {msg.linear.x:.2f}, angular: {msg.angular.z:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = MovementPatternExample()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
