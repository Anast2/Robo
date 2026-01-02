# Maestro Module Documentation

Complete documentation for the Maestro orchestration system in the Plantroid social robot.

## Documentation Structure

This folder contains comprehensive documentation for understanding and working with the Maestro module:

### 1. ARCHITECTURE.md
**Main architectural documentation with detailed diagrams**

**Contents:**
- System overview and component architecture
- State machine designs (3 concurrent state machines)
- Data flow diagrams for all major processes
- Component details and API reference
- Configuration guide
- Sensor and emotion mappings
- Threading model
- Dependencies and integration points
- Known issues and future enhancements

**Key Diagrams:**
- Overall system architecture
- Dialogue state machine (15 states)
- Robot state machine (Free/Busy)
- Problem state machine (OK/Problem)
- Human speech processing flow
- Emotion fusion process
- Response generation flow
- Notification handling flow
- Person detection cycle

**When to use:** Start here for complete understanding of system design

### 2. QUICK_REFERENCE.md
**Fast lookup guide for developers**

**Contents:**
- State machine quick reference tables
- ROS interface (topics, services, message formats)
- ChatBot pattern reference
- Sensor ID mappings
- Emotion values and strategies
- Common operations (code snippets)
- Debugging commands
- Configuration paths
- Performance benchmarks
- Error codes
- Testing commands
- Recovery procedures
- Best practices

**When to use:** Day-to-day development, debugging, quick lookups

### 3. SEQUENCE_DIAGRAMS.md
**Detailed interaction flows**

**Contains 8 major sequence diagrams:**
1. Normal human-initiated conversation
2. Problem detection and reporting
3. Complex query with LLM fallback
4. Sensor query processing
5. Vision query processing
6. Robot busy state handling
7. Multi-modal emotion fusion
8. Wikipedia query flow

Plus state transition summary table

**When to use:** Understanding specific interaction scenarios, debugging flow issues

### 4. This File (README_DOCS.md)
**Navigation and overview**

## Quick Navigation

### I need to understand...

**...how the system works overall**
→ Start with ARCHITECTURE.md (Overview and System Architecture sections)

**...how conversations are handled**
→ ARCHITECTURE.md (MAESTROmainNode section) + SEQUENCE_DIAGRAMS.md (Diagram 1)

**...how state machines work**
→ ARCHITECTURE.md (State Machine Architecture) + QUICK_REFERENCE.md (State Machine tables)

**...how emotions are processed**
→ ARCHITECTURE.md (Emotion Fusion Process) + SEQUENCE_DIAGRAMS.md (Diagram 7)

**...how the ChatBot works**
→ ARCHITECTURE.md (ChatBot Module) + QUICK_REFERENCE.md (ChatBot Patterns)

**...how to query sensors**
→ SEQUENCE_DIAGRAMS.md (Diagram 4) + QUICK_REFERENCE.md (Sensor ID Reference)

**...how problem reporting works**
→ SEQUENCE_DIAGRAMS.md (Diagram 2) + ARCHITECTURE.md (Notification Handling Flow)

**...ROS topics and services**
→ QUICK_REFERENCE.md (ROS Interface Quick Reference)

**...how to debug issues**
→ QUICK_REFERENCE.md (Debugging and Recovery sections)

**...configuration and setup**
→ ARCHITECTURE.md (Configuration section) + QUICK_REFERENCE.md (Configuration Paths)

## Module Overview

### What is Maestro?

Maestro is the central orchestration system for the Plantroid social robot. It coordinates:
- Multi-modal human-robot interaction
- Sensor monitoring and problem reporting
- Conversation management using pattern matching + LLM
- Emotion detection and fusion from voice, text, and facial expressions
- Person detection and tracking
- Behavioral state management

### Key Components

```
┌─────────────────────────────────────────────────────────────┐
│                    MAESTRO SYSTEM                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Core Nodes:                                                │
│  • MAESTROmainNode     - Main orchestration                 │
│  • PersonDetector      - Vision-based person detection      │
│  • PersonSeeker        - Person tracking behavior           │
│                                                             │
│  Supporting Modules:                                        │
│  • ChatBot            - Pattern-based responses             │
│  • StateMachine       - Generic FSM implementation          │
│  • utils              - Helper functions                    │
│                                                             │
│  State Machines:                                            │
│  • Dialogue (15 states)  - Conversation flow                │
│  • Robot (2 states)      - Busy/Free tracking               │
│  • Problem (2 states)    - Health monitoring                │
│                                                             │
│  External Services Used:                                    │
│  • Camera service      - Vision/emotion detection           │
│  • Sensors service     - Environmental monitoring           │
│  • LLM service         - Language generation                │
│  • Busy service        - Task state management              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Information Flow Summary

```
INPUT CHANNELS:
├─ Human Speech (messageTopic)
│  └─> Emotion fusion → Response generation → Speech output
│
├─ Sensor Alerts (notificationTopic)
│  └─> Problem detection → Seek human → Explain problem
│
└─ Person Detection (seenTopic)
   └─> Check problems → Initiate dialogue if needed

