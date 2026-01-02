#!/bin/bash

# Build script for Rooted project
# Automatically sources ROS and runs colcon build

set -e

echo "🤖 Setting up ROS environment..."

# Source ROS setup
if [ -f "/opt/ros/rolling/setup.bash" ]; then
    . /opt/ros/rolling/setup.bash
    echo "✓ Sourced ROS rolling"
    echo "  ROS_DISTRO: $ROS_DISTRO"
    echo "  CMAKE_PREFIX_PATH: $CMAKE_PREFIX_PATH"
else
    echo "❌ ROS setup file not found at /opt/ros/rolling/setup.bash"
    exit 1
fi

echo ""
echo "🔨 Building packages..."
echo ""

# Run colcon build
colcon build "$@"

