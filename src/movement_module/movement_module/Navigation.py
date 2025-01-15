#!/usr/bin/env python3
from std_msgs.msg import String
from rooted_msgs.srv import Busy, Camera, Command, NavigationOrder
from rooted_msgs.msg import *
import rclpy
from rooted_msgs.msg import Pose, Speed
from rclpy.node import Node
from math import sqrt
import numpy as np
from ast import literal_eval
import cv2
from math import atan2
import threading
from time import time
from movement_module.NeuralNav import NeuralNavigation, NeuralNavigationH5

###############################################################################################
#    This portion of the code should be uncommented in case it is running in a ARM computer   #
###############################################################################################
# import sys
# sys.path.append('/home/plantroid/plantroid_ws/src/plantroid_navigation/plantroid_navigation')
#c = get_config()
#os.environ['LD_PRELOAD'] = '/usr/lib/aarch64-linux-gnu/libgomp.so.1'
#c.Spawner.env.update('LD_PRELOAD')
# import sys
# sys.path.insert(1, './OKAO')
# from movement_module.OKAO_vision_interface import get_image_array
###############################################################################################

def min_mag(x1, x2):
    """! Function that selects which number has the smallest absolute value.
    @param x1 <int/float>: First number to have its magnitude compared.
    @param x2 <int/float>: Second number to have its magnitude compared.
    @return <int/float>: x1 or x2, whichever has the smallest magnitude.
    """
    if abs(x1) <= abs(x2):
        return x1
    return x2

def interval(x1, x2):
    """! Function that accurately calculates the difference between two angle values between -180 and 180.
    @param x1 <int/float>: First angle in radians.
    @param x2 <int/float>: Second angle in radians.
    @return <int/float>: Difference between angles.
    """
    if x2 - x1 > np.pi:
        return (x2 - x1) - 2 * np.pi
    elif x2 - x1 < -np.pi: 
        return 2 * np.pi + (x2 - x1)
    else:
        return x2 - x1

class BusyInterface(Node):
    """! Class responsible for interfacing with the Busy service."""
    def __init__(self):
        """! BusyInterface class initializer function."""
        super().__init__('movement_busy_interface')
        self.cli = self.create_client(Busy, 'busy_service')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Busy service not available, waiting again...')
        self.req = Busy.Request()

    def send_request(self, busy):
        """! Method responsible for sending busy/idle requests to the Busy service.
        @param busy <bool>: The busy status to send to the service.
        """
        self.req.request = busy
        self.future = self.cli.call_async(self.req)

class Cameras(Node):
    """! Class responsible for interfacing with the vision service."""
    def __init__(self):
        """! Cameras class initializer function."""
        super().__init__('navigation_camera_service')
        self.cli = self.create_client(Camera, 'camera')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = Camera.Request()

    def send_request(self, type):
        """! Method responsible for sending a request to the vision service.
        @param type <int>: The type of image request to send.
        """
        self.req.imagetype = type
        self.future = self.cli.call_async(self.req)

