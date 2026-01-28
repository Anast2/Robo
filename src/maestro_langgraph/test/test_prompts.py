import pytest
from maestro_langgraph.prompts import (
    ROBOT_PERSONA,
    INTENT_CLASSIFICATION_PROMPT,
    RESPONSE_GENERATION_PROMPT,
    EMOTION_DETECTION_PROMPT,
    BUSY_RESPONSE_PROMPT,
    PROBLEM_ANNOUNCEMENT_PROMPT,
    format_notifications,
)


class TestRobotPersona:

    def test_persona_is_string(self):
        assert isinstance(ROBOT_PERSONA, str)
        assert len(ROBOT_PERSONA) > 0

    def test_persona_contains_robot_name(self):
        assert "Plantroid" in ROBOT_PERSONA

    def test_persona_contains_key_traits(self):
        assert "friendly" in ROBOT_PERSONA.lower()
        assert "plant" in ROBOT_PERSONA.lower()


class TestIntentClassificationPrompt:

    def test_prompt_is_string(self):
        assert isinstance(INTENT_CLASSIFICATION_PROMPT, str)
        assert len(INTENT_CLASSIFICATION_PROMPT) > 0

    def test_prompt_has_message_placeholder(self):
        assert "{message}" in INTENT_CLASSIFICATION_PROMPT

    def test_prompt_mentions_intent_categories(self):
        prompt_lower = INTENT_CLASSIFICATION_PROMPT.lower()
        assert "greeting" in prompt_lower
        assert "farewell" in prompt_lower
        assert "question" in prompt_lower
        assert "acknowledgment" in prompt_lower
        assert "general" in prompt_lower


class TestResponseGenerationPrompt:

    def test_prompt_is_string(self):
        assert isinstance(RESPONSE_GENERATION_PROMPT, str)
        assert len(RESPONSE_GENERATION_PROMPT) > 0

    def test_prompt_has_required_placeholders(self):
        assert "{message}" in RESPONSE_GENERATION_PROMPT
        assert "{emotion}" in RESPONSE_GENERATION_PROMPT
        assert "{history}" in RESPONSE_GENERATION_PROMPT

    def test_prompt_mentions_emotions(self):
        prompt_lower = RESPONSE_GENERATION_PROMPT.lower()
        assert "happy" in prompt_lower
        assert "sad" in prompt_lower
        assert "angry" in prompt_lower


class TestEmotionDetectionPrompt:

    def test_prompt_is_string(self):
        assert isinstance(EMOTION_DETECTION_PROMPT, str)
        assert len(EMOTION_DETECTION_PROMPT) > 0

    def test_prompt_has_required_placeholders(self):
        assert "{user_message}" in EMOTION_DETECTION_PROMPT
        assert "{robot_response}" in EMOTION_DETECTION_PROMPT

    def test_prompt_lists_emotions(self):
        prompt_lower = EMOTION_DETECTION_PROMPT.lower()
        assert "neutral" in prompt_lower
        assert "happy" in prompt_lower
        assert "sad" in prompt_lower
        assert "anger" in prompt_lower
        assert "surprise" in prompt_lower


class TestBusyResponsePrompt:

    def test_prompt_is_string(self):
        assert isinstance(BUSY_RESPONSE_PROMPT, str)
        assert len(BUSY_RESPONSE_PROMPT) > 0

    def test_prompt_has_message_placeholder(self):
        assert "{message}" in BUSY_RESPONSE_PROMPT

    def test_prompt_mentions_busy_context(self):
        prompt_lower = BUSY_RESPONSE_PROMPT.lower()
        assert "busy" in prompt_lower

    def test_prompt_mentions_plantroid(self):
        assert "Plantroid" in BUSY_RESPONSE_PROMPT


class TestProblemAnnouncementPrompt:

    def test_prompt_is_string(self):
        assert isinstance(PROBLEM_ANNOUNCEMENT_PROMPT, str)
        assert len(PROBLEM_ANNOUNCEMENT_PROMPT) > 0

    def test_prompt_has_required_placeholders(self):
        assert "{message}" in PROBLEM_ANNOUNCEMENT_PROMPT
        assert "{problems}" in PROBLEM_ANNOUNCEMENT_PROMPT

    def test_prompt_mentions_problem_context(self):
        prompt_lower = PROBLEM_ANNOUNCEMENT_PROMPT.lower()
        assert "problem" in prompt_lower
        assert "soil" in prompt_lower


class TestFormatNotifications:

    def test_empty_notifications(self):
        result = format_notifications({})
        assert result == "No problems detected."

    def test_none_notifications(self):
        result = format_notifications(None)
        assert result == "No problems detected."

    def test_single_notification(self):
        notifications = {
            "moisture": ["low", "high"],
        }
        result = format_notifications(notifications)
        assert "moisture" in result
        assert "low" in result
        assert "high" in result

    def test_multiple_notifications(self):
        notifications = {
            "moisture": ["low", "high"],
            "temperature": ["25", "normal"],
            "pH": ["acidic", "medium"],
        }
        result = format_notifications(notifications)
        assert "moisture" in result
        assert "temperature" in result
        assert "pH" in result

    def test_notification_format(self):
        notifications = {
            "moisture": ["low", "high"],
        }
        result = format_notifications(notifications)
        assert result.startswith("-")
        assert "priority:" in result.lower()

    def test_notification_with_single_value(self):
        notifications = {
            "moisture": ["low"],
        }
        result = format_notifications(notifications)
        assert "moisture" in result
        assert "low" in result
        assert "normal" in result.lower()

    def test_notification_with_empty_values(self):
        notifications = {
            "moisture": [],
        }
        result = format_notifications(notifications)
        assert "moisture" in result
        assert "unknown" in result.lower()

    def test_return_type_is_string(self):
        assert isinstance(format_notifications({}), str)
        assert isinstance(format_notifications({"a": ["b"]}), str)
        assert isinstance(format_notifications(None), str)

    def test_multiline_output(self):
        notifications = {
            "moisture": ["low", "high"],
            "temperature": ["25", "normal"],
        }
        result = format_notifications(notifications)
        lines = result.strip().split("\n")
        assert len(lines) == 2

    def test_sensor_names_preserved(self):
        notifications = {
            "Soil Moisture": ["low", "high"],
            "pH Level": ["acidic", "medium"],
        }
        result = format_notifications(notifications)
        assert "Soil Moisture" in result
        assert "pH Level" in result
