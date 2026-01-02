# Maestro Module Architecture

## Overview

The Maestro module is the central orchestration system for the Plantroid social robot. It coordinates multi-modal human-robot interaction by managing conversations, emotions, sensor monitoring, and behavioral state machines.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MAESTRO MAIN NODE                           │
│                                                                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │ Dialogue State   │  │ Robot State      │  │ Problem State    │   │
│  │ Machine          │  │ Machine          │  │ Machine          │   │
│  │ (15 states)      │  │ (Free/Busy)      │  │ (OK/Problem)     │   │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │               Service Clients & Interfaces                   │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐  │   │
│  │  │ Camera  │ │ Sensors │ │   LLM   │ │  Busy   │ │ Memory │  │   │
│  │  │ Service │ │ Service │ │ Service │ │ Checker │ │ Access │  │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └────────┘  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                   ROS Topics (Pub/Sub)                       │   │
│  │  • messageTopic (input)                                      │   │
│  │  • notificationTopic (input)                                  │   │
│  │  • seenTopic (input)                                         │   │
│  │  • speechTopic (output)                                      │   │
│  │  • emotionTopic (output)                                     │   │
│  │  • ListenBlockTopic (output)                                 │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────┐                  ┌──────────────────┐
│ PersonDetector   │                  │  PersonSeeker    │
│      Node        │                  │     Module       │
│                  │                  │                  │
│ • Vision Check   │                  │ • Rotate to find │
│ • Publishes to   │                  │ • Motor control  │
│   seenTopic      │                  │ • Track person   │
└──────────────────┘                  └──────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        ChatBot Module                           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Pattern Matching Engine (NLTK Chat)                    │  │
│  │  • 40+ predefined patterns                              │  │
│  │  • Special commands: wikipedia, dictionary, sensors     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Sentiment Analysis (EmTract-DistilBERT)                │  │
│  │  • 7-emotion model → 5-emotion mapping                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  NLP Utilities                                           │  │
│  │  • Question detection                                    │  │
│  │  • Command detection                                     │  │
│  │  • Subject extraction                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## State Machine Architecture

### 1. Dialogue State Machine

The dialogue state machine manages conversation flow with 15 states and 14 possible events.

```
                    ┌─────────────────────────────────────┐
                    │          Silent (Initial)           │
                    │  • Robot is idle                    │
                    │  • Monitoring for human presence    │
                    └──────┬──────────────────┬───────────┘
                           │                  │
                 heard_human│                 │saw_human
                           │                  │
                    ┌──────▼──────┐   ┌───────▼──────────────┐
                    │  SpokeToMe  │   │ CheckProblemAndBusy  │
                    │  • Verify   │   │  • Check robot state │
                    │    speech   │   │  • Check problems    │
                    └──────┬──────┘   └──────┬───────────────┘
                           │                  │
                     yes   │           problem_detected
                           │                  │
                    ┌──────▼──────┐   ┌───────▼──────────┐
                    │  BusyCheck  │   │ StartDialogue1   │
                    │             │   │  • Init problem  │
                    └──────┬──────┘   │    reporting     │
                           │          └──────────────────┘
                      idle │
                           │
                    ┌──────▼────────┐
                    │  LookAtUser   │
                    │  • Turn to    │
                    │    face user  │
                    └──────┬────────┘
                           │
                    saw_human
                           │
                    ┌──────▼────────┐
                    │StartDialogue2 │
                    │  • Greeting   │
                    └──────┬────────┘
                           │
                    ┌──────▼────────┐
                    │ AnswerHuman   │◄──┐
                    │  • Process    │   │
                    │    response   │   │human_question
                    └──────┬────────┘   │
                           │            │
              robot_finished│     ┌──────┴───────────────┐
                           │     │ WaitHumanQuestion1/2 │
                           └────►│  • Wait for input    │
                                 │  • Timeout handling  │
                                 └──────────────────────┘
                                          │
                                   timeout│
                                          │
                                 ┌────────▼────────┐
                                 │    Goodbye      │
                                 │  • End dialogue │
                                 └────────┬────────┘
                                          │
                                   dialogue_end
                                          │
                                          ▼
                                     [Silent]
```

