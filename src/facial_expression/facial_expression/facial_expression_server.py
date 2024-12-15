#!/usr/bin/env python3
"""! @brief Defines the threads responsible for composing the face of the robot, its emotions and moving its mouth when the robot is speaking."""
##
# @file facial_expression_server.py
#
# @brief Defines the threads responsible for composing the face of the robot, its emotions and moving its mouth when the robot is speaking."""
#
# @section facial_expression_server Description
# Defines the classes responsible for componsing the face of the robot:
# - GestureRequests: class responsible for requesting certain gestures to the gestures module.
# - FaceController: class responsible for receinving talk and emotion requests from ros topics and for telling the Kivy app what images to use when composing the robot's face 
# - MyApp: class that defines the Kivy App responsible for showing the robot's face in the screen. 
#
# @section Rooted Author(s)
# - Created by Antonio Galiza Cerdeira Gonzalez
# - Last modified: 15/12/2024

import os
os.environ["KIVY_NO_ARGS"] = "1"
from kivy.config import Config
Config.set('kivy', 'window', 'x11')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
import rclpy
from rclpy.node import Node
from threading import Thread
from rooted_msgs.srv import Gesture
from rooted_msgs.msg import *
from std_msgs.msg import String
from time import time
from rcl_interfaces.msg import ParameterDescriptor

## boolean variable that determines whether the facial expression engine should be moving its mouth or not
is_talking = True
## global variable that holds a FaceController object
emotion_engine = None


class GestureRequests(Node):
    """! Class responsible for communicating with the gestures module."""
    def __init__(self):
        """!GestureRequests class initializer."""
        super().__init__('facial_expression_gestures_service_interface')
        ## Client for the gesture module
        self.cli = self.create_client(Gesture,"gesture")
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Sensor service not available, waiting again...')
        ## Gesture request variable
        self.req = Gesture.Request()

    def send_request(self, gesture):
        """! GestureRequests method responsible for sending requests for gestures.
        @param gesture <str>: that tells the gesture module which gesture to execute."""
        self.req.gesture = gesture
        ## variable used to verify whether gesture execution is finished or not. 
        self.future = self.cli.call_async(self.req)    


