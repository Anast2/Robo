# Maestro Sequence Diagrams

This document contains detailed sequence diagrams for all major interaction flows in the Maestro system.

## Diagram 1: Normal Human-Initiated Conversation

```
User          Listening    MAESTRO     Dialogue    Robot      ChatBot    LLM        Vision     Speech
              Module       Node        StateMachine State                           Module     Synth
 |              |            |            |          |           |         |          |          |
 |              |            |            |          |           |         |          |          |
 |-"Hello"----->|            |            |          |           |         |          |          |
 |              |            |            |          |           |         |          |          |
 |              |--VAD------>|            |          |           |         |          |          |
 |              |  Detect    |            |          |           |         |          |          |
 |              |            |            |          |           |         |          |          |
 |              |--STT------>|            |          |           |         |          |          |
 |              | "Hello;    |            |          |           |         |          |          |
 |              | ts;happy"  |            |          |           |         |          |          |
 |              |            |            |          |           |         |          |          |
 |              |            |--transition("heard_human")        |         |          |          |
 |              |            |            |--------------------->|         |          |          |
 |              |            |            |  Silent → SpokeToMe  |         |          |          |
 |              |            |            |<---------------------|         |          |          |
 |              |            |            |                      |         |          |          |
 |              |            |--get_emotion()                    |         |          |          |
 |              |            |------------------------------------Request(0)--------->|          |
 |              |            |                                   |         |          |          |
 |              |            |<-----------------------------------Face: "happy"-------|          |
 |              |            |            |                      |         |          |          |
 |              |            |--sentiment_analysis("Hello")      |         |          |          |
 |              |            |-------------------------->|        |         |          |          |
 |              |            |<-"happy"------------------|        |         |          |          |
 |              |            |            |                      |         |          |          |
 |              |            |--emotion_fusion([happy,happy,happy])        |          |          |
 |              |            |  Result: "happy"         |        |         |          |          |
 |              |            |            |              |       |         |          |          |
 |              |            |--map_response_emotion()   |       |         |          |          |
 |              |            |  happy → happy            |       |         |          |          |
 |              |            |            |              |       |         |          |          |
 |              |            |--conversate("Hello", "happy")     |         |          |          |
 |              |            |-------------------------->|        |         |          |          |
 |              |            |                           |--chatter("Hello")          |          |
 |              |            |                           |------->|         |          |          |
 |              |            |                           |        |--match pattern    |          |
 |              |            |                           |        |  "hi|hey|hello"   |          |
 |              |            |                           |<-------|         |          |          |
 |              |            |                           |  "Hello"         |          |          |
 |              |            |<--------------------------|        |         |          |          |
 |              |            |  "Hello"                  |        |         |          |          |
 |              |            |            |              |        |         |          |          |
 |              |            |--assign_prosody("Hello", "happy") |         |          |          |
 |              |            |  Result: [("Hello", [160,140,65])]|         |          |          |
 |              |            |            |              |        |         |          |          |
 |              |            |--publish(speechTopic)     |        |         |          |          |
 |              |            |-------------------------------------------------------------->|
 |              |            |  [("Hello", [160,140,65])]|        |         |          |          |
 |              |            |            |              |        |         |          |          |
 |              |            |--publish(emotionTopic)    |        |         |          |          |
 |              |            |  "happy"                  |        |         |          |          |
 |              |            |            |              |        |         |          |          |
 |              |            |--transition("yes")        |        |         |          |          |
 |              |            |            |------------->|        |         |          |          |
 |              |            |            | SpokeToMe → BusyCheck |         |          |          |
 |              |            |            |<-------------|        |         |          |          |
 |              |            |            |              |        |         |          |          |
 |              |            |--check_busy()             |        |         |          |          |
 |              |            |            |              |        |         |          |          |
 |              |            |--transition("idle")       |        |         |          |          |
 |              |            |            |------------->|        |         |          |          |
 |              |            |            | BusyCheck → LookAtUser|         |          |          |
 |              |            |            |<-------------|        |         |          |          |
 |              |            |            |              |        |         |          |          |
 |              |            |--PersonSeeker.rotate_to_person()   |         |          |          |
 |              |            |            |              |        |         |          |          |
 |              |            |<-rotation_complete--------         |         |          |          |
 |              |            |            |              |        |         |          |          |
 |              |            |--transition("saw_human")  |        |         |          |          |
 |              |            |            |------------->|        |         |          |          |
 |              |            |            | LookAtUser → StartDialogue2     |          |          |
 |              |            |            |<-------------|        |         |          |          |
 |              |            |            |              |        |         |          |          |
 |<---------------------------------------------------------"Hello"---------------------------|
 |              |            |            |              |        |         |          |          |
```