### 2. Robot State Machine

Simple binary state tracking robot availability.

```
┌─────────────┐    move    ┌─────────────┐
│    Free     │───────────►│    Busy     │
│ (idle/ready)│            │ (executing) │
└─────────────┘◄───────────└─────────────┘
                  finished
```

### 3. Problem State Machine

Tracks sensor/plant health issues.

```
┌─────────────┐  problem_detected  ┌─────────────┐
│     OK      │───────────────────►│   Problem   │
│  (healthy)  │                    │ (needs help)│
└─────────────┘◄───────────────────└─────────────┘
                 problem_cleared
```

## Data Flow Diagrams

### Human Speech Processing Flow

```
Human Speech
     │
     ▼
┌─────────────────┐
│ ListeningModule │ (separate package)
│  • Audio capture│
│  • VAD          │
│  • STT          │
└────────┬────────┘
         │ publishes to messageTopic
         ▼
  "text;metadata;emotion"
         │
         ▼
┌────────────────────────────────────────────────────┐
│         MAESTROmainNode.cb_function()              │
│                                                    │
│  1. Parse message (text, metadata, voice emotion) │
│  2. Get face emotion (camera service)             │
│  3. Content emotion (sentiment analysis)          │
│  4. Emotion fusion (majority vote)                │
│  5. Map emotion to response strategy              │
│  6. Generate response (ChatBot + LLM)             │
│  7. Assign prosody parameters                     │
│  8. Publish to speechTopic                        │
│  9. Update facial expression                      │
│  10. Trigger PersonSeeker if needed               │
└────────────────────────────────────────────────────┘
         │
         ▼
   speechTopic
         │
         ▼
┌─────────────────────────┐
│ Speech Synthesizer Node │
│  • TTS with prosody     │
│  • Audio output         │
└─────────────────────────┘
```

### Emotion Fusion Process

```
┌──────────────────┐
│ Voice Emotion    │───┐
│ (from STT)       │   │
└──────────────────┘   │
                       │
┌──────────────────┐   │    ┌───────────────────┐
│ Content Emotion  │───┼───►│ Emotion Fusion    │
│ (sentiment NLP)  │   │    │ (majority vote)   │
└──────────────────┘   │    └─────────┬─────────┘
                       │              │
┌──────────────────┐   │              │
│ Face Emotion     │───┘              │
│ (camera vision)  │                  │
└──────────────────┘                  ▼
                              ┌────────────────┐
                              │ Final Emotion  │
                              └────────┬───────┘
                                       │
                        ┌──────────────┴──────────────┐
                        │                             │
                        ▼                             ▼
              ┌──────────────────┐         ┌──────────────────┐
              │ Response Strategy│         │ Facial Expression│
              │  • Mirror mode   │         │  • Set emotion   │
              │  • Improve mode  │         │  • Update GUI    │
              └──────────────────┘         └──────────────────┘
```

### Response Generation Flow

```
User Question: "What is the soil moisture?"
     │
     ▼
┌─────────────────────────────┐
│ ChatBot Pattern Matching    │
│                             │
│ Pattern: "(.*)soil moisture"│
│ Match: YES                  │
│ Response: "sensor:3"        │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ conversate() interprets     │
│ • Detects "sensor:" prefix  │
│ • Extracts sensor number: 3 │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ get_sensor(3)               │
│ • Calls SensorReader client │
│ • Returns: "45"             │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Format response             │
│ "current soil moisture      │
│  sensor reading is 45%"     │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ LLM Paraphrase              │
│ + emotion context           │
│ Result: "The soil moisture  │
│  is at 45 percent right now"│
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ assign_prosody()            │
│ Based on emotion: neutral   │
│ [speed:150, pitch:100,      │
│  volume:45]                 │
└──────────┬──────────────────┘
           │
           ▼
  Publish to speechTopic
```

### Notification Handling Flow

