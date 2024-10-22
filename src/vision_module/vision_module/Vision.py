#!/usr/bin/env python3
import os
import rclpy
from rclpy.node import Node
from rooted_msgs.srv import *
from PIL import Image
from socket import * 
import face_recognition as fr 
from vision_module.ThermalCamera import ThermalCamera
from vision_module.OKAO.OKAO_vision_interface import get_emotions, get_image_array, detect_person
from vision_module.image_processing2 import *
from rcl_interfaces.msg import ParameterDescriptor


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
        id_descriptor = ParameterDescriptor(description='Location of the human identity database.')
        self.declare_parameter('identity_db', '', id_descriptor)  
        self.identity_db = self.get_parameter('identity_db').value
    def handle_camera(self, req, resp):
        img = None

        if req.imagetype == 0: #returns OKAO vision emotion estimate.
            print("Returning emotional analysis.")
            img = get_emotions()

        elif req.imagetype == 1: #returns image of the OKAO camera
            print("Returning black and white image.")
            img = get_image_array().tolist() #returns thermal image

        elif req.imagetype == 2:
            print("Returning thermal image.")
            img = get_thermal_image()

        elif req.imagetype == 3: #returns person detection
            print("Verifying if there are persons.")
            img = detect_person()

        elif req.imagetype == 4: #returns sunlight position. 
            print("Returning sunlight position.")
            img = get_image_array()
            img = get_dir_sunlight(img, None)

        elif req.imagetype == 5: #returns shadow position. 
            print("Returning shadow position.")
            img = get_image_array()
            img = get_shadow_pos(img, None)

        elif req.imagetype == 6: #returns sunlight coord on real world 
            print("Returning light coordinates on real world.")
            img = get_image_array()
            img = get_dir_sunlight(img, None)[0]
            Dy = 0.32*344/(img[1]-160)
            Dx = Dy*(img[0]-120)/266
            img = [Dx, Dy]

        elif req.imagetype == 7:#returns shadow coord on real world
            print("Returning light coordinates on real world.")
            img = get_image_array()
            img = get_shadow_pos(img, None)
            Dy = 0.32*344/(img[1]-160)
            Dx = Dy*(img[0]-120)/266
            img = [Dx, Dy]

        elif req.imagetype == 8:
            try:
                image = get_image_array()
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
            unknown_face = np.array(get_image_array())
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
        

def get_thermal_image():
    tc = ThermalCamera()
    return tc.i2cRead()


def main():
    rclpy.init(args=None)
    s = CameraServer()
    print("Ready to send images.")
    rclpy.spin(s)
    rclpy.shutdown()


if __name__ == "__main__":
#    startup_routine()
    main()
