#!/usr/bin/env python3
import os
os.environ["KIVY_NO_ARGS"] = "1"
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
import subprocess
from kivy.uix.image import Image
import utils
from ChatBot import chatter
from QLearning import QLearning
import rclpy
from rclpy.node import Node
from threading import Thread
import time
from rooted_msgs.srv import *
from rooted_msgs.msg import *
from std_msgs.msg import String
from time import time
import argparse
import os
import subprocess 
from ast import literal_eval
from beepy import beep 

s = "s0"
c = 0
image_folder = "./IMG/"
is_talking = False


class facialExpressionEngine:

    def __init__(self,initial_emotion, image_folder):
        self.image_folder = image_folder
        self.l_eye = "eye0_r.png"
        self.r_eye = "eye0.png"
        self.mouth = "empty.png"
        self.emotion = "empty.png"
        self.current_emotion = initial_emotion 
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
    def get_normal(self): return self.emotion_table[self.current_emotion][0]

    def get_speak(self): return self.emotion_table[self.current_emotion][1]

    def get_blink(self): return self.emotion_table[self.current_emotion][1]


emotion_engine = facialExpressionEngine("joy", image_folder)


class GestureCommander(Node):

    def __init__(self):
        super().__init__('GUI_gesture_command')
        self.cli = self.create_client(Gesture, 'gesture')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Gesture.Request()

    def send_request(self, gesture):
        try:
            self.req.gesture = str(gesture)
            self.future = self.cli.call_async(self.req)
        except Exception as e:
            print("Error: {}".format(e))
            print(usage())


class AudioVisualController(Node):

    def __init__(self):
        super().__init__('audiovisual_controller')
        self.subscription = self.create_subscription(String, 'speechTopic',
                                                     self.cb_function_message,
                                                     10)
        self.subscription
        self.emotion = self.create_subscription(String, 'emotionTopic',
                                                     self.cb_function_emotion,
                                                     10)

        self.publisher = self.create_publisher(String, 'ListenBlockTopic', 10)
        self.gesture_comm = GestureCommander()
        
    def cb_function_message(self, Data):
        reply = Data.data
        reply = literal_eval(reply)
        print(reply)
        self.speak(reply)
        
    
    def cb_function_emotion(self, Data):
        global emotion_engine
        if Data.data in ["fear", "anger", "joy","sadness", "disgust", 
                         "surprise", "dizzy", "sleepy", "thirsty",
                         "sweaty", "confused","neutral"]:
            emotion_engine.current_emotion = Data.data
            if Data.data == "surprise":
                self.gesture_comm.send_request("surprise")
                t0 = time()
                while time()-t0<3:pass
                emotion_engine.current_emotion = "neutral"
        else: pass

    def speak(self, speech):
        global is_talking
        for i, s in enumerate(speech):
            voice_engine = ['espeak']
            gib = s[0]
            volume, speed, pitch = s[1]
            vlm,ptc,spd = ["-a", str(volume)], ['-p', str(pitch)], ['-s',str(speed)]
            cmd = voice_engine+["-v","en-us+f3"]+ptc+vlm+spd+[gib]
            self.avoidEcho()    
            emotion_readings = list()
            process = subprocess.Popen(["python3",
                                        "../test/CameraTest.py", "0"],
                                        stdout=subprocess.PIPE)
            process.wait()
            emotion_now = literal_eval(process.communicate()[0].decode())#self.send_camera_request(0)
            print(emotion_now)
            emotion_readings.append(emotion_now)
            if "yes" in gib:
                self.gesture_comm.send_request("yes")
            is_talking = True      
            c = subprocess.Popen(cmd)
            while c.poll() is None: pass
            is_talking = False
            print("FINISHED SPEAKING")
            emotion_readings = list()
            process = subprocess.Popen(["python3",
                                        "../test/CameraTest.py", "0"],
                                        stdout=subprocess.PIPE)
            process.wait()
            emotion_now = literal_eval(process.communicate()[0].decode())#self.send_camera_request(0)
            print(emotion_now)
            emotion_readings.append(emotion_now)

            self.avoidEcho()    
        if 1:
            utils.write_sql("./mem/plantroid_memory.db", """
            INSERT INTO conversation
            (date, human_speech_filename, human_speech, robot_speech, human_emotion_timeseries)
            VALUES (?, ?, ?, ?, ?)
            """, [str(utils.now()), "../mem/audio/"+str(speech), str(speech), gib, str(emotion_readings)])

    def avoidEcho(self):
        msg = String()
        msg.data = " "
        self.publisher.publish(msg)
        self.get_logger().info("Changing listen blocking state.")

class MyApp(App):
    Window.clearcolor = (1, 1, 1, 1)
    Window.maximize()
    global is_talking
    global emotion_engine
    
    im_base = Image(source =image_folder+'Base.png', pos_hint={'center_x': .5,'center_y': .5}, size_hint=(1.5,1.5))
    im_l_eye = Image(source =image_folder+'eye0_r.png', pos_hint={'center_x': .65,'center_y': .65}, size_hint=(1.5,1.5))
    im_r_eye = Image(source =image_folder+'eye9.png', pos_hint={'center_x': .35,'center_y': .65}, size_hint=(1.5,1.5))
    im_mouth = Image(source =image_folder+'mouth3.png', pos_hint={'center_x': .5,'center_y': .205}, size_hint=(1.5,1.5))
    im_emotion = Image(source =image_folder+'empty.png', pos_hint={'center_x': .85,'center_y': .75}, size_hint=(1.5,1.5)) 
    frame = 0 
    
    def build(self):
        Window.bind(on_keyboard=self.on_keyboard)
        Clock.schedule_interval(self.mouther, .2)
        self.compose_face(emotion_engine.emotion_table[emotion_engine.current_emotion][0])
        Window.add_widget(self.im_l_eye)
        Window.add_widget(self.im_r_eye)
        Window.add_widget(self.im_mouth)
        Window.add_widget(self.im_emotion)
        Window.add_widget(self.im_base)
        #return Window

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if modifier == ['ctrl'] and codepoint == 'q':
            self.stop()

    def mouther(self, instance):
        global is_talking
        global emotion_engine
        if is_talking:
            if self.frame:
                self.frame = 0
            else:
                self.frame= 1
        else:
            self.frame = 0
        try:
            self.compose_face(emotion_engine.emotion_table[emotion_engine.current_emotion][self.frame])
        except:
            pass

    def compose_face(self, lista):
        self.im_l_eye.source = image_folder+lista[0]
        self.im_r_eye.source = image_folder+lista[1]
        self.im_mouth.source = image_folder+lista[2]
        self.im_emotion.source = image_folder+lista[3]


def GUI_main():
    plantroid_GUI = MyApp()
    plantroid_GUI.run()


def ROS2_main():
    rclpy.init(args=None)
    ROS_interface = AudioVisualController()
    rclpy.spin(ROS_interface)

def main():
    thread1 = Thread(target=ROS2_main)
    thread1.start()
    GUI_main()

if __name__ == '__main__':
    main()