#!/bin/bash

# Launch script for ROOTED - builds and runs with GUI support
# For macOS: requires XQuartz (brew install --cask xquartz)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== ROOTED Launch Script ==="

# Detect OS and setup display
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS"

    # Check for XQuartz
    if command -v xhost &> /dev/null; then
        # Start XQuartz if not running
        if ! pgrep -x "Xquartz" > /dev/null && ! pgrep -x "X11" > /dev/null; then
            echo "Starting XQuartz..."
            open -a XQuartz
            sleep 3
        fi

        # Allow connections from localhost
        xhost +localhost 2>/dev/null || xhost + 2>/dev/null || true

        # Get host IP for X11 forwarding
        HOST_IP=$(ipconfig getifaddr en0 2>/dev/null || echo "host.docker.internal")
        export DISPLAY="${HOST_IP}:0"
        echo "DISPLAY set to: $DISPLAY"
    else
        echo "WARNING: XQuartz not found. Running without GUI."
        echo "For GUI support, install: brew install --cask xquartz"
        export DISPLAY=""
    fi
else
    echo "Detected Linux"
    # Allow local connections for X11
    xhost +local:docker 2>/dev/null || true
    export DISPLAY="${DISPLAY:-:0}"
fi

echo ""
echo "Building and launching in Docker container..."
echo ""

# Run build and launch in Docker
# Use -it only if running interactively
DOCKER_TTY=""
if [ -t 0 ]; then
    DOCKER_TTY="-it"
fi

docker run --rm $DOCKER_TTY \
    --name plantroid_launcher \
    --network host \
    --privileged \
    -e DISPLAY="$DISPLAY" \
    -e QT_X11_NO_MITSHM=1 \
    -v "$SCRIPT_DIR":/workspace \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -w /workspace \
    osrf/ros:rolling-desktop-full \
    bash -c '
        set -e
        echo "=== Setting up ROS environment ==="
        . /opt/ros/rolling/setup.bash

        echo ""
        echo "=== Installing system dependencies ==="
        apt-get update -qq
        apt-get install -y -qq python3-pip python3-kivy espeak-ng >/dev/null 2>&1 || true

        echo ""
        echo "=== Installing Python dependencies ==="
        pip3 install --break-system-packages --quiet nltk transformers wikipedia PyDictionary SpeechRecognition beepy ollama 2>/dev/null || true

        echo ""
        echo "=== Setting up path symlinks for launch files ==="
        mkdir -p /home/user /home/plantroid
        ln -sf /workspace /home/user/rooted
        ln -sf /workspace /home/plantroid/rooted

        echo ""
        echo "=== Building workspace ==="
        colcon build

        echo ""
        echo "=== Sourcing workspace ==="
        . install/setup.bash

        echo ""
        echo "=== Launching ROOTED system ==="
        ros2 launch rooted_launchers pc_launch.py
    '
