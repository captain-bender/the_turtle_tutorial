# The ROS 2 Turtlesim Workshop

A hands-on introduction to ROS 2 Humble. You build a small ROS 2 package from scratch and use it to drive the turtle in the **turtlesim** simulator.

## What you will learn

- How a ROS 2 **workspace** and **package** are organised, and how to build them with `colcon`
- **Topics**: writing a publisher that sends velocity commands and a subscriber that reads the turtle's pose
- **Services**: writing a server that answers a question and a client that asks it
- **Launch files**: starting several nodes with one command
- *Extra:* **closed-loop control**: combining a subscriber and a publisher so the turtle drives itself to a target point

## Before you start

You need **Ubuntu 22.04 with ROS 2 Humble** installed (the course virtual machine already has this), or the Docker environment from [ros2-gazebo-docker-demo](https://github.com/captain-bender/ros2-gazebo-docker-demo).

Open a terminal and check that ROS 2 is available:

```bash
source /opt/ros/humble/setup.bash
ros2 pkg executables turtlesim
```

You should see a list that includes `turtlesim turtlesim_node`. If you get `ros2: command not found`, ROS 2 is not installed or not sourced. Ask for help before going further.

> **Tip:** you need `source /opt/ros/humble/setup.bash` in every new terminal. To do it automatically, run this once:
> `echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc`

## How to use this repository

| You want to… | Go to |
|---|---|
| Do the workshop | [docs/workshop_exercises.md](docs/workshop_exercises.md). Work through it in order, writing the code yourself. |
| Get unstuck on a task | Open the **hints** under that task first. If you are still stuck, read the matching section of [docs/complete_tutorial.md](docs/complete_tutorial.md). |
| See or run the finished package | [solution/](solution/) |

**You do not need to clone this repository to do the workshop.** You will create your own package with `ros2 pkg create` in Exercise 1. The `solution/` folder is a finished reference copy to compare against, not a starting point.

## Repository layout

```
turtle_controller/
├── README.md                     you are here
├── LICENSE
├── docs/
│   ├── workshop_exercises.md     the exercises you work through
│   └── complete_tutorial.md      worked solution for every exercise
└── solution/
    ├── README.md                 how to build and run the reference package
    └── turtle_controller/        the finished ROS 2 package
```

## Licence

Apache License 2.0. See [LICENSE](LICENSE).
