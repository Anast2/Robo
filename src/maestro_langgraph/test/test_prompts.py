# Copyright 2024 ROOTED Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for prompts.py module."""

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
    """Tests for ROBOT_PERSONA constant."""

    def test_persona_is_string(self):
        """Test that persona is a non-empty string."""
        assert isinstance(ROBOT_PERSONA, str)
        assert len(ROBOT_PERSONA) > 0

    def test_persona_contains_robot_name(self):
        """Test that persona mentions Plantroid."""
        assert "Plantroid" in ROBOT_PERSONA

    def test_persona_contains_key_traits(self):
        """Test that persona contains key personality traits."""
        assert "friendly" in ROBOT_PERSONA.lower()
        assert "plant" in ROBOT_PERSONA.lower()


class TestIntentClassificationPrompt:
    """Tests for INTENT_CLASSIFICATION_PROMPT constant."""

    def test_prompt_is_string(self):
        """Test that prompt is a non-empty string."""
        assert isinstance(INTENT_CLASSIFICATION_PROMPT, str)
        assert len(INTENT_CLASSIFICATION_PROMPT) > 0

    def test_prompt_has_message_placeholder(self):
        """Test that prompt has {message} placeholder."""
        assert "{message}" in INTENT_CLASSIFICATION_PROMPT

    def test_prompt_mentions_intent_categories(self):
        """Test that prompt lists all intent categories."""
        prompt_lower = INTENT_CLASSIFICATION_PROMPT.lower()
        assert "greeting" in prompt_lower
        assert "farewell" in prompt_lower
        assert "question" in prompt_lower
        assert "acknowledgment" in prompt_lower
        assert "general" in prompt_lower


class TestResponseGenerationPrompt:
    """Tests for RESPONSE_GENERATION_PROMPT constant."""

    def test_prompt_is_string(self):
        """Test that prompt is a non-empty string."""
        assert isinstance(RESPONSE_GENERATION_PROMPT, str)
        assert len(RESPONSE_GENERATION_PROMPT) > 0

    def test_prompt_has_required_placeholders(self):
        """Test that prompt has all required placeholders."""
        assert "{message}" in RESPONSE_GENERATION_PROMPT
        assert "{emotion}" in RESPONSE_GENERATION_PROMPT
        assert "{history}" in RESPONSE_GENERATION_PROMPT

    def test_prompt_mentions_emotions(self):
        """Test that prompt mentions emotional response guidelines."""
        prompt_lower = RESPONSE_GENERATION_PROMPT.lower()
        assert "happy" in prompt_lower
        assert "sad" in prompt_lower
        assert "angry" in prompt_lower


class TestEmotionDetectionPrompt:
    """Tests for EMOTION_DETECTION_PROMPT constant."""

    def test_prompt_is_string(self):
        """Test that prompt is a non-empty string."""
        assert isinstance(EMOTION_DETECTION_PROMPT, str)
        assert len(EMOTION_DETECTION_PROMPT) > 0

    def test_prompt_has_required_placeholders(self):
        """Test that prompt has all required placeholders."""
        assert "{user_message}" in EMOTION_DETECTION_PROMPT
        assert "{robot_response}" in EMOTION_DETECTION_PROMPT

    def test_prompt_lists_emotions(self):
        """Test that prompt lists all valid emotions."""
        prompt_lower = EMOTION_DETECTION_PROMPT.lower()
        assert "neutral" in prompt_lower
        assert "happy" in prompt_lower
        assert "sad" in prompt_lower
        assert "anger" in prompt_lower
        assert "surprise" in prompt_lower


class TestBusyResponsePrompt:
    """Tests for BUSY_RESPONSE_PROMPT constant."""

    def test_prompt_is_string(self):
        """Test that prompt is a non-empty string."""
        assert isinstance(BUSY_RESPONSE_PROMPT, str)
        assert len(BUSY_RESPONSE_PROMPT) > 0

    def test_prompt_has_message_placeholder(self):
        """Test that prompt has {message} placeholder."""
        assert "{message}" in BUSY_RESPONSE_PROMPT

    def test_prompt_mentions_busy_context(self):
        """Test that prompt mentions being busy."""
        prompt_lower = BUSY_RESPONSE_PROMPT.lower()
        assert "busy" in prompt_lower

    def test_prompt_mentions_plantroid(self):
        """Test that prompt mentions Plantroid."""
        assert "Plantroid" in BUSY_RESPONSE_PROMPT


class TestProblemAnnouncementPrompt:
    """Tests for PROBLEM_ANNOUNCEMENT_PROMPT constant."""

    def test_prompt_is_string(self):
        """Test that prompt is a non-empty string."""
        assert isinstance(PROBLEM_ANNOUNCEMENT_PROMPT, str)
        assert len(PROBLEM_ANNOUNCEMENT_PROMPT) > 0

    def test_prompt_has_required_placeholders(self):
        """Test that prompt has all required placeholders."""
        assert "{message}" in PROBLEM_ANNOUNCEMENT_PROMPT
        assert "{problems}" in PROBLEM_ANNOUNCEMENT_PROMPT

    def test_prompt_mentions_problem_context(self):
        """Test that prompt mentions problems."""
        prompt_lower = PROBLEM_ANNOUNCEMENT_PROMPT.lower()
        assert "problem" in prompt_lower
        assert "soil" in prompt_lower


class TestFormatNotifications:
    """Tests for format_notifications function."""

    def test_empty_notifications(self):
        """Test formatting empty notifications dict."""
        result = format_notifications({})
        assert result == "No problems detected."

    def test_none_notifications(self):
        """Test formatting None notifications."""
        result = format_notifications(None)
        assert result == "No problems detected."

    def test_single_notification(self):
        """Test formatting single notification."""
        notifications = {
            "moisture": ["low", "high"],
        }
        result = format_notifications(notifications)
        assert "moisture" in result
        assert "low" in result
        assert "high" in result

    def test_multiple_notifications(self):
        """Test formatting multiple notifications."""
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
        """Test that notifications are formatted as bullet points."""
        notifications = {
            "moisture": ["low", "high"],
        }
        result = format_notifications(notifications)
        assert result.startswith("-")
        assert "priority:" in result.lower()

    def test_notification_with_single_value(self):
        """Test notification with only level (no priority)."""
        notifications = {
            "moisture": ["low"],
        }
        result = format_notifications(notifications)
        assert "moisture" in result
        assert "low" in result
        # Priority should default to "normal"
        assert "normal" in result.lower()

    def test_notification_with_empty_values(self):
        """Test notification with empty values list."""
        notifications = {
            "moisture": [],
        }
        result = format_notifications(notifications)
        assert "moisture" in result
        assert "unknown" in result.lower()

    def test_return_type_is_string(self):
        """Test that return type is always string."""
        assert isinstance(format_notifications({}), str)
        assert isinstance(format_notifications({"a": ["b"]}), str)
        assert isinstance(format_notifications(None), str)

    def test_multiline_output(self):
        """Test that multiple notifications are on separate lines."""
        notifications = {
            "moisture": ["low", "high"],
            "temperature": ["25", "normal"],
        }
        result = format_notifications(notifications)
        lines = result.strip().split("\n")
        assert len(lines) == 2

    def test_sensor_names_preserved(self):
        """Test that sensor names are preserved exactly."""
        notifications = {
            "Soil Moisture": ["low", "high"],
            "pH Level": ["acidic", "medium"],
        }
        result = format_notifications(notifications)
        assert "Soil Moisture" in result
        assert "pH Level" in result
