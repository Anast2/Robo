#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rooted_msgs.srv import Busy
from std_msgs.msg import String

from time import time


class BusyServer(Node):

    def __init__(self):
        super().__init__("busy_server")
        self.srv = self.create_service(Busy,"busy_service",self.handle_request)
        self.state = 0
        self.busy_notifier = self.create_publisher(String, 'busy_state_publisher', 10)
        
    def handle_request(self, req, resp):
        data = req.request
        if data == "set_busy":
            self.state = 1
            self.busy_notifier.publish(str(self.state))
        elif data == "set_idle":
            self.state = 0
            self.busy_notifier.publish(str(self.state))
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
