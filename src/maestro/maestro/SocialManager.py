#!/usr/bin/env python3
import os
os.environ["KIVY_NO_ARGS"] = "1"
import sys
sys.path.append('') #  Add the location of this package on your computer
import utils
from ChatBot import chatter
#from QLearning import QLearning
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from threading import Thread
from ast import literal_eval
from plantroid_msgs.srv import *
from plantroid_msgs.msg import *
from time import time
import argparse
#from GSIP import GSIP
from beepy import beep
import subprocess
from random import choice
from threading import Thread
from GPTJinterface import GPTJ

s = "s0"
c = 0
image_folder = "./IMG/"
learning = False  # True  # True if Q-Learning is in use
is_talking = False

speech_style = 0
logging = 0
detect_person = 0

in_notebook = 0
OKAO = 0

def emotion_2_prompt(emotion):
	#neutral
	#happiness
	#surprise
	#anger
	#sadness
	#neg_pos
    i = emotion.index(max(emotion[:-1]))
    return [" in a happy tone", "", " in a calm tone", " in a calming tone", " to cheer up",""][i]


def process_notifications(notifications):
    gib = "I need your help, the soil has "
    for i, N in enumerate(notifications):
        gib += str(notifications[N][0]) + " " + N + ", " + str(notifications[N][1])+str(notifications[N][2])+  ", content "
        if i>0 and i<len(notifications)-1: gib+= " and "
    return gib

class SensorReader(Node):

    def __init__(self):
        super().__init__('social_central_sensor_reader')
        self.cli = self.create_client(Sensors, 'sensors_server')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Sensor service not available, waiting again...')
        self.req = Sensors.Request()

    def send_request(self, num):
        self.req.sensor_number = num
        self.future = self.cli.call_async(self.req)


class Cameras(Node):

    def __init__(self):
        super().__init__('social_central_camera_reader')
        self.cli = self.create_client(Camera, 'camera')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Camera service not available, waiting again...')
        self.req = Camera.Request()

    def send_request(self, type):
        self.req.imagetype = type
        self.future = self.cli.call_async(self.req)


class BusyChecker(Node):

    def __init__(self):
        super().__init__('social_busy_check')
        self.cli = self.create_client(Gesture, 'busy')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Camera service not available, waiting again...')
        self.req = Gesture.Request()

    def send_request(self, busy):
        self.req.gesture = "get"
        self.future = self.cli.call_async(self.req)


