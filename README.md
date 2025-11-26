# Turtle Controller - ROS 2 Humble Tutorial Package

A comprehensive beginner-friendly ROS 2 package demonstrating fundamental concepts using the turtlesim simulator. This package includes examples of publishers, subscribers, services, clients, and launch files.

## Overview

This package is designed as a complete learning resource for ROS 2 beginners. It demonstrates:

- **Topic Publishers** - Sending velocity commands to control turtle movement
- **Topic Subscribers** - Receiving and displaying turtle pose information
- **Service Servers** - Providing status checking services
- **Service Clients** - Calling status checking services
- **Launch Files** - Starting multiple nodes simultaneously

You should see output similar to: `ros2 cli version: 0.18.x`

## Package Structure

```
turtle_controller/
├── launch/
│   ├── turtle_system_launch.py          # Basic launch file
├── turtle_controller/
│   ├── __init__.py
│   ├── velocity_publisher.py            # Publishes velocity commands
│   ├── pose_subscriber.py               # Subscribes to turtle pose
│   ├── turtle_status_service.py         # Service server for status checking
│   └── turtle_status_client.py          # Service client for status checking
├── package.xml                          # Package metadata
├── setup.py                             # Python package setup
├── setup.cfg                            # Package configuration
└── README.md                            # This file
```

## Quick Start

### 1. Create Workspace and Clone Package

```bash
# Create workspace
mkdir -p ~/turtle_ws/src
cd ~/turtle_ws/src

# Clone or copy this package into src/
# (If you created it manually, skip this step)

cd ~/turtle_ws
```

### 2. Install Dependencies

```bash
rosdep install --from-paths src --ignore-src -r -y
```

### 3. Build the Package

```bash
cd ~/turtle_ws
colcon build
source install/setup.bash
```

### 4. Launch the Complete System

```bash
ros2 launch turtle_controller turtle_system_launch.py
```

You should see:
- Turtlesim window opens
- Turtle moves in a circle
- Pose information printed to terminal

## Nodes Description

### 0. Run the turlesim simulation
```bash
ros2 run turtlesim turtlesim_node
```

### 1. Velocity Publisher (`velocity_publisher`)

Publishes `Twist` messages to `/turtle1/cmd_vel` to make the turtle move in a circular pattern.

**Run standalone:**
```bash
ros2 run turtle_controller velocity_publisher
```

**Topics Published:**
- `/turtle1/cmd_vel` (geometry_msgs/msg/Twist) - Velocity commands

### 2. Pose Subscriber (`pose_subscriber`)

Subscribes to `/turtle1/pose` and displays the turtle's position and orientation.

**Run standalone:**
```bash
ros2 run turtle_controller pose_subscriber
```

**Topics Subscribed:**
- `/turtle1/pose` (turtlesim/msg/Pose) - Turtle position and orientation

### 3. Turtle Status Service (`turtle_status_service`)

Provides a service to check if the turtle is near the center of the window.

**Run standalone:**
```bash
ros2 run turtle_controller turtle_status_service
```

**Services Provided:**
- `/check_turtle_status` (std_srvs/srv/Trigger) - Check if turtle is near center

**Call the service manually:**
```bash
ros2 service call /check_turtle_status std_srvs/srv/Trigger
```

### 4. Turtle Status Client (`turtle_status_client`)

A command-line client that calls the turtle status service.

**Usage:**
```bash
ros2 run turtle_controller turtle_status_client
```

**Example output:**
```
✓ Turtle is near center! Position: (5.54, 5.54)
```

## Usage Examples

### Example 1: Manual Turtle Control with Pose Monitoring

**Terminal 1** - Start turtlesim:
```bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2** - Monitor pose:
```bash
ros2 run turtle_controller pose_subscriber
```

**Terminal 3** - Control with keyboard:
```bash
ros2 run turtlesim turtle_teleop_key
```

### Example 2: Automatic Movement with Status Checking

**Terminal 1** - Launch system:
```bash
ros2 launch turtle_controller turtle_system_launch.py
```

**Terminal 2** - Check turtle status:
```bash
ros2 run turtle_controller turtle_status_client
```

**Terminal 3** - Move turtle manually:
```bash
ros2 run turtlesim turtle_teleop_key
```

**Terminal 2** - Check status again after moving:
```bash
ros2 run turtle_controller turtle_status_client
```


## Development

### Building After Changes

After modifying any Python files:

```bash
cd ~/turtle_ws
colcon build --packages-select turtle_controller
source install/setup.bash
```

### Adding New Nodes

1. Create your Python script in `turtle_controller/`
2. Make it executable: `chmod +x your_script.py`
3. Add entry point in `setup.py`:
   ```python
   entry_points={
       'console_scripts': [
           'your_node = turtle_controller.your_script:main',
       ],
   },
   ```
4. Rebuild the package

### Testing Individual Components

**Test publisher only:**
```bash
# Terminal 1
ros2 run turtlesim turtlesim_node

# Terminal 2
ros2 run turtle_controller velocity_publisher
```

**Test service:**
```bash
# Terminal 1
ros2 run turtlesim turtlesim_node

# Terminal 2
ros2 run turtle_controller turtle_status_service

# Terminal 3
ros2 run turtle_controller turtle_status_client
```

## Troubleshooting

### Issue: "Package 'turtle_controller' not found"

**Solution:**
```bash
cd ~/turtle_ws
source install/setup.bash
```

### Issue: "No executable found"

**Solution:**
1. Check that entry points are correctly added in `setup.py`
2. Rebuild: `colcon build --packages-select turtle_controller`
3. Source: `source install/setup.bash`

### Issue: Service or topic not found

**Solution:**
1. Ensure turtlesim is running: `ros2 run turtlesim turtlesim_node`
2. List available topics: `ros2 topic list`
3. List available services: `ros2 service list`

### Issue: "Permission denied" when running scripts

**Solution:**
```bash
chmod +x ~/turtle_ws/src/turtle_controller/turtle_controller/*.py
```

### Issue: Import errors

**Solution:**
```bash
# Install missing dependencies
rosdep install --from-paths src --ignore-src -r -y
colcon build
source install/setup.bash
```

##  Useful Commands

### Inspect Running System

```bash
# List all nodes
ros2 node list

# List all topics
ros2 topic list

# See topic info
ros2 topic info /turtle1/cmd_vel

# Echo topic messages
ros2 topic echo /turtle1/pose

# List services
ros2 service list

# See service type
ros2 service type /rotate_turtle

# View computational graph
rqt_graph
```

### Debugging

```bash
# Run with debug output
ros2 run turtle_controller velocity_publisher --ros-args --log-level debug

# Check node info
ros2 node info /velocity_publisher

# Monitor topic frequency
ros2 topic hz /turtle1/cmd_vel
```