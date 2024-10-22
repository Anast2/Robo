import sched
import time
import ast
import json
import os
from rooted_msgs.srv import Sensors, NavigationOrder, MemoryRequest
from rooted_msgs.msg import *
from std_msgs.msg import String
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
        
        plant_info_descriptor = ParameterDescriptor(description='Plant description file location.')
        self.declare_parameter('plant_info_file', '', plant_info_descriptor)        
        self.plant_information_file = self.get_parameter('plant_info_file').value

        plant_db_descriptor = ParameterDescriptor(description='Measured plant parameters database location.')
        self.declare_parameter('db_path', '', plant_db_descriptor)        
        self.db = self.get_parameter('db_path').value1
        
        self.cli = self.create_client(Sensors, 'sensors_server')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Sensor service not available, waiting again...')
        self.req = Sensors.Request()

    def send_request(self, num):
        self.req.sensor_number = num
        self.future = self.cli.call_async(self.req)


class NavigationCommandSender(Node):
    def __init__(self):
        super().__init__('plant_model_navigation_command_sender')
        self.cli = self.create_client(NavigationOrder, "navigation_service")
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Navigation service not available, waiting again...')
        self.req = NavigationOrder.Request()
        
    def send_move_order(self, order):
        if order in ["light","shadow"]:
            self.req.move_to = order
        else:
            self.get_logger().error("Illegal order; orders should be either 'light' or 'shadow'!")


class NotificationSender(Node):
    def __init__(self):
        super().__init__('plant_model_notification_sender')
        self.notification_publisher = self.create_publisher(String, 'notificationTopic', 10)
        self.move_order_publisher = self.create_publisher(String, 'move_order', 10)
        self.notification_publisher
        self.move_order_publisher

    def send_notification(self, characteristic, status, measurement):
        self.notification_publisher.publish(f"{characteristic}:{status}:{measurement}")


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
notification_sender = NotificationSender()
robot_mover = NavigationCommandSender()
plant_info_file_path = sensor_interface.plant_information_file
plant_info = load_plant_needs(plant_info_file_path)
db_location = sensor_interface.db


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


def write_measurement(db, sql_command):
    # "/home/pantroid/plantroid_ws/src/robot_memory/db/measurements.db","SELECT ID, filepath FROM id_table"
    memory_interface.send_request(db, sql_command)


def soil_N_reading():
    safe_range = plant_info["plant"]["health"]["nutrients"]["N"]
    reading = sensor_reading(8)
    current_time = time.time()
    query = f"""
    INSERT INTO N (reading, time)
    VALUES ({reading}, {current_time})
    """
    global db_location
    memory_interface.send_request(db_location, query)
    problem = False

    if reading < safe_range[0] or reading > safe_range[1]:
        problem = True
    
    if problem:
        problem = "low"
        if reading>safe_range[0]:
            problem = "high"            
        notification_sender.send_notification("nitrogen", problem, str(reading))
        

def soil_P_reading(): 
    safe_range = plant_info["plant"]["health"]["nutrients"]["P"]
    reading = sensor_reading(9)
    current_time = time.time()
    query = f"""
    INSERT INTO P (reading, time)
    VALUES ({reading}, {current_time})
    """
    global db_location
    memory_interface.send_request(db_location, query)
    problem = False

    if reading < safe_range[0] or reading > safe_range[1]:
        problem = True
    
    if problem:
        problem = "low"
        if reading>safe_range[0]:
            problem = "high"            
        notification_sender.send_notification("phosphorus", problem, str(reading))


def soil_K_reading(): 
    safe_range = plant_info["plant"]["health"]["nutrients"]["K"]
    reading = sensor_reading(10)
    current_time = time.time()
    query = f"""
    INSERT INTO K (reading, time)
    VALUES ({reading}, {current_time})
    """
    global db_location
    memory_interface.send_request(db_location, query)    
    problem = False

    if reading < safe_range[0] or reading > safe_range[1]:
        problem = True
    
    if problem:
        problem = "low"
        if reading>safe_range[0]:
            problem = "high"            
        notification_sender.send_notification("potassium", problem, str(reading))


def soil_EC_reading(): 
    safe_range = plant_info["plant"]["health"]["EC"]
    reading = sensor_reading(6)
    current_time = time.time()
    query = f"""
    INSERT INTO EC (reading, time)
    VALUES ({reading}, {current_time})
    """
    global db_location
    memory_interface.send_request(db_location, query)
    problem = False

    if reading < safe_range[0] or reading > safe_range[1]:
        problem = True
    
    if problem:
        problem = "low"
        if reading>safe_range[0]:
            problem = "high"            
        notification_sender.send_notification("salinity", problem, str(reading))


