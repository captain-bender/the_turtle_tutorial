# ROS 2 Humble Turtlesim Workshop - Hands-On Exercises

## Introduction

Welcome to this hands-on ROS 2 workshop! Instead of copying and pasting code, you'll be writing it yourself with guidance and hints. This approach will help you truly understand ROS 2 concepts and become comfortable with the syntax and patterns.

## Exercise 1: Setting Up Your Workspace

### Goal
Create a ROS 2 workspace and package from scratch.

### Tasks

**Task 1.1:** Create a workspace directory structure
- Create a directory called `turtle_ws` in your home directory
- Inside it, create a `src` subdirectory
- Navigate to the workspace root

<details>
<summary>Hint 1.1</summary>

Use the `mkdir` command with the `-p` flag to create nested directories.
```bash
mkdir -p ~/directory_name/subdirectory_name
```
</details>

<details>
<summary>Check Your Work 1.1</summary>

Run `pwd` - you should be in `/home/your_username/turtle_ws`
Run `ls` - you should see a `src` directory
</details>

**Task 1.2:** Create a new ROS 2 Python package
- Navigate to the `src` directory
- Create a package named `turtle_controller`
- The package should depend on: `rclpy`, `geometry_msgs`, and `turtlesim`

<details>
<summary>Hint 1.2</summary>

Use the `ros2 pkg create` command with these flags:
- `--build-type ament_python` for Python packages
- `--dependencies` to list dependencies
</details>

<details>
<summary>More Help 1.2</summary>

```bash
ros2 pkg create --build-type ament_python PACKAGE_NAME \
  --dependencies dependency1 dependency2 dependency3
```
</details>

<details>
<summary>Check Your Work 1.2</summary>

- Navigate to `~/turtle_ws/src/turtle_controller`
- You should see: `package.xml`, `setup.py`, `setup.cfg`, `resource/`, `test/`, and a `turtle_controller/` directory
</details>

**Task 1.3:** Build your workspace
- Navigate back to the workspace root
- Build the package using colcon
- Source the installation

<details>
<summary>Hint 1.3</summary>

The build command is `colcon build`
After building, source the file: `install/setup.bash`
</details>

<details>
<summary>Check Your Work 1.3</summary>

Run: `ros2 pkg list | grep turtle_controller`
You should see `turtle_controller` in the output.
</details>

---

## Exercise 2: Creating a Topic Publisher

### Goal
Create a node that publishes velocity commands to make the turtle move in a circle.

### Background Information

**Key Concepts:**
- A **publisher** sends messages to a topic
- The turtlesim listens to `/turtle1/cmd_vel` for velocity commands
- Velocity commands use the `Twist` message type
- `Twist` has two main parts:
  - `linear` - forward/backward movement (we use `linear.x`)
  - `angular` - rotational movement (we use `angular.z`)

### Tasks

**Task 2.1:** Create the Python script file
- Navigate to `~/turtle_ws/src/turtle_controller/turtle_controller/`
- Create a file named `velocity_publisher.py`
- Make it executable

<details>
<summary>Hint 2.1</summary>

Use VScode to create the file.
Use `chmod +x filename.py` to make it executable.
</details>

**Task 2.2:** Write the basic node structure

Write a Python script that includes:
1. Shebang line for Python3
2. Import necessary modules (rclpy, Node, Twist)
3. A class that inherits from `Node`
4. A main function that initializes ROS, creates the node, and spins

<details>
<summary>Hint 2.2 - Imports</summary>

You need to import:
```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
```
</details>

<details>
<summary>Hint 2.2 - Class Structure</summary>

```python
class VelocityPublisher(Node):
    def __init__(self):
        super().__init__('node_name_here')
        # Your code here
```
</details>

<details>
<summary>Hint 2.2 - Main Function</summary>

