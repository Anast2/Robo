#!/usr/bin/env python3
import os
# import sys
# sys.path.append('') #  Add the location of this package on your computer
import maestro.utils as utils 
from maestro.simple_state_machine import StateMachine
from maestro.ChatBot import chatter
# import utils
# from simple_state_machine import StateMachine
# from ChatBot import chatter
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from threading import Thread
from ast import literal_eval
from rooted_msgs.srv import *
from rooted_msgs.msg import *
from time import time
from beepy import beep
import subprocess
from random import choice
from threading import Thread
import json

##########################################################################################################################
#                                    GLOBAL VARIABLES AREA, BE CAREFUL WHILE EDITING                                     #
##########################################################################################################################
s = "s0"
c = 0
is_talking = False
dialog_json = "" #  TODO: load dialogue state-machine and implement the dialogue following
speech_style = 0
logging = 0
detect_person = 0
in_notebook = 0
OKAO = 0

plantroid_problem_state_machine = StateMachine("problem", 
                                               ["OK", "Problem"],
                                               ["problem_detected", "problem_cleared"],
                                               {"OK":{"problem_detected":"Problem",
                                                      "problem_cleared":"OK"},
                                                "Problem":{"problem_detected":"Problem",
                                                           "problem_cleared":"OK"}})

plantroid_state_machine = StateMachine("plantroid",["Free","Busy"],
                                                   ["move","finished"],
                                                   {"Free":{"move":"Busy",
                                                            "finished":"Free"},
                                                    "Busy":{"move":"Busy",
                                                            "finished":"Free"}
                                                          })

plantroid_dialogue_state_machine = StateMachine("dialogue", ["Silent","SpokeToMe", "BusyCheck", 
                                                             "LookAtUser", "AnnounceBusy", "StartDialogue2", 
                                                             "AnswerHuman", "WaitHumanQuestion1", "CheckProblemAndBusy",
                                                               "StartDialogue1", "Goodbye", "AskIfHumanIsAvailable",
                                                               "AnnounceProblem", "WaitHumanQuestion2", "ClearProblem"],
                                                            ["alone", "dialogue_end", "saw_human", "heard_human",
                                                             "yes","no", "no_problem", "busy", "idle", "problem_detected",
                                                             "dialog_init", "human_question", "robot_finished", "timeout"],
                                                            {"Silent":{"alone":"Silent",
                                                                       "saw_human":"CheckProblemAndBusy",
                                                                       "heard_human":"SpokeToMe",
                                                                       },
                                                             "SpokeToMe":{"no":"Silent",
                                                                          "yes":"BusyCheck",
                                                                          },
                                                             "BusyCheck":{"idle":"LookAtUser",
                                                                          "busy":"AnnounceBusy",}, 
                                                             "LookAtUser":{"saw_human":"StartDialogue2",},
                                                             "AnnounceBusy":{"robot_finished":"Goodbye",},
                                                             "StartDialogue2":{"dialogue_init":"AnswerHuman",}, 
                                                             "AnswerHuman":{"robot_finished":"WaitHumanQuestion2",},
                                                             "WaitHumanQuestion1":{"human_question":"AnswerHuman",
                                                                                   "timeout":"ClearProblem",},
                                                             "CheckProblemAndBusy":{"busy":"Silent",
                                                                                    "no_problem":"Silent",
                                                                                    "problem_detected":"StartDialogue1"},
                                                             "StartDialogue1":{"dialogue_init":"AskIfHumanIsAvailable",},
                                                             "Goodbye":{"dialogue_end":"Silent",},
                                                             "AskIfHumanIsAvailable":{"yes":"AnnounceProblem",
                                                                                      "no":"Goodbye",},
                                                             "AnnounceProblem":{"robot_finished":"WaitHumanQuestion1",},
                                                             "WaitHumanQuestion2":{"human_question":"AnswerHuman",
                                                                                   "timeout":"Goodbye",},
                                                             "ClearProblem":{"robot_finished":"Goodbye",}})
##########################################################################################################################


def emotion_2_prompt(emotion):
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
        super().__init__('maestro_sensor_reader')
        self.cli = self.create_client(Sensors, 'sensors_server')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Sensor service not available, waiting again...')
        self.req = Sensors.Request()

    def send_request(self, num):
        self.req.sensor_number = num
        self.future = self.cli.call_async(self.req)