## Diagram 2: Problem Detection and Reporting

```
Sensor      MAESTRO      Problem       Dialogue       Person      Vision      Speech
Module      Node         StateMachine  StateMachine   Detector    Module      Synth
 |            |              |            |              |           |           |
 |            |              |            |              |           |           |
 |--publish-->|              |            |              |           |           |
 | "Water:    |              |            |              |           |           |
 | too low:   |              |            |              |           |           |
 | urgent"    |              |            |              |           |           |
 |            |              |            |              |           |           |
 |            |--cb_function_notification()            |           |           |
 |            |              |            |              |           |           |
 |            |--parse("Water:too low:urgent")         |           |           |
 |            |              |            |              |           |           |
 |            |--store_notification()    |              |           |           |
 |            |  notifications = {       |              |           |           |
 |            |    "Water":              |              |           |           |
 |            |    ["too low","urgent"]  |              |           |           |
 |            |  }           |            |              |           |           |
 |            |              |            |              |           |           |
 |            |--transition("problem_detected")         |           |           |
 |            |              |----------->|              |           |           |
 |            |              | OK → Problem              |           |           |
 |            |              |<-----------|              |           |           |
 |            |              |            |              |           |           |
 |            |--set_face("thirsty")     |              |           |           |
 |            |---------------------------------------------------->|           |
 |            |              |            |              |           |           |
 |            |              |            |              |           |           |
 |            |              |            |--detection_routine()    |           |
 |            |              |            |              |---------->|           |
 |            |              |            |              | Request(3)|           |
 |            |              |            |              |           |           |
 |            |              |            |              |<----------|           |
 |            |              |            |              | True      |           |
 |            |              |            |              |           |           |
 |            |              |            |              |--publish("Seen")      |
 |            |              |            |              |           |           |
 |            |<--------------------------------------------------------------|
 |            | seenTopic    |            |              |           |           |
 |            |              |            |              |           |           |
 |            |--cb_function_seen()      |              |           |           |
 |            |              |            |              |           |           |
 |            |--check_notifications()   |              |           |           |
 |            |  len(notifications) > 0  |              |           |           |
 |            |              |            |              |           |           |
 |            |--transition("saw_human") |              |           |           |
 |            |              |            |------------->|           |           |
 |            |              |            | Silent →     |           |           |
 |            |              |            | CheckProblemAndBusy      |           |
 |            |              |            |<-------------|           |           |
 |            |              |            |              |           |           |
 |            |--check_busy()            |              |           |           |
 |            |  Result: Free            |              |           |           |
 |            |              |            |              |           |           |
 |            |--check_problem()         |              |           |           |
 |            |              |<-----------|              |           |           |
 |            |              | State: Problem            |           |           |
 |            |              |            |              |           |           |
 |            |--transition("problem_detected")         |           |           |
 |            |              |            |------------->|           |           |
 |            |              |            | CheckProblemAndBusy      |           |
 |            |              |            | → StartDialogue1         |           |
 |            |              |            |<-------------|           |           |
 |            |              |            |              |           |           |
 |            |--generate_greeting()     |              |           |           |
 |            |  "Hello, "               |              |           |           |
 |            |              |            |              |           |           |
 |            |--transition("dialogue_init")            |           |           |
 |            |              |            |------------->|           |           |
 |            |              |            | StartDialogue1           |           |
 |            |              |            | → AskIfHumanIsAvailable  |           |
 |            |              |            |<-------------|           |           |
 |            |              |            |              |           |           |
 |            |--conversate("Do you have time?")        |           |           |
 |            |              |            |              |           |           |
 |            |--publish(speechTopic)    |              |           |           |
 |            |-------------------------------------------------------->|
 |            |              |            |              |           |           |
 |<--------------------------------------------------------------------|
 | User hears: "Do you have time?"       |              |           |           |
 |            |              |            |              |           |           |
 |-"Yes"----->|              |            |              |           |           |
 |            |              |            |              |           |           |
 |            |<-messageTopic("Yes;ts;neutral")         |           |           |
 |            |              |            |              |           |           |
 |            |--detect_affirmative()    |              |           |           |
 |            |              |            |              |           |           |
 |            |--transition("yes")       |              |           |           |
 |            |              |            |------------->|           |           |
 |            |              |            | AskIfHumanIsAvailable    |           |
 |            |              |            | → AnnounceProblem        |           |
 |            |              |            |<-------------|           |           |
 |            |              |            |              |           |           |
 |            |--process_notifications() |              |           |           |
 |            |  "I need your help,      |              |           |           |
 |            |   the soil has too low   |              |           |           |
 |            |   Water, urgent"         |              |           |           |
 |            |              |            |              |           |           |
 |            |--get_llm_response(paraphrase + emotion) |           |           |
 |            |              |            |              |           |           |
 |            |--publish(speechTopic)    |              |           |           |
 |            |-------------------------------------------------------->|
 |            |              |            |              |           |           |
 |<--------------------------------------------------------------------|
 | "I need help! The soil moisture is too low and it's urgent."       |
 |            |              |            |              |           |           |
 |            |--transition("robot_finished")           |           |           |
 |            |              |            |------------->|           |           |
 |            |              |            | AnnounceProblem          |           |
 |            |              |            | → WaitHumanQuestion1     |           |
 |            |              |            |<-------------|           |           |
 |            |              |            |              |           |           |
 |-"How long has it been like this?"---->|              |           |           |
 |            |              |            |              |           |           |
 |            |--conversate()            |              |           |           |
 |            |  [Pattern match + LLM]   |              |           |           |
 |            |              |            |              |           |           |
 |            |--publish(speechTopic)    |              |           |           |
 |            |-------------------------------------------------------->|
 |            |              |            |              |           |           |
 |            |--transition("human_question")           |           |           |
 |            |              |            |------------->|           |           |
 |            |              |            | WaitHumanQuestion1       |           |
 |            |              |            | → AnswerHuman            |           |
 |            |              |            |<-------------|           |           |
 |            |              |            |              |           |           |
 |            |              |            |              |           |           |
 | [After timeout with no more questions]|              |           |           |
 |            |              |            |              |           |           |
 |            |--transition("timeout")   |              |           |           |
 |            |              |            |------------->|           |           |
 |            |              |            | WaitHumanQuestion1       |           |
 |            |              |            | → ClearProblem           |           |
 |            |              |            |<-------------|           |           |
 |            |              |            |              |           |           |
 |            |--say("Thanks for listening")            |           |           |
 |            |-------------------------------------------------------->|
 |            |              |            |              |           |           |
 |            |--transition("robot_finished")           |           |           |
 |            |              |            |------------->|           |           |
 |            |              |            | ClearProblem |           |           |
 |            |              |            | → Goodbye    |           |           |
 |            |              |            |<-------------|           |           |
 |            |              |            |              |           |           |
 |            |--say("Goodbye")          |              |           |           |
 |            |-------------------------------------------------------->|
 |            |              |            |              |           |           |
 |            |--transition("dialogue_end")             |           |           |
 |            |              |            |------------->|           |           |
 |            |              |            | Goodbye → Silent         |           |
 |            |              |            |<-------------|           |           |
 |            |              |            |              |           |           |
 |            |--clear_notifications()   |              |           |           |
 |            |  notifications = {}      |              |           |           |
 |            |              |            |              |           |           |
```

