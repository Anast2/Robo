#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ast import literal_eval
from rooted_msgs.srv import LLM
from rooted_msgs.msg import *
import rooted_speech_synthesizer.speech_synthesis_interfaces as tts 
from rcl_interfaces.msg import ParameterDescriptor


class SpeechSynthesisServer(Node):

    def __init__(self, mode="local", IP="localhost", port=11434):
        super().__init__("tts_service")
        self.srv = self.create_service(LLM, "tts_server",
                                       self.cb_function)
        self.talking_status_publisher = self.create_publisher(String, 'IsTalkingTopic', 10)

        mode_descriptor = ParameterDescriptor(description='Whether the llm model is runninc locally on a remote server.')
        self.declare_parameter('mode', '', mode_descriptor)  
        self.mode = self.get_parameter("mode").value
        
        ip_descriptor = ParameterDescriptor(description='IP of the TTS server.')
        self.declare_parameter('IP', '', ip_descriptor)         
        self.IP = self.get_parameter("IP").value
        
        port_descriptor = ParameterDescriptor(description='Port of the TTS service.')
        self.declare_parameter('PORT', '', port_descriptor)         
        self.port = self.get_parameter("PORT").value

    def cb_function(self, req, resp):
        model = req.model 
        msg = req.prompt
        resp.response = "Success"
        try: 
            talking_msg = String()
            talking_msg.data = "talking"
            self.talking_status_publisher.publish(talking_msg)
            tts.tts_call(msg, model, self.mode, self.IP, self.port)
            talking_msg.data = "silent"
            self.talking_status_publisher.publish(talking_msg)

        except Exception as e:
            self.get_logger().error(f"Error {str(e)} happened.")
            resp.response = "Failure"
        
        return resp


def main():
    rclpy.init()
    TTS_server = SpeechSynthesisServer()
    rclpy.spin(TTS_server)


if __name__ == '__main__':
    main()