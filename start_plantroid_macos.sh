#!/bin/bash

# Start Plantroid ROS Docker Container - macOS Version
# This script sets up and runs the ROS rolling desktop full environment
# Note: X11 forwarding on macOS requires XQuartz to be installed
# Install with: brew install --cask xquartz

# Check if XQuartz is installed (optional, for GUI support)
if ! command -v xhost &> /dev/null; then
    echo "⚠️  XQuartz not found. GUI applications may not work."
    echo "Install with: brew install --cask xquartz"
    echo "Continuing without X11 forwarding..."
fi

# Get the IP address of the host machine on the Docker bridge network
HOST_IP=$(ifconfig | grep -A 1 "en0" | grep inet | awk '{print $2}' | head -1)

if [ -z "$HOST_IP" ]; then
    echo "⚠️  Could not determine host IP. Trying alternative method..."
    HOST_IP="host.docker.internal"
fi

echo "🐳 Starting ROS Docker container..."
echo "Host IP: $HOST_IP"

docker run -it --rm \
  -e DISPLAY=$HOST_IP:0 \
  --net host \
  -v $(pwd):/workspace \
  -v /tmp:/tmp \
  -w /workspace \
  osrf/ros:rolling-desktop-full \
  bash

