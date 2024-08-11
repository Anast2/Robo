#!/usr/bin/env python3
import sys
import os
#if os.uname()[4][:3] == "arm":  # checks if the node is running on Rasp
#    os.system("ln -sf ./OKAO/libSTB_ARM_x64.so ./libSTB.so")
#else:
#    os.system("ln -sf ./OKAO/libSTB_x64.so ./libSTB.so")
import cv2
import rclpy
from rclpy.node import Node
from rooted_msgs.srv import *
from PIL import Image
from socket import * 

running_on_pc = False
sys.path.append('') # add the location of this package, e.g., /home/you/rooted_ws/src/vision_module/vision_module

try:
    from ThermalCamera import ThermalCamera
except:
    running_on_pc = True
    print("Warning: Running on laptop PC, cannot take thermal pictures.")

sys.path.append('') # add the location of the OKAO vision folder, e.g., /home/you/rooted_ws/src/vision_module/vision_module/OKAO


from OKAO_vision_interface import get_emotions, get_image_array, detect_person

from image_processing2 import *

class CameraServer(Node):

    def __init__(self):
        super().__init__("camera_server")
        self.srv = self.create_service(Camera,"camera",self.handle_camera)

    def handle_camera(self, req, resp):
        img = None

        if req.imagetype == 0: #returns OKAO vision emotion estimate.
            print("Returning emotional analysis.")
            img = get_emotions()

        elif req.imagetype == 1: #returns image of the OKAO camera
            print("Returning black and white image.")
            img = get_image_array().tolist() #returns thermal image

        elif req.imagetype == 2 and not running_on_pc:
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
