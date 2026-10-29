# Quick Start Guide

Get up and running with the Turtle Controller package in 5 minutes!

## Installation

```bash
# 1. Create workspace
mkdir -p ~/turtle_ws/src
cd ~/turtle_ws/src

# 2. Clone this repository
git clone https://github.com/captain-bender/turtle_controller.git turtle_controller

# 3. Build the package
cd ~/turtle_ws
colcon build

# 4. Source the workspace
source install/setup.bash
```

## Quick Test

**Launch everything at once:**

```bash
ros2 launch turtle_controller turtle_system_launch.py
```

**Try checking turtle status (in a new terminal):**

```bash
source ~/turtle_ws/install/setup.bash
ros2 run turtle_controller turtle_status_client
```

## Troubleshooting

**Issue**: Package not found after building
```bash
# Solution: Make sure to source the workspace
source ~/turtle_ws/install/setup.bash
```

**Issue**: Turtlesim window doesn't open
```bash
# Solution: Install turtlesim if missing
sudo apt install ros-humble-turtlesim
```

**Issue**: Permission denied
```bash
# Solution: Make scripts executable
chmod +x ~/turtle_ws/src/turtle_controller/turtle_controller/*.py
```

## Testing Individual Components

**Test publisher only:**
```bash
# Terminal 1
ros2 run turtlesim turtlesim_node

# Terminal 2
ros2 run turtle_controller velocity_publisher
```

**Test subscriber only:**
```bash
# Terminal 1
ros2 run turtlesim turtlesim_node

# Terminal 2
ros2 run turtle_controller pose_subscriber

# Terminal 3 - Move turtle manually
ros2 run turtlesim turtle_teleop_key
```