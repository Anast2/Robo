#!/usr/bin/env python3
from __future__ import print_function

import rclpy
from rclpy.node import Node
from plantroid_msgs.srv import Sensors

import os
import serial
import syslog
import time
from pymodbus.client import ModbusSerialClient
from random import choice

computer = 0

class SensorServer(Node):

    def __init__(self):
        super().__init__("sensor_service")
        self.srv = self.create_service(Sensors, "sensors_server",
                                       self.cb_function)
    def cb_function(self, req, resp):
        sensor = req.sensor_number
        if sensor<=5:
            if sensor  == 3:
        	    resp.sensor_reading = str(32+choice(range(-10,5)))
            else:
                resp.sensor_reading = str(500+choice(range(12,47)))
        elif sensor == 6:
            resp.sensor_reading = str(10+choice([0,0,0,1,1,2,3]))
        elif sensor == 7:
            resp.sensor_reading = str(73+choice([0,0,0,1,1,2,3]))
        elif sensor == 8:
            resp.sensor_reading = str(100+choice([0,0,0,1,1,2,3]))
        elif sensor == 9:
            resp.sensor_reading = str(124+choice([0,0,0,1,1,2,3]))
        elif sensor == 10:
            resp.sensor_reading = str(112+choice([0,0,0,1,1,2,3]))            
        else:
            resp.sensor_reading = "0"
        return resp

def main():
    rclpy.init(args=None)
    s = SensorServer()
    print("Ready to read sensors")
    rclpy.spin(s)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
