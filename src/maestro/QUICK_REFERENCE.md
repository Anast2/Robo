# Maestro Quick Reference Guide

## State Machine Quick Reference

### Dialogue States

```
State                │ Purpose                      │ Next Possible States
─────────────────────┼──────────────────────────────┼─────────────────────────────
Silent               │ Idle monitoring              │ SpokeToMe, CheckProblemAndBusy
SpokeToMe            │ Verify user intent           │ Silent, BusyCheck
BusyCheck            │ Check availability           │ LookAtUser, AnnounceBusy
LookAtUser           │ Orient to person             │ StartDialogue2
AnnounceBusy         │ Explain unavailability       │ Goodbye
StartDialogue1       │ Robot-initiated greeting     │ AskIfHumanIsAvailable
StartDialogue2       │ Response to human            │ AnswerHuman
AskIfHumanIsAvailable│ Check user availability      │ AnnounceProblem, Goodbye
AnnounceProblem      │ Explain problem              │ WaitHumanQuestion1
AnswerHuman          │ Process response             │ WaitHumanQuestion1/2
WaitHumanQuestion1   │ Wait after problem           │ AnswerHuman, ClearProblem
WaitHumanQuestion2   │ Wait in normal dialogue      │ AnswerHuman, Goodbye
ClearProblem         │ Conclude problem report      │ Goodbye
CheckProblemAndBusy  │ Evaluate intervention need   │ Silent, StartDialogue1
Goodbye              │ End conversation             │ Silent
```

### Dialogue Events

```
Event              │ Trigger                          │ Source
───────────────────┼──────────────────────────────────┼─────────────────────
alone              │ No humans detected               │ PersonDetector
saw_human          │ Person detected visually         │ PersonDetector
heard_human        │ Voice activity detected          │ ListeningModule
yes                │ Affirmative response             │ Speech processing
no                 │ Negative response                │ Speech processing
busy               │ Robot executing task             │ BusyChecker
idle               │ Robot available                  │ BusyChecker
problem_detected   │ Sensor threshold exceeded        │ Sensor monitoring
no_problem         │ All sensors nominal              │ Sensor monitoring
dialogue_init      │ Ready to start conversation      │ Internal
robot_finished     │ Robot completed utterance        │ TTS completion
human_question     │ User asks question               │ NLP analysis
timeout            │ Wait period expired              │ Timer
dialogue_end       │ Conversation concluded           │ Internal
```

## ROS Interface Quick Reference

### Topics

```
Topic Name          │ Type   │ Direction │ Purpose
────────────────────┼────────┼───────────┼────────────────────────────────
messageTopic        │ String │ Subscribe │ Human speech + metadata
notificationTopic   │ String │ Subscribe │ Sensor alerts
seenTopic           │ String │ Subscribe │ Person detection events
speechTopic         │ String │ Publish   │ Robot speech output
emotionTopic        │ String │ Publish   │ Facial expression commands
ListenBlockTopic    │ String │ Publish   │ Echo prevention signal
```

### Services

```
Service Name    │ Type    │ Purpose
────────────────┼─────────┼─────────────────────────────────
camera          │ Camera  │ Vision requests (emotion, person, scene)
sensors_server  │ Sensors │ Environmental sensor readings
llm_server      │ LLM     │ Language model queries
busy            │ Gesture │ Robot busy state check/set
```

### Message Formats

**messageTopic:**
```
"text;metadata;voice_emotion"
Example: "Hello robot;timestamp;happy"
```

**notificationTopic:**
```
"sensor_name:level:priority"
Example: "Water:too low:urgent"
```

**speechTopic:**
```
[("text1", [speed, pitch, volume]), ("text2", [speed, pitch, volume])]
Example: [("Hello!", [150, 100, 45])]
```

## ChatBot Patterns Quick Reference

### Special Command Patterns

