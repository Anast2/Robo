#!/usr/bin/env python3
from time import time, sleep
import rclpy
from rclpy.node import Node
from rooted_msgs.srv import Command
from geometry_msgs.msg import Twist


class MotorSpeedControlServer(Node):

    def __init__(self, robot_kinematic_model=None, motors=None):
        super().__init__("encoder_motor_speed_control_server")
        self.srv = self.create_service(Command, "speed_command",
                                       self.handle_speed_command)
        self.virtual_robot_controller = self.create_publisher(Twist, "cmd_vel", 10)
        sleep(1)
        self.speed_command = Twist()
        self.speed_command

    def handle_speed_command(self, req, resp):
        lin_speed = req.speed_command.linear
        ang_speed = req.speed_command.angular
        self.speed_command.linear.x = lin_speed
        self.speed_command.angular.z = ang_speed
        self.virtual_robot_controller.publish(self.speed_command)

def main():    
    rclpy.init()
    controller = MotorSpeedControlServer()
    rclpy.spin(controller)

if __name__ == "__main__":
    main()