#!/usr/bin/env python3
"""ROS 2 node wrapper for LangGraph dialogue system.

Includes busy/problem context checking like original MAESTRO.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rcl_interfaces.msg import ParameterDescriptor
from ast import literal_eval

from rooted_interfaces.tts_interface import TTSinterface
from rooted_interfaces.busy_interface import BusyInterface

from .graph import process_message, set_chains
from .chains import DialogueChains


class MaestroLangGraphNode(Node):
    """ROS 2 node that uses LangGraph for dialogue management.

    Subscribes to:
        - messageTopic: Human speech input (format: "text;metadata;voice_emotion")
        - notificationTopic: Sensor alerts (format: "sensor_name:level:priority")
        - seenTopic: Person detection events
        - busy_state_publisher: Robot busy state

    Publishes to:
        - emotionTopic: Robot facial expression commands
        - ListenBlockTopic: Signal to pause listening during speech
    """

    def __init__(self):
        super().__init__('maestro_langgraph')

        # Parameters
        model_descriptor = ParameterDescriptor(
            description='Model name for dialogue generation (used by Ollama; LM Studio uses loaded model)'
        )
        self.declare_parameter('model_name', 'qwen2:0.5b', model_descriptor)
        self.model_name = self.get_parameter('model_name').value

        backend_descriptor = ParameterDescriptor(
            description='LLM backend: "ollama" or "lmstudio"'
        )
        self.declare_parameter('backend', 'ollama', backend_descriptor)
        self.backend = self.get_parameter('backend').value

        base_url_descriptor = ParameterDescriptor(
            description='LLM server URL (auto-detected if empty)'
        )
        self.declare_parameter('base_url', '', base_url_descriptor)
        base_url = self.get_parameter('base_url').value or None

        # Initialize chains with configured backend
        chains = DialogueChains(
            model_name=self.model_name,
            base_url=base_url,
            backend=self.backend,
        )
        set_chains(chains)
        self.get_logger().info(f'Initialized LangGraph dialogue with backend: {self.backend}, model: {self.model_name}')

        # Subscribers
        self.subscription = self.create_subscription(
            String,
            'messageTopic',
            self.cb_function_conversation,
            10
        )

        self.subscription_notifications = self.create_subscription(
            String,
            'notificationTopic',
            self.cb_function_notification,
            10
        )

        self.subscription_human_seen = self.create_subscription(
            String,
            'seenTopic',
            self.cb_function_seen,
            10
        )

        self.busy_state_listener = self.create_subscription(
            String,
            'busy_state_publisher',
            self.cb_function_busy_listener,
            10
        )

        # Publishers
        self.publisher_listen_block = self.create_publisher(String, 'ListenBlockTopic', 10)
        self.publisher_emotion = self.create_publisher(String, 'emotionTopic', 10)

        # TTS interface
        self.tts = TTSinterface("maestro_langgraph_tts")

        # Busy interface (for checking/setting robot busy state)
        self.busy_interface = BusyInterface("maestro_langgraph_busy")

        # State
        self.notifications = {}
        self.robot_busy = False
        self.conversation_history = []

        # Check initial busy state
        self._check_busy()

        self.get_logger().info('MaestroLangGraph node initialized')

    def cb_function_conversation(self, msg: String):
        """Handle incoming human speech."""
        # Parse message: "text;metadata;voice_emotion"
        parts = msg.data.split(";")
        human_speech = parts[0]
        voice_emotion = parts[2] if len(parts) > 2 else "neutral"

        self.get_logger().info(f'Received: "{human_speech}" (emotion: {voice_emotion})')

        # Block listening while processing
        self._publish_listen_block()

        # Process through LangGraph (includes busy/problem checking)
        result = process_message(
            message=human_speech,
            voice_emotion=voice_emotion,
            history=self.conversation_history,
            robot_busy=self.robot_busy,
            notifications=self.notifications,
        )

        # Update conversation history
        self.conversation_history = result.get("conversation_history", [])

        # Get response and status
        response = result.get("response", "")
        emotion = result.get("response_emotion", "neutral")
        prosody = result.get("prosody", (150, 100, 45))
        robot_status = result.get("robot_status", "free")

        self.get_logger().info(f'Response: "{response}" (emotion: {emotion}, status: {robot_status})')

        # Clear notifications after announcing problem (they've been addressed)
        if robot_status == "problem" and self.notifications:
            self.clear_notifications()

        # Publish emotion
        self._publish_emotion(emotion)

        # Send to TTS
        self._send_tts(response, prosody)

    def cb_function_notification(self, msg: String):
        """Handle sensor notifications."""
        # Parse: "sensor_name:level:priority"
        parts = msg.data.split(":")
        if len(parts) >= 3:
            sensor_name = parts[0]
            self.notifications[sensor_name] = parts[1:]
            self.get_logger().info(f'Notification: {sensor_name} = {parts[1:]}')

    def cb_function_seen(self, msg: String):
        """Handle person detection."""
        self.get_logger().info('Person detected')
        # Could trigger proactive conversation here

    def cb_function_busy_listener(self, msg: String):
        """Handle busy state changes from topic."""
        try:
            busy = literal_eval(msg.data)
            self.robot_busy = bool(busy)
        except (ValueError, SyntaxError):
            self.robot_busy = msg.data.lower() == "true"
        self.get_logger().info(f'Robot busy state changed: {self.robot_busy}')

    def _busy_request(self, request: str):
        """Make a request to the busy service.

        Args:
            request: "get", "set_busy", or "set_idle"

        Returns:
            Response from the service
        """
        self.busy_interface.send_request(request)
        while rclpy.ok():
            rclpy.spin_once(self.busy_interface)
            if self.busy_interface.future.done():
                try:
                    response = self.busy_interface.future.result().result
                    return literal_eval(response)
                except Exception as e:
                    self.get_logger().warning(f'Busy service call failed: {e}')
                    return None

    def _check_busy(self):
        """Check if robot is currently busy via service."""
        result = self._busy_request("get")
        if result is not None:
            self.robot_busy = bool(result)
            self.get_logger().debug(f'Checked busy state: {self.robot_busy}')

    def _set_busy(self):
        """Set robot state to busy."""
        self._busy_request("set_busy")
        self.robot_busy = True
        self.get_logger().info('Robot set to busy')

    def _set_idle(self):
        """Set robot state to idle."""
        self._busy_request("set_idle")
        self.robot_busy = False
        self.get_logger().info('Robot set to idle')

    def clear_notifications(self):
        """Clear all pending notifications after announcing them."""
        self.notifications = {}
        self.get_logger().info('Notifications cleared')

    def _publish_listen_block(self):
        """Signal to pause listening."""
        msg = String()
        msg.data = " "
        self.publisher_listen_block.publish(msg)

    def _publish_emotion(self, emotion: str):
        """Publish emotion for facial expression."""
        msg = String()
        msg.data = emotion
        self.publisher_emotion.publish(msg)
        self.get_logger().debug(f'Published emotion: {emotion}')

    def _send_tts(self, text: str, prosody: tuple):
        """Send text to TTS with prosody.

        Args:
            text: Text to speak
            prosody: (volume, speed, pitch) tuple
        """
        # Format for TTS: [(text, [volume, speed, pitch])]
        tts_input = str([(text, list(prosody))])

        self.tts.send_request(model="espeak_ng", prompt=tts_input)

        # Wait for TTS to complete
        while rclpy.ok():
            rclpy.spin_once(self.tts)
            if self.tts.future.done():
                try:
                    self.tts.future.result()
                except Exception as e:
                    self.get_logger().error(f'TTS failed: {e}')
                break


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)

    node = MaestroLangGraphNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