```
Pattern                      │ Response Format   │ Action
─────────────────────────────┼───────────────────┼─────────────────────────
"what is X"                  │ "wikipedia:X"     │ Fetch Wikipedia summary
"who was X"                  │ "wikipedia:X"     │ Fetch Wikipedia summary
"what is the meaning of X"   │ "dictionary:X"    │ Look up definition
"what do you see"            │ "vision_check"    │ Request scene description
"(.*)soil moisture(.*)"      │ "sensor:3"        │ Read sensor 3
"(.*)soil nitrogen(.*)"      │ "sensor:8"        │ Read sensor 8
"(.*)soil phosphorus(.*)"    │ "sensor:9"        │ Read sensor 9
"(.*)soil potassium(.*)"     │ "sensor:10"       │ Read sensor 10
"(.*)temperature(.*)"        │ "sensor:4"        │ Read sensor 4
"{(.*)}"                     │ "not_proc"        │ Process notifications
```

### Sensor ID Reference

```
ID │ Sensor           │ Unit          │ Typical Range
───┼──────────────────┼───────────────┼──────────────
0  │ Right ear light  │ lux           │ 0-10000
1  │ Tail light       │ lux           │ 0-10000
2  │ Left ear light   │ lux           │ 0-10000
3  │ Soil moisture    │ percent       │ 0-100
4  │ Temperature      │ Celsius       │ 10-40
6  │ Salinity (EC)    │ dS/cm         │ 0-5
7  │ pH               │ unitless      │ 4-9
8  │ Nitrogen         │ mg/kg         │ 0-500
9  │ Phosphorus       │ mg/kg         │ 0-200
10 │ Potassium        │ mg/kg         │ 0-1000
```

## Emotion Quick Reference

### Emotion Values

```
Value     │ Description
──────────┼────────────────────────────────────────
neutral   │ No strong emotion, calm
happy     │ Positive, joyful, excited
sad       │ Negative, disappointed, low energy
anger     │ Frustrated, irritated, hostile
surprise  │ Unexpected, startled
```

### Emotion Mapping (Improve Strategy)

```
User Emotion │ Robot Response │ Strategy
─────────────┼────────────────┼──────────────────────
neutral      │ neutral        │ Match baseline
happy        │ happy          │ Share positive emotion
sad          │ happy          │ Cheer up user
anger        │ neutral        │ De-escalate
surprise     │ neutral        │ Provide calm
```

### Prosody Parameters by Emotion

```
Emotion   │ Speed │ Pitch │ Volume │ Perceived As
──────────┼───────┼───────┼────────┼──────────────────────
neutral   │  150  │  100  │   45   │ Normal conversation
happy     │  160  │  140  │   65   │ Enthusiastic
sad       │   80  │   80  │   35   │ Melancholic
angry     │  180  │  200  │   55   │ Intense
surprise  │  200  │   80  │   65   │ Excited/startled
```

## Common Operations

### Initialize System

```python
rclpy.init()
maestro_thread = Thread(target=maestro)
person_detection_thread = Thread(target=person_detection)
maestro_thread.start()
person_detection_thread.start()
```

### Trigger State Transition

```python
plantroid_dialogue_state_machine.transition("heard_human")
```

### Get Current State

```python
current_state = plantroid_dialogue_state_machine.get_current_state()
```

### Check Robot Busy Status

```python
busy_check.send_request("get")
# Wait for response...
if response:
    robot_state_machine.transition("move")
else:
    robot_state_machine.transition("finished")
```

### Get Sensor Reading

```python
sensor_reader.send_request(sensor_id)  # e.g., 3 for moisture
# Wait for response...
value = sensor_reader.future.result().sensor_reading
```

### Get Vision Data

```python
vision_control.send_request(request_type)
# Types:
# 0 = emotion detection
# 3 = person detection
# 8 = scene description
```

### Query LLM

```python
llm.send_request(model="llama3", prompt=user_input)
# Wait for response...
response = llm.future.result().response
```

### Publish Speech

```python
msg = String()
msg.data = str([("Hello!", [150, 100, 45])])
publisher_speech.publish(msg)
```

### Set Facial Expression

```python
msg = String()
msg.data = "happy"  # or "sad", "neutral", "thirsty"
publisher_emotion.publish(msg)
```

## Debugging Quick Reference

### Enable Logging

```python
# In MAESTRO.py, modify:
logging = 1  # or higher level
```

### Check State Machine Status

```python
print(f"Dialogue: {plantroid_dialogue_state_machine.get_current_state()}")
print(f"Robot: {plantroid_state_machine.get_current_state()}")
print(f"Problem: {plantroid_problem_state_machine.get_current_state()}")
```