class FaceController(Node):
    """! Face controller class, responsible for selecting the images for each face component according to each emotion of the robot."""
    def __init__(self,initial_emotion="joy"):
        """!Initialization function of the FaceController class
        @param initial_emotion<str>: initial emotion of the robot."""

        super().__init__('facial_expression_node')
        ## description of the image_folder parameter.
        my_parameter_descriptor = ParameterDescriptor(description='Location of the folder containing the images that comnpose the face of your robot.')
        ## image_folder parameter to be obtained from the launchfile.
        self.declare_parameter('image_folder', '', my_parameter_descriptor)
        ## variable for interfacing with the gesture module. 
        self.gesture_com = GestureRequests()
        ## image folder path.
        self.image_folder = self.get_parameter('image_folder').value
        ## current left eye image.
        self.l_eye = "eye0_r.png"
        ## current right eye image.
        self.r_eye = "eye0.png"
        ## current mouth image.
        self.mouth = "empty.png"
        ## current emotion expression image.
        self.emotion = "empty.png"
        ## current system emotion.
        self.current_emotion = initial_emotion 
        ## table containing the set of images for each individual face part for a given emotion. 
        self.emotion_table = {"fear":[["eye5_r.png", "eye5.png", "empty.png","empty.png"],["eye5_r.png", "eye5.png", "mouth1.png","empty.png"],["eye9_r.png", "eye9.png", "empty.png","empty.png"]], 
                              "anger":[["eye1_r.png", "eye1.png", "mouth2.png","emo0.png"],["eye1_r.png", "eye1.png", "mouth1.png","emo0.png"], ["eye9_r.png", "eye9.png", "mouth2.png","emo0.png"]],
                              "neutral":[["eye0_r.png", "eye0.png", "empty.png","empty.png"],["eye0_r.png", "eye0.png", "mouth0.png","empty.png"],["eye9_r.png", "eye9.png", "empty.png","empty.png"]],
                              "joy":[["eye7_r.png", "eye7.png", "empty.png","empty.png"],["eye7_r.png", "eye7.png", "mouth0.png","empty.png"],["eye9_r.png", "eye9.png", "empty.png","empty.png"]],
                              "love":[["eye7_r.png", "eye7.png", "empty.png","empty.png"],["eye7_r.png", "eye7.png", "mouth0.png","empty.png"],["eye9_r.png", "eye9.png", "empty.png","empty.png"]],
                              "neutral":[["eye0_r.png", "eye0.png", "empty.png","empty.png"],["eye0_r.png", "eye0.png", "mouth0.png","empty.png"],["eye9_r.png", "eye9.png", "empty.png","empty.png"]],
                              "sadness":[["eye2_r.png", "eye2.png", "empty.png","empty.png"],["eye2_r.png", "eye2.png", "mouth1.png","empty.png"], ["eye9_r.png", "eye9.png", "mouth1.png","empty.png"]],
                              "disgust":[["eye6_r.png", "eye6.png", "mouth1.png","empty.png"],["eye6_r.png", "eye6.png", "empty.png","empty.png"], ["eye9_r.png", "eye9.png", "mouth1.png","empty.png"]],
                              "surprise":[["eye10_r.png", "eye10.png", "mouth1.png","emo2.png"],["eye10_r.png", "eye10.png", "empty.png","emo2.png"], ["eye9_r.png", "eye9.png", "mouth1.png","emo2.png"]],
                              "dizzy":[["eye8_r.png", "eye8.png", "empty.png","empty.png"],["eye8_r.png", "eye8.png", "mouth0.png","empty.png"],["eye8_r.png", "eye8.png", "empty.png","empty.png"]],
                              "sleepy":[["eye9_r.png", "eye9.png", "empty.png","emo3.png"],["eye9_r.png", "eye9.png", "empty.png","emo3.png"], ["eye9_r.png", "eye9.png", "empty.png","emo3.png"]],
                              "thirsty":[["eye11_r.png", "eye11.png", "mouth1.png","emo1.png"],["eye11_r.png", "eye11.png", "empty.png","emo1.png"], ["eye9_r.png", "eye9.png", "mouth1.png","emo1.png"]],
                              "sweaty":[["eye3_r.png", "eye3.png", "mouth1.png","emo1.png"],["eye3_r.png", "eye3.png", "empty.png","emo1.png"], ["eye9_r.png", "eye9.png", "mouth1.png","emo1.png"]],
                              "confused":[["eye2_r.png", "eye3.png", "empty.png","emo4.png"],["eye2_r.png", "eye3.png", "mouth0.png","emo4.png"], ["eye9_r.png", "eye9.png", "empty.png","emo4.png"]],                         
        }
        ## topic that controls whether the robot is talking or not. 
        self.subscription = self.create_subscription(String, 'IsTalkingTopic',
                                                     self.cb_function_message,
                                                     10)
        self.subscription
        ## topic that controls the current emotion of the robot. 
        self.emotion = self.create_subscription(String, 'emotionTopic',
                                                     self.cb_function_emotion,
                                                     10)

    def cb_function_message(self, Data):
        """! callback function for the topic that recives (stop) talking requests.
        @param Data<std_msgs.msg.String>: ros2 String received through the IsTalkingTopic topic."""
        global is_talking
        ## variable containing the talking request
        reply = Data.data
        # reply = literal_eval(reply)
        print(reply)
        if reply == "talking":
            is_talking = True
        else:
            is_talking = False

    def cb_function_emotion(self, Data):
        """! callback function for the topic that sets the current robot emotion
        @param Data<std_msgs.msg.String>: ros2 String received through the IsTalkingTopic topic."""
        if Data.data in ["fear", "anger", "joy","sadness", "disgust", 
                         "surprise", "dizzy", "sleepy", "thirsty",
                         "sweaty", "confused","neutral"]:
            self.current_emotion = Data.data
            if Data.data == "surprise":
                try:
                    self.gesture_comm.send_request("surprise")
                    ##time when the surprise gesture was sent so the robot can normalize its facial expression after 3 seconds. 
                    t0 = time()
                    while time()-t0<3:pass
                except Exception as e:
                    print(f"Failed to move neck due to {e}!")

                self.current_emotion = "neutral"
        else: pass