```python
def main(args=None):
    rclpy.init(args=args)
    node = YourClassName()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
</details>

**Task 2.3:** Create a publisher in the `__init__` method

Add code to create a publisher that:
- Publishes to the topic `/turtle1/cmd_vel`
- Uses the `Twist` message type
- Has a queue size of 10

<details>
<summary>Hint 2.3</summary>

Use the `create_publisher()` method:
```python
self.publisher_ = self.create_publisher(MessageType, 'topic_name', queue_size)
```
</details>

**Task 2.4:** Create a timer

Add a timer that calls a callback function every 0.5 seconds.

<details>
<summary>Hint 2.4</summary>

Use the `create_timer()` method:
```python
timer_period = 0.5  # seconds
self.timer = self.create_timer(timer_period, self.callback_function_name)
```
</details>

**Task 2.5:** Write the timer callback function

Create a method that:
1. Creates a new `Twist` message
2. Sets `linear.x` to 2.0 (move forward)
3. Sets `angular.z` to 1.0 (turn counter-clockwise)
4. Publishes the message
5. Logs the action using `self.get_logger().info()`

<details>
<summary>Hint 2.5 - Creating Twist Message</summary>

```python
def timer_callback(self):
    msg = Twist()
    msg.linear.x = # Your value here
    msg.angular.z = # Your value here
    # Publish and log
```
</details>

<details>
<summary>Hint 2.5 - Publishing</summary>

```python
self.publisher_.publish(msg)
```
</details>

**Task 2.6:** Register the node in setup.py

Edit the `setup.py` file to add an entry point for your node.

<details>
<summary>Hint 2.6</summary>

Find the `entry_points` section and add:
```python
entry_points={
    'console_scripts': [
        'velocity_publisher = turtle_controller.velocity_publisher:main',
    ],
},
```
</details>

**Task 2.7:** Build and test

- Build the package
- Source the workspace
- Test your publisher

<details>
<summary>Hint 2.7 - Testing</summary>

Terminal 1:
```bash
ros2 run turtlesim turtlesim_node
```

Terminal 2:
```bash
ros2 run turtle_controller velocity_publisher
```

The turtle should move in a circle!
</details>

<details>
<summary>Troubleshooting</summary>

**Problem:** "No executable found"
- Did you add the entry point in setup.py?
- Did you rebuild the package?
- Did you source install/setup.bash?

**Problem:** "Module not found"
- Check your imports
- Make sure you're importing from the correct packages

**Problem:** Turtle doesn't move
- Is turtlesim running?
- Check the topic name (should be `/turtle1/cmd_vel`)
- Verify with: `ros2 topic list`
</details>

---

## Exercise 3: Creating a Topic Subscriber

### Goal
Create a node that subscribes to the turtle's pose and prints its position.

### Background Information

**Key Concepts:**
- A **subscriber** receives messages from a topic
- The turtlesim publishes pose information to `/turtle1/pose`
- The `Pose` message contains: x, y, theta, linear_velocity, angular_velocity

### Tasks

**Task 3.1:** Create the subscriber script
- Create `pose_subscriber.py` in the `turtle_controller` directory
- Make it executable

**Task 3.2:** Write the basic structure

Similar to the publisher, create:
1. Shebang and imports (need `turtlesim.msg import Pose` instead of Twist)
2. A class inheriting from Node
3. Main function

<details>
<summary>Hint 3.2 - Imports</summary>

```python
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
```
</details>

**Task 3.3:** Create a subscriber in `__init__`

Create a subscriber that:
- Subscribes to `/turtle1/pose`
- Uses the `Pose` message type
- Calls a callback function when messages arrive
- Has a queue size of 10

<details>
<summary>Hint 3.3</summary>

Use the `create_subscription()` method:
```python
self.subscription = self.create_subscription(
    MessageType,
    'topic_name',
    self.callback_function_name,
    queue_size
)
```
</details>

**Task 3.4:** Write the callback function

Create a method that:
- Takes `msg` as a parameter (the received Pose message)
- Logs the turtle's x, y, and theta values
- Use formatted strings to display values nicely

<details>
<summary>Hint 3.4</summary>

```python
def pose_callback(self, msg):
    self.get_logger().info(f'X: {msg.x:.2f}, Y: {msg.y:.2f}, Theta: {msg.theta:.2f}')
