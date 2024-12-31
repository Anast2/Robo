#!/usr/bin/env python3
"""
@file navigation_node.py
@brief This file contains classes and functions for navigating the Plantroid robot.
"""

from std_msgs.msg import String
from rooted_msgs.srv import Busy, Camera, Command, NavigationOrder
from rooted_msgs.msg import *
import rclpy
from rooted_msgs.msg import Pose, Speed
from rclpy.node import Node
from math import pi, sqrt
import numpy as np
from ast import literal_eval
import cv2
from math import atan2
import threading
from time import time
from movement_module.NeuralNav import NeuralNavigation, NeuralNavigationH5

def min_mag(x1, x2):
    """! Function to return the value with the smaller magnitude.
    @param x1 (<float>): First value.
    @param x2 (<float>): Second value.
    @return: <float> Smaller magnitude value.
    """
    if abs(x1) <= abs(x2): return x1
    return x2

def interval(x1, x2):
    """! Function to calculate the angular interval between two angles.
    @param x1 (<float>): First angle in radians.
    @param x2 (<float>): Second angle in radians.
    @return: <float> Angular difference in radians.
    """
    if x2 - x1 > np.pi:
        return (x2 - x1) - 2 * np.pi
    elif x2 - x1 < -np.pi: 
        return 2 * np.pi + (x2 - x1)
    else:
        return x2 - x1

class BusyInterface(Node):
    """! ROS2 Node for interfacing with the 'busy' service."""
    def __init__(self):
        """! Constructor for BusyInterface class."""
        super().__init__('movement_busy_interface')
        self.cli = self.create_client(Busy, 'busy_servive')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Busy service not available, waiting again...')
        self.req = Busy.Request()

    def send_request(self, busy):
        """! Sends a request to the 'busy' service.
        @param busy (<str>): Request to send to the service.
        """
        self.req.request = busy
        self.future = self.cli.call_async(self.req)

class Cameras(Node):
    """! ROS2 Node for interfacing with the camera service."""
    def __init__(self):
        """! Constructor for Cameras class."""
        super().__init__('navigation_camera_service')
        self.cli = self.create_client(Camera, 'camera')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Camera service not available, waiting again...')
        self.req = Camera.Request()

    def send_request(self, type):
        """! Sends a request to capture an image of a specific type.
        @param type (<int>): Image type to request.
        """
        self.req.imagetype = type
        self.future = self.cli.call_async(self.req)

class NavigatorNode(Node):
    """! Main navigation node for the Plantroid robot."""
    def __init__(self):
        """! Constructor for NavigatorNode class."""
        super().__init__('vgg16_avoidance')
        ## Subscription to Pose messages.
        self.subscription = self.create_subscription(Pose, '/encoder', self.encoder_listener_callback, 10)
        self.subscription 
        ## Camera client instance.
        self.camera_client = Cameras()
        ## Busy service interface.
        self.busy_interface = BusyInterface()
        ## Current goal position.
        self.goal = None
        ## Current goal orientation.
        self.goal_theta = None
        ## Current monitored pose (x, y, theta).
        self.monitored_x, self.monitored_y, self.monitored_theta = 0, 0, 0 
        ## Speed command client.
        self.cli = self.create_client(Command, 'speed_command')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Speed Command service not available, waiting again...')
        self.req = Command.Request()
        ## Image history buffer.
        self.image_history = []

        ## Navigation service.
        self.srv = self.create_service(NavigationOrder, "/navigation_service", self.move_order_service_callback)

    def get_image(self):
        """! Retrieves an image from the camera client.
        @return: <list> Image data.
        """
        # Code...

    def get_person(self):
        """! Attempts to detect a person using the camera.
        @return: <bool> True if a person is detected, otherwise False.
        """
        # Code...

    def rotate_to_person(self):
        """! Rotates the robot to face a detected person."""
        # Code...

    def encoder_listener_callback(self, msg):
        """! Callback for handling encoder data.
        @param msg (<Pose>): Pose data from encoder.
        """
        # Code...

    def move_order_service_callback(self, req, resp):
        """! Callback for handling navigation orders.
        @param req (<NavigationOrder.Request>): Navigation request.
        @param resp (<NavigationOrder.Response>): Response to navigation request.
        @return: <NavigationOrder.Response> Response message.
        """
        # Code...

    def send_request(self, lin_spd, ang_spd):
        """! Sends speed commands to the robot.
        @param lin_spd (<float>): Linear speed command.
        @param ang_spd (<float>): Angular speed command.
        """
        # Code...

    def stitch(self):
        """! Stitches current and historical images.
        @return: <np.array> Stitched image.
        """
        # Code...

    def stitch10(self):
        """! Creates a larger stitched image using the latest and historical images.
        @return: <np.array> Stitched image.
        """
        # Code...

    def handle_busy(self, request):
        """! Handles busy state requests.
        @param request (<str>): Type of request ('get', 'set_busy', or 'set_idle').
        @return: <str> Busy state response.
        """
        # Code...

    def check_busy(self):
        """! Checks if the robot is busy.
        @return: <bool> True if busy, otherwise False.
        """
        return self.handle_busy("get")

    def set_busy(self):
        """! Sets the robot's state to busy."""
        self.handle_busy("set_busy")

    def set_idle(self):
        """! Sets the robot's state to idle."""
        self.handle_busy("set_idle")

def set_theta(navigator):
    """! Continuously updates the target orientation for the navigator.
    @param navigator (<NavigatorNode>): Navigator instance.
    """
    # Code...

def main():
    """! Main entry point for the navigation node."""
    rclpy.init(args=None)
    print("Starting NavigatorNode")
    t = NavigatorNode()
    t1 = threading.Thread(target=set_theta, args=(t,))
    t1.start()
    rclpy.spin(t)

if __name__ == "__main__":
    main()