OUTPUT CHANNELS:
├─ Speech (speechTopic)
│  └─> Text + prosody parameters
│
├─ Facial Expression (emotionTopic)
│  └─> Emotion name
│
└─ Listen Control (ListenBlockTopic)
   └─> Echo prevention
```

## Core Concepts

### State-Driven Architecture

All behavior is governed by state machines:
- **Dialogue State**: Tracks conversation phase
- **Robot State**: Tracks availability (Free/Busy)
- **Problem State**: Tracks health status (OK/Problem)

State transitions are triggered by:
- ROS topic messages (heard_human, saw_human)
- Service call results (busy check, sensor readings)
- Internal events (robot_finished, timeout)

### Multi-Modal Emotion Fusion

Emotion is determined from 3 sources:
1. **Voice emotion** from speech-to-text metadata
2. **Content emotion** from NLP sentiment analysis
3. **Face emotion** from computer vision

Fusion uses majority voting for robustness.

Response emotion can be:
- **Mirror mode**: Match user's emotion
- **Improve mode**: Try to improve user's emotional state (active by default)

### Conversational Strategy

Two-tier response generation:
1. **Pattern matching** (ChatBot): Fast, deterministic responses for known patterns
2. **LLM fallback**: Flexible, open-domain responses for unknown queries

Special commands trigger external services:
- `wikipedia:X` → Query Wikipedia
- `dictionary:X` → Look up definition
- `sensor:N` → Read sensor N
- `vision_check` → Describe visual scene

### Proactive Behavior

The robot doesn't just respond, it can:
- Detect problems through sensor monitoring
- Actively seek humans when help is needed
- Express appropriate emotions through face and voice
- Decide when to interrupt vs. wait

## File Reference

### Source Files

```
maestro/
├── MAESTRO.py               (470 lines)  Main orchestration node
├── ChatBot.py               (258 lines)  Pattern matching & NLP
├── PersonSeeker.py          (107 lines)  Person tracking behavior
├── simple_state_machine.py  (87 lines)   FSM implementation
├── utils.py                  (90 lines)   Helper functions
├── dialogue.json             (17 lines)   Dialogue templates
└── __init__.py               (0 lines)    Package marker
```

### Documentation Files

```
maestro/
├── README_DOCS.md           (this file)   Documentation overview
├── ARCHITECTURE.md          (~700 lines)  Complete system design
├── QUICK_REFERENCE.md       (~500 lines)  Developer quick guide
└── SEQUENCE_DIAGRAMS.md     (~900 lines)  Interaction flows
```

## Development Workflow

### Getting Started

1. Read ARCHITECTURE.md (Overview and System Architecture)
2. Review QUICK_REFERENCE.md (ROS Interface and Common Operations)
3. Explore SEQUENCE_DIAGRAMS.md for specific scenarios

### Adding New Features

**Adding a new conversation pattern:**
1. Add pattern to `ChatBot.py` (default_pairs)
2. If needed, add special command handler in `MAESTRO.py` (conversate method)
3. Test with manual topic publish (see QUICK_REFERENCE.md)

**Adding a new state to dialogue:**
1. Modify `plantroid_dialogue_state_machine` initialization in `MAESTRO.py`
2. Add state to transition table
3. Add dialogue template to `dialogue.json`
4. Update documentation

**Adding a new sensor:**
1. Add sensor ID to mapping dictionaries (lines 406-412 in MAESTRO.py)
2. Add ChatBot pattern for querying the sensor
3. Update QUICK_REFERENCE.md sensor table

**Adding a new emotion:**
1. Update emotion mapping in `ChatBot.py` (line 194)
2. Add prosody parameters in `MAESTRO.py` (assign_prosody method)
3. Update response strategy mapping if needed

### Debugging Workflow

1. Check QUICK_REFERENCE.md (Debugging Quick Reference)
2. Monitor relevant topics: `ros2 topic echo /topicname`
3. Check state machine status (see code snippets in QUICK_REFERENCE.md)
4. Review SEQUENCE_DIAGRAMS.md for expected flow
5. Check ARCHITECTURE.md (Known Issues) for documented bugs

## Common Tasks

### Understanding a Bug

1. **Reproduce the issue**
2. **Identify the interaction scenario** → Check SEQUENCE_DIAGRAMS.md
3. **Check state machine states** → Use debugging commands
4. **Monitor ROS topics** → See what messages are flowing
5. **Review the code flow** → Follow the sequence diagram
6. **Check Known Issues** → ARCHITECTURE.md lists documented bugs

### Adding Documentation

When adding features, update:
- ARCHITECTURE.md (if changing system design)
- QUICK_REFERENCE.md (if adding new commands/patterns/sensors)
- SEQUENCE_DIAGRAMS.md (if adding new interaction flows)
- This file (if adding new documentation sections)

### Testing Changes

See QUICK_REFERENCE.md (Testing Commands) for:
- Manual topic injection
- Service testing commands
- Pattern matching tests
- State machine validation

## Integration with Other Modules

### Required External Modules

```
listening_module/
├── ListeningModule   - Audio capture, VAD, STT
└── Publishes to messageTopic