## Diagram 3: Complex Query with LLM Fallback

```
User      Listening   MAESTRO    ChatBot    LLM         Speech
          Module      Node                  Service     Synth
 |          |           |          |          |           |
 |          |           |          |          |           |
 |-"What do you think about climate change?"->|          |
 |          |           |          |          |           |
 |          |--STT----->|          |          |           |
 |          |           |          |          |           |
 |          |           |--cb_function()     |           |
 |          |           |          |          |           |
 |          |           |--emotion_fusion()  |           |
 |          |           |  Result: "neutral" |           |
 |          |           |          |          |           |
 |          |           |--conversate("What do you think about climate change?",
 |          |           |            "neutral")           |
 |          |           |          |          |           |
 |          |           |          |--chatter("What do you think...")
 |          |           |          |          |           |
 |          |           |          |--pattern_match()     |
 |          |           |          |  [No match found]    |
 |          |           |          |          |           |
 |          |           |          |<---------|           |
 |          |           |          |  None    |           |
 |          |           |<---------|          |           |
 |          |           |          |          |           |
 |          |           |--detect_none()     |           |
 |          |           |          |          |           |
 |          |           |--get_llm_response("What do you think...")
 |          |           |          |          |           |
 |          |           |--send_request(model="llama3",  |
 |          |           |              prompt="What do you...")
 |          |           |------------------------->|      |
 |          |           |          |          |           |
 |          |           |          |  [LLM processing...] |
 |          |           |          |          |           |
 |          |           |<-------------------------|      |
 |          |           | "Climate change is a significant..."
 |          |           |          |          |           |
 |          |           |--add_emotion_context()         |
 |          |           |  " in a calm tone"  |           |
 |          |           |          |          |           |
 |          |           |--assign_prosody(response, "neutral")
 |          |           |  [("Climate change is...", [150,100,45])]
 |          |           |          |          |           |
 |          |           |--publish(speechTopic)          |
 |          |           |-------------------------------->|
 |          |           |          |          |           |
 |<---------------------------------------------------------|
 | "Climate change is a significant global challenge..."   |
 |          |           |          |          |           |
```

