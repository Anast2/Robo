Complete Implementation Plan: Sensor-Aware Response System

 Task Summary

 Enhance maestro_langgraph AI Agent with intelligent sensor monitoring that naturally integrates plant care issues into conversation.

 ---
 Step 1: Create sensor_tracker.py

 File: src/maestro_langgraph/maestro_langgraph/sensor_tracker.py

 """Sensor tracking and issue management system."""

 from dataclasses import dataclass, field
 from enum import Enum
 from typing import Dict, List, Optional
 from datetime import datetime


 class SensorType(str, Enum):
     TEMPERATURE = "temperature"
     MOISTURE = "moisture"
     LIGHT = "light"
     PH = "pH"


 class IssueSeverity(str, Enum):
     CRITICAL = "critical"
     HIGH = "high"
     MEDIUM = "medium"
     LOW = "low"
     OPTIMAL = "optimal"


 class UserResponseType(str, Enum):
     COMMITTED = "committed"      # "I'll do it now", "Done"
     DEFERRED = "deferred"        # "I'll do it later"
     REJECTED = "rejected"        # "No", "I can't"
     QUESTION = "question"        # "Why?", "What should I do?"
     UNRELATED = "unrelated"      # Didn't address the issue


 @dataclass
 class SensorThreshold:
     sensor_type: SensorType
     optimal_min: float
     optimal_max: float
     warning_min: float
     warning_max: float
     critical_min: float
     critical_max: float
     unit: str

     def classify(self, value: float) -> IssueSeverity:
         if self.optimal_min <= value <= self.optimal_max:
             return IssueSeverity.OPTIMAL
         elif value < self.critical_min or value > self.critical_max:
             return IssueSeverity.CRITICAL
         elif value < self.warning_min or value > self.warning_max:
             return IssueSeverity.HIGH
         elif value < self.optimal_min:
             return IssueSeverity.MEDIUM
         else:
             return IssueSeverity.LOW

     def get_direction(self, value: float) -> str:
         if value < self.optimal_min:
             return "too_low"
         return "too_high"


 # Threshold configurations per requirements
 THRESHOLDS = {
     SensorType.TEMPERATURE: SensorThreshold(
         sensor_type=SensorType.TEMPERATURE,
         optimal_min=20.0, optimal_max=25.0,
         warning_min=18.0, warning_max=27.0,
         critical_min=15.0, critical_max=30.0,
         unit="°C"
     ),
     SensorType.MOISTURE: SensorThreshold(
         sensor_type=SensorType.MOISTURE,
         optimal_min=40.0, optimal_max=60.0,
         warning_min=35.0, warning_max=65.0,
         critical_min=30.0, critical_max=70.0,
         unit="%"
     ),
     SensorType.LIGHT: SensorThreshold(
         sensor_type=SensorType.LIGHT,
         optimal_min=2000.0, optimal_max=4000.0,
         warning_min=1500.0, warning_max=4500.0,
         critical_min=1000.0, critical_max=5000.0,
         unit="lux"
     ),
     SensorType.PH: SensorThreshold(
         sensor_type=SensorType.PH,
         optimal_min=6.0, optimal_max=7.0,
         warning_min=5.5, warning_max=7.5,
         critical_min=5.0, critical_max=8.0,
         unit=""
     ),
 }

 # Mention frequency by severity
 MENTION_FREQUENCY = {
     IssueSeverity.CRITICAL: 1,   # Every interaction
     IssueSeverity.HIGH: 2,       # Every 2nd
     IssueSeverity.MEDIUM: 3,     # Every 3rd
     IssueSeverity.LOW: 999999,   # Once per conversation
 }


 @dataclass
 class SensorIssue:
     sensor_type: SensorType
     current_value: float
     severity: IssueSeverity
     direction: str  # "too_low" or "too_high"
     first_detected: datetime = field(default_factory=datetime.now)
     last_mentioned: Optional[datetime] = None
     mention_count: int = 0
     user_response: Optional[UserResponseType] = None
     solutions_suggested: List[str] = field(default_factory=list)

     def to_dict(self) -> dict:
         return {
             "sensor_type": self.sensor_type.value,
             "current_value": self.current_value,
             "severity": self.severity.value,
             "direction": self.direction,
             "first_detected": self.first_detected.isoformat(),
             "last_mentioned": self.last_mentioned.isoformat() if self.last_mentioned else None,
             "mention_count": self.mention_count,
             "user_response": self.user_response.value if self.user_response else None,
             "solutions_suggested": self.solutions_suggested,
         }

     @classmethod
     def from_dict(cls, data: dict) -> "SensorIssue":
         return cls(
             sensor_type=SensorType(data["sensor_type"]),
             current_value=data["current_value"],
             severity=IssueSeverity(data["severity"]),
             direction=data["direction"],
             first_detected=datetime.fromisoformat(data["first_detected"]),
             last_mentioned=datetime.fromisoformat(data["last_mentioned"]) if data.get("last_mentioned") else None,
             mention_count=data.get("mention_count", 0),
             user_response=UserResponseType(data["user_response"]) if data.get("user_response") else None,
             solutions_suggested=data.get("solutions_suggested", []),
         )


 class SensorTracker:
     """Tracks sensor issues and determines when to mention them."""

     def __init__(self):
         self.active_issues: Dict[str, SensorIssue] = {}
         self.interaction_count: int = 0
         self.mentioned_this_conversation: set = set()
         self.pending_issue: Optional[str] = None  # Issue being discussed

     def process_reading(self, sensor_type: SensorType, value: float) -> Optional[SensorIssue]:
         """Process a sensor reading and update issue tracking."""
         threshold = THRESHOLDS.get(sensor_type)
         if not threshold:
             return None

         severity = threshold.classify(value)
         key = sensor_type.value

         if severity == IssueSeverity.OPTIMAL:
             # Issue resolved
             if key in self.active_issues:
                 resolved = self.active_issues.pop(key)
                 return resolved  # Return for celebration
             return None

         direction = threshold.get_direction(value)

         if key in self.active_issues:
             # Update existing issue
             issue = self.active_issues[key]
             issue.current_value = value
             issue.severity = severity
             issue.direction = direction
         else:
             # New issue
             issue = SensorIssue(
                 sensor_type=sensor_type,
                 current_value=value,
                 severity=severity,
                 direction=direction,
             )
             self.active_issues[key] = issue

         return issue

     def process_notification(self, sensor_name: str, values: List[str]) -> Optional[SensorIssue]:
         """Process notification from notificationTopic."""
         # Map sensor name to type
         name_map = {
             "moisture": SensorType.MOISTURE,
             "soil_moisture": SensorType.MOISTURE,
             "temperature": SensorType.TEMPERATURE,
             "temp": SensorType.TEMPERATURE,
             "light": SensorType.LIGHT,
             "lux": SensorType.LIGHT,
             "ph": SensorType.PH,
             "acidity": SensorType.PH,
         }

         sensor_type = name_map.get(sensor_name.lower())
         if not sensor_type:
             return None

         # Try to extract numeric value
         try:
             value = float(values[0].replace("%", "").replace("°C", "").replace("lux", "").strip())
         except (ValueError, IndexError):
             return None

         return self.process_reading(sensor_type, value)

     def get_issues_to_mention(self) -> List[SensorIssue]:
         """Get issues that should be mentioned this interaction."""
         self.interaction_count += 1
         to_mention = []

         # Sort by severity (critical first)
         severity_order = [IssueSeverity.CRITICAL, IssueSeverity.HIGH, IssueSeverity.MEDIUM, IssueSeverity.LOW]
         sorted_issues = sorted(
             self.active_issues.values(),
             key=lambda i: severity_order.index(i.severity)
         )

         for issue in sorted_issues:
             key = issue.sensor_type.value
             frequency = MENTION_FREQUENCY[issue.severity]

             # Check if should mention based on frequency
             if issue.severity == IssueSeverity.LOW:
                 # Low: only once per conversation
                 if key not in self.mentioned_this_conversation:
                     to_mention.append(issue)
             elif self.interaction_count % frequency == 0 or issue.mention_count == 0:
                 # First time or frequency match
                 to_mention.append(issue)

         return to_mention

     def record_mention(self, issue: SensorIssue, solutions: List[str] = None):
         """Record that an issue was mentioned."""
         key = issue.sensor_type.value
         if key in self.active_issues:
             self.active_issues[key].last_mentioned = datetime.now()
             self.active_issues[key].mention_count += 1
             if solutions:
                 self.active_issues[key].solutions_suggested.extend(solutions)
             self.mentioned_this_conversation.add(key)
             self.pending_issue = key

     def record_user_response(self, response_type: UserResponseType):
         """Record user's response to pending issue."""
         if self.pending_issue and self.pending_issue in self.active_issues:
             self.active_issues[self.pending_issue].user_response = response_type

     def get_pending_issue(self) -> Optional[SensorIssue]:
         """Get the issue currently being discussed."""
         if self.pending_issue:
             return self.active_issues.get(self.pending_issue)
         return None

     def reset_conversation(self):
         """Reset conversation-level tracking."""
         self.mentioned_this_conversation.clear()
         self.pending_issue = None
         # Keep active_issues - they persist

     def to_state(self) -> dict:
         """Serialize to dict for state passing."""
         return {
             "active_issues": {k: v.to_dict() for k, v in self.active_issues.items()},
             "interaction_count": self.interaction_count,
             "mentioned_this_conversation": list(self.mentioned_this_conversation),
             "pending_issue": self.pending_issue,
         }

     def load_state(self, state: dict):
         """Load from serialized state."""
         if not state:
             return
         self.active_issues = {
             k: SensorIssue.from_dict(v)
             for k, v in state.get("active_issues", {}).items()
         }
         self.interaction_count = state.get("interaction_count", 0)
         self.mentioned_this_conversation = set(state.get("mentioned_this_conversation", []))
         self.pending_issue = state.get("pending_issue")

 ---
 Step 2: Create solutions.py

 File: src/maestro_langgraph/maestro_langgraph/solutions.py

 """Solution suggestions for sensor issues."""

 from dataclasses import dataclass
 from typing import Dict, List
 from .sensor_tracker import SensorType


 @dataclass
 class Solution:
     description: str
     action: str
     timeframe: str
     consequence: str
     time_until_damage: str
     complexity: int  # 1=simple, 2=moderate, 3=complex
     is_quick_fix: bool


 SOLUTIONS: Dict[SensorType, Dict[str, List[Solution]]] = {
     SensorType.MOISTURE: {
         "too_low": [
             Solution(
                 description="Manual watering",
                 action="water the plant thoroughly until water drains from the bottom",
                 timeframe="immediately",
                 consequence="wilting and potential plant death",
                 time_until_damage="24 hours",
                 complexity=1,
                 is_quick_fix=True,
             ),
             Solution(
                 description="Check irrigation system",
                 action="check the water flow and timer settings on the irrigation system",
                 timeframe="within an hour",
                 consequence="continued water stress",
                 time_until_damage="24-48 hours",
                 complexity=2,
                 is_quick_fix=False,
             ),
             Solution(
                 description="Add mulch",
                 action="add a layer of mulch around the plant to retain moisture",
                 timeframe="when possible",
                 consequence="rapid moisture loss",
                 time_until_damage="2-3 days",
                 complexity=2,
                 is_quick_fix=False,
             ),
         ],
         "too_high": [
             Solution(
                 description="Improve drainage",
                 action="check drainage holes and let soil dry out before watering again",
                 timeframe="immediately",
                 consequence="root rot and fungal infections",
                 time_until_damage="2-3 days",
                 complexity=1,
                 is_quick_fix=True,
             ),
             Solution(
                 description="Reduce watering frequency",
                 action="skip the next scheduled watering",
                 timeframe="next watering cycle",
                 consequence="oxygen deprivation for roots",
                 time_until_damage="3-5 days",
                 complexity=1,
                 is_quick_fix=True,
             ),
         ],
     },
     SensorType.TEMPERATURE: {
         "too_low": [
             Solution(
                 description="Move to warmer spot",
                 action="move the plant away from cold windows or drafts",
                 timeframe="immediately",
                 consequence="cold stress and slowed growth",
                 time_until_damage="12-24 hours",
                 complexity=1,
                 is_quick_fix=True,
             ),
             Solution(
                 description="Use heating mat",
                 action="place a seedling heating mat under the pot",
                 timeframe="within a day",
                 consequence="potential root damage",
                 time_until_damage="24-48 hours",
                 complexity=2,
                 is_quick_fix=False,
             ),
         ],
         "too_high": [
             Solution(
                 description="Increase airflow",
                 action="turn on a fan or open windows for better air circulation",
                 timeframe="immediately",
                 consequence="heat stress and wilting",
                 time_until_damage="6-12 hours",
                 complexity=1,
                 is_quick_fix=True,
             ),
             Solution(
                 description="Move to cooler spot",
                 action="move the plant away from direct sunlight or heat sources",
                 timeframe="immediately",
                 consequence="leaf burn and dehydration",
                 time_until_damage="12-24 hours",
                 complexity=1,
                 is_quick_fix=True,
             ),
         ],
     },
     SensorType.LIGHT: {
         "too_low": [
             Solution(
                 description="Move to brighter location",
                 action="move the plant closer to a window with indirect sunlight",
                 timeframe="when possible",
                 consequence="leggy growth and weak stems",
                 time_until_damage="1-2 weeks",
                 complexity=1,
                 is_quick_fix=True,
             ),
             Solution(
                 description="Add grow light",
                 action="set up a grow light above the plant",
                 timeframe="within a few days",
                 consequence="poor photosynthesis",
                 time_until_damage="2-3 weeks",
                 complexity=2,
                 is_quick_fix=False,
             ),
         ],
         "too_high": [
             Solution(
                 description="Add shade",
                 action="move the plant away from direct sunlight or add a sheer curtain",
                 timeframe="immediately",
                 consequence="leaf burn and bleaching",
                 time_until_damage="1-2 days",
                 complexity=1,
                 is_quick_fix=True,
             ),
         ],
     },
     SensorType.PH: {
         "too_low": [
             Solution(
                 description="Add lime",
                 action="add a small amount of garden lime to raise pH",
                 timeframe="when possible",
                 consequence="nutrient lockout",
                 time_until_damage="1-2 weeks",
                 complexity=2,
                 is_quick_fix=False,
             ),
         ],
         "too_high": [
             Solution(
                 description="Add sulfur",
                 action="add a small amount of sulfur to lower pH",
                 timeframe="when possible",
                 consequence="nutrient lockout",
                 time_until_damage="1-2 weeks",
                 complexity=2,
                 is_quick_fix=False,
             ),
         ],
     },
 }


 def get_solutions(sensor_type: SensorType, direction: str, exclude: List[str] = None) -> List[Solution]:
     """Get solutions for an issue, excluding already suggested ones."""
     exclude = exclude or []
     all_solutions = SOLUTIONS.get(sensor_type, {}).get(direction, [])
     return [s for s in all_solutions if s.description not in exclude]


 def get_quick_fix(sensor_type: SensorType, direction: str) -> Optional[Solution]:
     """Get the simplest quick fix for an issue."""
     solutions = get_solutions(sensor_type, direction)
     for s in solutions:
         if s.is_quick_fix:
             return s
     return solutions[0] if solutions else None

 ---
 Step 3: Update state.py

 File: src/maestro_langgraph/maestro_langgraph/state.py

 Add new fields to DialogueState:

 # Add after existing fields (line ~60):

     # Sensor awareness fields
     sensor_tracker_state: dict              # Serialized SensorTracker
     issues_to_mention: list                 # List of SensorIssue dicts
     sensor_context: Optional[str]           # Context for response generation
     user_response_type: Optional[str]       # committed/deferred/rejected/question/unrelated
     pending_issue: Optional[dict]           # Issue being discussed
     improvement_detected: Optional[dict]    # Resolved issue to celebrate
     last_suggested_solution: Optional[str]  # Track what was suggested

 ---
 Step 4: Update prompts.py

 File: src/maestro_langgraph/maestro_langgraph/prompts.py

 Add new prompts:

 # Add after existing prompts:

 # Detect user response to sensor issue
 USER_RESPONSE_CLASSIFICATION_PROMPT = """Classify the user's response to a sensor issue.

 The robot mentioned this issue: {issue_description}
 User said: {message}

 Categories:
 - committed: User will fix it now ("I'll do it", "OK I'll water it", "Done", "I watered it")
 - deferred: User will fix it later ("I'll do it later", "Maybe later", "Not now")
 - rejected: User won't fix it ("No", "I can't", "Not possible")
 - question: User asks about it ("Why?", "What should I do?", "How?")
 - unrelated: User didn't address the issue at all

 Respond with ONLY the category name."""


 # Integrate sensor info into response naturally
 SENSOR_INTEGRATED_RESPONSE_PROMPT = """You already have a response to the user. Now add sensor issue information naturally.

 Your base response: {base_response}

 Sensor issue to mention:
 - Type: {sensor_type}
 - Current value: {value}{unit}
 - Optimal range: {optimal_min}-{optimal_max}{unit}
 - Problem: {direction}
 - Severity: {severity}

 Suggested action: {action}
 Expected outcome: {outcome}

 Create a combined response that:
 1. First delivers your base response naturally
 2. Smoothly transitions ("I notice...", "By the way...", "I also noticed...")
 3. Mentions the issue with the actual value
 4. Suggests the action
 5. Explains briefly why it matters

 Keep total response to 3-4 sentences. Be caring but not alarming.

 Combined response:"""


 # Response when user defers action
 DEFERRED_RESPONSE_PROMPT = """The user said they will fix the issue later. Respond empathetically.

 Issue: {sensor_type} at {value}{unit} (should be {optimal_min}-{optimal_max}{unit})
 User said: {message}
 Time until damage: {time_until_damage}
 Quick fix alternative: {quick_fix_action}

 Generate a response that:
 1. Acknowledges their situation ("I understand you're busy")
 2. Gently reminds about time-sensitive consequences with timeframe
 3. Offers the quick fix as an easier alternative
 4. Asks if that would be possible

 Be friendly and understanding, not pushy. 2-3 sentences max.

 Response:"""


 # Celebrate resolved issue
 IMPROVEMENT_CELEBRATION_PROMPT = """A sensor issue was resolved! Respond happily.

 Your base response: {base_response}
 Resolved issue: {sensor_type} is now back to normal
 Previous value: {previous_value}
 Current value: {current_value}

 Add a brief, warm celebration to your response. Thank the user for their help.
 Keep it to 1-2 additional sentences.

 Response:"""


 # Follow-up on previous suggestion
 FOLLOW_UP_PROMPT = """Check on a previously suggested solution.

 Previous suggestion: {suggestion}
 Time elapsed: {time_elapsed}
 Sensor: {sensor_type}
 Current value: {current_value} (still {status})

 Generate a brief, friendly follow-up question to check if the user tried the solution.
 Be curious but not pushy.

 Response:"""

 ---
 Step 5: Update chains.py

 File: src/maestro_langgraph/maestro_langgraph/chains.py

 Add new methods and chains:

 # Add imports at top:
 from .prompts import (
     # ... existing imports ...
     USER_RESPONSE_CLASSIFICATION_PROMPT,
     SENSOR_INTEGRATED_RESPONSE_PROMPT,
     DEFERRED_RESPONSE_PROMPT,
     IMPROVEMENT_CELEBRATION_PROMPT,
 )
 from .sensor_tracker import UserResponseType, SensorType, THRESHOLDS
 from .solutions import get_solutions, get_quick_fix

 # Add to _setup_chains method:
     def _setup_chains(self):
         # ... existing chains ...

         # User response classification chain
         user_response_prompt = ChatPromptTemplate.from_template(USER_RESPONSE_CLASSIFICATION_PROMPT)
         self.user_response_chain = user_response_prompt | self.llm | StrOutputParser()

         # Sensor integrated response chain
         sensor_response_prompt = ChatPromptTemplate.from_template(SENSOR_INTEGRATED_RESPONSE_PROMPT)
         self.sensor_response_chain = sensor_response_prompt | self.llm | StrOutputParser()

         # Deferred response chain
         deferred_prompt = ChatPromptTemplate.from_template(DEFERRED_RESPONSE_PROMPT)
         self.deferred_chain = deferred_prompt | self.llm | StrOutputParser()

         # Celebration chain
         celebration_prompt = ChatPromptTemplate.from_template(IMPROVEMENT_CELEBRATION_PROMPT)
         self.celebration_chain = celebration_prompt | self.llm | StrOutputParser()

 # Add new methods:
     def classify_user_response(self, message: str, issue_description: str) -> UserResponseType:
         """Classify user's response to a sensor issue."""
         try:
             result = self.user_response_chain.invoke({
                 "message": message,
                 "issue_description": issue_description,
             })
             response = result.strip().lower()

             # Map to enum
             mapping = {
                 "committed": UserResponseType.COMMITTED,
                 "deferred": UserResponseType.DEFERRED,
                 "rejected": UserResponseType.REJECTED,
                 "question": UserResponseType.QUESTION,
                 "unrelated": UserResponseType.UNRELATED,
             }
             return mapping.get(response, UserResponseType.UNRELATED)
         except Exception as e:
             print(f"User response classification error: {e}")
             return UserResponseType.UNRELATED

     def generate_sensor_integrated_response(
         self,
         base_response: str,
         issue: dict,
         solution: dict,
     ) -> str:
         """Generate response that naturally integrates sensor issue."""
         try:
             sensor_type = SensorType(issue["sensor_type"])
             threshold = THRESHOLDS[sensor_type]

             result = self.sensor_response_chain.invoke({
                 "base_response": base_response,
                 "sensor_type": issue["sensor_type"],
                 "value": issue["current_value"],
                 "unit": threshold.unit,
                 "optimal_min": threshold.optimal_min,
                 "optimal_max": threshold.optimal_max,
                 "direction": "too low" if issue["direction"] == "too_low" else "too high",
                 "severity": issue["severity"],
                 "action": solution["action"] if solution else "check on it",
                 "outcome": f"get it back to optimal levels ({threshold.optimal_min}-{threshold.optimal_max}{threshold.unit})",
             })
             return result.strip()
         except Exception as e:
             print(f"Sensor integrated response error: {e}")
             return base_response

     def generate_deferred_response(
         self,
         message: str,
         issue: dict,
         quick_fix: dict,
     ) -> str:
         """Generate empathetic response when user defers action."""
         try:
             sensor_type = SensorType(issue["sensor_type"])
             threshold = THRESHOLDS[sensor_type]

             result = self.deferred_chain.invoke({
                 "sensor_type": issue["sensor_type"],
                 "value": issue["current_value"],
                 "unit": threshold.unit,
                 "optimal_min": threshold.optimal_min,
                 "optimal_max": threshold.optimal_max,
                 "message": message,
                 "time_until_damage": quick_fix["time_until_damage"] if quick_fix else "soon",
                 "quick_fix_action": quick_fix["action"] if quick_fix else "a quick check",
             })
             return result.strip()
         except Exception as e:
             print(f"Deferred response error: {e}")
             return "I understand. Just keep an eye on it when you can."

     def generate_celebration_response(
         self,
         base_response: str,
         sensor_type: str,
         previous_value: float,
         current_value: float,
     ) -> str:
         """Generate happy response for resolved issue."""
         try:
             result = self.celebration_chain.invoke({
                 "base_response": base_response,
                 "sensor_type": sensor_type,
                 "previous_value": previous_value,
                 "current_value": current_value,
             })
             return result.strip()
         except Exception as e:
             print(f"Celebration response error: {e}")
             return base_response

 ---
 Step 6: Update graph.py

 File: src/maestro_langgraph/maestro_langgraph/graph.py

 Add new nodes and modify graph:

 # Add imports:
 from .sensor_tracker import SensorTracker, UserResponseType, SensorType, THRESHOLDS
 from .solutions import get_solutions, get_quick_fix

 # Global tracker (persistent)
 _tracker: SensorTracker = None

 def get_tracker() -> SensorTracker:
     global _tracker
     if _tracker is None:
         _tracker = SensorTracker()
     return _tracker

 def set_tracker(tracker: SensorTracker):
     global _tracker
     _tracker = tracker


 # NEW NODE: Process sensor issues
 def process_sensor_issues_node(state: DialogueState) -> DialogueState:
     """Update tracker and determine which issues to mention."""
     tracker = get_tracker()

     # Load state if provided
     if state.get("sensor_tracker_state"):
         tracker.load_state(state["sensor_tracker_state"])

     # Process notifications
     notifications = state.get("notifications", {})
     improvement = None

     for sensor_name, values in notifications.items():
         result = tracker.process_notification(sensor_name, values)
         if result and result.severity.value == "optimal":
             improvement = result  # Issue resolved!

     # Get issues to mention
     issues = tracker.get_issues_to_mention()

     return {
         **state,
         "sensor_tracker_state": tracker.to_state(),
         "issues_to_mention": [i.to_dict() for i in issues],
         "improvement_detected": improvement.to_dict() if improvement else None,
     }


 # NEW NODE: Check user response to issue
 def check_user_response_node(state: DialogueState) -> DialogueState:
     """Check if user responded to a pending sensor issue."""
     tracker = get_tracker()
     chains = get_chains()

     pending = tracker.get_pending_issue()
     if not pending:
         return {**state, "user_response_type": None}

     message = state.get("human_message", "")
     issue_desc = f"{pending.sensor_type.value} is {pending.direction.replace('_', ' ')}"

     response_type = chains.classify_user_response(message, issue_desc)
     tracker.record_user_response(response_type)

     return {
         **state,
         "user_response_type": response_type.value,
         "pending_issue": pending.to_dict(),
         "sensor_tracker_state": tracker.to_state(),
     }


 # NEW NODE: Integrate sensor info into response
 def integrate_sensor_response_node(state: DialogueState) -> DialogueState:
     """Add sensor issue information to response naturally."""
     chains = get_chains()
     tracker = get_tracker()

     base_response = state.get("response", "")
     user_response_type = state.get("user_response_type")
     issues = state.get("issues_to_mention", [])
     pending = state.get("pending_issue")
     improvement = state.get("improvement_detected")

     # Case 1: Celebrate improvement
     if improvement:
         response = chains.generate_celebration_response(
             base_response=base_response,
             sensor_type=improvement["sensor_type"],
             previous_value=improvement.get("current_value", 0),
             current_value=0,  # Now optimal
         )
         return {**state, "response": response, "response_emotion": "happy"}

     # Case 2: User deferred action
     if user_response_type == UserResponseType.DEFERRED.value and pending:
         sensor_type = SensorType(pending["sensor_type"])
         quick_fix = get_quick_fix(sensor_type, pending["direction"])

         response = chains.generate_deferred_response(
             message=state.get("human_message", ""),
             issue=pending,
             quick_fix={"action": quick_fix.action, "time_until_damage": quick_fix.time_until_damage} if quick_fix else None,
         )
         return {**state, "response": response}

     # Case 3: User committed to fix
     if user_response_type == UserResponseType.COMMITTED.value:
         # Simple acknowledgment, issue will be tracked
         return {**state, "response": base_response + " Thank you, I appreciate your help!"}

     # Case 4: New issues to mention
     if issues:
         issue = issues[0]  # Most critical first
         sensor_type = SensorType(issue["sensor_type"])
         solutions = get_solutions(sensor_type, issue["direction"], issue.get("solutions_suggested", []))
         solution = solutions[0] if solutions else None

         response = chains.generate_sensor_integrated_response(
             base_response=base_response,
             issue=issue,
             solution={"action": solution.action} if solution else None,
         )

         # Record mention
         tracker.record_mention(
             tracker.active_issues[issue["sensor_type"]],
             [solution.description] if solution else []
         )

         return {
             **state,
             "response": response,
             "last_suggested_solution": solution.description if solution else None,
             "sensor_tracker_state": tracker.to_state(),
         }

     return state


 # Update build_dialogue_graph:
 def build_dialogue_graph() -> StateGraph:
     """Build the sensor-aware dialogue graph."""
     graph = StateGraph(DialogueState)

     # Nodes
     graph.add_node("check_context", check_context_node)
     graph.add_node("process_sensors", process_sensor_issues_node)  # NEW
     graph.add_node("classify_intent", classify_intent_node)
     graph.add_node("check_user_response", check_user_response_node)  # NEW
     graph.add_node("check_search", check_search_node)
     graph.add_node("generate_response", generate_response_node)
     graph.add_node("integrate_sensors", integrate_sensor_response_node)  # NEW
     graph.add_node("determine_emotion", determine_emotion_node)
     graph.add_node("update_history", update_history_node)

     # Entry
     graph.set_entry_point("check_context")

     # Conditional after context check
     graph.add_conditional_edges(
         "check_context",
         route_after_context,
         {
             "busy_response": "generate_response",
             "normal_flow": "process_sensors",
         }
     )

     # Flow
     graph.add_edge("process_sensors", "classify_intent")
     graph.add_edge("classify_intent", "check_user_response")
     graph.add_edge("check_user_response", "check_search")
     graph.add_edge("check_search", "generate_response")
     graph.add_edge("generate_response", "integrate_sensors")
     graph.add_edge("integrate_sensors", "determine_emotion")
     graph.add_edge("determine_emotion", "update_history")
     graph.add_edge("update_history", END)

     return graph.compile()


 # Update process_message to accept tracker state:
 def process_message(
     message: str,
     voice_emotion: str = "neutral",
     history: list = None,
     robot_busy: bool = False,
     notifications: dict = None,
     sensor_tracker_state: dict = None,  # NEW
 ) -> DialogueState:
     """Process a user message through the dialogue graph."""
     initial_state: DialogueState = {
         "human_message": message,
         "voice_emotion": voice_emotion,
         "conversation_history": history or [],
         "robot_busy": robot_busy,
         "has_problem": bool(notifications),
         "notifications": notifications or {},
         "search_context": None,
         "sensor_tracker_state": sensor_tracker_state or {},  # NEW
     }

     graph = build_dialogue_graph()
     final_state = graph.invoke(initial_state)

     return final_state

 ---
 Step 7: Update maestro_node.py

 File: src/maestro_langgraph/maestro_langgraph/maestro_node.py

 Integrate sensor tracker:

 # Add import:
 from .sensor_tracker import SensorTracker
 from .graph import set_tracker

 # In __init__, add:
         # Persistent sensor tracker
         self.sensor_tracker = SensorTracker()
         set_tracker(self.sensor_tracker)

 # Update cb_function_conversation:
     def cb_function_conversation(self, msg: String):
         """Handle incoming human speech."""
         parts = msg.data.split(";")
         human_speech = parts[0]
         voice_emotion = parts[2] if len(parts) > 2 else "neutral"

         self.get_logger().info(f'Received: "{human_speech}" (emotion: {voice_emotion})')
         self._publish_listen_block()

         # Process with sensor tracker state
         result = process_message(
             message=human_speech,
             voice_emotion=voice_emotion,
             history=self.conversation_history,
             robot_busy=self.robot_busy,
             notifications=self.notifications,
             sensor_tracker_state=self.sensor_tracker.to_state(),  # NEW
         )

         # Update tracker from result
         if result.get("sensor_tracker_state"):
             self.sensor_tracker.load_state(result["sensor_tracker_state"])

         self.conversation_history = result.get("conversation_history", [])
         response = result.get("response", "")
         emotion = result.get("response_emotion", "neutral")
         prosody = result.get("prosody", (150, 100, 45))
         robot_status = result.get("robot_status", "free")

         self.get_logger().info(f'Response: "{response}" (emotion: {emotion})')

         # DON'T clear all notifications - only clear acknowledged ones
         user_response = result.get("user_response_type")
         if user_response == "committed":
             # Clear only the acknowledged issue
             pending = result.get("pending_issue")
             if pending:
                 sensor_type = pending.get("sensor_type")
                 self._clear_notification_for_sensor(sensor_type)

         self._publish_emotion(emotion)
         self._send_tts(response, prosody)

 # Add helper method:
     def _clear_notification_for_sensor(self, sensor_type: str):
         """Clear notifications related to a specific sensor type."""
         if not sensor_type:
             return

         mapping = {
             "moisture": ["moisture", "soil_moisture"],
             "temperature": ["temperature", "temp"],
             "light": ["light", "lux"],
             "pH": ["ph", "acidity"],
         }

         keys_to_remove = mapping.get(sensor_type, [])
         for key in list(self.notifications.keys()):
             if key.lower() in keys_to_remove:
                 del self.notifications[key]

         self.get_logger().info(f'Cleared notifications for {sensor_type}')

 ---
 Step 8: Update __init__.py

 File: src/maestro_langgraph/maestro_langgraph/__init__.py

 Add exports:

 from .sensor_tracker import (
     SensorTracker,
     SensorType,
     IssueSeverity,
     SensorIssue,
     UserResponseType,
     THRESHOLDS,
 )
 from .solutions import Solution, get_solutions, get_quick_fix

 ---
 Verification

 Test Conversation Flow:

 1. Start with notification: moisture=32%

 User: "Hello, how are you today?"
 Expected: "Hi! I'm doing well, thank you for asking. I notice the soil moisture
           is quite low (32%). Would you mind checking the irrigation system?
           A quick check of the water flow and timer settings should help get
           it back to optimal levels."

 User: "I'll do it later."
 Expected: "I understand you're busy. Just keep in mind that the plants might
           start showing stress signs within 24 hours if this isn't addressed.
           The quickest fix would be a manual watering for now. Would that be possible?"

 User: "OK, I'll water it now."
 Expected: "Thank you, I appreciate your help!"

 [Later, moisture=45%]
 User: "Hi again"
 Expected: "Hello! Great news - the soil moisture is back to normal levels now.
           Thank you so much for taking care of that!"

 Test Commands:

 # Inject notification
 ros2 topic pub /notificationTopic std_msgs/String "data: 'moisture:32:critical'"

 # Send message
 ros2 topic pub /messageTopic std_msgs/String "data: 'Hello how are you;meta;neutral'"