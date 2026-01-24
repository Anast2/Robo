"""Dialogue state schema for LangGraph."""

from typing import TypedDict, Optional, Literal
from enum import Enum


class Intent(str, Enum):
    """Intent types for dialogue classification."""
    GREETING = "greeting"
    FAREWELL = "farewell"
    QUESTION = "question"
    ACKNOWLEDGMENT = "acknowledgment"  # yes/no
    GENERAL = "general"  # fallback


class Emotion(str, Enum):
    """Emotion types matching the robot's 5-emotion model."""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGER = "anger"
    SURPRISE = "surprise"


class RobotStatus(str, Enum):
    """Robot availability status."""
    FREE = "free"
    BUSY = "busy"
    PROBLEM = "problem"  # has notifications to announce


class DialogueState(TypedDict, total=False):
    """State schema for the LangGraph dialogue flow.

    This state is passed through the graph and updated by each node.
    """
    # Input (from ROS message)
    human_message: str
    voice_emotion: str  # emotion detected from voice

    # Robot context
    robot_busy: bool
    robot_status: str  # "free", "busy", or "problem"
    has_problem: bool
    notifications: dict  # sensor alerts {sensor_name: [level, priority, ...]}

    # Conversation context
    conversation_history: list  # list of (role, message) tuples

    # Processing results
    intent: str  # classified intent
    entities: dict  # extracted entities (for tools)
    search_context: Optional[str]  # web search results
    context_response: Optional[str]  # response for busy/problem context

    # Output
    response: str
    response_emotion: str
    prosody: tuple  # (volume, speed, pitch) for TTS
    should_end_early: bool  # if True, skip normal response generation

    # Sensor awareness fields
    sensor_tracker_state: dict  # Serialized SensorTracker
    issues_to_mention: list  # List of SensorIssue dicts
    sensor_context: Optional[str]  # Context for response generation
    user_response_type: Optional[str]  # committed/deferred/rejected/question/unrelated
    pending_issue: Optional[dict]  # Issue being discussed
    improvement_detected: Optional[dict]  # Resolved issue to celebrate
    last_suggested_solution: Optional[str]  # Track what was suggested


# Prosody presets for each emotion
PROSODY_PRESETS = {
    Emotion.NEUTRAL: (150, 100, 45),
    Emotion.HAPPY: (160, 140, 65),
    Emotion.SAD: (80, 80, 35),
    Emotion.ANGER: (180, 200, 55),
    Emotion.SURPRISE: (200, 80, 65),
}


def get_prosody_for_emotion(emotion: str) -> tuple:
    """Get prosody values (volume, speed, pitch) for an emotion."""
    try:
        return PROSODY_PRESETS[Emotion(emotion)]
    except (ValueError, KeyError):
        return PROSODY_PRESETS[Emotion.NEUTRAL]