class PlantroidMainNode(Node):

    def __init__(self):
        super().__init__('plantroid')
        self.subscription = self.create_subscription(String, 'messageTopic',
                                                     self.cb_function,
                                                     10)

        self.subscription_notifications = self.create_subscription(String, 'notificationTopic',
                                                                   self.cb_function_notification,
                                                                   10)

        self.subscription_human_seen = self.create_subscription(String, 'seenTopic',
                                                     self.cb_function_seen,
                                                     10)

        self.subscription
        self.subscription_notifications
        self.subscription_human_seen
        self.publisher = self.create_publisher(String, 'ListenBlockTopic', 10)
        self.publisher_emotion = self.create_publisher(String, 'emotionTopic', 10)
        self.publisher_speech = self.create_publisher(String, 'speechTopic', 10)
        self.vision_control = Cameras()
        self.busy_check = BusyChecker()
        self.sensor_reader = SensorReader()
        self.busy = self.check_busy()
        self.last_time_seen = -10000
        self.notifications = {}
        self.time_last_seen = -float("inf")

    def cb_function(self, subscribedData):
        data = subscribedData.data.split(";")[0]
        self.get_logger().info('Subscribed: ' + data)
        beep(1)
        response = str(self.assign_prosody(self.conversate(data),"Glabber"))
        msg = String()
        msg.data = response

        if not self.busy:
            os.system("python /home/plantroid/plantroid_ws/src/plantroid_social/plantroid_social/PersonSeeker.py")

        self.publisher_speech.publish(msg)

    def cb_function_notification(self, subscribedData):
        data = subscribedData.data
        data_breakdown = data.split(":")
        self.notifications[data_breakdown[0]] = data_breakdown[1:]
        if "Water" in self.notifications:
            self.set_emotion("thirsty")
        else:
            self.set_emotion("sad")
        print (self.notifications)
        self.get_logger().info('Subscribed: ' + data)

    def cb_function_seen(self, subscribedData):
            data = subscribedData.data
            print("Saw person!")
            self.get_logger().info('Subscribed: ' + data)
            a = String()
            a.data = "Hello"
            if len(self.notifications)>0:
                self.last_time_seen = time()
                self.cb_function(a)
                a.data = str(self.notifications)
                self.cb_function(a)
            elif time()-self.last_time_seen>300:
                self.last_time_seen = time()
                self.cb_function(a)

    def avoidEcho(self):
        msg = String()
        msg.data = " "
        self.publisher.publish(msg)
        self.get_logger().info("Changing listen blocking state.")

    def check_busy(self):
        self.busy = 0
        self.busy_check.send_request("get")
        while rclpy.ok():
            rclpy.spin_once(self.busy_check)
            if self.busy_check.future.done():
                try:
                    response = self.busy_check.future.result().result
                except Exception as e:
                    self.busy = True
                    self.busy_check.get_logger().info(
                        'Service call failed %r' % (e,))
                else:
                    print(response)
                    response = literal_eval(response)
                    self.busy = response
                break

    def get_vision(self):
        response = "" #get_image_array().astype(np.uint8)
        self.vision_control.send_request(8)
        while rclpy.ok():
            rclpy.spin_once(self.vision_control)
            if self.vision_control.future.done():
                try:
                    response = self.vision_control.future.result().image
                except Exception as e:
                    self.vision_control.get_logger().info(
                        'Service call failed %r' % (e,))
                else:
                    return response

    def set_emotion(self, emotion):
        msg = String()
        msg.data = emotion
        self.publisher_emotion.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)

    def get_emotion(self):
        response = False #get_image_array().astype(np.uint8)
        self.vision_control.send_request(0)
        while rclpy.ok():
            rclpy.spin_once(self.vision_control)
            if self.vision_control.future.done():
                try:
                    response = self.vision_control.future.result().image
                except Exception as e:
                    self.vision_control.get_logger().info(
                        'Service call failed %r' % (e,))
                else:
                    print(response)
                    response = literal_eval(response)
                break
        return response

    def get_sensor(self, num):
        response = 0
        self.sensor_reader.send_request(num)
        while rclpy.ok():
            rclpy.spin_once(self.sensor_reader)
            if self.sensor_reader.future.done():
                try:
                    response = self.sensor_reader.future.result().sensor_reading
                except Exception as e:
                    self.vision_control.get_logger().info(
                        'Service call failed %r' % (e,))
                else:
                    print(response)
                    response = literal_eval(response)
                break
        return response

    def conversate(self, data):
        gib = chatter(data)
        current_emotion = self.get_emotion()
        #human_content_emotion = GPTJ(data, port=5052)
        #print(content_emotion)
        addendum = emotion_2_prompt(current_emotion)
        IP = "localhost"
        PORT = 12345
        if gib is None:
            gib = GPTJ(data,IP,PORT)
        else:
            if "wikipedia:" in gib:
                gib = gib.split(":")[1]
                gib = utils.wikipedia_query(gib)
                gib = "Paraphrase the following sentence"+addendum+": "+gib
                gib = GPTJ(gib,IP,PORT)
            elif "dictionary:" in gib:
                gib = gib.split(":")[1]
                gib = utils.dictionary_query(gib)
                gib = "Paraphrase the following sentence"+addendum+": "+gib
                gib = GPTJ(gib,IP,PORT)
            elif "sensor:" in gib:
                split = gib.split(":")
                sensor_reading = self.get_sensor(int(split[1]))
                sensor_dict = {0:"right ear light", 1:"tail light",
                               2:"left ear light", 3:"soil moisture", 4:"temperature", 
                               5:"None", 6:"Salinity", 7:"pH", 8:"Nitrogen", 9:"Phosphorus", 10:"Potassium"}
                unit_dict = {0:"lux", 1:"lux",2:"lux", 3:" per cent", 4:" Degrees Celsius", 5:"", 
                             6:" deciSiemes per centimeter", 7:"", 8:" miligrams per kilogram of soil", 
                             9:" miligrams per kilogram of soil", 10:" miligrams per kilogram of soil"}                               
                gib = "current "+sensor_dict[int(split[1])]+" sensor reading is "+str(sensor_reading)+unit_dict[int(split[1])]
                gib = "Paraphrase the following sentence"+addendum+": "+gib
                gib = GPTJ(gib,IP,PORT)
            elif gib == "vision_check":
                gib = self.get_vision()
                gib = "Paraphrase the following sentence"+addendum+": "+gib 
                gib = GPTJ(gib,IP,PORT)
            elif gib =="not_proc":
                gib = process_notifications(self.notifications)
                print(gib)
                gib = "Paraphrase the following sentence"+addendum+": "+gib
                gib = GPTJ(gib,IP,PORT)
                self.notifications = {}
        robot_content_emotion = GPTJ(gib, IP, port=PORT+1)
        self.set_emotion(robot_content_emotion)
        return gib

    def assign_prosody(self, utterance, method="random"):
        if not isinstance(utterance, list):
            utterance = [utterance]
        prosody = []
        if method == "random":
            return [(i,[choice(range(10,200)),choice(range(80,450)),choice(range(0,99))]) for i in utterance]
        #elif method == "GSIP":
        #    my_profile = [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        #                  0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        #                  0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        #                  0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        #                  0.04]
        #    return GSIP(utterance, my_profile)
        else:
            return ([(i,[150,100,45]) for i in utterance])

def main():
    rclpy.init()
    ROS_interface = PlantroidMainNode()
    rclpy.spin(ROS_interface)

if __name__ == '__main__':
    main()

