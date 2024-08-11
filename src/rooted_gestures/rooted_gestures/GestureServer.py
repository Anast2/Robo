#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rooted_msgs.srv import *
from rooted_msgs.msg import *
from std_msgs.msg import String

from time import time


class MotorCommander(Node):

    def __init__(self):
        super().__init__('gesture_servo_commander')
        self.cli = self.create_client(Command, 'speed_command')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Encoder service not available, waiting again...')
        self.req = Command.Request()

    def send_request(self, vels):
        speed = Speed()
        speed.linear = float(vels[0])
        speed.angular = float(vels[1])
        self.req.speed_command = speed
        self.future = self.cli.call_async(self.req)
        

class NeckCommander(Node):

    def __init__(self):
        super().__init__('gesture_neck_servo')
        self.cli = self.create_client(NeckServo, 'neck_servo')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = NeckServo.Request()

    def send_request(self, angle):
        try:
            self.req.angle = float(angle)
            self.future = self.cli.call_async(self.req)
        except Exception as e:
            print("Error: {}".format(e))


class GestureServer(Node):

    def __init__(self):
        super().__init__("gesture_server")
        self.srv = self.create_service(Gesture,"gesture",self.handle_gesture)
        self.nc = NeckCommander()
        self.mc = MotorCommander()
    def handle_gesture(self, req, resp):
        data = req.gesture
        if data == "bow":
            
            #t0 = time()
            bow = 8
            while bow<9:
                self.nc.send_request(bow)
                bow+=0.001
            t0 = time()
            while time()-t0<2:pass
            while bow>8:
                self.nc.send_request(bow)
                bow-=0.001            
            self.nc.send_request(0)
        elif data == "yes":
            nc = NeckCommander()
            #t0 = time()
            for i in range(3):
                bow = 7
                while bow<9:
                    nc.send_request(bow)
                    bow+=0.005
                t0 = time()
                while bow>8:
                    nc.send_request(bow)
                    bow-=0.05            
                nc.send_request(8)
        
        elif data == "no":
             for i in [.5, -1, .5]:
                 t0 = time()
                 self.mc.send_request([0,i/abs(i)*0.5])
                 while time()-t0<abs(i):pass
             self.mc.send_request([0, 0])
             self.mc.send_request([0, 0])
        elif data == "surprise":
            self.nc = NeckCommander()
            #t0 = time()
            bow = 8
            while bow>7:
                self.nc.send_request(bow)
                bow-=0.01
            t0 = time()
            while time()-t0<2:pass
            while bow<8:
                self.nc.send_request(bow)
                bow+=0.001            
            self.nc.send_request(0)

        resp.result = "Done."
        return resp

def main():
    rclpy.init(args=None)
    s = GestureServer()
    print("Ready to make gestures.")
    rclpy.spin(s)
    #rclpy.shutdown()

if __name__ == "__main__":
#    startup_routine()
    main()