### Monitor Topics

```bash
ros2 topic echo /messageTopic
ros2 topic echo /speechTopic
ros2 topic echo /emotionTopic
ros2 topic echo /notificationTopic
ros2 topic echo /seenTopic
```

### Check Service Availability

```bash
ros2 service list
ros2 service type /camera
ros2 service type /sensors_server
ros2 service type /llm_server
ros2 service type /busy
```

### Test Pattern Matching

```python
from ChatBot import chatter
response = chatter("what is the soil moisture")
print(response)  # Should return "sensor:3"
```

### Test Sentiment Analysis

```python
from ChatBot import sentiment_analysis
emotion = sentiment_analysis("I am very happy today")
print(emotion)  # Should return "happy"
```

## Configuration Paths

### Files to Update

```
dialogue.json location:
  Line 239 in MAESTRO.py
  Default: '/location/of/your/dialogue.json'

PersonSeeker.py location:
  Line 262 in MAESTRO.py
  Default: "/location/of/this/package/PersonSeeker.py"
```

### Environment Variables (Suggested)

```bash
export MAESTRO_HOME=/path/to/maestro
export MAESTRO_DIALOGUES=$MAESTRO_HOME/dialogue.json
export MAESTRO_IMAGE_FOLDER=$MAESTRO_HOME/IMG
```

## Performance Benchmarks

### Expected Latencies

```
Operation                    │ Typical Time │ Timeout
─────────────────────────────┼──────────────┼─────────
Service connection           │ 1-5 sec      │ 5 sec
Camera request               │ 100-500 ms   │ N/A
Sensor reading               │ 50-200 ms    │ N/A
LLM query (llama3)           │ 1-5 sec      │ N/A
Sentiment analysis (local)   │ 100-300 ms   │ N/A
Pattern matching             │ 1-10 ms      │ N/A
State transition             │ <1 ms        │ N/A
PersonSeeker rotation        │ 2-10 sec     │ N/A
```

## Error Codes & Messages

### Common Errors

```
"Sensor service not available, waiting again..."
  → sensors_server node not running

"Camera service not available, waiting again..."
  → vision_module node not running

"LLM service not available, waiting again..."
  → rooted_llm node not running

"Service call failed"
  → Service node crashed or network issue

"Error, event not present in the event set for current state"
  → Invalid state transition attempted
```

## Testing Commands

### Manual State Injection

```bash
# Simulate person detected
ros2 topic pub /seenTopic std_msgs/String "data: 'Seen'"

# Simulate sensor alert
ros2 topic pub /notificationTopic std_msgs/String "data: 'Water:too low:urgent'"

# Simulate speech input
ros2 topic pub /messageTopic std_msgs/String "data: 'Hello robot;metadata;happy'"
```

### Service Testing

```bash
# Test camera service
ros2 service call /camera rooted_msgs/srv/Camera "{imagetype: 3}"

# Test sensor service
ros2 service call /sensors_server rooted_msgs/srv/Sensors "{sensor_number: 3}"

# Test LLM service
ros2 service call /llm_server rooted_msgs/srv/LLM "{model: 'llama3', prompt: 'Hello'}"
```

## Recovery Procedures

### Stuck in State

```python
# Force state reset
plantroid_dialogue_state_machine.set_current_state("Silent")
plantroid_state_machine.set_current_state("Free")
plantroid_problem_state_machine.set_current_state("OK")
```

### Clear Notifications

```python
# In MAESTROmainNode instance
self.notifications = {}
plantroid_problem_state_machine.transition("problem_cleared")
```

### Restart Detection

```python
# Stop and restart PersonDetector thread
person_detection_thread.join()
person_detection_thread = Thread(target=person_detection)
person_detection_thread.start()
```

## Best Practices

1. Always check service availability before calling
2. Handle service call exceptions gracefully
3. Clear notification dictionary after announcing
4. Update state machines atomically
5. Use emotion fusion for robustness
6. Provide LLM fallback for unknown queries
7. Log state transitions for debugging
8. Test state machine validity on initialization
9. Use timeout for waiting states
10. Clean up threads on shutdown