```
Sensor Alert: "Water:too low:urgent"
     │
     ▼
┌─────────────────────────────┐
│ notificationTopic           │
│ (from sensor monitoring)    │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ cb_function_notification()  │
│                             │
│ 1. Parse notification       │
│ 2. Store in dict:           │
│    {"Water": ["too low",    │
│     "urgent"]}              │
│ 3. Update problem state     │
│    machine                  │
│ 4. Set facial expression    │
│    (thirsty/sad)            │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Problem State Machine       │
│ OK → Problem                │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Wait for human interaction  │
│ (PersonDetector active)     │
└──────────┬──────────────────┘
           │
           ▼ (human detected)
┌─────────────────────────────┐
│ Dialogue State Machine      │
│ Silent → CheckProblemAndBusy│
│         → StartDialogue1    │
│         → AnnounceProblem   │
└─────────────────────────────┘
```

### Person Detection Cycle

```
┌─────────────────────────────────────────────────┐
│         PersonDetector (separate thread)        │
└──────────┬──────────────────────────────────────┘
           │ Periodic check (timer-based)
           ▼
┌─────────────────────────────┐
│ Check conditions:           │
│ • Dialogue state = Silent?  │
│ • Robot state = Free?       │
└──────────┬──────────────────┘
           │ YES
           ▼
┌─────────────────────────────┐
│ Request camera service      │
│ Type: 3 (person detection)  │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Vision response: True/False │
└──────────┬──────────────────┘
           │
           ▼ (if True)
┌─────────────────────────────┐
│ Publish to seenTopic        │
│ Message: "Seen"             │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ MAESTROmainNode receives    │
│ cb_function_seen()          │
│                             │
│ • Transition dialogue state │
│ • Check for problems        │
│ • Initiate interaction      │
└─────────────────────────────┘
```

## Component Details

### MAESTROmainNode

Main orchestration node inheriting from `rclpy.Node`.

**Subscriptions:**
- `messageTopic` (String): Human speech input with metadata
- `notificationTopic` (String): Sensor alerts and problems
- `seenTopic` (String): Person detection events

**Publications:**
- `speechTopic` (String): Robot speech output with prosody
- `emotionTopic` (String): Facial expression commands
- `ListenBlockTopic` (String): Audio echo prevention

**Service Clients:**
- `Camera` service: Vision requests (emotion detection, person detection, scene description)
- `Sensors` service: Environmental sensor readings (moisture, NPK, pH, etc.)
- `LLM` service: Language model queries for open-ended responses
- `Gesture` service: Robot busy state management

**Core Methods:**

```python
cb_function(subscribedData)
    # Main speech processing callback
    # Flow: Parse → Emotion Fusion → Generate Response → Publish

cb_function_notification(subscribedData)
    # Handle sensor alerts
    # Flow: Parse → Store → Update State → Set Expression

cb_function_seen(subscribedData)
    # Handle person detection
    # Flow: Trigger dialogue if problems exist

conversate(data, response_emotion)
    # Generate response using ChatBot + LLM
    # Handles: wikipedia, dictionary, sensors, vision

emotion_fusion(emotion_list)
    # Majority voting across emotion sources

assign_prosody(utterance, method)
    # Map emotion to speech parameters
    # [speed, pitch, volume]
```

### ChatBot Module

Pattern-based conversation system using NLTK.

**Pattern Categories:**

1. **Greetings**: "hi", "hello", "howdy" → Friendly responses
2. **Identity**: "what is your name", "who are you" → Self-introduction
3. **Knowledge Queries**:
   - Wikipedia: "what is X", "who was Y"
   - Dictionary: "what is the meaning of X"
4. **Sensor Queries**: Soil moisture, NPK, pH, temperature, light
5. **Vision Queries**: "what do you see", "describe what you see"
6. **Notification Processing**: "{...}" → Parse notifications

**Sentiment Analysis:**
- Model: EmTract-DistilBERT
- 7 emotions → 5 emotions mapping
- Emotions: neutral, happy, sad, anger, surprise

**NLP Utilities:**
- `question_detection()`: Identifies interrogative sentences
- `get_subject()`: Extracts question subject
- `is_command()`: Detects imperative sentences

### PersonSeeker Module

Behavior for finding and facing humans.

**Functionality:**
1. Request person detection from camera service
2. If not found: Rotate in place
3. When found: Stop and face person
4. Publish completion