class Cameras(Node):

    def __init__(self):
        super().__init__('maestro_camera_reader')
        self.cli = self.create_client(Camera, 'camera')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Camera service not available, waiting again...')
        self.req = Camera.Request()

    def send_request(self, type):
        self.req.imagetype = type
        self.future = self.cli.call_async(self.req)


class LLMinterface(Node):
    def __init__(self):
        super().__init__('maestro_llm_interface')
        self.cli = self.create_client(LLM, 'llm_server')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('LLM service not available, waiting again...')
        self.req = LLM.Request()
        self.req

    def send_request(self, model, prompt):
        self.req.model = model
        self.req.prompt = prompt
        self.future = self.cli.call_async(self.req)


class BusyInterface(Node):
    def __init__(self):
        super().__init__('maestro_busy_interface')
        self.cli = self.create_client(Busy, 'busy_servive')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Busy service not available, waiting again...')
        self.req = Busy.Request()

    def send_request(self, busy):
        self.req.request = busy
        self.future = self.cli.call_async(self.req)


class MemoryAccess(Node):
    def __init__(self):
        super().__init__('maestro_memory_access')
        self.cli = self.create_client(MemoryRequest, 'memory_reader')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Memory service not available, waiting again...')
        self.req = MemoryRequest.Request()

    def send_request(self, DB, command):
        self.req.db_name = DB
        self.req.command = command
        self.future = self.cli.call_async(self.req)


class PersonDetector(Node):
    def __init__(self):
        super().__init__('person_detector')
        self.vision_control = Cameras()
        self.person_detect_alarm = self.create_publisher(String, 'seenTopic', 10)

    def get_vision(self):
        response = "" #get_image_array().astype(np.uint8)
        self.vision_control.send_request(3)
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
                
    def detection_routine(self):
        global plantroid_state_machine
        global plantroid_dialogue_state_machine
        if (plantroid_dialogue_state_machine.get_current_state() == "Silent" and 
            plantroid_state_machine.get_current_state() == "Free"):
            result = self.get_vision()
            if result == True or result == "True":
                self.person_detect_alarm.publish("Seen")
            else:
                pass

