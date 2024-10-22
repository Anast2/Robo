#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ast import literal_eval
from rooted_msgs.srv import *
from rooted_msgs.msg import *
import sys
from rcl_interfaces.msg import ParameterDescriptor

sys.path.append('') #  Add the location of this package on your computer
import LLM_interfaces as llm 


class LLMServer(Node):

    def __init__(self, mode="local", IP="localhost", port=11434):
        super().__init__("llm_service")
        self.srv = self.create_service(LLM, "llm_server",
                                       self.cb_function)

        mode_descriptor = ParameterDescriptor(description='Whether the llm model is runninc locally on a remote server.')
        self.declare_parameter('mode', '', mode_descriptor)   
        self.mode = self.get_parameter('mode').value 

        ip_descriptor = ParameterDescriptor(description='IP of the llm server.')
        self.declare_parameter('IP', '', ip_descriptor)   
        self.IP = self.get_parameter('IP').value

        port_descriptor = ParameterDescriptor(description='Port of the llm service.')
        self.declare_parameter('PORT', '', port_descriptor)   
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