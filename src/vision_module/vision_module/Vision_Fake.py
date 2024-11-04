#!/usr/bin/env python3
import os
import cv2
import rclpy
from rclpy.node import Node
from rooted_msgs.srv import MemoryRequest, Camera
from PIL import Image
from sensor_msgs.msg import Image as Img
from socket import * 
from std_msgs.msg import String, Bool, Int8
import numpy as np
import face_recognition as fr 
from cv_bridge import CvBridge
from vision_module.image_processing2 import get_dir_sunlight, get_dir_shadow
from rcl_interfaces.msg import ParameterDescriptor
import numpy as np 


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

        id_descriptor = ParameterDescriptor(description='Location of the human identity database.')
        self.declare_parameter('identity_db', '', id_descriptor)  
        self.identity_db = self.get_parameter('identity_db').value
        
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
        
        pc_cam_descriptor = ParameterDescriptor(description='Describes which camera is being used - pc or gazebo.')
        self.declare_parameter('use_pc_camera', '', pc_cam_descriptor)  
        self.use_pc_camera = self.get_parameter('use_pc_camera').value
        self.camera_number = None
        self.camera_topic = None
        self.camera_source = None
        if self.use_pc_camera:
            self.camera_source = "PC" # "Gazebo"

            cam_num_descriptor = ParameterDescriptor(description='Number of the PC camera to be used.')
            self.declare_parameter('pc_camera_number', '', cam_num_descriptor)  
            self.camera_number = self.get_parameter('pc_camera_number').value
        else:
            self.camera_source = "Gazebo"
            cam_topic_descriptor = ParameterDescriptor(description='Gazebo camera topic.')
            self.declare_parameter('camera_topic', '', cam_topic_descriptor)  
            self.camera_topic = self.get_parameter('camera_topic').value

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
            img = get_image_array(source=self.camera_topic,
                                  camera_number=self.camera_number,
                                  camera_img_topic=self.camera_source)

        elif req.imagetype == 2:
            img = get_image_array(source=self.camera_topic,
                                  camera_number=self.camera_number,
                                  camera_img_topic=self.camera_source)
            img = cv2.resize(img, (32,24))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        elif req.imagetype == 3: #returns person detection
            print("Verifying if there are persons.")
            img = self.person_detected

        elif req.imagetype == 4: #returns sunlight position. 
            print("Returning sunlight position.")
            img = get_image_array(source=self.camera_topic,
                                  camera_number=self.camera_number,
                                  camera_img_topic=self.camera_source)
            img = get_dir_sunlight(img, None)

        elif req.imagetype == 5: #returns shadow position. 
            print("Returning shadow position.")
            img = get_image_array(source=self.camera_topic,
                                  camera_number=self.camera_number,
                                  camera_img_topic=self.camera_source)
            img = get_dir_shadow(img, None)

        elif req.imagetype == 6: #returns sunlight coord on real world 
            print("Returning light coordinates on real world.")
            img = get_image_array(source=self.camera_topic,
                                  camera_number=self.camera_number,
                                  camera_img_topic=self.camera_source)
            Dy = 0.32*344/(img[1]-160)
            Dx = Dy*(img[0]-120)/266
            img = [Dx, Dy]

        elif req.imagetype == 7:#returns shadow coord on real world
            print("Returning light coordinates on real world.")
            img = get_image_array(source=self.camera_topic,
                                  camera_number=self.camera_number,
                                  camera_img_topic=self.camera_source)
            img = get_dir_shadow(img, None)
            Dy = 0.32*344/(img[1]-160)
            Dx = Dy*(img[0]-120)/266
            img = [Dx, Dy]

        elif req.imagetype == 8:
            try:
                image = get_image_array(source=self.camera_topic,
                                        camera_number=self.camera_number,
                                        camera_img_topic=self.camera_source)
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
            unknown_face = np.array(image = get_image_array(source=self.camera_topic,
                                                            camera_number=self.camera_number,
                                                            camera_img_topic=self.camera_source))
            unknown_face = Image.fromarray(unknown_face)  
            id_face_list = []
            self.memory_access.send_request(self.identity_db,"SELECT ID, filepath FROM id_table")
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
    def __init__(self, camera_img_topic):
        super().__init__('gazebo_camera_reader')
        self.camera_img_topic = camera_img_topic
        self.cli = self.create_client(Img, self.camera_img_topic)
        self.gazebo_camera_interface = self.create_subscription(Img, self.camera_img_topic,
                                                      self.camera_cb_function,
                                                      10)
        self.br = CvBridge()
        self.latest_image = np.zeros((240,320)).tolist()
    
    def camera_cb_function(self, msg):
        self.latest_image = msg.data
        return self.br.cv2_to_imgmsg(msg.data).tolist()

def get_image_array(source="PC", camera_number=0, camera_img_topic = ""):
    img = np.zeros((240,320)).tolist()
    if source == "PC":
        camera = cv2.VideoCapture(camera_number)
        return_value, img = camera.read()
        img = cv2.resize(img, (240,320))
        img = img.tolist()
    else:
        GazeboCamera = GazeboCameraClient(camera_img_topic)
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