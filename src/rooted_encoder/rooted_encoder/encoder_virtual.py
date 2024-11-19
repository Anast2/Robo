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

    def __init__(self, robot_kinematic_model=None, motors=None,
                 motor_angles=None, initial_speed=None, timer=None):
        super().__init__('encoder_node')
        self.pose_publisher = self.create_publisher(Pose, "encoder", 10)
        self.pose_msg = Pose()
        self.pose_msg
        self.subscription_odometry = self.create_subscription(Odometry, 
                                                              'odom', 
                                                              self.cb_function_odom,
                                                              10)
        sleep(1)
    
    def cb_function_odom(self, msg):
        pose = msg.pose
        x, y = pose.pose.position.x, pose.pose.position.y
        _, _, theta = self.euler_from_quaternion(pose.pose.orientation)
        self.pose_msg.x = x
        self.pose_msg.y = y
        self.pose_msg.theta = theta
        self.pose_publisher.publish(self.pose_msg)

    def euler_from_quaternion(quaternion):
        """
        Converts quaternion (w in last place) to euler roll, pitch, yaw
        quaternion = [x, y, z, w]
        Bellow should be replaced when porting for ROS 2 Python tf_conversions is done.
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
    rclpy.init()
    encoder = Encoder()
    rclpy.spin(encoder)


if __name__ == "__main__":
    main()