```
</details>

**Task 3.5:** Update setup.py and test

- Add the entry point for `pose_subscriber`
- Build and source
- Test with turtlesim and turtle_teleop_key

<details>
<summary>Hint 3.5 - Testing</summary>

Terminal 1:
```bash
ros2 run turtlesim turtlesim_node
```

Terminal 2:
```bash
ros2 run turtle_controller pose_subscriber
```

Terminal 3:
```bash
ros2 run turtlesim turtle_teleop_key
```

Use arrow keys to move the turtle and watch the pose output!
</details>

---

## Exercise 4: Creating a Service Server

### Goal
Create a service that checks if the turtle is near the center of the window.

### Background Information

**Key Concepts:**
- A **service** provides request-response communication (different from continuous topics)
- Services are used when you need to ask for something and wait for an answer
- The turtle status service will check the turtle's position and report if it's near the center
- We use the `Trigger` service type which is simple: no request data, returns success + message

### Tasks

**Task 4.1:** Create the service script
- Create `turtle_status_service.py` in the `turtle_controller` directory
- Make it executable

**Task 4.2:** Set up imports and class structure

You'll need:
- Standard ROS imports (rclpy, Node)
- `from std_srvs.srv import Trigger`
- `from turtlesim.msg import Pose`

<details>
<summary> Hint 4.2 - Imports</summary>

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from std_srvs.srv import Trigger
```
</details>

**Task 4.3:** Create a service server

In `__init__`, create:
1. A service server named `/check_turtle_status`
2. That uses `Trigger` service type
3. With a callback function to handle requests

<details>
<summary> Hint 4.3</summary>

```python
self.srv = self.create_service(
    Trigger,
    '/check_turtle_status',
    self.handle_status_request
)
```

The `Trigger` service type is simple:
- Request: Empty (no fields)
- Response: `bool success` and `string message`
</details>

**Task 4.4:** Subscribe to current pose

You need to know the turtle's current position. Create a subscriber to `/turtle1/pose`:
- Store the current pose in `self.current_pose`
- Update it in a callback function

<details>
<summary> Hint 4.4</summary>

```python
# In __init__:
self.current_pose = Pose()

self.pose_subscription = self.create_subscription(
    Pose,
    '/turtle1/pose',
    self.pose_callback,
    10
)

def pose_callback(self, msg):
    self.current_pose = msg
```
</details>

**Task 4.5:** Write the service callback function

Create a function that:
1. Takes `request` and `response` as parameters
2. Checks if turtle is near center (5.5, 5.5)
3. Sets `response.success` to True if near (within 1 unit), False if far
4. Sets `response.message` with turtle's position
5. Returns the response

<details>
<summary> Hint 4.5 - Logic</summary>

```python
def handle_status_request(self, request, response):
    center_x = 5.5
    center_y = 5.5
    
    # Calculate distance from center
    distance_x = abs(self.current_pose.x - center_x)
    distance_y = abs(self.current_pose.y - center_y)
    
    # Check if within 1 unit of center
    if distance_x < 1.0 and distance_y < 1.0:
        response.success = True
        response.message = f'Turtle is near center! Position: ({self.current_pose.x:.2f}, {self.current_pose.y:.2f})'
    else:
        response.success = False
        response.message = f'Turtle is far from center. Position: ({self.current_pose.x:.2f}, {self.current_pose.y:.2f})'
    
    return response
```
</details>

**Task 4.6:** Complete the node structure

Add the main function and proper initialization:
- `rclpy.init()`
- Create node instance
- `rclpy.spin()`
- Cleanup

<details>
<summary> Hint 4.6</summary>

