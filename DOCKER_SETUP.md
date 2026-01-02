# Plantroid Docker Setup Guide

This guide explains the different ways to run the Plantroid ROS Docker container.

## Prerequisites

- Docker installed and running
- For GUI support: XQuartz installed (macOS) or X11 server running (Linux)

## Option 1: Shell Script (Linux)

**File:** `start_plantroid.sh`

```bash
./start_plantroid.sh
```

Features:
- ✅ X11 forwarding for GUI applications
- ✅ PipeWire audio support
- ✅ Sudo access configured
- ✅ Device access (sound card, etc.)
- ✅ Network host mode for ROS networking

## Option 2: Shell Script (macOS)

**File:** `start_plantroid_macos.sh`

```bash
./start_plantroid_macos.sh
```

**macOS Setup:**
1. Install XQuartz for X11 support:
   ```bash
   brew install --cask xquartz
   ```

2. Configure XQuartz for Docker:
   ```bash
   # Allow connections from network
   defaults write org.xquartz.X11 nolisten_tcp 0
   ```

3. Start XQuartz:
   ```bash
   open -a XQuartz
   ```

4. In XQuartz terminal, run:
   ```bash
   xhost +local:
   ```

Features:
- ✅ Automatic host IP detection
- ✅ Fallback to `host.docker.internal` if needed
- ✅ Home directory mounting
- ✅ Compatible with macOS networking

## Option 3: Docker Compose

**File:** `docker-compose.yml`

Start the container:
```bash
docker-compose up -d
```

Attach to the running container:
```bash
docker-compose exec plantroid bash
```

Stop the container:
```bash
docker-compose down
```

Features:
- ✅ Declarative configuration
- ✅ Easy to modify environment variables
- ✅ GPU support option (uncomment in file)
- ✅ Persistent configuration

## Environment Variables

When using Docker Compose, you can override defaults:

```bash
DISPLAY=:0 docker-compose up
```

Or set in `.env` file:
```
DISPLAY=:0
XDG_RUNTIME_DIR=/run/user/1000
```

## Troubleshooting

### GUI not appearing
- **Linux:** Check `echo $DISPLAY` returns `:0`, `:1`, etc.
- **macOS:** Ensure XQuartz is running and `xhost +local:` was executed

### Audio not working
- Check `/dev/snd` exists and is accessible
- Linux: Verify PipeWire is running on host

### Cannot connect to ROS master
- Ensure `--net host` is set (included in all scripts)
- Check firewall rules allowing ROS ports (11311, etc.)

### Permission denied errors
- Run with `sudo` if device access is required
- Or add your user to the `docker` group: `sudo usermod -aG docker $USER`

## Advanced Usage

### Build a custom image

Create a `Dockerfile`:
```dockerfile
FROM osrf/ros:rolling-desktop-full

# Add your customizations here
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
```

Build and use:
```bash
docker build -t plantroid:custom .
# Update scripts to use plantroid:custom instead of osrf/ros:rolling-desktop-full
```

### Run with specific ROS distribution

Change the image tag in scripts:
- `osrf/ros:rolling-desktop-full` → Latest rolling
- `osrf/ros:humble-desktop-full` → ROS 2 Humble
- `osrf/ros:iron-desktop-full` → ROS 2 Iron

### GPU Support

For NVIDIA GPU support, install NVIDIA Container Runtime and uncomment GPU section in `docker-compose.yml`.