**Integration:**
- Called by MAESTRO when transitioning to user interaction
- Uses motor command service for rotation
- Operates in separate process/thread

### StateMachine Class

Generic finite state machine implementation.

**Features:**
- States, events, transition table
- Current state tracking
- Dynamic modification (add/remove states, events, transitions)
- Validity checking on initialization
- Error handling for invalid transitions

**Usage in Maestro:**
- 3 state machines run concurrently
- Events trigger transitions based on ROS callbacks
- State queries guide behavior selection

### Utility Functions

**wikipedia_query(title):**
- Fetches 2-sentence summary from Wikipedia
- Handles missing articles gracefully

**dictionary_query(word):**
- Uses PyDictionary for word definitions
- Formats multiple grammatical forms

**gibberish():**
- Generates phoneme sequences for testing
- Used for TTS/audio system validation

## Configuration

### Global Variables (MAESTRO.py)

```python
image_folder = "./IMG/"          # Vision data storage
learning = False                 # Q-learning toggle (unused)
speech_style = 0                 # TTS style selector
logging = 0                      # Debug logging level
detect_person = 0                # Person detection enable
dialog_json = ""                 # Dialogue template path
OKAO = 0                         # Vision system toggle
```

### Dialogue Templates (dialogue.json)

Predefined responses for each dialogue state. Supports:
- Multiple response variants (random selection)
- Template variables `{}`
- Timeout counters for waiting states

### Sensor Mapping

```
ID  │ Sensor Type        │ Unit
────┼────────────────────┼──────────────────────
 0  │ Right ear light    │ lux
 1  │ Tail light         │ lux
 2  │ Left ear light     │ lux
 3  │ Soil moisture      │ percent
 4  │ Temperature        │ Celsius
 5  │ None               │ -
 6  │ Salinity (EC)      │ dS/cm
 7  │ pH                 │ unitless
 8  │ Nitrogen (N)       │ mg/kg
 9  │ Phosphorus (P)     │ mg/kg
10  │ Potassium (K)      │ mg/kg
```

## Interaction Scenarios

### Scenario 1: Human Initiates Conversation

```
1. User speaks: "Hello Plantroid"
2. ListeningModule publishes to messageTopic
3. MAESTRO.cb_function() triggered
4. Dialogue state: Silent → heard_human → SpokeToMe
5. Check if addressed to robot: YES
6. Dialogue state: SpokeToMe → yes → BusyCheck
7. Check robot state: Free
8. Dialogue state: BusyCheck → idle → LookAtUser
9. PersonSeeker executes (rotate to face user)
10. Dialogue state: LookAtUser → saw_human → StartDialogue2
11. Generate greeting with emotion
12. Publish to speechTopic
13. Set facial expression
14. Dialogue state: StartDialogue2 → dialogue_init → AnswerHuman
15. Wait for user response
```

### Scenario 2: Robot Detects Problem and Seeks Help

```
1. Sensor monitoring detects low moisture
2. Publish to notificationTopic: "Water:too low:urgent"
3. MAESTRO.cb_function_notification() triggered
4. Store notification in dictionary
5. Problem state: OK → problem_detected → Problem
6. Set facial expression: "thirsty"
7. PersonDetector becomes active (monitoring)
8. PersonDetector sees human
9. Publish to seenTopic: "Seen"
10. MAESTRO.cb_function_seen() triggered
11. Dialogue state: Silent → saw_human → CheckProblemAndBusy
12. Check: Problem detected + Free
13. Dialogue state: CheckProblemAndBusy → problem_detected → StartDialogue1
14. Generate greeting
15. Dialogue state: StartDialogue1 → dialogue_init → AskIfHumanIsAvailable
16. Ask: "Do you have time?"
17. If yes: AnnounceProblem → "I need help, soil moisture is too low"
18. Wait for questions or timeout
19. On timeout: ClearProblem → Goodbye → Silent
20. Problem state: Problem → problem_cleared → OK (manual or timeout)
```

### Scenario 3: Complex Query with LLM Fallback