class MyApp(App):
    """! Kivy app definiton for the face GUI."""
    def __init__(self, **kwargs):
        """! Face GUI initializer function."""
        super().__init__(**kwargs)
        global emotion_engine
        ## current face frame.
        self.frame = 0
        Clock.schedule_interval(self.mouther, 0.2)

    def build(self):
        """! Kivy window builder function."""
        global emotion_engine
        Window.clearcolor = (1, 1, 1, 1)
        while emotion_engine is None:
            print("Waiting for ROS2 node to start.")
        ## current layout of the Face GUI.
        layout = FloatLayout()
        ## current face base image
        self.im_base = Image(source=emotion_engine.image_folder+'Base.png', pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(1.5, 1.5))
        ## current left eye image
        self.im_l_eye = Image(source=emotion_engine.image_folder+'eye0_r.png', pos_hint={'center_x': .65, 'center_y': .65}, size_hint=(1.5, 1.5))
        ## current right eye image
        self.im_r_eye = Image(source=emotion_engine.image_folder+'eye9.png', pos_hint={'center_x': .35, 'center_y': .65}, size_hint=(1.5, 1.5))
        ## current mouth image. 
        self.im_mouth = Image(source=emotion_engine.image_folder+'mouth3.png', pos_hint={'center_x': .5, 'center_y': .205}, size_hint=(1.5, 1.5))
        ## current emotino marker image
        self.im_emotion = Image(source=emotion_engine.image_folder+'empty.png', pos_hint={'center_x': .85, 'center_y': .75}, size_hint=(1.5, 1.5))
    
        layout.add_widget(self.im_base)
        layout.add_widget(self.im_l_eye)
        layout.add_widget(self.im_r_eye)
        layout.add_widget(self.im_mouth)
        layout.add_widget(self.im_emotion)

        self.compose_face(emotion_engine.emotion_table[emotion_engine.current_emotion][0])
        
        return layout

    def mouther(self):
        """! Function that opens and closes the mouth of the face GUI if the robot is talking."""
        global is_talking
        global emotion_engine
        if is_talking:
            self.frame = 1 if self.frame == 0 else 0
        else:
            self.frame = 0
        
        try:
            self.compose_face(emotion_engine.emotion_table[emotion_engine.current_emotion][self.frame])
        except KeyError:
            pass

    def compose_face(self, lista):
        """! Face composition function
        @param lista(<list><str>): """
        global emotion_engine
        self.im_l_eye.source = emotion_engine.image_folder + lista[0]
        self.im_r_eye.source = emotion_engine.image_folder + lista[1]
        self.im_mouth.source = emotion_engine.image_folder + lista[2]
        self.im_emotion.source = emotion_engine.image_folder + lista[3]


def ROS_main():
    """! ROS node initialization function."""
    rclpy.init()
    global emotion_engine
    ## current emotion engine. 
    emotion_engine = FaceController()
    rclpy.spin(emotion_engine)


def GUI_main():
    """! Kivy GUI initialization function."""
    ## defines the present face GUI
    plantroid_GUI = MyApp()
    plantroid_GUI.run()


def main():
    """! main function of the package, instantiating the ros thread and the GUI kivy thread."""
    ## ROS thread.
    thread1 = Thread(target=ROS_main,args=())
    thread1.start()
    GUI_main()

if __name__ == '__main__':
    main()