#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ast import literal_eval
from rooted_msgs.srv import *
from rooted_msgs.msg import *
#sys.path.append('') #  Add the location of this package on your computer
import rooted_speech_synthesizer.speech_synthesis_interfaces as tts 


class SpeechSynthesisServer(Node):

    def __init__(self, mode="local", IP="localhost", port=11434):
        super().__init__("tts_service")
        self.srv = self.create_service(LLM, "tts_server",
                                       self.cb_function)
        self.mode = self.get_parameter("mode").value
        self.IP = self.get_parameter("IP").value
        self.port = self.get_parameter("PORT").value

    def cb_function(self, req, resp):
        model = req.model 
        msg = req.prompt
        resp.response = "Success"
        try: 
            tts.tts_call(msg, model, self.mode, self.IP, self.PORT)
        except:
            resp.response = "Failure"
        return resp


def main():
    rclpy.init()
    TTS_server = SpeechSynthesisServer()
    rclpy.spin(TTS_server)


if __name__ == '__main__':
    main()