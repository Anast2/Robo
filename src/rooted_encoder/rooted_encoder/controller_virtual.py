#!/usr/bin/env python3
from time import time, sleep
import rclpy
from rclpy.node import Node
from rooted_msgs.srv import Command
from geometry_msgs.msg import Twist


class MotorSpeedControlServer(Node):
    """!
    A ROS2 Node that provides a service for controlling the robot's motor speed
    based on linear and angular velocity commands.
    """

    def __init__(self, robot_kinematic_model=None, motors=None):
        """!
        Constructor for the MotorSpeedControlServer class.
        Initializes the ROS2 service and publisher for motor speed control.

        @param robot_kinematic_model<optional>: (Unused) Placeholder for robot kinematics.
        @param motors<optional>: (Unused) Placeholder for motor controller integration.
        """
        super().__init__("encoder_motor_speed_control_server")
        self.srv = self.create_service(Command, "speed_command", self.handle_speed_command)
        self.virtual_robot_controller = self.create_publisher(Twist, "cmd_vel", 10)
        sleep(1)  ## Allows time for the publisher to initialize
        self.speed_command = Twist()  ## Twist message to hold velocity commands

    def handle_speed_command(self, req, resp):
        """!
        Callback to handle service requests for setting the robot's motor speed.

        @param req<Command.Request>: The service request containing linear and angular speed commands.
        @param resp<Command.Response>: The service response indicating success or failure.
        @return Command.Response: The response indicating the status of the command execution.
        """
        lin_speed = req.speed_command.linear  ## Linear speed command
        ang_speed = req.speed_command.angular  ## Angular speed command

        self.speed_command.linear.x = lin_speed
        self.speed_command.angular.z = ang_speed

        self.virtual_robot_controller.publish(self.speed_command)
        resp.result = "Speed command executed successfully."
        return resp


def main():
    """!
    Entry point for the motor speed control server application.
    Initializes the ROS2 node and starts spinning to handle speed commands.
    """
    rclpy.init()
    controller = MotorSpeedControlServer()
    rclpy.spin(controller)


if __name__ == "__main__":
    main()