def soil_pH_reading(): 
    safe_range = plant_info["plant"]["health"]["pH"]
    reading = sensor_reading(7)
    current_time = time.time()
    query = f"""
    INSERT INTO pH (reading, time)
    VALUES ({reading}, {current_time})
    """
    global db_location
    memory_interface.send_request(db_location, query)
    problem = False

    if reading < safe_range[0] or reading > safe_range[1]:
        problem = True
    
    if problem:
        problem = "low"
        if reading>safe_range[0]:
            problem = "high"            
        notification_sender.send_notification("pH", problem, str(reading))


def soil_moisture_reading(): 
    safe_range = plant_info["plant"]["health"]["soil_moisture"]
    reading = sensor_reading(4)
    current_time = time.time()
    query = f"""
    INSERT INTO water (reading, time)
    VALUES ({reading}, {current_time})
    """
    global db_location
    memory_interface.send_request(db_location, query)
    problem = False

    if reading < safe_range[0] or reading > safe_range[1]:
        problem = True
    
    if problem:
        problem = "low"
        if reading>safe_range[0]:
            problem = "high"            
        notification_sender.send_notification("water", problem, str(reading))


def no_store_temperature_reading(): return sensor_reading(5)


def move_2_light(): #  Notifies that the robot needs to move to sunlight
   robot_mover.send_move_order("light")


def move_2_shade(): #  Notifies that the robot needs to move into shade
   robot_mover.send_move_order("shadow")


def temperature_reading(): 
    safe_range = plant_info["plant"]["environment"]["temperature"]   
    reading = no_store_temperature_reading()
    current_time = time.time()
    query = f"""
    INSERT INTO temperature (reading, time)
    VALUES ({reading}, {current_time})
    """
    global db_location
    memory_interface.send_request(db_location, query)
    problem = False

    if reading < safe_range[0] or reading > safe_range[1]:
        problem = True
    
    if problem:
        problem = "low"
        if reading>safe_range[0]:
            problem = "high"            
            move_2_shade()
        notification_sender.send_notification("temperature", problem, str(reading))


def irradiance_reading():
    safe_range = plant_info["plant"]["environment"]["light"]
    safe_range_temperature = plant_info["plant"]["environment"]["temperature"]
    top_left = sensor_reading(1)
    top_right = sensor_reading(2)
    rear = sensor_reading(3)
    reading =  [top_left, top_right, rear]
    current_time = time.time()
    current_temperature = no_store_temperature_reading()
    high_temp = current_temperature > safe_range_temperature[1]
    query = f"""
    INSERT INTO light (top_left, top_right, bottom, time)
    VALUES ({reading[0]}, {reading[1]}, {reading[2]}, {current_time})
    """
    global db_location
    memory_interface.send_request(db_location, query)
    problem = False

    for l in reading:
        if l < safe_range[0] and not high_temp:
            problem = True
            move_2_light()
        elif l > safe_range[1]:
            problem = True
            move_2_shade()

    if problem:
        problem = "low"
        if reading>safe_range[0]:
            problem = "high"            
        notification_sender.send_notification("", problem, str(reading))


plantroid_scheduler= sched.scheduler(time.time,  time.sleep)


def schedule_sensor_tasks():
    plantroid_scheduler.enter(10, 1, run_sensor_task, ('soil_N_reading', soil_N_reading, 24*3600)) #  Daily measurement
    plantroid_scheduler.enter(20, 1, run_sensor_task, ('soil_P_reading', soil_P_reading, 24*3600)) #  Daily measurement
    plantroid_scheduler.enter(30, 1, run_sensor_task, ('soil_K_reading', soil_K_reading, 24*3600)) #  Daily measurement
    plantroid_scheduler.enter(30, 1, run_sensor_task, ('soil_K_reading', soil_pH_reading, 24*3600)) #  Daily measurement
    plantroid_scheduler.enter(30, 1, run_sensor_task, ('soil_K_reading', soil_EC_reading, 24*3600)) #  Daily measurement
    plantroid_scheduler.enter(40, 1, run_sensor_task, ('soil_moisture_reading', soil_moisture_reading, 3600))  # Hourly measurement
    plantroid_scheduler.enter(60, 1, run_sensor_task, ('irradiance_reading', irradiance_reading)) #  Every 5 minutes
    plantroid_scheduler.enter(60, 1, run_sensor_task, ('irradiance_reading', temperature_reading)) #  Every 5 minutes
    # Repeat task execution
    plantroid_scheduler.run()


def run_sensor_task(task_name, task_fn, period):
    readings = task_fn()
    if readings is not None:
        print(f"{task_name}: {readings}")
    plantroid_scheduler.enter(period, 1, run_sensor_task, (task_name, task_fn)) # Schedule next run after period. 


def main():
    rclpy.init()
    schedule_sensor_tasks()


if __name__ == "__main__":
    main()