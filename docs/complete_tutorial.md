# ROS 2 Humble Beginner Tutorial with Turtlesim

## Table of Contents
1. [Creating a Workspace](#1-creating-a-workspace)
2. [Creating a Package](#2-creating-a-package)
3. [Building and Installing the Package](#3-building-and-installing-the-package)
4. [Creating a Topic Publisher](#4-creating-a-topic-publisher)
5. [Creating a Topic Subscriber](#5-creating-a-topic-subscriber)
6. [Creating a Service Server](#6-creating-a-service-server)
7. [Creating a Service Client](#7-creating-a-service-client)
8. [Testing Everything Together](#8-testing-everything-together)

---

## 1. Creating a Workspace

A **workspace** is a directory where you organize and build your ROS 2 packages.

### Step 1.1: Create the workspace directory structure

```bash
# Create the workspace root directory
mkdir -p ~/turtle_ws/src

# Navigate to the workspace
cd ~/turtle_ws
```

**Explanation:**
- `~/turtle_ws` is your workspace root directory
- `src` is where all your ROS 2 packages will live
- The `-p` flag creates parent directories if they don't exist

---

## 2. Creating a Package

A **package** is the basic unit of organization in ROS 2. It contains your code, configuration files, and dependencies.

### Step 2.1: Navigate to the src directory

```bash
cd ~/turtle_ws/src
```

### Step 2.2: Create a new Python package

```bash
ros2 pkg create --build-type ament_python turtle_controller \
  --dependencies rclpy geometry_msgs turtlesim
```

**Explanation:**
- `ros2 pkg create`: Command to create a new package
- `--build-type ament_python`: Specifies we're creating a Python package
- `turtle_controller`: The name of our package
- `--dependencies`: Lists the packages our package depends on
  - `rclpy`: ROS 2 Python client library
  - `geometry_msgs`: Contains message types like Twist (for velocity commands)
  - `turtlesim`: The turtle simulator package

### Step 2.3: Understand the package structure

After creation, your package structure looks like this:

```
turtle_controller/
├── package.xml          # Package metadata and dependencies
├── setup.py            # Python package setup file
├── setup.cfg           # Configuration for Python package
├── resource/           # Resource files
├── test/              # Test files
└── turtle_controller/ # Python module directory (where your code goes)
    └── __init__.py
```

---

## 3. Building and Installing the Package

### Step 3.1: Navigate to workspace root

```bash
cd ~/turtle_ws
```

### Step 3.2: Build the package

```bash
colcon build
```

**Explanation:**
- `colcon`: The build tool for ROS 2
- This command compiles your code and sets up installation files

You should see output like:
```
Starting >>> turtle_controller
Finished <<< turtle_controller [0.50s]

Summary: 1 package finished [0.70s]
```

### Step 3.3: Source the workspace

```bash
source install/setup.bash
```

**Important:** You need to source this file in **every new terminal** where you want to use your package, or add it to your `~/.bashrc`:

```bash
echo "source ~/turtle_ws/install/setup.bash" >> ~/.bashrc
```

---

## 4. Creating a Topic Publisher

A **publisher** sends messages to a topic. We'll create a node that publishes velocity commands to move the turtle.

### Step 4.1: Create the publisher script

```bash
cd ~/turtle_ws/src/turtle_controller/turtle_controller
```
Create velocity_publisher.py file using VS Code

### Step 4.2: Write the publisher code

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityPublisher(Node):
    """
    A ROS 2 node that publishes velocity commands to make the turtle move in a circle.
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
```

### Step 4.3: Make the script executable

```bash
chmod +x velocity_publisher.py
```

### Step 4.4: Update setup.py

Edit the setup.py file to register our new node:

```bash
cd ~/turtle_ws/src/turtle_controller
```
Edit setup.py file using VS Code

Find the `entry_points` section and modify it:

```python
entry_points={
    'console_scripts': [
        'velocity_publisher = turtle_controller.velocity_publisher:main',
    ],
},
```

**Explanation:**
- This registers `velocity_publisher` as a command you can run with `ros2 run`
- Format: `'command_name = package_name.script_name:function_name'`

### Step 4.5: Build and test

```bash
cd ~/turtle_ws
colcon build
source install/setup.bash
```

**Test the publisher:**

Terminal 1 - Start turtlesim:
```bash
ros2 run turtlesim turtlesim_node
```

Terminal 2 - Run your publisher:
```bash
ros2 run turtle_controller velocity_publisher
```

You should see the turtle moving in a circle!

---

## 5. Creating a Topic Subscriber

A **subscriber** receives messages from a topic. We'll create a node that listens to the turtle's pose (position and orientation).

### Step 5.1: Create the subscriber script

```bash
cd ~/turtle_ws/src/turtle_controller/turtle_controller
```
Create pose_subscriber.py file using VS Code

### Step 5.2: Write the subscriber code

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose


class PoseSubscriber(Node):
    """
    A ROS 2 node that subscribes to the turtle's pose and prints it.
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
            msg (Pose): The received pose message
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
```

### Step 5.3: Make executable and update setup.py

```bash
chmod +x pose_subscriber.py
cd ~/turtle_ws/src/turtle_controller
```
Edit setup.py file using VS Code

Update entry_points:

```python
entry_points={
    'console_scripts': [
        'velocity_publisher = turtle_controller.velocity_publisher:main',
        'pose_subscriber = turtle_controller.pose_subscriber:main',
    ],
},
```

### Step 5.4: Build and test

```bash
cd ~/turtle_ws
colcon build
source install/setup.bash
```

**Test the subscriber:**

Terminal 1 - Turtlesim:
```bash
ros2 run turtlesim turtlesim_node
```

Terminal 2 - Your subscriber:
```bash
ros2 run turtle_controller pose_subscriber
```

Terminal 3 - Control the turtle manually:
```bash
ros2 run turtlesim turtle_teleop_key
```

Use arrow keys to move the turtle and watch the subscriber print the pose!

---

## 6. Creating a Service Server

### Goal
Create a service that checks if the turtle is near the center of the window.

### Background Information

**Key Concepts:**
- A **service** provides request-response communication (different from continuous topics)
- Services are used when you need to ask for something and wait for an answer
- The turtle status service will check the turtle's position and report if it's near the center
- We use the `Trigger` service type which is simple: no request data, returns success + message

**Why this example?**
- Simple logic: just checking X and Y coordinates
- No cascading: doesn't call other services
- Visual: you can see where the turtle actually is
- Practical: status checking is common in robotics

### Tasks

**Task 6.1:** Create the service server script

```bash
cd ~/turtle_ws/src/turtle_controller/turtle_controller
```

Create turtle_status_service.py using VS Code.

**Task 6.2:** Write the complete service code

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from std_srvs.srv import Trigger


class TurtleStatusService(Node):
    """
    A simple ROS 2 service that reports if the turtle is near the center.
    
    This demonstrates the service pattern without cascading service calls.
    """
    
    def __init__(self):
        super().__init__('turtle_status_service')
        
        # Store the turtle's current position
        self.current_pose = Pose()
        
        # Subscribe to turtle's pose to track position
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
```

**Task 6.3:** Make executable and update setup.py

```bash
chmod +x turtle_status_service.py
cd ~/turtle_ws/src/turtle_controller
```
Edit the setup.py file using VS Code.

Update entry_points:

```python
entry_points={
    'console_scripts': [
        'velocity_publisher = turtle_controller.velocity_publisher:main',
        'pose_subscriber = turtle_controller.pose_subscriber:main',
        'turtle_status_service = turtle_controller.turtle_status_service:main',
    ],
},
```

**Task 6.4:** Build and test

```bash
cd ~/turtle_ws
colcon build
source install/setup.bash
```

**Test the service:**

Terminal 1 - Turtlesim:
```bash
ros2 run turtlesim turtlesim_node
```

Terminal 2 - Your service:
```bash
ros2 run turtle_controller turtle_status_service
```

Terminal 3 - Call the service manually:
```bash
ros2 service call /check_turtle_status std_srvs/srv/Trigger
```

You should see output like:
```
success: True
message: 'Turtle is near center! Position: (5.54, 5.54)'
```

Terminal 4 - Move the turtle:
```bash
ros2 run turtlesim turtle_teleop_key
```

Use arrow keys to move the turtle to a corner, then call the service again in Terminal 3. You should now see:
```
success: False
message: 'Turtle is far from center. Position: (2.30, 8.45)'
```

---

## 7. Creating a Service Client

### Goal
Create a client that calls the turtle status service and displays the result.

### Background Information

**Key Concepts:**
- A **service client** calls services and receives responses
- The client sends a request and waits for the server to respond
- Our client will call the status service and display whether the turtle is near the center

### Tasks

**Task 7.1:** Create the service client script

```bash
cd ~/turtle_ws/src/turtle_controller/turtle_controller
```
Create turtle_status_client.py file using VS Code

**Task 7.2:** Write the complete client code

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class TurtleStatusClient(Node):
    """
    A simple ROS 2 service client that checks the turtle's status.
    
    This demonstrates how to create a service client that sends
    requests and handles responses.
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
            
            # Display the result with visual indicators
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
```

**Task 7.3:** Make executable and update setup.py

```bash
chmod +x turtle_status_client.py
cd ~/turtle_ws/src/turtle_controller
```
Edit setup.py using VS Code

Update entry_points:

```python
entry_points={
    'console_scripts': [
        'velocity_publisher = turtle_controller.velocity_publisher:main',
        'pose_subscriber = turtle_controller.pose_subscriber:main',
        'turtle_status_service = turtle_controller.turtle_status_service:main',
        'turtle_status_client = turtle_controller.turtle_status_client:main',
    ],
},
```

**Task 7.4:** Build and test

```bash
cd ~/turtle_ws
colcon build
source install/setup.bash
```

**Test the client:**

Terminal 1 - Turtlesim:
```bash
ros2 run turtlesim turtlesim_node
```

Terminal 2 - Service server:
```bash
ros2 run turtle_controller turtle_status_service
```

Terminal 3 - Service client:
```bash
ros2 run turtle_controller turtle_status_client
```

You should see output like:
```
[INFO] [turtle_status_client]: Checking turtle status...
[INFO] [turtle_status_client]: ✓ Turtle is near center! Position: (5.54, 5.54)
```

Terminal 4 - Move the turtle:
```bash
ros2 run turtlesim turtle_teleop_key
```

Use arrow keys to move the turtle away from center, then run the client again in Terminal 3:
```bash
ros2 run turtle_controller turtle_status_client
```

You should now see:
```
[INFO] [turtle_status_client]: Checking turtle status...
[INFO] [turtle_status_client]: ✗ Turtle is far from center. Position: (2.30, 8.45)
```

---

## 8. Testing Everything Together

Now let's run all components together to see the complete system in action!

### Complete System Test

**Terminal 1** - Start turtlesim:
```bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2** - Start the pose subscriber:
```bash
ros2 run turtle_controller pose_subscriber
```

**Terminal 3** - Start the status service:
```bash
ros2 run turtle_controller turtle_status_service
```

**Terminal 4** - Start the velocity publisher (turtle will start moving):
```bash
ros2 run turtle_controller velocity_publisher
```

**Terminal 5** - Check status periodically:
```bash
# Check status while turtle is moving
ros2 run turtle_controller turtle_status_client

# Wait a few seconds and check again
ros2 run turtle_controller turtle_status_client
```

You'll see the status change as the turtle moves around in its circular pattern!

---

## 9. Creating a Launch File

**Launch files** allow you to start multiple nodes with a single command. Instead of opening 5 different terminals, you can launch everything at once!

### What is a Launch File?

A launch file is a Python script (in ROS 2) that describes:
- Which nodes to start
- What parameters to set
- What arguments to pass
- Remapping of topics/services
- Conditional logic for different scenarios

### Step 9.1: Create the launch directory

```bash
cd ~/turtle_ws/src/turtle_controller
mkdir launch
cd launch
```

### Step 9.2: Create a simple launch file

Create turtle_system_launch.py file using VS Code

### Step 9.3: Write the launch file code

```python
#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    Launch file to start the complete turtle control system.
    
    This will start:
    1. Turtlesim node
    2. Velocity publisher (makes turtle move)
    3. Pose subscriber (prints turtle position)
    4. Rotate service (provides rotation service)
    """
    
    return LaunchDescription([
        # Start the turtlesim node
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen'
        ),
        
        # Start our velocity publisher
        Node(
            package='turtle_controller',
            executable='velocity_publisher',
            name='velocity_publisher',
            output='screen'
        ),
        
        # Start our pose subscriber
        Node(
            package='turtle_controller',
            executable='pose_subscriber',
            name='pose_subscriber',
            output='screen'
        ),
        
        # Start our turtle status service
        Node(
            package='turtle_controller',
            executable='turtle_status_service',
            name='turtle_status_service',
            output='screen'
        ),
    ])
```

**Explanation of parameters:**
- `package`: The ROS 2 package containing the executable
- `executable`: The name of the node executable (from setup.py entry_points)
- `name`: The name to give this node instance (can override the node's internal name)
- `output='screen'`: Print node output to the terminal (instead of log files)

### Step 9.4: Update setup.py to include the launch file

```bash
cd ~/turtle_ws/src/turtle_controller
```
Edit setup.py file using VS Code

Add the following import at the top:

```python
from setuptools import setup
import os
from glob import glob
```

Then modify the setup function to include the launch files (find the `data_files` section):

```python
data_files=[
    ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    # Include launch files
    (os.path.join('share', package_name, 'launch'), glob('launch/*launch.py')),
],
```

**Complete setup.py should look like this:**

```python
from setuptools import setup
import os
from glob import glob

package_name = 'turtle_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='Turtle controller package for ROS 2 tutorial',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'velocity_publisher = turtle_controller.velocity_publisher:main',
            'pose_subscriber = turtle_controller.pose_subscriber:main',
            'turtle_status_service = turtle_controller.turtle_status_service:main',
            'turtle_status_client = turtle_controller.turtle_status_client:main',
        ],
    },
)
```

### Step 9.5: Build and source the workspace

```bash
cd ~/turtle_ws
colcon build
source install/setup.bash
```

### Step 9.6: Run the launch file

```bash
ros2 launch turtle_controller turtle_system_launch.py
```

You should see:
- The turtlesim window open
- The turtle start moving in a circle
- Pose information printing to the terminal
- All nodes running together!

To stop everything, press **Ctrl+C** once - it will shut down all nodes.

### Step 9.7: Test the service while the system is running

Open a new terminal:

```bash
source ~/turtle_ws/install/setup.bash
ros2 run turtle_controller turtle_status_client
```

The turtle will rotate while continuing to move!