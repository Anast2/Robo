#!/usr/bin/env python3
from __future__ import print_function

import rclpy
from rclpy.node import Node
from rooted_msgs.srv import NeckServo
from time import time
from rcl_interfaces.msg import ParameterDescriptor


class FakeServo():  # for tests out of the raspberry pi.
    def __init__(self, pin, initial_pwm):
        self.PIN = pin
        self.pwm = initial_pwm     

    def ChangeDutyCycle(self, pwm):
        self.pwm = pwm
        pos_dict = {1:0, 2:18, 3:36, 4:54, 5:72, 6:90, 7:108, 8:126, 9:144,
                    10:162, 11:180}
        print("Fake servo on pin"+str(self.PIN)+"moving to "+
            str(pos_dict[pwm])+" degrees.")


class NeckServoServer(Node):
    def __init__(self):
        super().__init__("neck_servo_service")
        self.srv = self.create_service(NeckServo, "neck_servo",
                                       self.handle_neck_servo)
        self.servoPIN = 17
        raspi_descriptor = ParameterDescriptor(description='Variable that represents whethe the code is running on a raspberry pi or not.')
        self.declare_parameter('raspi', '', raspi_descriptor)        
        self.raspi = self.get_parameter('raspi').value   
        if self.raspi:
            try:
                import RPi.GPIO as GPIO
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.servoPIN, GPIO.OUT)
                self.controller = GPIO.PWM(self.servoPIN, 50)
                self.controller.start(0)
            except:
                self.controller = FakeServo(self.servoPIN, 50)
        else:
            self.controller = FakeServo(self.servoPIN, 50)

    def handle_neck_servo(self, req, resp):
        angle = req.angle
        if angle <= 10:
            self.controller.ChangeDutyCycle(angle)
            resp.status = "Tilted head to "+str(angle)
        else:
            initial = 4
            final = 3
            angle = initial
            while angle>final:
                angle-=0.2
                t0 = time()
                self.controller.ChangeDutyCycle(angle)
                while time()-t0<0.25:
                    pass
            while angle < initial:
                angle+=0.2
                t0 = time()
                self.controller.ChangeDutyCycle(angle)
                while time()-t0<0.25:
                    pass
            self.controller.ChangeDutyCycle(5)
        print("Tilted head to "+str(angle))
        return resp
        #intervals = [-float("inf"), 0, 18, 36, 54, 72, 90, 108, 126, 144, 162,
        #             180]
        #for i in range(len(intervals)-1):
        #    if angle>=intervals[i] and angle<=intervals[i+1]:
        #        self.controller.ChangeDutyCycle(i+1)
        #        resp.status = "Tilted head to " + str(intervals[i+1]) +\
        #            " degrees."
        #        t0 = time()
        #        while time()-t0<1: pass
        #        return resp


def main():
    rclpy.init(args=None)
    s = NeckServoServer()
    print("Ready to tilt head.")
    rclpy.spin(s)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
