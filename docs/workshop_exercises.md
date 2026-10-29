# ROS 2 Humble Turtlesim Workshop – Hands-On Exercises

## How this workshop works

You will build a ROS 2 package called `turtle_controller` from scratch, one piece at a time. Instead of copying finished code, you write it yourself with guidance.

Under each task you will find:

- **Hint**: a nudge in the right direction. Try this first.
- **More help**: a code skeleton with the key line or two left for you to fill in.
- **Check Your Work**: a command and the output you should see. Do not move on until it matches.

If you are still stuck after the hints, each exercise links to the matching section of the [complete tutorial](complete_tutorial.md), which explains the finished solution. Section numbers there match the exercise numbers here.

| Exercise | You will build |
|---|---|
| 1 | A workspace and an empty package |
| 2 | A **publisher** that drives the turtle in a circle |
| 3 | A **subscriber** that prints the turtle's position |
| 4 | A **service server** that says whether the turtle is near the centre |
| 5 | A **service client** that asks that question |
| 6 | A **launch file** that starts everything at once |
| 7 *(extra)* | A **controller** that drives the turtle to a target point |

---

## Before you start

1. Check that ROS 2 Humble works. The [README](../README.md#before-you-start) shows how.
2. You will use **several terminals at once**. In every new terminal, ROS 2 must be sourced:
   ```bash
   source /opt/ros/humble/setup.bash
   ```
   Once your workspace is built (Exercise 1.3), also source it in every new terminal:
   ```bash
   source ~/turtle_ws/install/setup.bash
   ```
   Forgetting this is the most common reason for `Package 'turtle_controller' not found`.
3. **The simulator is a separate program, and you start it yourself.** Your nodes only send and receive messages; they do not open the turtlesim window. In Exercises 2–5 and 7, start turtlesim first in its own terminal and leave it running:
   ```bash
   ros2 run turtlesim turtlesim_node
   ```
   If you close the window or press Ctrl+C in that terminal, the turtle is gone, and your nodes will have nothing to talk to. In Exercise 6 you write a launch file that starts turtlesim for you.
4. Use VS Code (or another editor) to create and edit files.

---

## Exercise 1: Setting Up Your Workspace

### Goal
Create a ROS 2 workspace and an empty Python package, and build it.

### Tasks

**Task 1.1:** Create a workspace directory structure
- Create a directory called `turtle_ws` in your home directory
- Inside it, create a `src` subdirectory
- Navigate to the workspace root

<details>
<summary>Hint 1.1</summary>

Use the `mkdir` command with the `-p` flag to create nested directories:
```bash
mkdir -p ~/directory_name/subdirectory_name
```
</details>

<details>
<summary>Check Your Work 1.1</summary>

Run `pwd`. You should be in `/home/your_username/turtle_ws`.
Run `ls`. You should see a `src` directory.
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
<summary>More help 1.2</summary>

```bash
ros2 pkg create --build-type ament_python PACKAGE_NAME \
  --dependencies dependency1 dependency2 dependency3
```
</details>

<details>
<summary>Check Your Work 1.2</summary>

Run `ls ~/turtle_ws/src/turtle_controller`. You should see:
`package.xml  resource  setup.cfg  setup.py  test  turtle_controller`

Open `package.xml`. You should see a `<depend>` line for each of `rclpy`, `geometry_msgs` and `turtlesim`.
</details>

**Task 1.3:** Build your workspace
- Navigate back to the workspace root
- Build the package using colcon
- Source the installation

<details>
<summary>Hint 1.3</summary>

Always build from the workspace root (`~/turtle_ws`), never from inside `src`.
The build command is `colcon build`. After building, source `install/setup.bash`.
</details>

<details>
<summary>Check Your Work 1.3</summary>

`colcon build` should end with `Summary: 1 package finished`.

Then run:
```bash
ros2 pkg list | grep turtle_controller
```
You should see `turtle_controller`.
</details>

> **Stuck?** See [Tutorial §1](complete_tutorial.md#1-workspace-and-package).

---

## Exercise 2: Creating a Topic Publisher

### Goal
Create a node that publishes velocity commands to make the turtle move in a circle.

### Background

- A **node** is a running program that takes part in a ROS 2 system.
- A **publisher** sends messages to a named **topic**. Any node that subscribes to that topic receives them.
- Turtlesim listens to `/turtle1/cmd_vel` for velocity commands.
- Velocity commands use the `geometry_msgs/msg/Twist` message type. It has two parts:
  - `linear`: movement. The turtle only uses `linear.x` (forwards/backwards).
  - `angular`: rotation. The turtle only uses `angular.z` (turning left/right).
- Turtlesim **stops the turtle if no command arrives for 1 second**, so the publisher must keep sending.

### Tasks

**Task 2.1:** Create the Python file
- Navigate to `~/turtle_ws/src/turtle_controller/turtle_controller/`. This is the inner folder, next to `__init__.py`.
- Create a file named `velocity_publisher.py`

> You do not need `chmod +x`. `ros2 run` starts your code through the entry point you register in `setup.py` (Task 2.6), not by running the file directly.

**Task 2.2:** Write the basic node structure

Write a Python script that includes:
1. A shebang line for Python 3
2. The imports you need (`rclpy`, `Node`, `Twist`)
3. A class that inherits from `Node`
4. A `main` function that initialises ROS, creates the node, spins it, and cleans up when you press Ctrl+C

<details>
<summary>Hint 2.2 - Shebang and imports</summary>

```python
#!/usr/bin/env python3

from geometry_msgs.msg import Twist
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
```

`ExternalShutdownException` is only needed for a clean exit when you press Ctrl+C (see the main function hint).
</details>

<details>
<summary>Hint 2.2 - Class structure</summary>

```python
class VelocityPublisher(Node):
    def __init__(self):
        super().__init__('node_name_here')
        # Your code here
```
</details>

<details>
<summary>Hint 2.2 - Main function</summary>

```python
def main(args=None):
    rclpy.init(args=args)
    node = YourClassName()
    try:
        rclpy.spin(node)  # runs until you press Ctrl+C
    except (KeyboardInterrupt, ExternalShutdownException):
        pass  # Ctrl+C is the normal way to stop a node
    finally:
        node.destroy_node()
        if rclpy.ok():  # Ctrl+C may already have shut ROS down
            rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Without the `try`/`except`, pressing Ctrl+C prints a long `KeyboardInterrupt` traceback. That looks like an error but is not one. Every node in this workshop uses this same `main` pattern.
</details>

**Task 2.3:** Create a publisher in the `__init__` method

Add code to create a publisher that:
- Publishes to the topic `/turtle1/cmd_vel`
- Uses the `Twist` message type
- Has a queue depth of 10

<details>
<summary>Hint 2.3</summary>

Nodes have a `create_publisher()` method. It takes the message type, the topic name and the queue depth, in that order. Store the result in `self.publisher_` so you can use it later.
</details>

<details>
<summary>More help 2.3</summary>

```python
self.publisher_ = self.create_publisher(MessageType, 'topic_name', queue_depth)
```
</details>

**Task 2.4:** Create a timer

Add a timer that calls a callback method every 0.5 seconds.

<details>
<summary>Hint 2.4</summary>

```python
timer_period = 0.5  # seconds
self.timer = self.create_timer(timer_period, self.callback_method_name)
```

Note that you pass `self.timer_callback` **without** brackets. You are telling ROS which method to call, not calling it yourself.
</details>

**Task 2.5:** Write the timer callback method

Create a method that:
1. Creates a new `Twist` message
2. Sets `linear.x` to 2.0 (move forward)
3. Sets `angular.z` to 1.0 (turn counter-clockwise)
4. Publishes the message
5. Logs what it published using `self.get_logger().info()`

<details>
<summary>Hint 2.5</summary>

A new `Twist()` has every field set to 0.0, so you only need to set the two fields you use.
</details>

<details>
<summary>More help 2.5</summary>

```python
def timer_callback(self):
    msg = Twist()
    msg.linear.x = # Your value here
    msg.angular.z = # Your value here
    self.publisher_.publish(msg)
    # Log here
```
</details>

**Task 2.6:** Register the node in `setup.py`

Edit `~/turtle_ws/src/turtle_controller/setup.py` to add an entry point for your node. This entry point is what makes `ros2 run turtle_controller velocity_publisher` work.

<details>
<summary>Hint 2.6</summary>

Find the `entry_points` section and add one line inside `console_scripts`:
```python
entry_points={
    'console_scripts': [
        'velocity_publisher = turtle_controller.velocity_publisher:main',
    ],
},
```
The format is `'command_name = package_folder.file_name:function_name'`.

Your generated `setup.py` may differ slightly from other people's (for example `tests_require` or `extras_require`). Only edit `entry_points` and leave the rest as it is.
</details>

**Task 2.7:** Build and test

1. Build the package and source the workspace:
   ```bash
   cd ~/turtle_ws
   colcon build
   source install/setup.bash
   ```
2. **Start the simulator first.** In a new terminal (Terminal 1), run:
   ```bash
   ros2 run turtlesim turtlesim_node
   ```
   A window with a turtle in the middle should open. Leave this terminal running.
3. In another terminal (Terminal 2), source the workspace and run your publisher:
   ```bash
   source ~/turtle_ws/install/setup.bash
   ros2 run turtle_controller velocity_publisher
   ```

From now on, every test starts the same way: turtlesim in Terminal 1, your node(s) in other terminals.

<details>
<summary>Check Your Work 2.7</summary>

- The turtle drives in a circle and Terminal 2 prints `Publishing: linear.x=2.0, angular.z=1.0` twice per second.
- In a third terminal, check the publishing rate:
  ```bash
  ros2 topic hz /turtle1/cmd_vel
  ```
  You should see `average rate: 2.000` (give or take a little).
- Press Ctrl+C in Terminal 2. The node stops without a traceback, and the turtle stops about a second later.
</details>

> **Try this:** change `timer_period` to `1.5`, rebuild and run again. Why does the turtle now stop and start? (Look back at the Background section.) Set it back to `0.5` afterwards.

> **Stuck?** See [Tutorial §2](complete_tutorial.md#2-topic-publisher).

---

## Exercise 3: Creating a Topic Subscriber

### Goal
Create a node that subscribes to the turtle's pose and prints its position.

### Background

- A **subscriber** receives messages from a topic. ROS calls your **callback** method once for every message.
- Turtlesim publishes the turtle's pose on `/turtle1/pose`, about 60 times per second.
- The `turtlesim/msg/Pose` message contains `x`, `y`, `theta` (heading in **radians**), `linear_velocity` and `angular_velocity`.

### Tasks

**Task 3.1:** Create `pose_subscriber.py` in the same folder as `velocity_publisher.py`.

**Task 3.2:** Write the basic structure

As in Exercise 2, write a shebang, imports, a class that inherits from `Node`, and the same `main` function. This time you need `from turtlesim.msg import Pose` instead of `Twist`.

**Task 3.3:** Create a subscriber in `__init__`

Create a subscriber that:
- Subscribes to `/turtle1/pose`
- Uses the `Pose` message type
- Calls a callback method when messages arrive
- Has a queue depth of 10

<details>
<summary>Hint 3.3</summary>

Use `create_subscription()`. It takes the same arguments as `create_publisher()`, plus the callback method, which goes third.
</details>

<details>
<summary>More help 3.3</summary>

```python
self.subscription = self.create_subscription(
    MessageType,
    'topic_name',
    self.callback_method_name,
    queue_depth
)
```
</details>

**Task 3.4:** Write the callback method

Create a method that:
- Takes `msg` as a parameter (the received `Pose` message)
- Logs the turtle's `x`, `y` and `theta`, each with 2 decimal places

<details>
<summary>Hint 3.4</summary>

The fields are `msg.x`, `msg.y` and `msg.theta`. In an f-string, `{value:.2f}` shows a number with 2 decimal places.
</details>

**Task 3.5:** Register, build and test

- Add the entry point for `pose_subscriber` to `setup.py`. Keep the `velocity_publisher` line and add a new line under it.
- Build and source
- Run turtlesim, your subscriber, and the keyboard controller:

```bash
# Terminal 1
ros2 run turtlesim turtlesim_node
# Terminal 2
ros2 run turtle_controller pose_subscriber
# Terminal 3 (click into this terminal, then use the arrow keys)
ros2 run turtlesim turtle_teleop_key
```

<details>
<summary>Check Your Work 3.5</summary>

Terminal 2 prints the pose very quickly, for example `Turtle Pose - X: 5.54, Y: 5.54, Theta: 0.00`. The numbers change when you drive the turtle.

Check how fast the pose arrives:
```bash
ros2 topic hz /turtle1/pose
```
You should see roughly `average rate: 62.5`.
</details>

**Task 3.6:** Calm the output down

That many log lines per second is hard to read. Limit your log line to at most **once per second**, without throttling the subscription itself.

<details>
<summary>Hint 3.6</summary>

ROS 2 log calls accept an extra keyword argument, `throttle_duration_sec`.
</details>

<details>
<summary>More help 3.6</summary>

```python
self.get_logger().info(f'...your message...', throttle_duration_sec=____)
```
</details>

<details>
<summary>Check Your Work 3.6</summary>

Rebuild and run again. The pose now prints about once per second. `ros2 topic hz /turtle1/pose` still shows about 62.5 Hz, because your callback still receives every message; only the logging is throttled.
</details>

> **Stuck?** See [Tutorial §3](complete_tutorial.md#3-topic-subscriber).

---

## Exercise 4: Creating a Service Server

### Goal
Create a service that reports whether the turtle is near the centre of the window.

### Background

- A **service** is request–response communication. A client asks once and the server answers once. Compare this with topics, where messages flow continuously.
- Use a service when you want to *ask a question and wait for the answer*.
- We use the `std_srvs/srv/Trigger` service type:
  - **Request:** empty (no fields)
  - **Response:** `bool success` and `string message`
- To answer the question, the server needs to know where the turtle is. It will also subscribe to `/turtle1/pose`.

### Tasks

**Task 4.1:** Add the `std_srvs` dependency

`Trigger` comes from the `std_srvs` package, which you did not list when you created the package. Add it to `package.xml`.

<details>
<summary>Hint 4.1</summary>

Open `~/turtle_ws/src/turtle_controller/package.xml` and find the existing `<depend>` lines. Add one more in the same style.
</details>

<details>
<summary>Why bother, if it might work anyway?</summary>

On a full ROS 2 desktop install, `std_srvs` is already there, so your code may run without this line. On a minimal install, or when someone else installs your package's dependencies with `rosdep`, only the packages listed in `package.xml` get installed. Listing every package you import is what makes your package work on other machines.
</details>

<details>
<summary>Check Your Work 4.1</summary>

`package.xml` now has four `<depend>` lines: `rclpy`, `geometry_msgs`, `turtlesim` and `std_srvs`.
</details>

**Task 4.2:** Create `turtle_status_service.py` with the usual shebang, imports, class and `main`.

You need `from std_srvs.srv import Trigger` and `from turtlesim.msg import Pose`, as well as the standard imports.

**Task 4.3:** Keep track of the turtle's pose

In `__init__`:
- Create `self.current_pose` and set it to `None` (meaning "no pose received yet")
- Subscribe to `/turtle1/pose` with a callback that stores each message in `self.current_pose`

<details>
<summary>Hint 4.3</summary>

This is the subscriber from Exercise 3. The only difference is that the callback saves the message instead of logging it: `self.current_pose = msg`.
</details>

**Task 4.4:** Create the service server

In `__init__`, create a service:
1. Named `/check_turtle_status`
2. Using the `Trigger` service type
3. With a callback method that handles requests

<details>
<summary>Hint 4.4</summary>

Use `create_service()`. It takes the service type, the service name and the callback method.
</details>

**Task 4.5:** Write the service callback

Your callback is called with two arguments, `request` and `response`. It must fill in `response` and return it. It should:

1. If no pose has arrived yet (`self.current_pose is None`), set `success` to `False` and give a helpful message
2. Otherwise, decide whether the turtle is **near the centre**: within 1 unit of (5.5, 5.5) along both x and y
3. Set `response.success` to `True` or `False`
4. Set `response.message` to a sentence that includes the turtle's position
5. Log the message and return `response`

<details>
<summary>Hint 4.5</summary>

- `abs(a - b)` gives the distance between two numbers along one axis.
- You need that check for x **and** for y.
- The turtle starts at about (5.54, 5.54), so straight after starting turtlesim it should count as near the centre.
</details>

<details>
<summary>More help 4.5</summary>

```python
def handle_status_request(self, request, response):
    if self.current_pose is None:
        response.success = False
        response.message = 'No pose received yet. Is turtlesim running?'
        return response

    x = self.current_pose.x
    y = self.current_pose.y

    near_center = ____  # True when within 1.0 of 5.5 in both x and y

    response.success = near_center
    response.message = ____  # e.g. include f'({x:.2f}, {y:.2f})'

    self.get_logger().info(response.message)
    return response
```
</details>

**Task 4.6:** Register, build and test

Add the `turtle_status_service` entry point to `setup.py`, rebuild and source. Then:

```bash
# Terminal 1
ros2 run turtlesim turtlesim_node
# Terminal 2
ros2 run turtle_controller turtle_status_service
# Terminal 3 - call the service by hand
ros2 service call /check_turtle_status std_srvs/srv/Trigger
```

<details>
<summary>Check Your Work 4.6</summary>

Terminal 3 should print:
```
requester: making request: std_srvs.srv.Trigger_Request()

response:
std_srvs.srv.Trigger_Response(success=True, message='Turtle is near center! Position: (5.54, 5.54)')
```
Your message wording can differ. What matters is `success=True` and the position.

Now open Terminal 4, run `ros2 run turtlesim turtle_teleop_key`, and drive the turtle towards a corner. Call the service again. You should now get `success=False` and the new position.

Your service node (Terminal 2) should log the same message every time it is called.
</details>

> **Stuck?** See [Tutorial §4](complete_tutorial.md#4-service-server).

---

## Exercise 5: Creating a Service Client

### Goal
Create a node that calls the turtle status service once, prints the answer and exits.

### Background

- A **service client** sends a request and waits for the response.
- The server might not be running yet, so a client normally **waits for the service** before calling it.
- `call_async()` sends the request and returns a **future**: a placeholder that will hold the response once it arrives.

### Tasks

**Task 5.1:** Create `turtle_status_client.py` with the shebang, imports (`rclpy`, `ExternalShutdownException`, `Node` and `Trigger`) and a class that inherits from `Node`.

**Task 5.2:** Create the client

In `__init__`, create a client for the `/check_turtle_status` service.

<details>
<summary>Hint 5.2</summary>

`create_client()` takes the service type and the service name.
</details>

**Task 5.3:** Write a `check_status()` method

The method should:
1. Wait until the service is available, logging a message while it waits
2. Create an empty `Trigger.Request()`
3. Send it with `call_async()`
4. Wait for the response
5. Log the message with ✓ if `success` is `True` and ✗ if not

<details>
<summary>Hint 5.3</summary>

- `self.client.wait_for_service(timeout_sec=1.0)` returns `False` if the service did not appear within a second. Put it in a `while not ...:` loop.
- `rclpy.spin_until_future_complete(self, future)` processes callbacks until the response arrives.
- `future.result()` is the response, or `None` if the call failed.
</details>

<details>
<summary>More help 5.3</summary>

```python
def check_status(self):
    while not ____:
        self.get_logger().info('Waiting for /check_turtle_status service...')

    request = Trigger.Request()
    future = self.client.call_async(request)
    rclpy.spin_until_future_complete(self, future)

    response = future.result()
    if response is None:
        self.get_logger().error('Service call failed!')
    elif ____:
        self.get_logger().info(f'✓ {response.message}')
    else:
        self.get_logger().info(f'✗ {response.message}')
```
</details>

**Task 5.4:** Write `main`

This node does one job and then exits, so instead of `rclpy.spin(node)` it calls `node.check_status()`. Keep the same `try` / `except` / `finally` structure as the other nodes.

**Task 5.5:** Register, build and test

Add the `turtle_status_client` entry point, rebuild and source. With turtlesim and your service running (Exercise 4), run in another terminal:

```bash
ros2 run turtle_controller turtle_status_client
```

<details>
<summary>Check Your Work 5.5</summary>

With the turtle at the centre:
```
[INFO] [...] [turtle_status_client]: Checking turtle status...
[INFO] [...] [turtle_status_client]: ✓ Turtle is near center! Position: (5.54, 5.54)
```
Drive the turtle away with `turtle_teleop_key` and run the client again. You should see ✗ and the new position.

Now stop your service (Ctrl+C) and run the client. It should print `Waiting for /check_turtle_status service...` once per second. Start the service again and the client should finish on its own.
</details>

> **Stuck?** See [Tutorial §5](complete_tutorial.md#5-service-client).

---

## Exercise 6: Creating a Launch File

### Goal
Start turtlesim, the publisher, the subscriber and the service with a single command.

### Background

- So far you have started turtlesim and each of your nodes by hand, each in its own terminal. A launch file does all of that with one command, **including starting turtlesim**.
- A **launch file** describes a set of nodes to start together. ROS 2 launch files can be written in Python, XML or YAML; we use Python.
- Launch files live in a `launch/` folder in your package.
- They must be **installed** by `setup.py` so that `ros2 launch` can find them.

### Tasks

**Task 6.1:** Create a `launch` folder in your package root (`~/turtle_ws/src/turtle_controller/launch`). This is next to `setup.py`, not inside the inner `turtle_controller/` folder.

**Task 6.2:** Create `turtle_system_launch.py` in that folder. It needs:
1. The imports below
2. A function called `generate_launch_description()` that returns a `LaunchDescription` containing a list of `Node` actions

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
            executable='executable_name',
            name='node_name',
            output='screen'
        ),
        # More nodes here...
    ])
```
</details>

**Task 6.3:** Add four nodes:
1. `turtlesim_node` from the `turtlesim` package
2. `velocity_publisher`
3. `pose_subscriber`
4. `turtle_status_service`

Leave the client out. You will run it by hand.

<details>
<summary>Hint 6.3</summary>

For each node:
- `package`: the package that contains the executable (`turtlesim` or `turtle_controller`)
- `executable`: the name before the `=` in your `setup.py` entry point (or `turtlesim_node`)
- `name`: the node's name in the running system
- `output='screen'`: show its log messages in this terminal
</details>

**Task 6.4:** Install the launch file and declare its dependencies

1. In `setup.py`, add the launch folder to `data_files`, so the file is copied into `install/` when you build.
2. In `package.xml`, add `<exec_depend>launch</exec_depend>` and `<exec_depend>launch_ros</exec_depend>`. These are needed to *run* the launch file.

<details>
<summary>Hint 6.4 - setup.py</summary>

Add these imports at the top of `setup.py`:
```python
from glob import glob
import os
```

Then add this line inside the `data_files=[...]` list:
```python
(os.path.join('share', package_name, 'launch'), glob('launch/*launch.py')),
```
</details>

**Task 6.5:** Build and test

First, **stop everything you started by hand**: press Ctrl+C in each terminal that is running turtlesim or one of your nodes. Otherwise you will end up with two turtlesim windows and two copies of each node.

Then build and launch:

```bash
cd ~/turtle_ws
colcon build
source install/setup.bash
ros2 launch turtle_controller turtle_system_launch.py
```

<details>
<summary>Check Your Work 6.5</summary>

- The turtlesim window opens and the turtle drives in a circle.
- The terminal shows log lines from all your nodes, each prefixed with its name. The pose line appears about once a second.
- In a second terminal, `ros2 node list` shows:
  ```
  /pose_subscriber
  /turtle_status_service
  /turtlesim
  /velocity_publisher
  ```
- Still in the second terminal, run `ros2 run turtle_controller turtle_status_client` a few times. The answer changes between ✓ and ✗ as the turtle circles.
- Press Ctrl+C once in the launch terminal. All the nodes stop.
</details>

> **Stuck?** See [Tutorial §6](complete_tutorial.md#6-launch-file).

---

## Exercise 7 (Extra): Driving to a Point

### Goal
Write a node that drives the turtle from wherever it is now to a point a given **distance** away in a given **heading**, then stops.

```bash
ros2 run turtle_controller go_to_point --ros-args -p distance:=3.0 -p heading:=45.0
```

### Background

- **Open loop vs closed loop.** The publisher in Exercise 2 sends the same command no matter where the turtle is (open loop). Here the node reads the pose, compares it with the target, and adjusts its command every step (closed loop). That is why it needs both a **subscriber** and a **publisher**.
- **Where is the target?** Heading is measured in the turtlesim window: 0° points right (+x) and 90° points up (+y). From a start point (x, y):
  - target x = x + distance × cos(heading)
  - target y = y + distance × sin(heading)

  Python's `math.cos` and `math.sin` use radians, so convert with `math.radians()` first.
- **Which way to turn?** The direction from the turtle to the target is `math.atan2(dy, dx)`. The **heading error** is that direction minus the turtle's `theta`. Wrap it into −π…π, otherwise the turtle may turn the long way round:
  ```python
  math.atan2(math.sin(angle), math.cos(angle))
  ```
- **Proportional (P) control.** Make each speed proportional to its error: turn faster when the heading error is large, and drive faster when the target is far away. The turtle naturally slows down as it arrives. Cap the speeds so it never goes too fast.
- **Parameters** let you set values when you start a node, without editing code. A node declares a parameter with a default value and reads it back. You set it with `--ros-args -p name:=value`.

### Tasks

**Task 7.1:** Create `go_to_point.py` with the usual structure. You need `math`, `Twist`, `Pose` and the standard imports.

**Task 7.2:** Declare and read two parameters
- `distance` with a default of `2.0`
- `heading` (in degrees) with a default of `90.0`. Convert it to radians and store that.

<details>
<summary>Hint 7.2</summary>

```python
self.declare_parameter('distance', 2.0)
self.distance = self.get_parameter('distance').value
```
</details>

**Task 7.3:** Set up communication

In `__init__`:
- Create a publisher to `/turtle1/cmd_vel`
- Subscribe to `/turtle1/pose` and store the latest message in `self.pose` (starting as `None`)
- Set `self.target = None` and `self.done = False`
- Create a timer that calls a `control_loop` method 10 times per second

**Task 7.4:** Work out the target, once

In `control_loop`, do nothing until the first pose has arrived. The first time a pose is available, calculate the target point from the formulas in the Background section and store it in `self.target`.

If the target is outside the window (x or y below 0 or above 11), log an error, set `self.done = True` and stop. Otherwise the turtle would drive into the wall and never arrive.

**Task 7.5:** Write the controller

On every call to `control_loop` (after the target is set):
1. Work out `dx`, `dy` and the remaining distance to the target (`math.hypot(dx, dy)`)
2. If the remaining distance is below 0.05, publish a zero `Twist`, log that you have arrived, set `self.done = True` and return
3. Work out the wrapped heading error
4. Choose the speeds:
   - `angular.z` = 4.0 × heading error, limited to ±2.0
   - If the heading error is bigger than 0.1 rad (about 6°), `linear.x` = 0, so the turtle **turns on the spot first**
   - Otherwise, `linear.x` = 1.5 × remaining distance, limited to 2.0
5. Publish the `Twist`

<details>
<summary>Hint 7.5</summary>

A small helper keeps the speed limits tidy:
```python
def clamp(value, limit):
    return max(-limit, min(limit, value))
```
Keep the numbers (gains, limits, tolerances) as named constants at the top of the file, such as `K_ANGULAR = 4.0`, so they are easy to experiment with.
</details>

<details>
<summary>More help 7.5</summary>

```python
dx = self.target[0] - self.pose.x
dy = self.target[1] - self.pose.y
distance_error = math.hypot(dx, dy)

if distance_error < DISTANCE_TOLERANCE:
    # stop, log, set self.done ...
    return

angle_error = normalize_angle(____ - self.pose.theta)

msg = Twist()
msg.angular.z = clamp(K_ANGULAR * angle_error, MAX_ANGULAR)
if abs(angle_error) > ANGLE_TOLERANCE:
    msg.linear.x = 0.0
else:
    msg.linear.x = ____
self.publisher_.publish(msg)
```
</details>

**Task 7.6:** Stop when done

Unlike the other nodes, this one should exit by itself once it arrives. In `main`, replace `rclpy.spin(node)` with a loop that handles one callback at a time and stops when the controller has finished:

```python
while rclpy.ok() and not node.done:
    rclpy.spin_once(node)
```

**Task 7.7:** Register, build and test

Add a `go_to_point` entry point, rebuild and source. Start turtlesim, then try a few targets:

```bash
ros2 run turtle_controller go_to_point
ros2 run turtle_controller go_to_point --ros-args -p distance:=3.0 -p heading:=45.0
ros2 run turtle_controller go_to_point --ros-args -p distance:=2.0 -p heading:=180.0
ros2 run turtle_controller go_to_point --ros-args -p distance:=8.0 -p heading:=0.0
```

<details>
<summary>Check Your Work 7.7</summary>

- With no parameters, the turtle turns to face up, drives 2 units, stops, and the node exits by itself.
- Your node logs the start and target points. The final "arrived" position is within about 0.05 of the target.
- With `heading:=180.0`, the turtle turns round and drives left.
- With `distance:=8.0` from the centre, the node refuses with an error, because the target is outside the window.
- Run it several times in a row: each run starts from wherever the last one ended.
</details>

<details>
<summary>Troubleshooting 7.7</summary>

**`InvalidParameterTypeException ... expecting type 'DOUBLE'`.** You typed a whole number, such as `distance:=3`. The parameter was declared with `2.0`, so it only accepts decimals. Use `distance:=3.0`.

**The turtle spins forever.** Check that you wrap the heading error, and that you compute `target direction - theta`, not the other way round.

**The turtle wobbles around the target.** The gains are too high. Try lowering `K_ANGULAR` or `K_LINEAR`.

**Nothing happens.** Is turtlesim running? Add a log line to check that `self.pose` is being set.
</details>

> **Try this:**
> - Remove the "turn on the spot first" rule, so the turtle always drives forward while it turns. How does the path change?
> - Double `K_LINEAR`. What happens near the target?

> **Stuck?** See [Tutorial §7](complete_tutorial.md#7-extra-go-to-point-controller).

---

## Troubleshooting (all exercises)

**`Package 'turtle_controller' not found`**
- You have not sourced the workspace in this terminal: `source ~/turtle_ws/install/setup.bash`

**`No executable found`**
- Is the entry point in `setup.py`, and is it spelled the same as in your `ros2 run` command?
- Did you rebuild (`colcon build` from `~/turtle_ws`) and source again afterwards?

**`ModuleNotFoundError` / `ImportError`**
- Check the spelling of your imports, for example `geometry_msgs.msg`, `turtlesim.msg` and `std_srvs.srv`.
- Check that the package you import from is listed in `package.xml`.

**My code changes don't seem to take effect**
- Python files are copied into `install/` when you build. After every change, run `colcon build` and source again.

**The turtle doesn't move**
- Is turtlesim running? Does `ros2 topic list` show `/turtle1/cmd_vel`?
- Is your node publishing? Run `ros2 topic echo /turtle1/cmd_vel` while it is running.

**Two turtlesim windows, or the turtle moves strangely after `ros2 launch`**
- A turtlesim or node you started by hand is still running alongside the launch file. Stop everything with Ctrl+C and launch again. `ros2 node list` should show each node only once.

**`colcon build` reports *duplicate package names***
- You have two packages called `turtle_controller` in `~/turtle_ws/src`, often because the whole workshop repository was cloned there. Keep only your own package in this workspace.

## Useful commands

```bash
ros2 node list                         # running nodes
ros2 node info /velocity_publisher     # a node's publishers, subscribers and services
ros2 topic list                        # all topics
ros2 topic echo /turtle1/pose          # print messages on a topic (Ctrl+C to stop)
ros2 topic hz /turtle1/cmd_vel         # how fast a topic is publishing
ros2 topic info /turtle1/cmd_vel       # message type and number of publishers/subscribers
ros2 service list                      # all services
ros2 service type /check_turtle_status # a service's type
rqt_graph                              # picture of how the nodes are connected
```
