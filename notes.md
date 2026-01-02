- Just use docker with ROS image, do not care about deployemnt.

![1763396107202](image/notes/1763396107202.png)

![1763396417346](image/notes/1763396417346.png)

#!/bin/sh
xhost +
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
