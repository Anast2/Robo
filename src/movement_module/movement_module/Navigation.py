#!/usr/bin/env python3
from std_msgs.msg import String
from rooted_msgs.srv import *
from rooted_msgs.msg import *
import rclpy
from rooted_msgs.msg import Pose, Speed, State
from rclpy.node import Node
from math import pi, sqrt
import numpy as np
from ast import literal_eval
import cv2
from math import atan2
import threading
from time import time
from movement_module.NeuralNav import NeuralNavigation, NeuralNavigationH5

# import sys
# sys.path.append('/home/plantroid/plantroid_ws/src/plantroid_navigation/plantroid_navigation')

#c = get_config()
#os.environ['LD_PRELOAD'] = '/usr/lib/aarch64-linux-gnu/libgomp.so.1'
#c.Spawner.env.update('LD_PRELOAD')
# import sys
# sys.path.insert(1, './OKAO')
# from movement_module.OKAO_vision_interface import get_image_array


def min_mag(x1, x2):
    if abs(x1)<=abs(x2):return x1
    return x2


def interval(x1, x2):
    if x2-x1>np.pi:
        return (x2-x1)-2*np.pi
    elif x2-x1<-np.pi: 
        return 2*np.pi+(x2-x1)
    else:
        return x2-x1


class BusyInterface(Node):
    def __init__(self):
        super().__init__('movement_busy_interface')
        self.cli = self.create_client(Busy, 'busy_servive')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Busy service not available, waiting again...')
        self.req = Busy.Request()

    def send_request(self, busy):
        self.req.request = busy
        self.future = self.cli.call_async(self.req)


class Cameras(Node):
    def __init__(self):
        super().__init__('navigation_camera_service')
        self.cli = self.create_client(Camera, 'camera')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Camera.Request()

    def send_request(self, type):
        self.req.imagetype = type
        self.future = self.cli.call_async(self.req)


