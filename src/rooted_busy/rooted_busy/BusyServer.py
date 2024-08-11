#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rooted_msgs.srv import *
from rooted_msgs.msg import *
from std_msgs.msg import String

from time import time


class BusyServer(Node):

    def __init__(self):
        super().__init__("busy_server")
        self.srv = self.create_service(Gesture,"busy",self.handle_gesture)
        self.state = 0
        
    def handle_gesture(self, req, resp):
        data = req.gesture
        if data[:-1] == "set":
            self.state = bool(int(data[-1]))
        resp.result = str(self.state)
        return resp

def main():
    rclpy.init(args=None)
    s = BusyServer()
    print("Ready to get busy.")
    rclpy.spin(s)
    #rclpy.shutdown()

if __name__ == "__main__":
    main()
