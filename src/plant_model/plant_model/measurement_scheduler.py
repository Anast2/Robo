import sched
import time
import ast
import json
import os
from rooted_msgs.srv import *
from rooted_msgs.msg import *
import rclpy
from rclpy.node import Node


safe_N_range=[0,0]
safe_P_range=[0,0]
safe_K_range=[0,0]
safe_EC_range=[0,0]
safe_pH_range=[0,0]
safe_moisture_range=[0,0]
safe_temperature_range=[0,0]   
safe_irradiance_range=[0,0]


def load_plant_needs(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    else:
        return {}


class SensorReader(Node):
    def __init__(self):
        super().__init__('plant_model_sensor_reader')
        self.plant_information_file = self.get_parameter('plant_info_file').value  
        self.cli = self.create_client(Sensors, 'sensors_server')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Sensor service not available, waiting again...')
        self.req = Sensors.Request()

    def send_request(self, num):
        self.req.sensor_number = num
        self.future = self.cli.call_async(self.req)


class NotificationSender(Node):
    def __init__(self):
        super().__init__('plant_model_sensor_reader')
        self.cli = self.create_client(Sensors, 'sensors_server')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Sensor service not available, waiting again...')
        self.req = Sensors.Request()

    def send_request(self, num):
        self.req.sensor_number = num
        self.future = self.cli.call_async(self.req)


class MemoryAccess(Node):
    def __init__(self):
        super().__init__('plant_model_memory_access')
        self.cli = self.create_client(MemoryRequest, 'memory_reader')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Memory service not available, waiting again...')
        self.req = MemoryRequest.Request()

    def send_request(self, DB, command):
        self.req.db_name = DB
        self.req.command = command
        self.future = self.cli.call_async(self.req)


sensor_interface = SensorReader()
memory_interface = MemoryAccess()
plant_info_file_path = sensor_interface.plant_information_file
plant_info = load_plant_needs(plant_info_file_path)


def sensor_reading(sensor_ID):
    sensor_interface.send_request(sensor_ID)
    rclpy.spin_once(sensor_interface)  # Non-blocking
    if sensor_interface.future.done():
        try:
            response = sensor_interface.future.result().sensor_reading
            try:  # Convert result to a number (int, float) or list
                response = ast.literal_eval(response)
            except:
                pass  # Keep as string if malformed
        except Exception as e:
            sensor_interface.get_logger().info('Service call failed %r' % (e,))
        else:
            return response
    return None


def reading_memory_write():pass


def soil_N_reading():
    safe_range = plant_info["plant"]["health"]["nutrients"]["N"]
    reading = sensor_reading(8)
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
    problem = False

    if reading < safe_range[0] or reading > safe_range[1]:
        problem = True
    
    if problem: pass
        

def soil_P_reading(): 
    safe_range = plant_info["plant"]["health"]["nutrients"]["P"]
    reading = sensor_reading(9)


def soil_K_reading(): 
    safe_range = plant_info["plant"]["health"]["nutrients"]["K"]
    reading = sensor_reading(10)


def soil_EC_reading(): 
    safe_range = plant_info["plant"]["health"]["EC"]
    reading = sensor_reading(6)


def soil_pH_reading(): 
    safe_range = plant_info["plant"]["health"]["pH"]
    reading = sensor_reading(7)


def soil_moisture_reading(): 
    safe_range = plant_info["plant"]["health"]["soil_moisture"]
    reading = sensor_reading(4)


def temperature_reading(): 
    safe_range = plant_info["plant"]["environment"]["temperature"]   
    reading = sensor_reading(5)


def irradiance_reading():
    safe_range = plant_info["plant"]["environment"]["light"]
    top_left = sensor_reading(1)
    top_right = sensor_reading(2)
    rear = sensor_reading(3)
    return [top_left, top_right, rear]


s = sched.scheduler(time.time, time.sleep)


def schedule_sensor_tasks():
    s.enter(10, 1, run_sensor_task, ('soil_N_reading', soil_N_reading))  # Every 10 seconds
    s.enter(20, 1, run_sensor_task, ('soil_P_reading', soil_P_reading))  # Every 20 seconds
    s.enter(30, 1, run_sensor_task, ('soil_K_reading', soil_K_reading))  # Every 30 seconds
    s.enter(40, 1, run_sensor_task, ('soil_moisture_reading', soil_moisture_reading))  # Every 40 seconds
    s.enter(60, 1, run_sensor_task, ('irradiance_reading', irradiance_reading))  # Every 60 seconds
    # Repeat task execution
    s.run()


def run_sensor_task(task_name, task_fn):
    readings = task_fn()
    if readings is not None:
        print(f"{task_name}: {readings}")
        send_ros2_message({task_name: readings})
    s.enter(60, 1, run_sensor_task, (task_name, task_fn))  # Schedule next run after 60 seconds


rclpy.init()
schedule_sensor_tasks()