class NavigatorNode(Node):
    def __init__(self):
        super().__init__('vgg16_avoidance')
        self.subscription = self.create_subscription(Pose,'/encoder', self.encoder_listener_callback,10)
        self.subscription 
        self.goal_subscription
        self.camera_client = Cameras()
        self.busy_interface = BusyInterface()
        self.goal = None
        self.goal_theta = None
        self.monitored_x, self.monitored_y, self.monitored_theta = 0, 0, 0 
        self.cli = self.create_client(Command, 'speed_command')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Servo Command service not available, waiting again...')
        self.req = Command.Request()
        self.image_history = [] #[cv2.resize(self.get_image(),(30,40))]*15
        self.srv = self.create_service(NavigationOrder, "/move_order",
                                       self.move_order_service_callback)


    def get_image(self):
        self.camera_client.send_request(1)
        while rclpy.ok():
            rclpy.spin_once(self.camera_client)
            if self.camera_client.future.done():
                try:
                    response = self.camera_client.future.result()
                except Exception as e:
                    self.camera_client.get_logger().info(
                        'Service call failed %r' % (e,))
                else:
                    return literal_eval(response)

    def get_person(self):
        response = False #get_image_array().astype(np.uint8)
        self.camera_client.send_request(3)
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
            self.send_request([0, 0.5])
        print("person found!")
        for i in range(4):
            self.send_request([0, 0])

    def encoder_listener_callback(self,msg):
        self.monitored_x, self.monitored_y, self.monitored_theta = msg.x, msg.y, msg.theta
        # print(msg.x, msg.y, msg.theta)
        #print(self.monitored_x, self.monitored_y)
        if self.goal is not None:
            error = sqrt((self.goal[0]-msg.x)**2+(self.goal[1]-msg.y)**2)
            #print(error)
            #theta_line = atan2(self.goal[1]-self.monitored_y, self.goal[0]-self.monitored_x)
            #self.goal_theta = NeuralNavigation(self.get_image(),
            #                                   self.monitored_theta, theta_line, error)
            if abs(error)>.15:
                error_theta = interval(self.monitored_theta, self.goal_theta)
                print("Dist E: ", error, "Rot E: ", error_theta)
                PI_lin, PI_rot = 1, 0.5
                tz = 0.000001
                rot_spd, lin_spd = error_theta, error * PI_lin #min_mag((error_theta+tz)/abs((error_theta+tz))*0.8, error_theta), error * PI_lin
                self.send_request(min(0.15,lin_spd), rot_spd)#max(.25*error_theta, 0.2*error_theta/abs(error_theta)))
                print("Sending: ", lin_spd, rot_spd)
            else:
                self.goal = None
                self.goal_theta = None
                self.image_history = []
                self.set_idle()
                for i in range(4):
                    self.send_request(0, 0)
    
    def move_order_service_callback(self, req, resp):
        resp = "Success"
        if not self.check_busy():
            if req.move_to != "human":
                if req.move_to == "light":
                    self.camera_client.send_request(6)
                else:
                    self.camera_client.send_request(7)
                while rclpy.ok():
                    rclpy.spin_once(self.camera_client)
                    if self.camera_client.future.done():
                        try:
                            response = self.camera_client.future.result()
                        except Exception as e:
                            self.camera_client.get_logger().info(
                                'Service call failed %r' % (e,))
                        else:
                            self.goal = literal_eval(response.image)[::-1] #TODO: check if -1 is necessary? it should not be, if any corrections need to be done, they should be in the Vision server and not in the actual navigation server, as the format should be [x,y]...
                            print("GOAL WAS SET AS: ", self.goal)
                        break
                self.set_busy()
                self.goal_theta = atan2(self.goal[1]-self.monitored_y, self.goal[0]-self.monitored_x) #  TODO: check if the logic still follows the ::-1  thing above. 
                self.image_history = [cv2.resize(self.get_image(),(30,40))]*15 # Assumes that with the new computer getting the image from the vision server will be quick enough. If that is not the case, we need to change how get_image works to interface directly with the camera module. Another idea is to directly run the model in the vision server, like it was done for the previous version of the robot navigation. 
            else:
                self.set_busy()
                self.rotate_to_person()
        else:
            self.get_logger().warn("Plantroid is already busy, please send request later.")
            resp = "Failure"
        return resp

    def send_request(self, lin_spd, ang_spd):
        #print("A")
        speed = Speed()
       # print("B")
        speed.linear = float(lin_spd)
        speed.angular = float(ang_spd)
        #print("C")
        self.req.speed_command = speed
        #print("D")
        self.future = self.cli.call_async(self.req)
        #print("E")

    def stitch(self):
        stitched = []
        present_img = [self.get_image()]
        img_hist = self.image_history
        for index, current_image in enumerate(present_img):
            #print(current_image)
            height, width = 160, 120
            canvas = np.zeros((int(height), int(width)), dtype=np.float32)
            current_image = cv2.resize(current_image,(30,40))
            current_image = np.squeeze(current_image)
            resized_previous_images = [current_image]+img_hist[:15]
            self.image_history = resized_previous_images[:15]
            for i in range(4):
                for j in range(4):
                    current_index = 4*i+j
                    img = resized_previous_images[current_index]
                    #print(img.shape)
                    for y in range(img.shape[0]):
                        for x in range(img.shape[1]):
                            canvas[y+img.shape[0]*i, x+img.shape[1]*j] = img[y,x]

            canvas = np.array(np.expand_dims(canvas, axis=-1))
            stitched.append(canvas)
        return stitched[0]

    def stitch10(self):
        stitched = []
        present_img = [cv2.resize(self.get_image(),(120,160))]
        img_hist = self.image_history
        height, width = 160, 120

        for index, current_image in enumerate(present_img):
            canvas = np.zeros((200, 150), dtype=np.uint8)
            current_image = np.squeeze(current_image)
            canvas[0:height, 0:width] = current_image
            resized_previous_images = img_hist[:9]            
            self.image_history = [cv2.resize(current_image,(30,40))]+self.image_history[:14]            

            for i in range(5):
                img = resized_previous_images[i]
                for y in range(img.shape[0]):
                    for x in range(img.shape[1]):
                        canvas[y+img.shape[0]*i, width+x] = img[y,x]
            resized_previous_images = resized_previous_images[::-1]
            
            for i in range(4):
                img = resized_previous_images[i]
                for y in range(img.shape[0]):
                    for x in range(img.shape[1]):
                        canvas[height+y, x+(img.shape[1]*i)] = img[y,x]

            canvas = np.array(np.expand_dims(canvas, axis=-1))
            #cv2.imwrite("Stitched.png", canvas)
            #cv2.waitKey(2000)
            #cv2.destroyAllWindows()
            stitched.append(canvas)
        return stitched[0]

    def handle_busy(self,request):
        self.busy_interface.send_request("request")
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

    def check_busy(self): return self.handle_busy(self,"get")

    def set_busy(self): self.handle_busy(self,"set_busy")

    def set_idle(self): self.handle_busy(self,"set_idle")


def set_theta(navigator):
    while navigator.goal is not None:
        x, y, t = navigator.monitored_x, navigator.monitored_y, navigator.monitored_theta
        xg, yg = navigator.goal
        distance = sqrt((xg-x)**2+(yg-y)**2)
        theta_line = atan2(yg-y,xg-x)
        #img = cv2.resize(navigator.get_image(), (120,160))
        t0 = time()
        navigator.goal_theta =  NeuralNavigationH5(navigator.stitch10(), t, theta_line, distance)
        print("Inference time: ", time()-t0)


def main():
    rclpy.init(args=None)
    print("Iniciando")
    #command_service_client()
    t = NavigatorNode()
    t1 = threading.Thread(target=set_theta, args=(t,))
    t1.start()
    rclpy.spin(t)


if __name__ == "__main__":
    main()