## Diagram 4: Sensor Query Processing

```
User      Listening   MAESTRO    ChatBot    Sensor      LLM         Speech
          Module      Node                  Service     Service     Synth
 |          |           |          |          |           |           |
 |          |           |          |          |           |           |
 |-"What is the soil moisture?"-->|          |           |           |
 |          |           |          |          |           |           |
 |          |--STT----->|          |          |           |           |
 |          |           |          |          |           |           |
 |          |           |--conversate("What is the soil moisture?")  |
 |          |           |          |          |           |           |
 |          |           |          |--chatter("What is the soil moisture?")
 |          |           |          |          |           |           |
 |          |           |          |--pattern_match()     |           |
 |          |           |          |  Match: "(.*)soil moisture(.*)"  |
 |          |           |          |  Response: "sensor:3"|           |
 |          |           |          |          |           |           |
 |          |           |          |<---------|           |           |
 |          |           |<---------|          |           |           |
 |          |           |  "sensor:3"         |           |           |
 |          |           |          |          |           |           |
 |          |           |--detect_special_command()       |           |
 |          |           |  Type: "sensor"     |           |           |
 |          |           |  ID: 3              |           |           |
 |          |           |          |          |           |           |
 |          |           |--get_sensor(3)      |           |           |
 |          |           |          |          |           |           |
 |          |           |--send_request(sensor_number=3)  |           |
 |          |           |------------------------->|      |           |
 |          |           |          |          |           |           |
 |          |           |<-------------------------|      |           |
 |          |           | sensor_reading: "45"    |       |           |
 |          |           |          |          |           |           |
 |          |           |--format_sensor_response()       |           |
 |          |           |  sensor_dict[3] = "soil moisture"|          |
 |          |           |  unit_dict[3] = " per cent"     |           |
 |          |           |          |          |           |           |
 |          |           |  Result: "current soil moisture |           |
 |          |           |          sensor reading is 45 per cent"     |
 |          |           |          |          |           |           |
 |          |           |--paraphrase_with_emotion()      |           |
 |          |           |  Prompt: "Paraphrase the following         |
 |          |           |          sentence in a neutral tone:       |
 |          |           |          current soil moisture sensor      |
 |          |           |          reading is 45 per cent"           |
 |          |           |          |          |           |           |
 |          |           |--get_llm_response(prompt)       |           |
 |          |           |------------------------------------->|      |
 |          |           |          |          |           |           |
 |          |           |<--------------------------------------|      |
 |          |           | "The soil moisture is currently at 45 percent"
 |          |           |          |          |           |           |
 |          |           |--set_face("neutral")|           |           |
 |          |           |          |          |           |           |
 |          |           |--assign_prosody(response, "neutral")       |
 |          |           |          |          |           |           |
 |          |           |--publish(speechTopic)           |           |
 |          |           |-------------------------------------------->|
 |          |           |          |          |           |           |
 |<----------------------------------------------------------------------|
 | "The soil moisture is currently at 45 percent"                        |
 |          |           |          |          |           |           |
```

