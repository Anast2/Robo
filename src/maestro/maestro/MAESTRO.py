#!/usr/bin/env python3
import os
# import sys
# sys.path.append('') #  Add the location of this package on your computer
import maestro.utils as utils 
from maestro.simple_state_machine import StateMachine
from maestro.ChatBot import chatter, sentiment_analysis
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
from random import choice
from threading import Thread
import json
import pickle 


def emotion_2_prompt(emotion):
    i = emotion.index(max(emotion[:-1]))
    return [" in a happy tone", "", " in a calm tone", " in a calming tone", " to cheer up",""][i]


def process_notifications(notifications):
    gib = "I need your help, the soil has "
    for i, N in enumerate(notifications):
        gib += str(notifications[N][0]) + " " + N + ", " + str(notifications[N][1])+str(notifications[N][2])+  ", content "
        if i>0 and i<len(notifications)-1: gib+= " and "
    return gib


class StateMachineContainer(Node):  # TODO: convert the state machine class to read from json files
    def __init__(self):
        super().__init__('maestro_state_machines')
        self.busy_state_machine = self.get_parameter('busy_state_machine').value
        with open(self.busy_state_machine, 'rb') as file: 
            self.busy_state_machine = pickle.load(file)
        
        self.problem_state_machine = self.get_parameter('problem_state_machine').value
        with open(self.problem_state_machine, 'rb') as file: 
            self.problem_state_machine = pickle.load(file)

        self.dialog_state_machine = self.get_parameter('dialog_state_machine').value
        with open(self.dialog_state_machine, 'rb') as file: 
            self.dialog_state_machine = pickle.load(file)


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
    def __init__(self, busy_state_machine, dialogue_state_machine):
        super().__init__('person_detector')
        self.vision_control = Cameras()
        self.person_detect_alarm = self.create_publisher(String, 'seenTopic', 10)
        self.busy_state_machine = busy_state_machine
        self.dialogue_state_machine = dialogue_state_machine

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
                
    def detection_routine(self): #  TODO: this is probably going to lead the node to hog the camera for itself only... better modify this to make the detector pause for some time between detection requests.
        if (self.dialogue_state_machine.get_current_state() == "Silent" and 
            self.busy_state_machine.get_current_state() == "Free"):
            result = self.get_vision()
            if result == True or result == "True":
                self.person_detect_alarm.publish("Seen")
            else:
                pass


class NavigationCommandSender(Node):
    def __init__(self):
        super().__init__('plant_model_navigation_command_sender')
        self.cli = self.create_client(NavigationOrder, "navigation_service")
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Navigation service not available, waiting again...')
        self.req = NavigationOrder.Request()
        
    def send_move_order(self, order):
        if order in ["human"]:
            self.req.move_to = order
        else:
            self.get_logger().error("Illegal order; orders should be either 'light' or 'shadow'!")


