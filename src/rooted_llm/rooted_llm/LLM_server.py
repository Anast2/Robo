#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ast import literal_eval
from rooted_msgs.srv import *
from rooted_msgs.msg import *
import sys

sys.path.append('') #  Add the location of this package on your computer
import LLM_interfaces as llm 


class LLMServer(Node):

    def __init__(self, mode="local", IP="localhost", port=11434):
        super().__init__("llm_service")
        self.srv = self.create_service(LLM, "llm_server",
                                       self.cb_function)
        
        self.mode = self.get_parameter('mode').value 
        self.IP = self.get_parameter('IP').value
        self.port = self.get_parameter('PORT').value 

    def cb_function(self, req, resp):
        model = req.model 
        msg = req.prompt
        if self.mode == "local":
            resp.response = llm.ollama_local(msg, model)
        else:
            resp.response = llm.ollama_server(msg, model=model, IP=self.IP, port=self.port)
        return resp


def main():
    rclpy.init()
    LLM_server = LLMServer()
    rclpy.spin(LLM_server)


if __name__ == '__main__':
    main()