class MAESTROmainNode(Node):

    def __init__(self, dialogue_state_machine, robot_state_machine):
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
        self.busy_interface = BusyInterface()
        self.sensor_reader = SensorReader()
        self.llm = LLMinterface()
        self.memory_access = MemoryAccess()
        self.busy = self.check_busy()
        self.notifications = {}
        self.time_last_seen = -float("inf")
        self.diag_state_machine = dialogue_state_machine
        self.robot_state_machine = robot_state_machine
        self.current_emotion = "neutral"
        try:
            with open('/location/of/your/dialogue.json', 'r') as f:
                self.dialogues = json.load(f)
        except Exception as e:
            self.dialogues = {}

    def cb_function(self, subscribedData):
        self.diag_state_machine.transition("heard_human")
        data = subscribedData.data.split(";")
        speaker_voice_emotion = data[2]
        content_emotion = sentiment_analysis(data[0])
        face_emotion = self.get_emotion()
        
        final_emotion = self.emotion_fusion([speaker_voice_emotion, content_emotion, face_emotion])
        # response_emotion = final_emotion #  Uncoment this line if you desire the robot to copy the emotion of the human, "mirror strategy". Comment line below.
        response_emotion = {"neutral":"neutral","happy":"happy","sad":"happy","anger":"neutral","surprise":"neutral"}[final_emotion] # Uncoment this line if you want the robot to try to improve human emotional state. Comment line above
        self.current_emotion = response_emotion
        self.get_logger().info('Subscribed: ' + data[0])
        beep(1)
        response = str(self.assign_prosody(self.conversate(data[0], response_emotion), response_emotion))
        msg = String()
        msg.data = response

        if self.robot_state_machine.get_current_state()=="Free":
            os.system("python /location/of/this/package/PersonSeeker.py") #  Change the string to the location of this package

        self.publisher_speech.publish(msg)

    def cb_function_notification(self, subscribedData):
        global plantroid_problem_state_machine
        plantroid_problem_state_machine.transition("problem_detected")
        data = subscribedData.data
        data_breakdown = data.split(":")
        self.notifications[data_breakdown[0]] = data_breakdown[1:]
        if "water" in self.notifications:
            self.set_face("thirsty")
        else:
            self.set_face("sad")
        print (self.notifications)
        self.get_logger().info('Subscribed: ' + data)

    def cb_function_seen(self, subscribedData):
            self.diag_state_machine.transition("saw_human")
            data = subscribedData.data
            if len(self.notifications)>0 and self.robot_state_machine.get_current_state()=="Free":
                self.last_time_seen = time()
                self.cb_function(a) #  TODO: Correct this line, what is a supposed to be???
                a.data = str(self.notifications) #  TODO: Correct this line, what is a supposed to be???
                self.cb_function(a) #  TODO: Correct this line, what is a supposed to be???

    def avoidEcho(self):
        msg = String()
        msg.data = " "
        self.publisher.publish(msg)
        self.get_logger().info("Changing listen blocking state.")

    def busy_request(self, request):
        self.busy_interface.send_request(request)
        while rclpy.ok():
            rclpy.spin_once(self.busy_interface)
            if self.busy_interface.future.done():
                try:
                    response = self.busy_interface.future.result().result
                except Exception as e:
                    self.busy_interface.get_logger().info(
                        'Service call failed %r' % (e,))
                else:
                    return literal_eval(response)

    def check_busy(self):
        busy = self.busy_request("get")
        if busy:
            self.robot_state_machine.transition("move")
        else:
            self.robot_state_machine.transition("finished")
            
    def set_busy(self): self.busy_request("set_busy")

    def set_idle(self): self.busy_request("set_idle")

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

    def set_face(self, emotion):
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

    def emotion_fusion(self,emotion_list): return max(set([(i, emotion_list.count(i)) for i in set(emotion_list)]),key=lambda x:x[1])[0]

    def get_llm_response(self, msg):
        self.llm.send_request(model="llama3", prompt=msg)
        while rclpy.ok():
            rclpy.spin_once(self.llm)
            if self.llm.future.done():
                try:
                    msg = self.llm.future.result().response
                except Exception as e:
                    self.llm.get_logger().info('Service call failed %r' % (e,))
                else:
                    msg = str(msg)
                break
        return msg 

    def conversate(self, data, response_emotion):
        gib = chatter(data)
        #human_content_emotion = GPTJ(data, port=5052)
        #print(content_emotion)
        addendum = response_emotion
        if gib:
            if "wikipedia:" in gib:
                gib = gib.split(":")[1]
                gib = utils.wikipedia_query(gib)

            elif "dictionary:" in gib:
                gib = gib.split(":")[1]
                gib = utils.dictionary_query(gib)

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

            elif gib == "vision_check":
                gib = self.get_vision()

            elif gib =="not_proc":
                gib = process_notifications(self.notifications)
                print(gib)
                self.notifications = {}

            gib = f"Briefly and politely paraphrase the following text in a {addendum} tone: {gib}"
            gib = self.get_llm_response(gib)

        else:
            gib = self.get_llm_response(data)
        self.set_face(response_emotion)
        command = f"INSERT INTO conversation (input, response) VALUES ({data}, {gib})"
        self.memory_access.send_request("/home/plantroid/plantroid_ws/src/robot_memory/db/conversation_history.db", command)
        while rclpy.ok():
            rclpy.spin_once(self.memory_access)
            if self.memory_access.future.done():
                try:
                    response = self.memory_access.future.result().result
                except Exception as e:
                    self.memory_access.get_logger().info(
                        'Service call failed %r' % (e,))
                else:
                    pass
                break        
        return gib

    def assign_prosody(self, utterance, method="random"):
        if not isinstance(utterance, list):
            utterance = [utterance]
        prosody = []
        if method == "random":
            return [(i,[choice(range(10,200)),choice(range(80,450)),choice(range(0,99))]) for i in utterance]
        elif method == "angry":
            return ([(i,[180,200,55]) for i in utterance])
        elif method == "happy":
            return ([(i,[160,140,65]) for i in utterance])
        elif method == "neutral":
            return ([(i,[150,100,45]) for i in utterance])
        elif method == "surprise":
            return ([(i,[200,80,65]) for i in utterance])
        elif method == "sadness":
            return ([(i,[80,80,35]) for i in utterance])
        else:
            return ([(i,[150,100,45]) for i in utterance])


def maestro():
    ROS_interface = MAESTROmainNode()
    rclpy.spin(ROS_interface)
    ROS_interface.destroy_node()


def person_detection():
    detector = PersonDetector()
    rclpy.spin(detector)
    detector.destroy_node()


def main():
    rclpy.init()
    maestro_thread = Thread(target = main)
    person_detection_thread = Thread(target = person_detection)
    maestro_thread.start()
    person_detection_thread.start()
    rclpy.shutdown()


if __name__ == '__main__':
    main()