```python
def main(args=None):
    rclpy.init(args=args)
    turtle_status = TurtleStatusService()
    rclpy.spin(turtle_status)
    turtle_status.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
</details>

**Task 4.7:** Update setup.py and test

Add the entry point in setup.py, then build and test.

<details>
<summary> Hint 4.7 - setup.py</summary>

```python
entry_points={
    'console_scripts': [
        'velocity_publisher = turtle_controller.velocity_publisher:main',
        'pose_subscriber = turtle_controller.pose_subscriber:main',
        'turtle_status_service = turtle_controller.turtle_status_service:main',
    ],
},
```
</details>

<details>
<summary> Hint 4.7 - Testing</summary>

Terminal 1:
```bash
ros2 run turtlesim turtlesim_node
```

Terminal 2:
```bash
ros2 run turtle_controller turtle_status_service
```

Terminal 3 - Call the service manually:
```bash
ros2 service call /check_turtle_status std_srvs/srv/Trigger
```

You should see:
```
success: True
message: 'Turtle is near center! Position: (5.54, 5.54)'
```

Terminal 4 - Move the turtle:
```bash
ros2 run turtlesim turtle_teleop_key
```

Use arrow keys to move to a corner, then call the service again. You should now see:
```
success: False
message: 'Turtle is far from center. Position: (2.30, 8.45)'
```
</details>

<details>
<summary> Check Your Work</summary>

Your service should:
- Subscribe to `/turtle1/pose` to track position
- Provide service `/check_turtle_status`
- Return True/False based on distance from center
- Include position in the message
- Log the status when called

Test by moving the turtle and calling the service multiple times!
</details>

<details>
<summary> Troubleshooting</summary>

**Problem:** Service not found
- Did you add the entry point in setup.py?
- Did you rebuild: `colcon build`?
- Did you source: `source install/setup.bash`?

**Problem:** Service always returns same position
- Is the pose subscriber working?
- Check that `pose_callback` is being called
- Use `self.get_logger().info()` to debug

**Problem:** "Trigger not found"
- Did you import from `std_srvs.srv`?
- Check that package.xml includes `<depend>std_srvs</depend>`
</details>

---

## Exercise 5: Creating a Service Client

### Goal
Create a client that calls the turtle status service and displays the result.

### Background Information

**Key Concepts:**
- A **service client** calls services and receives responses
- The client sends a request and waits for the server to respond
- Our client will call the status service and display whether the turtle is near the center

### Tasks

**Task 5.1:** Create the client script
- Create `turtle_status_client.py` in the `turtle_controller` directory
- Make it executable

**Task 5.2:** Set up imports

You'll need:
- Standard ROS imports (rclpy, Node)
- `from std_srvs.srv import Trigger`

<details>
<summary> Hint 5.2</summary>

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
```

Note: No need for `sys` or `math` - this client is simpler!
</details>

**Task 5.3:** Create a service client

In `__init__`:
- Create a client for `/check_turtle_status` service
- Wait for the service to be available

<details>
<summary> Hint 5.3</summary>

```python
self.client = self.create_client(Trigger, '/check_turtle_status')

while not self.client.wait_for_service(timeout_sec=1.0):
    self.get_logger().info('Waiting for /check_turtle_status service...')
```
</details>

**Task 5.4:** Write a method to check status

Create a method called `check_status()` that:
1. Creates a service request (empty for Trigger)
2. Calls the service asynchronously
3. Waits for the response
4. Displays the result with ✓ or ✗

<details>
<summary> Hint 5.4</summary>

```python
def check_status(self):
    # Create request (Trigger has no fields)
    request = Trigger.Request()
    
    self.get_logger().info('Checking turtle status...')
    
    # Call service
    future = self.client.call_async(request)
    rclpy.spin_until_future_complete(self, future)
    
    # Handle response
    if future.result() is not None:
        response = future.result()
        if response.success:
            self.get_logger().info(f'✓ {response.message}')
        else:
            self.get_logger().info(f'✗ {response.message}')
```
</details>

**Task 5.5:** Write the main function

In the main function:
1. Initialize rclpy
2. Create the client node
3. Call `check_status()`
4. Cleanup

<details>
<summary> Hint 5.5</summary>

