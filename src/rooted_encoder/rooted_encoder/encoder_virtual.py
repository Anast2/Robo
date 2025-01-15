#!/usr/bin/env python3
from time import time, sleep
import rclpy
from rclpy.node import Node
from rooted_msgs.msg import Pose
from rooted_msgs.srv import Command
from threading import Thread
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import numpy as np


class Encoder(Node):
    """!
    A ROS2 Node that simulates an encoder to publish the robot's pose based on odometry data.
    """

    def __init__(self, robot_kinematic_model=None, motors=None, motor_angles=None, initial_speed=None, timer=None):
        """!
        Constructor for the Encoder class.
        Initializes the publisher, subscriber, and pose message.

        @param robot_kinematic_model<optional>: Placeholder for the robot's kinematic model.
        @param motors<optional>: Placeholder for motor objects.
        @param motor_angles<optional>: Placeholder for initial motor angles.
        @param initial_speed<optional>: Placeholder for the robot's initial speed.
        @param timer<optional>: Placeholder for a timing mechanism.
        """
        super().__init__('encoder_node')
        self.pose_publisher = self.create_publisher(Pose, "encoder", 10)  ## Publishes the robot's pose
        self.pose_msg = Pose()  ## Pose message to store position and orientation

        self.subscription_odometry = self.create_subscription(
            Odometry,
            'odom',
            self.cb_function_odom,
            10
        )  ## Subscribes to the 'odom' topic to receive odometry data

        sleep(1)  ## Allows time for ROS2 communication setup

    def cb_function_odom(self, msg):
        """!
        Callback function to process incoming odometry messages and update the pose.

        @param msg<Odometry>: The received odometry message.
        """
        pose = msg.pose
        x, y = pose.pose.position.x, pose.pose.position.y  ## Extract position
        _, _, theta = self.euler_from_quaternion(pose.pose.orientation)  ## Extract orientation in yaw

        self.pose_msg.x = x
        self.pose_msg.y = y
        self.pose_msg.theta = theta

        self.pose_publisher.publish(self.pose_msg)  ## Publish updated pose

    @staticmethod
    def euler_from_quaternion(quaternion):
        """!
        Converts a quaternion to Euler angles (roll, pitch, yaw).

        @param quaternion<Quaternion>: The quaternion to convert (x, y, z, w).
        @return tuple: A tuple containing roll, pitch, and yaw angles.
        """
        x = quaternion.x
        y = quaternion.y
        z = quaternion.z
        w = quaternion.w

        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = np.arctan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (w * y - z * x)
        pitch = np.arcsin(sinp)

        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = np.arctan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw


def main():
    """!
    Entry point for the encoder node application.
    Initializes the ROS2 node and starts spinning to process odometry data.
    """
    rclpy.init()
    encoder = Encoder()
    rclpy.spin(encoder)


if __name__ == "__main__":
    main()