## Diagram 5: Vision Query Processing

```
User      Listening   MAESTRO    ChatBot    Vision      LLM         Speech
          Module      Node                  Module      Service     Synth
 |          |           |          |          |           |           |
 |          |           |          |          |           |           |
 |-"What do you see?"-->|          |          |           |           |
 |          |           |          |          |           |           |
 |          |--STT----->|          |          |           |           |
 |          |           |          |          |           |           |
 |          |           |--conversate("What do you see?") |           |
 |          |           |          |          |           |           |
 |          |           |          |--chatter("What do you see?")     |
 |          |           |          |          |           |           |
 |          |           |          |--pattern_match()     |           |
 |          |           |          |  Match: "what do you see(.*)"    |
 |          |           |          |  Response: "vision_check"        |
 |          |           |          |          |           |           |
 |          |           |          |<---------|           |           |
 |          |           |<---------|          |           |           |
 |          |           |  "vision_check"     |           |           |
 |          |           |          |          |           |           |
 |          |           |--detect_special_command()       |           |
 |          |           |  Type: "vision_check"           |           |
 |          |           |          |          |           |           |
 |          |           |--get_vision()       |           |           |
 |          |           |          |          |           |           |
 |          |           |--send_request(imagetype=8)      |           |
 |          |           |          |          |           |           |
 |          |           |------------------------->|      |           |
 |          |           |          |  [Vision processing...]          |
 |          |           |          |  [Scene analysis]   |           |
 |          |           |          |  [Object detection] |           |
 |          |           |          |          |           |           |
 |          |           |<-------------------------|      |           |
 |          |           | image: "I see a person standing in front   |
 |          |           |         of a potted plant on a table"      |
 |          |           |          |          |           |           |
 |          |           |--paraphrase_with_emotion()      |           |
 |          |           |  Prompt: "Paraphrase the following         |
 |          |           |          sentence in a neutral tone:       |
 |          |           |          I see a person standing in        |
 |          |           |          front of a potted plant on a table"
 |          |           |          |          |           |           |
 |          |           |--get_llm_response(prompt)       |           |
 |          |           |------------------------------------->|      |
 |          |           |          |          |           |           |
 |          |           |<--------------------------------------|      |
 |          |           | "Right now, I can see you standing near    |
 |          |           |  a plant on the table"          |           |
 |          |           |          |          |           |           |
 |          |           |--assign_prosody(response, "neutral")       |
 |          |           |          |          |           |           |
 |          |           |--publish(speechTopic)           |           |
 |          |           |-------------------------------------------->|
 |          |           |          |          |           |           |
 |<----------------------------------------------------------------------|
 | "Right now, I can see you standing near a plant on the table"        |
 |          |           |          |          |           |           |
```

## Diagram 6: Robot Busy State Handling