rooted_llm/
├── LLM Server        - Language model interface
└── Provides LLM service

vision_module/
├── Vision processing - Person detection, emotion detection
└── Provides Camera service

other_sensors/
├── Sensor monitoring - Environmental sensors
└── Provides Sensors service

rooted_speech_synthesizer/
├── Speech synthesis  - TTS with prosody
└── Subscribes to speechTopic

facial_expression/
├── Face GUI          - Visual expression display
└── Subscribes to emotionTopic

rooted_busy/
├── Busy state        - Task execution tracking
└── Provides Gesture service
```

### Module Communication Diagram

```
┌──────────────┐         ┌──────────────┐
│  Listening   │────────►│   MAESTRO    │
│   Module     │ message │     Node     │
└──────────────┘         └───────┬──────┘
                                 │
                                 │ speech
┌──────────────┐                │
│   Sensors    │◄───────────────┼────────┐
│   Module     │    sensor      │        │
└──────────────┘    request     │        │
                                 │        │
┌──────────────┐                │        │
│    Vision    │◄───────────────┼────────┤
│   Module     │    vision      │        │
└──────────────┘    request     │        │
                                 │        │
┌──────────────┐                │        │
│     LLM      │◄───────────────┼────────┤
│   Service    │    prompt      │        │
└──────────────┘                │        │
                                 │        │
                        ┌────────▼────┐   │
                        │   Speech    │   │
                        │ Synthesizer │◄──┘
                        └─────────────┘
                                 │
                        ┌────────▼────┐
                        │   Facial    │
                        │ Expression  │
                        └─────────────┘
```

## Performance Characteristics

### Latency Profile

```
Speech Input → Response Output: 2-6 seconds
├─ STT Processing:         500-1500 ms
├─ Emotion Fusion:         200-500 ms
├─ Response Generation:    1-4 seconds
│  ├─ Pattern Matching:    1-10 ms
│  └─ LLM Query:           1-5 seconds (if needed)
└─ TTS Processing:         500-1500 ms
```

### Resource Usage

- **Memory**: ~500MB (mainly from transformer models)
- **CPU**: Moderate (spikes during emotion analysis and LLM queries)
- **Network**: Minimal (unless using remote LLM)

## Known Issues Summary

(See ARCHITECTURE.md for details)

1. **PersonSeeker Integration**: Hardcoded path, subprocess call
2. **Memory Access**: Incomplete implementation
3. **Callback Bug**: Undefined variable in cb_function_seen (lines 284-286)
4. **Hardcoded Paths**: Configuration files need environment variables
5. **Main Function Bug**: Recursion in thread target (line 462)

## Future Enhancements Summary

(See ARCHITECTURE.md for details)

- Long-term conversation memory
- Q-learning for dialogue optimization
- Weighted emotion fusion
- Context-aware responses
- Proactive plant care scheduling
- User profiling
- Gesture integration
- Full navigation capabilities

## Getting Help

### Troubleshooting Steps

1. Check QUICK_REFERENCE.md (Error Codes & Recovery)
2. Review SEQUENCE_DIAGRAMS.md for expected behavior
3. Check logs for state transitions
4. Verify all required services are running
5. Check ARCHITECTURE.md (Known Issues)

### Additional Resources

- ROS 2 documentation: https://docs.ros.org/
- NLTK documentation: https://www.nltk.org/
- State machine design patterns: https://en.wikipedia.org/wiki/Finite-state_machine

## Contributing

When modifying Maestro:

1. **Understand** the current architecture (read ARCHITECTURE.md)
2. **Plan** your changes (consider state machine implications)
3. **Implement** following coding standards
4. **Test** thoroughly (use manual topic injection)
5. **Document** your changes (update all relevant docs)
6. **Review** state machine validity

## Version History

- **Initial Documentation**: Comprehensive documentation created covering full system architecture, quick reference, and sequence diagrams

## Document Maintenance

These documents should be updated when:
- Adding/removing states from state machines
- Adding new ROS topics or services
- Modifying emotion processing logic
- Adding new ChatBot patterns
- Changing configuration file locations
- Fixing known issues
- Adding new features

## Summary

The Maestro module is a sophisticated behavior-based orchestration system that enables natural, context-aware human-robot interaction. It uses state machines to coordinate multiple concurrent behaviors, fuses multi-modal emotional input for robust understanding, and combines rule-based and AI-driven approaches for flexible response generation.

This documentation provides everything needed to understand, modify, debug, and extend the system.

**Happy coding!**

