#!/usr/bin/env python3
from time import time, sleep

import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped, Twist
import tf_transformations
from rooted_encoder.rkm import KinematicModel
import numpy as np
from rooted_encoder.Ax12 import Ax12

Ax12.DEVICENAME = '/dev/ttyUSB0' # Change for the appropriate device name  # TODO: change to rosparam
Ax12.BAUDRATE = 1_000_000 # Change for the appropriate baurate for your device  # TODO: change to rosparam
Ax12.connect()


def servo_setup(servo):
    servo.set_cw_angle_limit(0)
    servo.set_ccw_angle_limit(0)
    servo.set_moving_speed(0)


LS = Ax12(1)
RS = Ax12(2)

servo_setup(LS)
servo_setup(RS)

LS.set_moving_speed(0)
RS.set_moving_speed(0)


def speed_command_convert(s,l=0):
    if s ==0:
        return 0
    if l:
        if s<0:
            return min(-s*180/np.pi*1023/300, 1023)
        else:
            return min(2046, s*180/np.pi*1023/300+1023)
    else:
        if s<0:
            return min(2046, -s*180/np.pi*1023/300+1023)
        else:
            return min(1023, s*180/np.pi*1023/300)


class Encoder(Node):

    def __init__(self, robot_kinematic_model=KinematicModel(), motors=[LS, RS], timer=None):
        super().__init__('Encoder')
        
        self.moving = True
        self.tf_broadcaster = TransformBroadcaster(self)
        self.speed_publisher = self.create_publisher(Twist, '/plantroid/actual_vel', 10)
        self.speed_command_subscription = self.create_subscription(
            Twist,
            '/plantroid/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        self.pose_timer = self.create_timer(0.1, self.publish_pose)
        self.speed_timer = self.create_timer(2**0.5 / 10, self.publish_speed)
        self.command_timer = self.create_timer(5**0.5 / 10, self.issue_speed_command)

        self.rkm = robot_kinematic_model
        self.x, self.y, self.theta = robot_kinematic_model.pose

        self.l_servo, self.r_servo = motors
        self.l_id = self.l_servo.get_id()
        self.r_id = self.r_servo.get_id()
        self.motor_angle_l = self.l_servo.get_present_position()
        self.motor_angle_r = self.r_servo.get_present_position()

        if timer is None:
            self.timer = time()
        else:
            self.timer = timer 

        self.speed_command_pile = []

    def cmd_vel_callback(self, msg):
        lin_speed = msg.linear.x
        ang_speed = msg.angular.z

        self.get_logger().info(
            "Received speed: ["+str(lin_speed)+","+str(ang_speed)+"]")

        left_servo_speed, right_servo_speed = self.rkm.convert_LinearAngular_to_LeftRight(lin_speed, ang_speed)
        left_servo_speed = speed_command_convert(left_servo_speed, 1)
        right_servo_speed = speed_command_convert(right_servo_speed, 0)        
        self.speed_command_pile.append([right_servo_speed, left_servo_speed])        

    def speed_convert_mx12w(self, v):
        return int(v % 1024)

    def issue_speed_command(self):
        if self.speed_command_pile:
            right_servo_speed, left_servo_speed = self.speed_command_pile.pop(0)
            self.l_servo.set_moving_speed(int(left_servo_speed))
            self.r_servo.set_moving_speed(int(right_servo_speed))

    def publish_pose(self):
        speed_r = self.speed_convert_mx12w(self.r_servo.get_present_speed())*360/1023
        speed_l = self.speed_convert_mx12w(self.l_servo.get_present_speed())*360/1023
        dt= time() - self.timer
        self.timer = time()
        self.rkm.left_speed, self.rkm.right_speed = speed_l, speed_r
        self.rkm.update(dt)
        pose = {"x":self.rkm.pose[0],"y":self.rkm.pose[1], "theta":self.rkm.pose[2]}
        transform_stamped = TransformStamped()
        transform_stamped.header.stamp = self.get_clock().now().to_msg()
        transform_stamped.header.frame_id = 'world'
        transform_stamped.child_frame_id = 'plantroid_base'
        transform_stamped.transform.translation.x = pose["x"]
        transform_stamped.transform.translation.y = pose["y"]
        transform_stamped.transform.translation.z = 0.0
        quaternion = tf_transformations.quaternion_from_euler(0, 0, pose["theta"])
        transform_stamped.transform.rotation.x = quaternion[0]
        transform_stamped.transform.rotation.y = quaternion[1]
        transform_stamped.transform.rotation.z = quaternion[2]
        transform_stamped.transform.rotation.w = quaternion[3]
        self.tf_broadcaster.sendTransform(transform_stamped)
        twist = Twist()
        twist.linear.x, twist.angular.z = self.rkm.speed
        self.speed_publisher.publish(twist)
        

def main():
    myRKM = KinematicModel()
    rclpy.init(args=None)
    encoder = Encoder(robot_kinematic_model=myRKM)
    encoder.speed_command_pile = [[0,0]]
    rclpy.spin(encoder)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