```
User      Listening   MAESTRO    Busy        Dialogue       Speech
          Module      Node       Checker     StateMachine   Synth
 |          |           |          |            |              |
 |          |           |          |            |              |
 |          |  [Robot currently executing navigation task]    |
 |          |           |          |            |              |
 |-"Hello robot"------>|          |            |              |
 |          |           |          |            |              |
 |          |--STT----->|          |            |              |
 |          |           |          |            |              |
 |          |           |--cb_function()        |              |
 |          |           |          |            |              |
 |          |           |--transition("heard_human")           |
 |          |           |          |            |------------->|
 |          |           |          |            | Silent → SpokeToMe
 |          |           |          |            |<-------------|
 |          |           |          |            |              |
 |          |           |--verify_addressing() |              |
 |          |           |  Result: YES         |              |
 |          |           |          |            |              |
 |          |           |--transition("yes")   |              |
 |          |           |          |            |------------->|
 |          |           |          |            | SpokeToMe → BusyCheck
 |          |           |          |            |<-------------|
 |          |           |          |            |              |
 |          |           |--check_busy()        |              |
 |          |           |          |            |              |
 |          |           |--send_request("get") |              |
 |          |           |-------------->|      |              |
 |          |           |          |            |              |
 |          |           |<--------------|      |              |
 |          |           |  result: True        |              |
 |          |           |          |            |              |
 |          |           |--robot_state_machine.transition("move")
 |          |           |  State: Free → Busy  |              |
 |          |           |          |            |              |
 |          |           |--transition("busy")  |              |
 |          |           |          |            |------------->|
 |          |           |          |            | BusyCheck → AnnounceBusy
 |          |           |          |            |<-------------|
 |          |           |          |            |              |
 |          |           |--generate_busy_message()            |
 |          |           |  (from dialogue.json)               |
 |          |           |  "Sorry, I am busy now; I will      |
 |          |           |   talk to you in a moment"          |
 |          |           |          |            |              |
 |          |           |--assign_prosody(msg, "neutral")     |
 |          |           |          |            |              |
 |          |           |--publish(speechTopic)               |
 |          |           |---------------------------------------->|
 |          |           |          |            |              |
 |<-----------------------------------------------------------------|
 | "Sorry, I am busy now; I will talk to you in a moment"          |
 |          |           |          |            |              |
 |          |           |--transition("robot_finished")       |
 |          |           |          |            |------------->|
 |          |           |          |            | AnnounceBusy → Goodbye
 |          |           |          |            |<-------------|
 |          |           |          |            |              |
 |          |           |--say("Goodbye")      |              |
 |          |           |---------------------------------------->|
 |          |           |          |            |              |
 |          |           |--transition("dialogue_end")         |
 |          |           |          |            |------------->|
 |          |           |          |            | Goodbye → Silent
 |          |           |          |            |<-------------|
 |          |           |          |            |              |
```

## Diagram 7: Multi-Modal Emotion Fusion

```
User      Listening   Vision      MAESTRO    Sentiment   Emotion     Speech
Voice     Module      Module      Node       Analyzer    Fusion      Synth
 |          |           |           |          |           |           |
 |          |           |           |           |          |           |
 |-"I'm feeling sad today"-------->|           |          |           |
 | [Spoken with           |         |           |          |           |
 |  sad intonation]       |         |           |          |           |
 |          |             |         |           |          |           |
 |          |--STT + Voice Emotion->|           |          |           |
 |          | "I'm feeling sad today;timestamp;sad"       |           |
 |          |             |         |           |          |           |
 |          |             |         |--cb_function()       |           |
 |          |             |         |           |          |           |
 |          |             |         |--parse_message()     |           |
 |          |             |         |  text: "I'm feeling sad today"   |
 |          |             |         |  voice_emotion: "sad"|           |
 |          |             |         |           |          |           |
 |          |             |         |--get_emotion() [face]|           |
 |          |             |         |           |          |           |
 |          |             |         |--send_request(imagetype=0)       |
 |          |             |         |---------->|          |           |
 |          |             |         |           |          |           |
 |          |             |<--------|  [Facial emotion detection]      |
 |          |             |         |           |          |           |
 |          |             |---------|---------->|          |           |
 |          |             |         |  face_emotion: "sad" |           |
 |          |             |         |           |          |           |
 |          |             |         |--sentiment_analysis()|           |
 |          |             |         |  "I'm feeling sad today"         |
 |          |             |         |           |          |           |
 |          |             |         |-------------------->|            |
 |          |             |         |  [NLP processing]   |            |
 |          |             |         |  [EmTract-DistilBERT]            |
 |          |             |         |           |          |           |
 |          |             |         |<--------------------|            |
 |          |             |         |  content_emotion: "sad"          |
 |          |             |         |           |          |           |
 |          |             |         |--emotion_fusion()    |           |
 |          |             |         |  Input: ["sad", "sad", "sad"]    |
 |          |             |         |  Method: Majority vote           |
 |          |             |         |           |          |           |
 |          |             |         |--------------------------------->|
 |          |             |         |           |  [Count occurrences] |
 |          |             |         |           |  sad: 3             |
 |          |             |         |           |  Result: "sad"      |
 |          |             |         |<---------------------------------|
 |          |             |         |           |          |           |
 |          |             |         |--map_response_emotion()          |
 |          |             |         |  Strategy: Improve mode          |
 |          |             |         |  sad → happy (cheer up)          |
 |          |             |         |           |          |           |
 |          |             |         |--conversate(text, "happy")       |
 |          |             |         |  Generate uplifting response     |
 |          |             |         |           |          |           |
 |          |             |         |--assign_prosody(response, "happy")
 |          |             |         |  Parameters: [160, 140, 65]      |
 |          |             |         |           |          |           |
 |          |             |         |--set_face("happy")  |           |
 |          |             |         |  Update robot expression         |
 |          |             |         |           |          |           |
 |          |             |         |--publish(speechTopic)            |
 |          |             |         |------------------------------------>|
 |          |             |         |           |          |           |
 |<--------------------------------------------------------------------|
 | [Cheerful voice]: "I'm sorry to hear that! Is there anything I can do
 |                    to help cheer you up?"                           |
 |          |             |         |           |          |           |
```

