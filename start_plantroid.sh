#!/bin/bash

# Start Plantroid ROS Docker Container
# This script sets up and runs the ROS rolling desktop full environment with X11 and necessary mounts

docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /etc/sudoers.d:/etc/sudoers.d:ro \
  --net host \
  -v /home:/home \
  -v ~/Volumes:/home/usr/ \
  -v /media:/media \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v ${XDG_RUNTIME_DIR}/pipewire-0:${XDG_RUNTIME_DIR}/pipewire-0 \
  -e PIPEWIRE_RUNTIME_DIR=${XDG_RUNTIME_DIR}/pipewire-0 \
  --device /dev/snd:/dev/snd \
  --privileged \
  osrf/ros:rolling-desktop-full