```python
def main(args=None):
    rclpy.init(args=args)
    
    status_client = TurtleStatusClient()
    status_client.check_status()
    
    status_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Note: No command-line arguments needed - much simpler!
</details>

**Task 5.6:** Update setup.py and test

Add the entry point for the client, then build and test.

<details>
<summary> Hint 5.6 - setup.py</summary>

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
</details>

<details>
<summary> Hint 5.6 - Testing</summary>

Make sure turtlesim and the service server are running, then:

Terminal 1:
```bash
ros2 run turtlesim turtlesim_node
```

Terminal 2:
```bash
ros2 run turtle_controller turtle_status_service
```

Terminal 3 - Run the client:
```bash
ros2 run turtle_controller turtle_status_client
```

Output when turtle is at center:
```
[INFO] [turtle_status_client]: Checking turtle status...
[INFO] [turtle_status_client]: ✓ Turtle is near center! Position: (5.54, 5.54)
```

Terminal 4 - Move the turtle:
```bash
ros2 run turtlesim turtle_teleop_key
```

Move to a corner, then run the client again:
```bash
ros2 run turtle_controller turtle_status_client
```

Output when turtle is far:
```
[INFO] [turtle_status_client]: Checking turtle status...
[INFO] [turtle_status_client]: ✗ Turtle is far from center. Position: (2.30, 8.45)
```
</details>

<details>
<summary> Check Your Work</summary>

Your client should:
- Connect to `/check_turtle_status` service
- Create empty request (Trigger type)
- Display result with ✓ or ✗
- Show turtle's position
- Work without command-line arguments

Test by running multiple times while moving the turtle!
</details>

<details>
<summary> Troubleshooting</summary>

**Problem:** "Service not available"
- Is the service server running?
- Check with: `ros2 service list`
- Should see `/check_turtle_status`

**Problem:** Client executable not found
- Did you add entry point in setup.py?
- Did you rebuild the package?
- Did you source install/setup.bash?

**Problem:** No output shown
- Check that turtlesim is running
- Verify service server is running
- Try calling service manually first
</details>

---

## Exercise 6: Creating Launch Files

### Goal
Create launch files to start multiple nodes with a single command.

### Background Information

**Key Concepts:**
- **Launch files** start multiple nodes at once
- Written in Python for ROS 2
- Located in a `launch/` directory
- Must be registered in setup.py

### Tasks

**Task 6.1:** Create launch directory
- Navigate to your package root (`~/turtle_ws/src/turtle_controller`)
- Create a `launch` directory

**Task 6.2:** Create a basic launch file

Create `turtle_system_launch.py` in the launch directory that:
1. Imports necessary modules
2. Defines a `generate_launch_description()` function
3. Returns a `LaunchDescription` with multiple Node actions

<details>
<summary>Hint 6.2 - Imports</summary>

```python
from launch import LaunchDescription
from launch_ros.actions import Node
```
</details>

<details>
<summary>Hint 6.2 - Structure</summary>

```python
def generate_launch_description():
    return LaunchDescription([
        Node(
            package='package_name',
            executable='node_name',
            name='node_name',
            output='screen'
        ),
        # More nodes here...
    ])
```
</details>

**Task 6.3:** Add nodes to launch

Add Node actions for:
1. turtlesim_node (from turtlesim package)
2. velocity_publisher
3. pose_subscriber
4. turtle_status_service

<details>
<summary>Hint 6.3</summary>

For each node, specify:
- `package`: The package containing the executable
- `executable`: The name from setup.py entry_points
- `name`: A name for this node instance
- `output='screen'`: Print to terminal
</details>

**Task 6.4:** Update setup.py to include launch files

Modify setup.py to install launch files:
1. Add imports at the top
2. Add launch files to `data_files`

<details>
<summary>Hint 6.4 - Imports</summary>

```python
import os
from glob import glob
```
</details>

<details>
<summary>Hint 6.4 - data_files</summary>

Add this line to the `data_files` list:
```python
(os.path.join('share', package_name, 'launch'), glob('launch/*launch.py')),
```
</details>

**Task 6.5:** Build and test the launch file

<details>
<summary>Hint 6.5</summary>

```bash
cd ~/turtle_ws
colcon build
source install/setup.bash
ros2 launch turtle_controller turtle_system_launch.py
```

Everything should start at once!
</details>


## Useful Debugging Commands

When something doesn't work, try these:

**Check if your package is visible:**
```bash
ros2 pkg list | grep turtle_controller
```

**List all topics:**
```bash
ros2 topic list
```

**Echo a topic to see messages:**
```bash
ros2 topic echo /turtle1/cmd_vel
```

**List all services:**
```bash
ros2 service list
```

**Check node information:**
```bash
ros2 node info /node_name
```

**View the computational graph:**
```bash
rqt_graph
```


