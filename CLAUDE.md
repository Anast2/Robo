# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ROOTED (Open Source toolkit for Dialogue Systems in Human Robot Interaction) is a ROS 2-based social robot framework for a plant-care robot called "Plantroid". The system handles multi-modal dialogue (speech, vision, sensors), emotional response, and robotic control.

## Build Commands

```bash
# Build everything (sources ROS automatically)
./build.sh

# Or manually:
source /opt/ros/rolling/setup.bash
colcon build

# Build specific package
colcon build --packages-select <package_name>

# Build with symlink install (faster iteration)
colcon build --symlink-install

# After building, source the workspace
source install/setup.bash
```

## Testing

```bash
# Run all tests (linting: flake8, pep257, copyright)
colcon test

# Test specific package
colcon test --packages-select <package_name>

# View test results
colcon test-result --verbose
```

Note: Tests are primarily style/lint checks. No functional unit tests exist currently.

## Running the System

```bash
# One-command build and launch with GUI (requires Docker)
# On macOS: also requires XQuartz (brew install --cask xquartz)
./launch.sh

# Or manually in Docker:
docker run -it --rm --network host -v $(pwd):/workspace -w /workspace osrf/ros:rolling-desktop-full bash
# Then inside container:
source /opt/ros/rolling/setup.bash
colcon build
source install/setup.bash
ros2 launch rooted_launchers pc_launch.py

# Launch individual packages
ros2 launch maestro maestro_launch.py
ros2 launch facial_expression facial_expression_launch.py
ros2 launch other_sensors fake_sensors_launch.py
```

## Architecture

### Core Orchestration: Maestro

The `maestro` package is the central brain, running 3 concurrent state machines:
- **Dialogue State Machine** (15 states): Manages conversation flow from Silent → SpokeToMe → AnswerHuman → Goodbye
- **Robot State Machine** (2 states): Free/Busy for task availability
- **Problem State Machine** (2 states): OK/Problem for sensor alerts

Key components in `src/maestro/maestro/`:
- `MAESTRO.py`: Main orchestration node (~470 lines)
- `ChatBot.py`: NLTK pattern matching + sentiment analysis (EmTract-DistilBERT)
- `simple_state_machine.py`: Generic FSM implementation

### Interface Layer: rooted_interfaces

The `rooted_interfaces` package provides a unified service abstraction layer. All packages communicate through this layer rather than directly. Interface classes in `src/rooted_interfaces/rooted_interfaces/`:
- `sensors_interface.py` → other_sensors
- `vision_interface.py` → vision_module
- `llm_interface.py` → rooted_llm
- `tts_interface.py` → rooted_speech_synthesizer
- `gestures_interface.py` → rooted_gestures
- etc.

### Message Definitions: rooted_msgs

Custom ROS messages/services/actions in `src/rooted_msgs/`. This is the only CMake package (ament_cmake); all others use ament_python.

### ROS Communication Pattern

**Topics (Pub/Sub):**
- `messageTopic`: Human speech from listening_module (format: `"text;metadata;voice_emotion"`)
- `speechTopic`: Robot speech output (format: `[("text", [speed, pitch, volume])]`)
- `emotionTopic`: Facial expression commands (values: neutral, happy, sad, anger, surprise)
- `notificationTopic`: Sensor alerts (format: `"sensor_name:level:priority"`)
- `seenTopic`: Person detection events

**Services (RPC):**
- `/camera` (Camera.srv): Vision requests (0=emotion, 3=person, 8=scene)
- `/sensors_server` (Sensors.srv): Environmental sensor readings
- `/llm_server` (LLM.srv): Ollama LLM queries
- `/busy` (Busy.srv): Robot availability state

## Package Structure

16 packages total, organized by function:

**Input:** listening_module (STT), vision_module (camera/emotion), other_sensors (environmental)

**Output:** rooted_speech_synthesizer (TTS with prosody), facial_expression (emotion GUI)

**Behavior:** rooted_busy, rooted_gestures, plantroid_neck, movement_module, rooted_encoder

**Data:** robot_memory (conversation storage), rooted_llm (Ollama integration), plant_model

**Infrastructure:** rooted_msgs, rooted_interfaces, rooted_launchers

## Debugging

```bash
# Monitor topics
ros2 topic echo /messageTopic
ros2 topic echo /speechTopic
ros2 topic echo /emotionTopic

# Check service availability
ros2 service list

# Manual topic injection for testing
ros2 topic pub /seenTopic std_msgs/String "data: 'Seen'"
ros2 topic pub /messageTopic std_msgs/String "data: 'Hello robot;metadata;happy'"

# Test services
ros2 service call /sensors_server rooted_msgs/srv/Sensors "{sensor_number: 3}"
ros2 service call /camera rooted_msgs/srv/Camera "{imagetype: 3}"
```

## Sensor IDs

| ID | Sensor | ID | Sensor |
|----|--------|----|----|
| 0 | Right ear light | 6 | Salinity (EC) |
| 1 | Tail light | 7 | pH |
| 2 | Left ear light | 8 | Nitrogen |
| 3 | Soil moisture | 9 | Phosphorus |
| 4 | Temperature | 10 | Potassium |

## Key Configuration Files

- `src/maestro/maestro/dialogue.json`: Dialogue templates per state
- `src/rooted_launchers/launch/pc_launch.py`: Full system launch with all parameters
- Package entry points defined in each package's `setup.py`

## Known Issues (from ARCHITECTURE.md)

1. PersonSeeker uses hardcoded paths with `os.system()`
2. MemoryAccess class incomplete (has TODO)
3. Hardcoded file paths for dialogue.json and PersonSeeker.py
4. State machine wait states have no timeout handling