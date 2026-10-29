# ROS 2 Humble Turtlesim Workshop – Complete Tutorial (Solutions)

This is the worked solution to the [workshop exercises](workshop_exercises.md). Section numbers match the exercise numbers.

Each section links to the finished file in [`solution/turtle_controller`](../solution/turtle_controller) and explains the parts that matter. The full code lives only in those files, so what you read here always matches what runs.

> **Try the exercise first.** Reading a solution is much easier than writing one. You will learn far more by getting stuck, using the hints, and only then coming here.

## Contents

1. [Workspace and package](#1-workspace-and-package)
2. [Topic publisher](#2-topic-publisher)
3. [Topic subscriber](#3-topic-subscriber)
4. [Service server](#4-service-server)
5. [Service client](#5-service-client)
6. [Launch file](#6-launch-file)
7. [Extra: go-to-point controller](#7-extra-go-to-point-controller)

---

## 1. Workspace and package

```bash
mkdir -p ~/turtle_ws/src
cd ~/turtle_ws/src
ros2 pkg create --build-type ament_python turtle_controller \
  --dependencies rclpy geometry_msgs turtlesim
cd ~/turtle_ws
colcon build
source install/setup.bash
```

- **Workspace** (`~/turtle_ws`): where you build. Your packages go in `src/`. `colcon build` creates `build/`, `install/` and `log/` next to it.
- **Package** (`src/turtle_controller`): the unit ROS 2 builds and installs. For a Python package, the important files are:

| File | Purpose |
|---|---|
| `package.xml` | Name, version and the **ROS packages you depend on** |
| `setup.py` | Which **executables** to create (`entry_points`) and which extra files to install (`data_files`) |
| `setup.cfg` | Tells colcon where to put the executables so `ros2 run` can find them. You never edit it. |
| `resource/turtle_controller` | An empty marker file that lets ROS 2 find the installed package |
| `turtle_controller/` (inner folder) | Your Python code goes here, next to `__init__.py` |
| `test/` | Style checks (`colcon test`). Not used in this workshop. |

`source install/setup.bash` adds your workspace to the current terminal's environment. It only affects that terminal, which is why every new terminal needs it.

---

## 2. Topic publisher

**Solution:** [`velocity_publisher.py`](../solution/turtle_controller/turtle_controller/velocity_publisher.py)

The node creates a publisher and a timer. Each time the timer fires, it publishes one `Twist`:

```python
self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
self.timer = self.create_timer(timer_period, self.timer_callback)
```

```python
msg = Twist()
msg.linear.x = 2.0  # units per second
msg.angular.z = 1.0  # radians per second, positive = counter-clockwise
self.publisher_.publish(msg)
```

Key points:

- **`10` is the queue depth**: how many messages to keep if they cannot be sent immediately. It is part of the publisher's QoS (quality of service) settings; 10 is a sensible default for everything in this workshop.
- **Why a circle?** Constant forward speed plus constant turning rate gives a circle of radius `linear.x / angular.z` = 2 units.
- **Why 0.5 s?** Turtlesim stops the turtle if it receives no command for 1 second. With a period longer than that, the turtle stops and starts between messages.
- **Registering the executable.** This line in [`setup.py`](../solution/turtle_controller/setup.py) creates the `velocity_publisher` command:
  ```python
  'velocity_publisher = turtle_controller.velocity_publisher:main',
  ```
  This is also why `chmod +x` is not needed: `ros2 run` starts a small wrapper that colcon generates from this line.

### The `main` function and Ctrl+C

Every node uses the same pattern:

```python
try:
    rclpy.spin(node)
except (KeyboardInterrupt, ExternalShutdownException):
    pass
finally:
    node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()
```

- `rclpy.spin(node)` keeps the program alive and runs callbacks (timers, subscriptions, services) as they become due.
- Pressing Ctrl+C makes `spin` raise an exception. Catching it avoids a long traceback that looks like a crash.
- ROS 2 Humble already shuts ROS down when you press Ctrl+C. Calling `rclpy.shutdown()` a second time raises an error, so the code checks `rclpy.ok()` first.

**Verify:** the turtle drives in a circle; `ros2 topic hz /turtle1/cmd_vel` shows about 2 Hz.

---

## 3. Topic subscriber

**Solution:** [`pose_subscriber.py`](../solution/turtle_controller/turtle_controller/pose_subscriber.py)

```python
self.subscription = self.create_subscription(
    Pose,
    '/turtle1/pose',
    self.pose_callback,
    10
)
```

ROS calls `pose_callback(msg)` for **every** message, about 62 times per second. Logging each one floods the terminal, so the solution throttles just the log line:

```python
self.get_logger().info(
    f'Turtle Pose - X: {msg.x:.2f}, Y: {msg.y:.2f}, Theta: {msg.theta:.2f}',
    throttle_duration_sec=1.0
)
```

Key points:

- **Throttling the log is not the same as receiving fewer messages.** `ros2 topic hz /turtle1/pose` still shows about 62.5 Hz. The callback still runs every time; only the print is limited.
- **`theta` is in radians**, from −π to π. 0 points right, π/2 (about 1.57) points up.
- The turtle starts at about (5.54, 5.54), the centre of an 11.09 × 11.09 window.

**Verify:** with `turtle_teleop_key`, the printed position changes as you drive, about once per second.

---

## 4. Service server

**Solution:** [`turtle_status_service.py`](../solution/turtle_controller/turtle_controller/turtle_status_service.py)

### Dependency

`Trigger` comes from `std_srvs`, so [`package.xml`](../solution/turtle_controller/package.xml) lists it:

```xml
<depend>std_srvs</depend>
```

It may work without this line on a full desktop install. It is still needed so `rosdep` (and anyone else using your package) knows to install it.

### Structure

The node does two jobs:

1. **Subscribes** to `/turtle1/pose` and keeps the latest message in `self.current_pose`.
2. **Serves** `/check_turtle_status`:
   ```python
   self.srv = self.create_service(
       Trigger,
       '/check_turtle_status',
       self.handle_status_request
   )
   ```

The callback receives the (empty) request and a response to fill in. It must **return** the response:

```python
near_center = abs(x - center_x) < 1.0 and abs(y - center_y) < 1.0

response.success = near_center
```

Key points:

- **`self.current_pose` starts as `None`, not `Pose()`.** An empty `Pose()` is at (0, 0). A request that arrives before the first pose would then report "far from centre at (0.00, 0.00)", which is wrong rather than unknown. The solution checks for `None` first and says no pose has arrived yet.
- **"Near" is a square**: within 1 unit along x *and* along y. Using `math.hypot(dx, dy) < 1.0` instead would give a circle. Either is a reasonable definition.
- The service answers instantly with the most recent pose. It does not wait for a new one.

**Verify:**

```bash
ros2 service call /check_turtle_status std_srvs/srv/Trigger
```
```
requester: making request: std_srvs.srv.Trigger_Request()

response:
std_srvs.srv.Trigger_Response(success=True, message='Turtle is near center! Position: (5.54, 5.54)')
```

---

## 5. Service client

**Solution:** [`turtle_status_client.py`](../solution/turtle_controller/turtle_controller/turtle_status_client.py)

`check_status()` has three steps:

```python
while not self.client.wait_for_service(timeout_sec=1.0):
    self.get_logger().info('Waiting for /check_turtle_status service...')
```
```python
future = self.client.call_async(request)
rclpy.spin_until_future_complete(self, future)
```
```python
response = future.result()
```

Key points:

- **Wait first.** If the client calls before the server exists, the request goes nowhere. `wait_for_service` checks once per second, so the client works whether you start it before or after the server.
- **`call_async` + `spin_until_future_complete`.** The request is sent straight away. The client then runs callbacks until the response arrives, which is how the response gets delivered.
- **No `rclpy.spin()`.** The client does one job and exits, so `main` calls `node.check_status()` instead. The wait is inside `check_status()`, within the `try` block, so Ctrl+C while waiting exits cleanly.

**Verify:** with the turtle at the centre, the client prints `✓ Turtle is near center! Position: (5.54, 5.54)`. With the server stopped, it prints the waiting message once per second.

---

## 6. Launch file

**Solution:** [`launch/turtle_system_launch.py`](../solution/turtle_controller/launch/turtle_system_launch.py)

The launch file returns a `LaunchDescription` with one `Node` action per process:

```python
Node(
    package='turtle_controller',
    executable='velocity_publisher',
    name='velocity_publisher',
    output='screen'
),
```

| Argument | Meaning |
|---|---|
| `package` | The package that contains the executable |
| `executable` | The entry-point name from `setup.py` (or `turtlesim_node`) |
| `name` | The node name in the running system; this overrides the name in the code |
| `output='screen'` | Show the node's log output in this terminal |

### Installing it

`ros2 launch` looks in the **install** folder, so [`setup.py`](../solution/turtle_controller/setup.py) copies the launch files there:

```python
(os.path.join('share', package_name, 'launch'), glob('launch/*launch.py')),
```

The glob only matches names ending in `launch.py`, so name launch files accordingly.

[`package.xml`](../solution/turtle_controller/package.xml) declares what is needed to run them:

```xml
<exec_depend>launch</exec_depend>
<exec_depend>launch_ros</exec_depend>
```

`exec_depend` means "needed at run time only", unlike `depend`, which covers building and running.

**Verify:** `ros2 launch turtle_controller turtle_system_launch.py` opens turtlesim with the turtle circling. `ros2 node list` shows four nodes. Ctrl+C once stops all of them.

---

## 7. Extra: go-to-point controller

**Solution:** [`go_to_point.py`](../solution/turtle_controller/turtle_controller/go_to_point.py)

```bash
ros2 run turtle_controller go_to_point --ros-args -p distance:=3.0 -p heading:=45.0
```

### Parameters

```python
self.declare_parameter('distance', 2.0)   # turtlesim units
self.declare_parameter('heading', 90.0)   # degrees in the world frame
```

The default value also fixes the parameter's **type**. Because the defaults are `2.0` and `90.0`, the parameters are decimals (`DOUBLE`), and `distance:=3` (an integer) is rejected. This is why the instructions always use `3.0`.

### The target

Calculated once, from the first pose received:

```python
target_x = self.pose.x + self.distance * math.cos(self.heading)
target_y = self.pose.y + self.distance * math.sin(self.heading)
```

The heading is converted to radians when it is read, and is measured in the window's frame (0 = right, 90° = up), not relative to the way the turtle is facing. Targets outside 0–11 are rejected. Otherwise the turtle would push against the wall forever.

### The control law

`compute_command()` runs 10 times per second:

```python
angle_to_target = math.atan2(dy, dx)
angle_error = normalize_angle(angle_to_target - self.pose.theta)

angular = clamp(K_ANGULAR * angle_error, MAX_ANGULAR)
if abs(angle_error) > ANGLE_TOLERANCE:
    linear = 0.0  # facing the wrong way: turn first
else:
    linear = clamp(K_LINEAR * distance_error, MAX_LINEAR)
```

Key points:

- **Closed loop.** Every step uses the *measured* pose. If the turtle drifts or overshoots, the next command corrects it. Compare this with Exercise 2, which never looks at where the turtle is.
- **Wrapping the angle.** Without `normalize_angle`, an error of, say, 350° makes the turtle turn almost all the way round instead of 10° the other way.
- **Turn first, then drive.** If the turtle drove while badly misaligned, it would swing out in a wide arc. Turning on the spot until within about 6° keeps the path straight.
- **Proportional control.** Speed is proportional to error, so the turtle slows smoothly as it arrives. The clamps cap the speed when the error is large.
- **Stopping.** When within `DISTANCE_TOLERANCE` (0.05) of the target, the node publishes a zero command and sets `self.done`. `main` uses `spin_once` in a loop that checks `node.done`, so the program ends by itself.

**Verify:** the turtle arrives within about 0.05 of the logged target for any heading, including 180° and −90°. With `distance:=8.0` from the centre, it refuses with an error.
