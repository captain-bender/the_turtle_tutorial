# Examples Directory

This directory contains additional example scripts that demonstrate various ROS 2 concepts and turtle movement patterns.

## Available Examples

### movement_patterns.py

Demonstrates different turtle movement patterns by varying linear and angular velocities.

**Patterns included:**
- Circle: Constant forward + rotation
- Square: Alternating forward and turn
- Forward: Straight line
- Spin: Rotation in place

**How to use:**

1. Start turtlesim:
```bash
ros2 run turtlesim turtlesim_node
```

2. Run the example:
```bash
cd ~/turtle_ws/src/turtle_controller/examples
chmod +x movement_patterns.py
python3 movement_patterns.py
```

**Experiment:**
Try modifying the pattern variable and velocity values to create your own movement patterns!