```
1. User: "What do you think about climate change?"
2. ChatBot pattern matching: No match found → returns None
3. conversate() detects None response
4. Fall back to LLM:
   - get_llm_response(data)
   - Model: llama3
   - Prompt: "What do you think about climate change?"
5. LLM generates response
6. Add emotion context (e.g., "in a calm tone")
7. assign_prosody() based on current emotion
8. Publish response
```

## Emotion Mapping

### Input Emotion Sources

1. **Voice Emotion**: From speech-to-text metadata
2. **Content Emotion**: NLP sentiment analysis
3. **Face Emotion**: Visual emotion detection

### Fusion Strategy

Majority voting:
```python
def emotion_fusion(emotion_list):
    return max(set([(i, emotion_list.count(i))
                    for i in set(emotion_list)]),
               key=lambda x:x[1])[0]
```

### Response Strategy

**Mirror Mode** (commented out):
```python
response_emotion = final_emotion
```

**Improve Mode** (active):
```python
response_emotion = {
    "neutral": "neutral",
    "happy": "happy",
    "sad": "happy",      # Cheer up sad users
    "anger": "neutral",  # Calm angry users
    "surprise": "neutral"
}[final_emotion]
```

### Prosody Mapping

```
Emotion   │ Speed │ Pitch │ Volume
──────────┼───────┼───────┼────────
angry     │  180  │  200  │   55
happy     │  160  │  140  │   65
neutral   │  150  │  100  │   45
surprise  │  200  │   80  │   65
sad       │   80  │   80  │   35
```

## Threading Model

```
┌──────────────────────────────────────┐
│          Main Process                │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Thread 1: MAESTROmainNode     │ │
│  │  • ROS spinning                │ │
│  │  • Callback processing         │ │
│  │  • Service client calls        │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Thread 2: PersonDetector      │ │
│  │  • ROS spinning                │ │
│  │  • Periodic vision checks      │ │
│  │  • Person detection publishing │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Sub-process: PersonSeeker     │ │
│  │  • Spawned when needed         │ │
│  │  • Motor control               │ │
│  │  • Exits after completion      │ │
│  └────────────────────────────────┘ │
└──────────────────────────────────────┘
```

## Dependencies

### External Libraries
- `rclpy`: ROS 2 Python client
- `nltk`: Natural language processing
- `transformers`: Emotion classification model
- `wikipedia`: Wikipedia API
- `PyDictionary`: Dictionary lookups
- `beepy`: Audio feedback
- `cv2`: Computer vision (PersonSeeker)

### ROS Dependencies
- `std_msgs.msg.String`: Standard string messages
- `rooted_msgs.srv.*`: Custom service definitions
- `rooted_msgs.msg.*`: Custom message definitions

### Internal Modules
- `utils`: Helper functions
- `simple_state_machine`: State machine class
- `ChatBot`: Pattern-based responses

## Known Issues & TODOs

1. **PersonSeeker Integration** (line 262):
   - Uses `os.system()` subprocess call
   - Path hardcoded, needs configuration

2. **Memory Access** (lines 161-172):
   - MemoryAccess class incomplete
   - Marked with TODO comment

3. **Callback Bug** (lines 284-286):
   - Variable `a` undefined in `cb_function_seen()`
   - Code will crash when person detected with problems

4. **Hardcoded Paths**:
   - Line 239: dialogue.json path
   - Line 262: PersonSeeker.py path
   - Need environment variables or config file

5. **Main Function** (line 462):
   - Recursion bug: `maestro_thread = Thread(target = main)`
   - Should be `target = maestro`

6. **State Machine Edge Cases**:
   - No timeout handling in WaitHumanQuestion states
   - Could get stuck waiting indefinitely

## Future Enhancements

1. **Memory System**: Implement long-term conversation memory
2. **Learning**: Enable Q-learning for dialogue optimization
3. **Multi-modal Fusion**: Weight emotion sources by reliability
4. **Context Awareness**: Track conversation history
5. **Proactive Behaviors**: Schedule-based plant care reminders
6. **User Profiles**: Personalized interactions per user
7. **Gesture Integration**: Add non-verbal communication
8. **Navigation**: Full mobility for seeking humans
