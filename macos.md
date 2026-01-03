# Running ROOTED GUI on macOS

## Prerequisites

1. **Install XQuartz** (X11 server for macOS):
   ```bash
   brew install --cask xquartz
   ```

2. **Configure XQuartz for network connections**:
   ```bash
   # Allow TCP connections
   defaults write org.xquartz.X11 nolisten_tcp -bool false
   ```

3. **Restart XQuartz** (or log out and back in)

## Running

```bash
./launch.sh
```

The script will:
- Start XQuartz if not running
- Allow localhost connections (`xhost +localhost`)
- Build and launch the ROS 2 system in Docker with X11 forwarding

## Troubleshooting

### GUI not displaying

1. Ensure XQuartz is running:
   ```bash
   open -a XQuartz
   ```

2. Allow connections:
   ```bash
   xhost +localhost
   ```

3. Verify DISPLAY is set:
   ```bash
   echo $DISPLAY  # Should show something like "192.168.x.x:0"
   ```

### OpenGL errors on Apple Silicon

The Docker image runs x86_64 emulation on ARM Macs, which can cause OpenGL issues. The launch script sets software rendering (`LIBGL_ALWAYS_SOFTWARE=1`) to mitigate this.

### "Cannot open display" error

Restart XQuartz with TCP listening enabled:
```bash
killall Xquartz
defaults write org.xquartz.X11 nolisten_tcp -bool false
open -a XQuartz
sleep 3
xhost +localhost
```