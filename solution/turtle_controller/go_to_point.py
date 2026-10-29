#!/usr/bin/env python3
"""
Exercise 7 solution: drive the turtle to a point at a given distance and heading.

Run it with turtlesim already running, for example:

    ros2 run turtle_controller go_to_point --ros-args -p distance:=3.0 -p heading:=45.0

The heading is measured in the turtlesim world: 0 degrees points right (+x),
90 degrees points up (+y). Always type a decimal point (3.0, not 3), because
the parameters are declared as floating-point numbers.
"""

import math

from geometry_msgs.msg import Twist
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from turtlesim.msg import Pose

# Controller settings
K_LINEAR = 1.5            # forward speed per unit of remaining distance
K_ANGULAR = 4.0           # turning speed per radian of heading error
MAX_LINEAR = 2.0          # units per second
MAX_ANGULAR = 2.0         # radians per second
DISTANCE_TOLERANCE = 0.05  # "arrived" when this close to the target
ANGLE_TOLERANCE = 0.1     # radians (about 6 degrees): turn first if worse than this

# Turtlesim's world runs from 0 to about 11.09 in x and y
WORLD_MIN = 0.0
WORLD_MAX = 11.0


def normalize_angle(angle):
    """Wrap an angle in radians into the range -pi to pi."""
    return math.atan2(math.sin(angle), math.cos(angle))


def clamp(value, limit):
    """Limit value to the range -limit to +limit."""
    return max(-limit, min(limit, value))


class GoToPoint(Node):
    """
    Drive the turtle from where it is now to a point set by distance and heading.

    Combines a subscriber (pose feedback) and a publisher (velocity commands)
    in one node to make a closed-loop controller: every control step compares
    where the turtle is with where it should be, and corrects the command.
    """

    def __init__(self):
        super().__init__('go_to_point')

        # Parameters can be set from the command line with --ros-args -p name:=value
        self.declare_parameter('distance', 2.0)   # turtlesim units
        self.declare_parameter('heading', 90.0)   # degrees in the world frame
        self.distance = self.get_parameter('distance').value
        self.heading = math.radians(self.get_parameter('heading').value)

        self.pose = None     # latest pose from turtlesim
        self.target = None   # (x, y) goal, worked out from the first pose
        self.done = False    # set to True when the turtle arrives (or cannot)

        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10)

        # Run the controller 10 times per second
        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info(
            f'Go To Point started: distance={self.distance:.2f}, '
            f'heading={math.degrees(self.heading):.1f} deg')

    def pose_callback(self, msg):
        """Store the turtle's latest pose."""
        self.pose = msg

    def set_target(self):
        """Work out the goal point from the current pose; return False if it is off the map."""
        target_x = self.pose.x + self.distance * math.cos(self.heading)
        target_y = self.pose.y + self.distance * math.sin(self.heading)

        if not (WORLD_MIN < target_x < WORLD_MAX and WORLD_MIN < target_y < WORLD_MAX):
            self.get_logger().error(
                f'Target ({target_x:.2f}, {target_y:.2f}) is outside the turtlesim '
                'window. Try a shorter distance or a different heading.')
            return False

        self.target = (target_x, target_y)
        self.get_logger().info(
            f'Start ({self.pose.x:.2f}, {self.pose.y:.2f}) -> '
            f'target ({target_x:.2f}, {target_y:.2f})')
        return True

    def compute_command(self):
        """
        Return (linear, angular, arrived) for the current pose and target.

        Turn on the spot until roughly facing the target, then drive forward
        while making small steering corrections. Both speeds are proportional
        to the error, so the turtle slows down as it gets close.
        """
        dx = self.target[0] - self.pose.x
        dy = self.target[1] - self.pose.y
        distance_error = math.hypot(dx, dy)

        if distance_error < DISTANCE_TOLERANCE:
            return 0.0, 0.0, True

        # Direction to the target, compared with the way the turtle is facing
        angle_to_target = math.atan2(dy, dx)
        angle_error = normalize_angle(angle_to_target - self.pose.theta)

        angular = clamp(K_ANGULAR * angle_error, MAX_ANGULAR)
        if abs(angle_error) > ANGLE_TOLERANCE:
            linear = 0.0  # facing the wrong way: turn first
        else:
            linear = clamp(K_LINEAR * distance_error, MAX_LINEAR)

        return linear, angular, False

    def control_loop(self):
        """Run one control step (10 times per second)."""
        if self.done or self.pose is None:
            return  # finished, or no pose received yet

        if self.target is None and not self.set_target():
            self.done = True
            return

        linear, angular, arrived = self.compute_command()

        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.publisher_.publish(msg)

        if arrived:
            self.get_logger().info(
                f'Arrived at ({self.pose.x:.2f}, {self.pose.y:.2f})')
            self.done = True


def main(args=None):
    rclpy.init(args=args)
    node = GoToPoint()
    try:
        # Spin one callback at a time until the controller says it is done
        while rclpy.ok() and not node.done:
            rclpy.spin_once(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