class NavigatorNode(Node):
    """! Class that implements the node responsible for safely navigating the robot."""
    def __init__(self):
        """! NavigatorNode initializer method."""
        super().__init__('vgg16_avoidance')
        self.subscription = self.create_subscription(Pose, '/encoder', self.encoder_listener_callback, 10)
        self.goal_subscription = None
        self.camera_client = Cameras()
        self.busy_interface = BusyInterface()
        self.goal = None
        self.goal_theta = None
        self.monitored_x, self.monitored_y, self.monitored_theta = 0, 0, 0 
        self.cli = self.create_client(Command, 'speed_command')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Servo Command service not available, waiting again...')
        self.req = Command.Request()
        self.image_history = []
        self.srv = self.create_service(NavigationOrder, "/navigation_service", self.move_order_service_callback)

    def get_image(self):
        """! Method responsible for capturing an image from the camera service.
        @return <numpy.array>: Image data captured from the camera service.
        """
        self.camera_client.send_request(1)
        while rclpy.ok():
            rclpy.spin_once(self.camera_client)
            if self.camera_client.future.done():
                try:
                    response = self.camera_client.future.result()
                except Exception as e:
                    self.camera_client.get_logger().info('Service call failed: %r' % (e,))
                else:
                    return literal_eval(response)

    def get_person(self):
        """! Method responsible for detecting a person using the vision service.
        @return <bool/array>: Detection result or image data.
        """
        response = False
        self.camera_client.send_request(3)
        while rclpy.ok():
            rclpy.spin_once(self.camera_client)
            if self.camera_client.future.done():
                try:
                    response = self.camera_client.future.result().image
                except Exception as e:
                    self.camera_client.get_logger().info('Service call failed: %r' % (e,))
                else:
                    response = literal_eval(response)
                break
        return response

    def rotate_to_person(self):
        """! Method responsible for rotating the robot to face a detected person."""
        person = self.get_person()
        while not person:
            print("Seeking humans")
            person = self.get_person()
            self.send_request([0, 0.5])
        print("Person found!")
        for _ in range(4):
            self.send_request([0, 0])

    def encoder_listener_callback(self, msg):
        """! Callback function to handle encoder data updates.
        @param msg <Pose>: Pose message containing the robot's position and orientation.
        """
        self.monitored_x, self.monitored_y, self.monitored_theta = msg.x, msg.y, msg.theta
        if self.goal is not None:
            error = sqrt((self.goal[0] - msg.x) ** 2 + (self.goal[1] - msg.y) ** 2)
            if abs(error) > 0.15:
                error_theta = interval(self.monitored_theta, self.goal_theta)
                PI_lin, PI_rot = 1, 0.5
                rot_spd, lin_spd = error_theta, error * PI_lin
                self.send_request(min(0.15, lin_spd), rot_spd)
            else:
                self.goal = None
                self.goal_theta = None
                self.image_history = []
                self.set_idle()
                for _ in range(4):
                    self.send_request(0, 0)

    def move_order_service_callback(self, req, resp):
        """! Callback function to handle navigation orders.
        @param req <NavigationOrder>: Navigation order request.
        @param resp <str>: Response status of the navigation order.
        @return <str>: "Success" or "Failure" based on the navigation order handling.
        """
        resp = "Success"
        if not self.check_busy():
            if req.move_to != "human":
                self.camera_client.send_request(6 if req.move_to == "light" else 7)
                while rclpy.ok():
                    rclpy.spin_once(self.camera_client)
                    if self.camera_client.future.done():
                        try:
                            response = self.camera_client.future.result()
                        except Exception as e:
                            self.camera_client.get_logger().info('Service call failed: %r' % (e,))
                        else:
                            self.goal = literal_eval(response.image)[::-1]
                        break
                self.set_busy()
                self.goal_theta = atan2(self.goal[1] - self.monitored_y, self.goal[0] - self.monitored_x)
                self.image_history = [cv2.resize(self.get_image(), (30, 40))] * 15
            else:
                self.set_busy()
                self.rotate_to_person()
        else:
            self.get_logger().warn("Plantroid is already busy, please send request later.")
            resp = "Failure"
        return resp

    def send_request(self, lin_spd, ang_spd):
        """! Method responsible for sending movement commands.
        @param lin_spd <float>: Linear speed to set.
        @param ang_spd <float>: Angular speed to set.
        """
        speed = Speed()
        speed.linear = float(lin_spd)
        speed.angular = float(ang_spd)
        self.req.speed_command = speed
        self.future = self.cli.call_async(self.req)

    def stitch(self):
        """! Method that stitches a series of images into a larger image.
        @return <numpy.array>: Stitched image data.
        """
        stitched = []
        present_img = [self.get_image()]
        img_hist = self.image_history
        for current_image in present_img:
            height, width = 160, 120
            canvas = np.zeros((int(height), int(width)), dtype=np.float32)
            current_image = cv2.resize(current_image, (30, 40))
            current_image = np.squeeze(current_image)
            resized_previous_images = [current_image] + img_hist[:15]
            self.image_history = resized_previous_images[:15]
            for i in range(4):
                for j in range(4):
                    current_index = 4 * i + j
                    img = resized_previous_images[current_index]
                    for y in range(img.shape[0]):
                        for x in range(img.shape[1]):
                            canvas[y + img.shape[0] * i, x + img.shape[1] * j] = img[y, x]
            canvas = np.array(np.expand_dims(canvas, axis=-1))
            stitched.append(canvas)
        return stitched[0]

    def stitch10(self):
        """! Method that stitches a series of 10 images into a larger image.
        @return <numpy.array>: Stitched image data.
        """
        stitched = []
        present_img = [cv2.resize(self.get_image(), (120, 160))]
        img_hist = self.image_history
        height, width = 160, 120

        for current_image in present_img:
            canvas = np.zeros((200, 150), dtype=np.uint8)
            current_image = np.squeeze(current_image)
            canvas[0:height, 0:width] = current_image
            resized_previous_images = img_hist[:9]
            self.image_history = [cv2.resize(current_image, (30, 40))] + self.image_history[:14]

            for i in range(5):
                img = resized_previous_images[i]
                for y in range(img.shape[0]):
                    for x in range(img.shape[1]):
                        canvas[y + img.shape[0] * i, width + x] = img[y, x]
            resized_previous_images = resized_previous_images[::-1]
            
            for i in range(4):
                img = resized_previous_images[i]
                for y in range(img.shape[0]):
                    for x in range(img.shape[1]):
                        canvas[height + y, x + (img.shape[1] * i)] = img[y, x]

            canvas = np.array(np.expand_dims(canvas, axis=-1))
            stitched.append(canvas)
        return stitched[0]

    def set_idle(self):
        """! Method to set the robot's busy status to idle."""
        self.busy_interface.send_request(False)

    def set_busy(self):
        """! Method to set the robot's busy status to busy."""
        self.busy_interface.send_request(True)

    def check_busy(self):
        """! Method to check if the robot is currently busy.
        @return <bool>: True if busy, False otherwise.
        """
        if self.busy_interface.future.done():
            try:
                response = self.busy_interface.future.result()
            except Exception as e:
                self.camera_client.get_logger().info('Service call failed: %r' % (e,))
                return False
            else:
                return response.status

def main(args=None):
    """! Main function that initializes the ROS node and keeps it running."""
    rclpy.init(args=args)
    navigator_node = NavigatorNode()
    rclpy.spin(navigator_node)
    navigator_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()