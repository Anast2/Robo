"""
maestro_langgraph - LangGraph-based dialogue system for ROOTED robot.

This package replaces the hardcoded regex-based dialogue system with an
LLM-based solution using LangGraph for flow control and LangChain for
structured outputs.

Now includes sensor-aware response system for intelligent plant care.
"""

__version__ = "0.2.0"

from .sensor_tracker import (
    SensorTracker,
    SensorType,
    IssueSeverity,
    SensorIssue,
    UserResponseType,
    SensorThreshold,
    THRESHOLDS,
    MENTION_FREQUENCY,
)
from .solutions import (
    Solution,
    SOLUTIONS,
    get_solutions,
    get_quick_fix,
)
from .state import (
    DialogueState,
    Intent,
    Emotion,
    RobotStatus,
    PROSODY_PRESETS,
    get_prosody_for_emotion,
)
from .graph import (
    process_message,
    get_chains,
    set_chains,
    get_tracker,
    set_tracker,
)
from .chains import DialogueChains

__all__ = [
    # Sensor tracking
    "SensorTracker",
    "SensorType",
    "IssueSeverity",
    "SensorIssue",
    "UserResponseType",
    "SensorThreshold",
    "THRESHOLDS",
    "MENTION_FREQUENCY",
    # Solutions
    "Solution",
    "SOLUTIONS",
    "get_solutions",
    "get_quick_fix",
    # State
    "DialogueState",
    "Intent",
    "Emotion",
    "RobotStatus",
    "PROSODY_PRESETS",
    "get_prosody_for_emotion",
    # Graph
    "process_message",
    "get_chains",
    "set_chains",
    "get_tracker",
    "set_tracker",
    # Chains
    "DialogueChains",
]
