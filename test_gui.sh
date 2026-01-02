#!/bin/bash
. /opt/ros/rolling/setup.bash

mkdir -p /home/user /home/plantroid
ln -sf /workspace /home/user/rooted
ln -sf /workspace /home/plantroid/rooted

apt-get update -qq
apt-get install -y -qq python3-pip python3-kivy espeak-ng mesa-utils libgl1-mesa-glx >/dev/null 2>&1
pip3 install --break-system-packages --quiet wikipedia beepy nltk PyDictionary ollama SpeechRecognition 2>/dev/null || true

# Force software rendering for OpenGL
export LIBGL_ALWAYS_SOFTWARE=1
export KIVY_GL_BACKEND=sdl2

colcon build 2>&1 | grep "Summary"

. install/setup.bash

echo ""
echo "=== Launching ROOTED with GUI ==="
ros2 launch rooted_launchers pc_launch.py
