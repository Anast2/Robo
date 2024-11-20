#!/usr/bin/env python3
from time import time, sleep
import rclpy
from rclpy.node import Node
from rooted_msgs.msg import Pose, Speed, State
from rooted_msgs.srv import Command
from threading import Thread
from rooted_encoder.rkm import KinematicModel
import numpy as np
from math import sin, cos
# import sys
# sys.path.append('') # Change for the location of this package on your computer, e.g. /home/you/rooted_ws/src/rooted_encoder/rooted_encoder/
# from Ax12 import Ax12
from rooted_encoder.Ax12 import Ax12

Ax12.DEVICENAME = '/dev/ttyServo' # Change for the appropriate device name  # TODO: change to rosparam
Ax12.BAUDRATE = 1_000_000 # Change for the appropriate baurate for your device  # TODO: change to rosparam

Ax12.connect()


def min_mag(l):
    l2=[abs(i) for i in l]
    return l[l2.index(min(l2))]

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


spd_cmd_pile = []

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


def sign(x):
    if x!=0:return abs(x)/x
    return 0


class Encoder(Node):

    def __init__(self, robot_kinematic_model=KinematicModel(), motors=[LS,RS],
                 motor_angles=[0,0], initial_speed=[0,0], timer=None):
        super().__init__('Encoder')
        self.publisher = self.create_publisher(Pose, "encoder", 10)
        self.moving = True
        self.x, self.y, self.theta = robot_kinematic_model.pose
        self.rkm = robot_kinematic_model
        self.l_servo, self.r_servo = motors
        self.l_id = self.l_servo.get_id()
        self.r_id = self.r_servo.get_id()
        self.motor_angle_l = self.l_servo.get_present_position()
        self.motor_angle_r = self.r_servo.get_present_position()

        self.speed_command = initial_speed
        self.current_speed = self.speed_command
        self.prev_speed = initial_speed
        if timer is None:
            self.timer = time()
        else:
            self.timer = timer

        self.srv = self.create_service(Command, "speed_command",
                                       self.handle_speed_command)

    def handle_speed_command(self, req, resp):
        lin_speed = req.speed_command.linear
        ang_speed = req.speed_command.angular
        #self.get_logger().info(
        #    "Received speed: ["+str(lin_speed)+","+str(ang_speed)+"]")
        #left_servo_speed, right_servo_speed = lin_speed, ang_speed
        left_servo_speed, right_servo_speed = self.rkm.convert_LinearAngular_to_LeftRight(lin_speed, ang_speed)
        left_servo_speed = speed_command_convert(left_servo_speed, 1)
        right_servo_speed = speed_command_convert(right_servo_speed, 0)
        global spd_cmd_pile 
        spd_cmd_pile = spd_cmd_pile.append([right_servo_speed, left_servo_speed])
        
        #print(left_servo_speed, right_servo_speed)
        resp.status = "Speed Command issued."
        return resp

    def speed_convert(self,v):
        v = int(v*1023/300)
        if abs(v)<100:
            return 0
        if v < 0:
            v = 1023-v
            if v > 2046:
                return 2046
            return v
        elif v > 1023:
            return 1023
        return int(v)

    def speed_convert_mx12w(self,v):
        if v > 1023:
            v -= 1023
        return int(v)


    def encoder_MX12W(self, publish):
        global spd_cmd_pile
        speed_r = 0
        speed_l = 0
        dt= time()-self.timer

        if spd_cmd_pile != []:
            right_servo_speed, left_servo_speed = spd_cmd_pile[0]
            spd_cmd_pile=spd_cmd_pile[1:]
            self.l_servo.set_moving_speed(int(left_servo_speed))
            self.r_servo.set_moving_speed(int(right_servo_speed))
        
        speed_r = self.speed_convert_mx12w(self.r_servo.get_present_speed())*360/1023
        speed_l = self.speed_convert_mx12w(self.l_servo.get_present_speed())*360/1023
        self.timer = time()

        if speed_l!=0 or speed_r!=0:
            self.rkm.left_speed, self.rkm.right_speed = speed_l, speed_r
            self.rkm.update(dt)
            self.current_speed = [speed_l, speed_r]
        else:
            pass

        msg = Pose()
        msg.x, msg.y, msg.theta = [float(i) for i in self.rkm.pose]
        if publish:
            self.publisher.publish(msg)

    def encoder(self, publish):
        ang0_r, ang0_l = 0, 0
        ang1_r, ang1_l = 300, 300
        speed_r, speed_l = 0, 0
        self.previous_speed = self.current_speed
        total_time = time()
        t0=time()
        while 300 in [ang0_r, ang0_l, ang1_r, ang1_l] or 0 in [ang0_r, ang0_l, ang1_r, ang1_l]:
            global spd_cmd_pile
            if spd_cmd_pile == []:
                dt=0
                ang0_r = round(self.r_servo.get_present_position() * 300 / 1023)
                ang0_l = round(self.l_servo.get_present_position() * 300 / 1023)
                while time()-t0<.1: pass
                ang1_r = round(self.r_servo.get_present_position() * 300 / 1023)
                ang1_l = round(self.l_servo.get_present_position() * 300 / 1023)
            
                dt = time()-t0
                sr=(ang1_r-ang0_r)/dt * np.pi/180
                sl=-(ang1_l-ang0_l)/dt * np.pi/180
                speed_r = min_mag([sr, sign(sr)*(2*np.pi-abs(sr))])
                speed_l = min_mag([sl, sign(sl)*(2*np.pi-abs(sl))])
            else:
                right_servo_speed, left_servo_speed = spd_cmd_pile
                self.l_servo.set_moving_speed(int(left_servo_speed))
                self.r_servo.set_moving_speed(int(right_servo_speed))
                spd_cmd_pile = []

        if speed_l!=0 or speed_r!=0:
            self.rkm.left_speed, self.rkm.right_speed = speed_l, speed_r
            self.rkm.update(time()-total_time)
            #print ("Angular Wheel speed(L,R): ", '(', ang0_l,ang1_l,')', 
            #       round(speed_l*100)/100, '(', ang0_r, ang1_r,')',round(speed_r*100)/100)
            self.current_speed = [speed_l, speed_r]
        else:
            pass

        msg = Pose()
        msg.x, msg.y, msg.theta = [float(i) for i in self.rkm.pose]
        if publish:
            self.publisher.publish(msg)
            #self.get_logger().info("Published: " + str(self.rkm.pose))


myRKM = KinematicModel()


def spin_encoder():
    encoder = Encoder(robot_kinematic_model=myRKM)
    encoder.speed_command = [0, 0]
    t0 = time()
    while 1:
        if time()-t0>.5:
            encoder.encoder_MX12W(1)
            t0=time()
        else:
            encoder.encoder_MX12W(0)


def update_RKM():
    global myRKM
    while 1:
        myRKM.update()


def main():
    rclpy.init(args=None)
    spin_encoder()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
