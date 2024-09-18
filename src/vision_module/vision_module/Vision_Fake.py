#!/usr/bin/env python3
import sys
import os
import cv2
import rclpy
from rclpy.node import Node
from rooted_msgs.srv import *
from PIL import Image
from sensor_msgs.msg import Image as Img
from socket import * 
from std_msgs.msg import String, Bool, Int8
import numpy as np
import face_recognition as fr 
from cv_bridge import CvBridge
sys.path.append('') # add the location of this package, e.g., /home/you/rooted_ws/src/vision_module/vision_module
from image_processing2 import *


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


class CameraServer(Node):
    def __init__(self):
        super().__init__("camera_server")
        self.srv = self.create_service(Camera,"camera",self.handle_camera)
        self.current_emotion = "neutral"
        self.emotion_setter = self.create_subscription(String, 'set_emotion',
                                                       self.emotion_cb_function,
                                                       10)
        self.person_detected = True
        self.detection_setter = self.create_subscription(Bool, 'set_person_detection',
                                                       self.person_cb_function,
                                                       10)
        self.camera_setter = self.create_subscription(Int8, 'set_camera_number',
                                                      self.camera_cb_function,
                                                      10)
        self.camera_number = 0 
        self.camera_source = "PC" # "Gazebo"

        self.memory_access = MemoryAccess()

    def emotion_cb_function(self, msg):
        self.current_emotion = msg.data

    def person_cb_function(self, msg):
        self.person_detected = msg.data

    def camera_cb_function(self, msg):
        self.person_detected = msg.data

    def handle_camera(self, req, resp):
        img = None

        if req.imagetype == 0: #returns OKAO vision emotion estimate.
            print("Returning emotional analysis.")
            img = self.current_emotion

        elif req.imagetype == 1: #returns image of the OKAO camera
            print("Returning black and white image.")
            img = get_image_array(self.camera_number)

        elif req.imagetype == 2 and not running_on_pc:
            img = get_image_array(self.camera_number)
            img = cv2.resize(img, (32,24))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        elif req.imagetype == 3: #returns person detection
            print("Verifying if there are persons.")
            img = self.person_detected

        elif req.imagetype == 4: #returns sunlight position. 
            print("Returning sunlight position.")
            img = get_image_array(self.camera_number)
            img = get_dir_sunlight(img, None)

        elif req.imagetype == 5: #returns shadow position. 
            print("Returning shadow position.")
            img = get_image_array(self.camera_number)
            img = get_shadow_pos(img, None)

        elif req.imagetype == 6: #returns sunlight coord on real world 
            print("Returning light coordinates on real world.")
            img = get_image_array(self.camera_number)
            Dy = 0.32*344/(img[1]-160)
            Dx = Dy*(img[0]-120)/266
            img = [Dx, Dy]

        elif req.imagetype == 7:#returns shadow coord on real world
            print("Returning light coordinates on real world.")
            img = get_image_array(self.camera_number)
            img = get_shadow_pos(img, None)
            Dy = 0.32*344/(img[1]-160)
            Dx = Dy*(img[0]-120)/266
            img = [Dx, Dy]

        elif req.imagetype == 8:
            try:
                image = get_image_array(self.camera_number)
                image = Image.fromarray(image,"L")
                image.save("img.png","PNG")
                response = ""
                img_bytes = open("img.png", "rb")
                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.connect(("165.93.125.232", 5051))
                while 1:
                    data = img_bytes.read(1024)
                    clientSocket.send(data)
                    if not data: break

                while 1:
                    print("Waiting")
                    try:
                        response = clientSocket.recv(1024)
                    except Exception as e:
                        if e[0]=="time out": break 
                    if not response: pass
                    else:
                        response = response.decode("utf8")
	                    #print(response)
                        break
                clientSocket.close()
                os.system("rm img.png")
                img = response  
            except: pass   

        elif req.imagetype == 9: # Identity recognition
            id_match = False
            matched_id = None
            unknown_face = np.array(get_image_array()) #  TODO: convert to a format that works with this library.
            unknown_face = Image.fromarray(unknown_face)  
            id_face_list = []
            self.memory_access.send_request("/home/pantroid/plantroid_ws/src/robot_memory/db","SELECT ID, filepath FROM id_table")  # substitute with your absolute path for your database
            while rclpy.ok():
                rclpy.spin_once(self.memory_access)
                if self.memory_access.future.done():
                    try:
                        response = self.memory_access.future.result().result
                    except Exception as e:
                        self.memory_access.get_logger().info(
                            'Service call failed %r' % (e,))
                    else:
                        id_face_list = response
                    break

            for ID,face_file in id_face_list:
                id_face = fr.load_image_file(face_file)
                id_face_encoding = fr.face_encodings(id_face)[0]
                unknown_face_encoding = fr.face_encodings(unknown_face)[0]
                id_match = fr.compare_faces([id_face_encoding], unknown_face_encoding)
                if id_match:
                    img = ID
                    break

        else:
            print("Error: unkown request")
        resp.image = str(img)
        return resp

class GazeboCameraClient(Node):
    def __init__(self):
        super().__init__('gazebo_camera_reader')
        self.cli = self.create_client(Img, 'camera')
        self.gazebo_camera_interface = self.create_subscription(Img, 'camera',
                                                      self.camera_cb_function,
                                                      10)
        self.br = CvBridge()
        self.latest_image = np.zeros((240,320)).tolist()
    
    def camera_cb_function(self, msg):
        self.latest_image = msg.data
        return self.br.cv2_to_imgmsg(msg.data).tolist()

def get_image_array(camera_number=0, source="PC"):
    img = np.zeros((240,320)).tolist()
    if source == "PC":
        camera = cv2.VideoCapture(camera_number)
        return_value, img = camera.read()
        img = cv2.resize(img, (240,320))
        img = img.tolist()
    else:
        GazeboCamera = GazeboCameraClient()
        rate = GazeboCamera.node.create_timer(1)
        rate.sleep()
        img = GazeboCamera.latest_image
    return img

def main():
    rclpy.init(args=None)
    s = CameraServer()
    print("Ready to send images.")
    rclpy.spin(s)
    rclpy.shutdown()

if __name__ == "__main__":
#    startup_routine()
    main()