class MAESTROmainNode(Node):
    def __init__(self, busy_state_machine, problem_state_machine, dialogue_state_machine):
        super().__init__('plantroid')

        # defining subscribers
        self.subscription = self.create_subscription(String, 'messageTopic',
                                                     self.cb_function_conversation,
                                                     10)
        self.subscription_notifications = self.create_subscription(String, 'notificationTopic',
                                                                   self.cb_function_notification,
                                                                   10)
        self.subscription_human_seen = self.create_subscription(String, 'seenTopic',
                                                     self.cb_function_seen,
                                                     10)

        self.busy_state_listener = self.create_subscription(String, 'busy_state_publisher',
                                                            self.cb_function_busy_listener,
                                                            10)

        self.finished_talking_listener = self.create_subscription(String, 'finished_speaking',
                                                                  self.cb_function_finished_speech,
                                                                  10)

        self.subscription
        self.subscription_notifications
        self.subscription_human_seen
        self.busy_state_listener
        
        # defining publishers 
        self.publisher = self.create_publisher(String, 'ListenBlockTopic', 10)
        self.publisher_emotion = self.create_publisher(String, 'emotionTopic', 10)
        self.publisher_speech = self.create_publisher(String, 'speechTopic', 10)

        # service interfaces
        self.vision_control = Cameras()
        self.busy_interface = BusyInterface()
        self.sensor_reader = SensorReader()
        self.llm = LLMinterface()
        self.memory_access = MemoryAccess()
        self.robot_mover = NavigationCommandSender()        

        # load parameters from launchfile.
        self.logging = self.get_parameter('store_chat_log').value
        self.detect_person = self.get_parameter('keep_eye_contact').value
        self.pc_mode = self.get_parameter('pc_mode').value
        self.store_emotion = self.get_parameter('store_emotion_change').value
        
        # definition of important internal variables 
        self.busy = self.check_busy()
        self.notifications = {}
        self.time_last_seen = -float("inf")
        self.busy_state_machine = busy_state_machine
        self.problem_state_machine = problem_state_machine
        self.dialogue_state_machine = dialogue_state_machine
        self.current_emotion = "neutral"
        self.last_time_seen = float("inf")
        self.is_talking = False

        # loading external information 
        self.dialogues = {}
        dialogue_file_location = self.get_parameter('dialogue_json').value

        try:
            with open(dialogue_file_location, 'r') as f:
                self.dialogues = json.load(f)
        except Exception as e:
            self.get_logger.error(str(e))

    def cb_function_conversation(self, subscribedData):
        self.dialogue_state_machine.transition("heard_human")
        data = subscribedData.data.split(";")
        speaker_voice_emotion = data[2]
        content_emotion = sentiment_analysis(data[0])
        face_emotion = self.get_face_emotion()
        
        final_emotion = self.emotion_fusion([speaker_voice_emotion, content_emotion, face_emotion])
        # response_emotion = final_emotion #  Uncoment this line if you desire the robot to copy the emotion of the human, "mirror strategy". Comment line below.
        response_emotion = {"neutral":"neutral","happy":"happy","sad":"happy","anger":"neutral","surprise":"neutral"}[final_emotion] # Uncoment this line if you want the robot to try to improve human emotional state. Comment line above
        self.current_emotion = response_emotion
        self.get_logger().info('Subscribed: ' + data[0])
        beep(1)
        response = str(self.assign_prosody(self.conversate(data[0], response_emotion), response_emotion))
        msg = String()
        msg.data = response
        if self.logging:
            emotion_delta = tuple()
            if self.store_emotion:
                final_face_emotion = self.get_face_emotion()
                emotion_delta = (final_emotion, final_face_emotion)
            self.store_dialogue_exchange(data, gib, time(), f"{emotion_delta}")

        if self.busy_state_machine.get_current_state()=="Free":
            self.robot_mover.send_move_order("human")
            
        self.is_talking = True
        self.publisher_speech.publish(msg)

    def cb_function_notification(self, subscribedData):
        self.problem_state_machine.transition("problem_detected")
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
            self.dialogue_state_machine.transition("saw_human")
            data = subscribedData.data
            if len(self.notifications)>0 and self.busy_state_machine.get_current_state()=="Free":
                self.last_time_seen = time()
                send_hello = String()
                send_hello.data = "Hello;None;happy"
                self.cb_function_conversation(send_hello) #TODO: adjust so it does not disturb the dialogue flow. 

    def cb_function_busy_listener(self, msg):
        busy = literal_eval(msg.data)
        if busy:
            self.busy_state_machine.transition("move")
        else:
            self.busy_state_machine.transition("finished")

    def cb_function_finished_speech(self,msg):
        self.is_talking = False

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

    def get_face_emotion(self):
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
        basic_prompts = self.dialogue_prompts.get(self.dialogue_state_machine.get_current_state())
        #TODO: add other analysis accorsing to the state instead of only parsing it from the json file. 
        if basic_prompts:
            gib = chatter(data, pairs=basic_prompts)
        else:
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

    def store_dialogue_exchange(self, humam_input, robot_output, time_stamp, emotion):
        command = f"INSERT INTO conversation (input, response, time, emotion) VALUES ({humam_input}, {robot_output}, {time_stamp}, {emotion})"
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
 

def maestro():
    ROS_interface = MAESTROmainNode()
    rclpy.spin(ROS_interface)
    ROS_interface.destroy_node()


def person_detection(busy_state_machine, dialogue_state_machine):
    detector = PersonDetector(busy_state_machine, dialogue_state_machine)
    rclpy.spin(detector)
    detector.destroy_node()


def main():
    rclpy.init()
    state_machines = StateMachineContainer()
    maestro_thread = Thread(target = maestro,
                            args = ())
    person_detection_thread = Thread(target = person_detection,
                                     args=(state_machines.busy_state_machine, 
                                           state_machines.dialog_state_machine))
    maestro_thread.start()
    person_detection_thread.start()
    rclpy.shutdown()


if __name__ == '__main__':
    main()