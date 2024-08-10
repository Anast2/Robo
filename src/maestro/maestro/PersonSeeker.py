import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ast import literal_eval
from plantroid_msgs.srv import *
from plantroid_msgs.msg import *
from time import time
import matplotlib.pyplot as plt
import numpy as np
import cv2
from image_processing2 import *
from datetime import datetime
import math 
#import sys
#sys.path.insert(1, './OKAO')
#from OKAO_vision_interface import get_image_array


def list_threshold (l,t):
    for i in l:
        if i<t:return False
    return True


class Cameras(Node):
    def __init__(self):
        super().__init__('person_camera_service')
        self.cli = self.create_client(Camera, 'camera')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Camera.Request()

    def send_request(self, type):
        self.req.imagetype = type
        self.future = self.cli.call_async(self.req)


class PersonSeeker(Node):

    def __init__(self):
        super().__init__('_seeker')
        self.motors_command = self.create_client(Command, 'speed_command')
        while not self.motors_command.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('service not available, waiting again...')
        self.req_command = Command.Request()
        self.speed_vector = [0,0]
        #STATE 0:idle, 1:seek light, 2:seek_shadow
        self.state = 0
        self.notebook_mode = False

    def send_command_request(self, vector):
        if not self.notebook_mode:
            speed = Speed()
            speed.linear = float(vector[0])
            speed.angular = float(vector[1])
            self.req_command.speed_command = speed
            future = self.motors_command.call_async(self.req_command)
        else:
            print("Warning: This function does not work in notebook mode.")
            return None

    def get_person(self):
        response = False #get_image_array().astype(np.uint8)
        if self.state == 0:
            return False
        else:
            camera_client = Cameras()
            camera_client.send_request(3)
            while rclpy.ok():
                rclpy.spin_once(camera_client)
                if camera_client.future.done():
                    try:
                        response = camera_client.future.result().image
                    except Exception as e:
                        camera_client.get_logger().info(
                            'Service call failed %r' % (e,))
                    else:
                        print(response)
                        response = literal_eval(response)
                    break
            return response


    def rotate_to_person(self):
        person = self.get_person()
        while not person:
            print("Seeking humans")
            person = self.get_person()
            self.send_command_request([0, 0.5])
        print("person found!")
        self.send_command_request([0, 0])
            
            
if __name__ == '__main__':
    rclpy.init(args=None)
    L = PersonSeeker()    
    L.state = 1
    #L.get_sun()
    L.rotate_to_person()
    rclpy.shutdown()
    # while 1:
    #     try:
    #         L.direction_from_pics()
    #     except:
    #         print("Some error happened")
