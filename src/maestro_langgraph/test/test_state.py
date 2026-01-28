import pytest
from maestro_langgraph.state import (
    Intent,
    Emotion,
    RobotStatus,
    DialogueState,
    PROSODY_PRESETS,
    get_prosody_for_emotion,
)


class TestIntentEnum:

    def test_intent_values(self):
        assert Intent.GREETING.value == "greeting"
        assert Intent.FAREWELL.value == "farewell"
        assert Intent.QUESTION.value == "question"
        assert Intent.ACKNOWLEDGMENT.value == "acknowledgment"
        assert Intent.GENERAL.value == "general"

    def test_intent_count(self):
        assert len(Intent) == 5

    def test_intent_from_string(self):
        assert Intent("greeting") == Intent.GREETING
        assert Intent("farewell") == Intent.FAREWELL
        assert Intent("question") == Intent.QUESTION

    def test_intent_invalid_value(self):
        with pytest.raises(ValueError):
            Intent("invalid_intent")


class TestEmotionEnum:

    def test_emotion_values(self):
        assert Emotion.NEUTRAL.value == "neutral"
        assert Emotion.HAPPY.value == "happy"
        assert Emotion.SAD.value == "sad"
        assert Emotion.ANGER.value == "anger"
        assert Emotion.SURPRISE.value == "surprise"

    def test_emotion_count(self):
        assert len(Emotion) == 5

    def test_emotion_from_string(self):
        assert Emotion("neutral") == Emotion.NEUTRAL
        assert Emotion("happy") == Emotion.HAPPY
        assert Emotion("sad") == Emotion.SAD

    def test_emotion_invalid_value(self):
        with pytest.raises(ValueError):
            Emotion("excited")


class TestRobotStatusEnum:

    def test_robot_status_values(self):
        assert RobotStatus.FREE.value == "free"
        assert RobotStatus.BUSY.value == "busy"
        assert RobotStatus.PROBLEM.value == "problem"

    def test_robot_status_count(self):
        assert len(RobotStatus) == 3

    def test_robot_status_from_string(self):
        assert RobotStatus("free") == RobotStatus.FREE
        assert RobotStatus("busy") == RobotStatus.BUSY
        assert RobotStatus("problem") == RobotStatus.PROBLEM


class TestProsodyPresets:

    def test_prosody_presets_keys(self):
        for emotion in Emotion:
            assert emotion in PROSODY_PRESETS, f"Missing preset for {emotion}"

    def test_prosody_preset_format(self):
        for emotion, prosody in PROSODY_PRESETS.items():
            assert isinstance(prosody, tuple), f"Prosody for {emotion} is not a tuple"
            assert len(prosody) == 3, f"Prosody for {emotion} doesn't have 3 values"
            assert all(isinstance(v, int) for v in prosody), \
                f"Prosody values for {emotion} are not all integers"

    def test_prosody_preset_values(self):
        assert PROSODY_PRESETS[Emotion.NEUTRAL] == (150, 100, 45)
        assert PROSODY_PRESETS[Emotion.HAPPY] == (160, 140, 65)
        assert PROSODY_PRESETS[Emotion.SAD] == (80, 80, 35)
        assert PROSODY_PRESETS[Emotion.ANGER] == (180, 200, 55)
        assert PROSODY_PRESETS[Emotion.SURPRISE] == (200, 80, 65)

    def test_prosody_values_in_valid_range(self):
        for emotion, (volume, speed, pitch) in PROSODY_PRESETS.items():
            assert 0 <= volume <= 300, f"Volume for {emotion} out of range"
            assert 0 <= speed <= 300, f"Speed for {emotion} out of range"
            assert 0 <= pitch <= 100, f"Pitch for {emotion} out of range"


class TestGetProsodyForEmotion:

    def test_valid_emotion_string(self):
        assert get_prosody_for_emotion("neutral") == (150, 100, 45)
        assert get_prosody_for_emotion("happy") == (160, 140, 65)
        assert get_prosody_for_emotion("sad") == (80, 80, 35)
        assert get_prosody_for_emotion("anger") == (180, 200, 55)
        assert get_prosody_for_emotion("surprise") == (200, 80, 65)

    def test_invalid_emotion_returns_neutral(self):
        neutral_prosody = (150, 100, 45)
        assert get_prosody_for_emotion("invalid") == neutral_prosody
        assert get_prosody_for_emotion("excited") == neutral_prosody
        assert get_prosody_for_emotion("") == neutral_prosody
        assert get_prosody_for_emotion("HAPPY") == neutral_prosody

    def test_return_type(self):
        result = get_prosody_for_emotion("happy")
        assert isinstance(result, tuple)
        assert len(result) == 3


class TestDialogueState:

    def test_create_empty_state(self):
        state: DialogueState = {}
        assert state == {}

    def test_create_partial_state(self):
        state: DialogueState = {
            "human_message": "Hello",
            "voice_emotion": "happy",
        }
        assert state["human_message"] == "Hello"
        assert state["voice_emotion"] == "happy"

    def test_create_full_state(self):
        state: DialogueState = {
            "human_message": "Hello robot",
            "voice_emotion": "neutral",
            "robot_busy": False,
            "robot_status": "free",
            "has_problem": False,
            "notifications": {},
            "conversation_history": [],
            "intent": "greeting",
            "entities": {},
            "search_context": None,
            "context_response": None,
            "response": "Hello!",
            "response_emotion": "happy",
            "prosody": (160, 140, 65),
            "should_end_early": False,
        }
        assert state["human_message"] == "Hello robot"
        assert state["response"] == "Hello!"
        assert state["prosody"] == (160, 140, 65)

    def test_state_with_notifications(self):
        state: DialogueState = {
            "notifications": {
                "moisture": ["low", "high"],
                "temperature": ["25", "normal"],
            },
        }
        assert "moisture" in state["notifications"]
        assert state["notifications"]["moisture"] == ["low", "high"]

    def test_state_with_conversation_history(self):
        state: DialogueState = {
            "conversation_history": [
                ("Human", "Hello"),
                ("Plantroid", "Hi there!"),
                ("Human", "How are you?"),
                ("Plantroid", "I'm great!"),
            ],
        }
        assert len(state["conversation_history"]) == 4
        assert state["conversation_history"][0] == ("Human", "Hello")
