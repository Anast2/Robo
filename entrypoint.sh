#!/bin/bash

# ROS Docker Entrypoint
# Automatically sources ROS environment

echo "🤖 Setting up ROS environment..."

# Source ROS setup
if [ -f "/opt/ros/rolling/setup.bash" ]; then
    . /opt/ros/rolling/setup.bash
    echo "✓ Sourced ROS rolling"
    echo "ROS_DISTRO: $ROS_DISTRO"
else
    echo "⚠️  ROS setup file not found at /opt/ros/rolling/setup.bash"
    exit 1
fi

# If no command provided, start bash
if [ $# -eq 0 ]; then
    echo "Starting bash shell... Type 'colcon build' to build packages"
    exec bash
else
    exec bash -c "$*"
fi

