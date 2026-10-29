# Reference solution

This folder holds the **finished `turtle_controller` package**: what your package should look like after the [workshop exercises](../docs/workshop_exercises.md). Try each exercise yourself first. Use this to compare when you are done, or when you are stuck after reading the hints.

## What's in it

| File | Exercise | What it does |
|---|---|---|
| [`turtle_controller/velocity_publisher.py`](turtle_controller/turtle_controller/velocity_publisher.py) | 2 | Publishes `Twist` commands on `/turtle1/cmd_vel` so the turtle drives in a circle |
| [`turtle_controller/pose_subscriber.py`](turtle_controller/turtle_controller/pose_subscriber.py) | 3 | Subscribes to `/turtle1/pose` and logs the position once per second |
| [`turtle_controller/turtle_status_service.py`](turtle_controller/turtle_controller/turtle_status_service.py) | 4 | Service `/check_turtle_status` (`std_srvs/srv/Trigger`): is the turtle near the centre? |
| [`turtle_controller/turtle_status_client.py`](turtle_controller/turtle_controller/turtle_status_client.py) | 5 | Calls the status service once and prints the answer |
| [`launch/turtle_system_launch.py`](turtle_controller/launch/turtle_system_launch.py) | 6 | Starts turtlesim, the publisher, the subscriber and the service together |
| [`turtle_controller/go_to_point.py`](turtle_controller/turtle_controller/go_to_point.py) | 7 (extra) | Drives the turtle to a point at a given distance and heading |
| [`setup.py`](turtle_controller/setup.py), [`package.xml`](turtle_controller/package.xml) | 1–7 | Entry points, launch file installation and dependencies |

## Building and running it

> **Do not clone this repository into the workspace you use for the exercises.**
> Your own package is also called `turtle_controller`. If both are in the same workspace, `colcon build` stops with a *duplicate package names* error.

Build the solution in its own workspace instead:

```bash
# Get the repository (anywhere outside your exercise workspace)
git clone https://github.com/captain-bender/turtle_controller.git ~/turtle_controller_repo

# Create a separate workspace and copy the solution package into it
mkdir -p ~/solution_ws/src
cp -r ~/turtle_controller_repo/solution/turtle_controller ~/solution_ws/src/

# Build and source it
cd ~/solution_ws
colcon build
source install/setup.bash
```

**Check:** `ros2 pkg executables turtle_controller` lists all five executables, including `go_to_point`.

> Use one workspace per terminal. If you source both `~/turtle_ws` and `~/solution_ws` in the same terminal, the one sourced last wins and it is hard to tell whose code is running. Open a fresh terminal when you switch.

### Run the whole system

```bash
ros2 launch turtle_controller turtle_system_launch.py
```

In a second terminal (source `~/solution_ws/install/setup.bash` first):

```bash
ros2 run turtle_controller turtle_status_client
```

### Run the go-to-point controller

Start turtlesim on its own, then:

```bash
ros2 run turtle_controller go_to_point --ros-args -p distance:=3.0 -p heading:=45.0
```

Always type a decimal point (`3.0`, not `3`).