## Diagram 8: Wikipedia Query Flow

```
User      Listening   MAESTRO    ChatBot    Wikipedia   LLM         Speech
          Module      Node                  API         Service     Synth
 |          |           |          |          |           |           |
 |          |           |          |          |           |           |
 |-"What is photosynthesis?"----->|          |           |           |
 |          |           |          |          |           |           |
 |          |--STT----->|          |          |           |           |
 |          |           |          |          |           |           |
 |          |           |--conversate("What is photosynthesis?")     |
 |          |           |          |          |           |           |
 |          |           |          |--chatter("What is photosynthesis?")
 |          |           |          |          |           |           |
 |          |           |          |--pattern_match()     |           |
 |          |           |          |  Match: "what is (.*)"           |
 |          |           |          |  Capture: "photosynthesis"       |
 |          |           |          |  Response: "wikipedia:photosynthesis"
 |          |           |          |          |           |           |
 |          |           |          |<---------|           |           |
 |          |           |<---------|          |           |           |
 |          |           |  "wikipedia:photosynthesis"     |           |
 |          |           |          |          |           |           |
 |          |           |--detect_special_command()       |           |
 |          |           |  Type: "wikipedia"  |           |           |
 |          |           |  Query: "photosynthesis"        |           |
 |          |           |          |          |           |           |
 |          |           |--wikipedia_query("photosynthesis")          |
 |          |           |          |          |           |           |
 |          |           |          |--utils.wikipedia_query()         |
 |          |           |          |          |           |           |
 |          |           |          |          |---------->|           |
 |          |           |          |  [API call to Wikipedia]         |
 |          |           |          |          |           |           |
 |          |           |          |<---------|           |           |
 |          |           |          |  "Photosynthesis is a process    |
 |          |           |          |   used by plants and other       |
 |          |           |          |   organisms to convert light     |
 |          |           |          |   energy into chemical energy... |
 |          |           |          |   (2 sentences)"     |           |
 |          |           |<---------|          |           |           |
 |          |           |          |          |           |           |
 |          |           |--paraphrase_with_emotion()      |           |
 |          |           |  Prompt: "Paraphrase the following         |
 |          |           |          sentence in a neutral tone:       |
 |          |           |          Photosynthesis is a process..."   |
 |          |           |          |          |           |           |
 |          |           |--get_llm_response(prompt)       |           |
 |          |           |------------------------------------->|      |
 |          |           |          |          |           |           |
 |          |           |<--------------------------------------|      |
 |          |           | "Photosynthesis is how plants use sunlight |
 |          |           |  to make food and energy. It's a vital     |
 |          |           |  process for life on Earth."    |           |
 |          |           |          |          |           |           |
 |          |           |--assign_prosody(response, "neutral")       |
 |          |           |          |          |           |           |
 |          |           |--publish(speechTopic)           |           |
 |          |           |-------------------------------------------->|
 |          |           |          |          |           |           |
 |<----------------------------------------------------------------------|
 | "Photosynthesis is how plants use sunlight to make food and energy.  |
 |  It's a vital process for life on Earth."                            |
 |          |           |          |          |           |           |
```
