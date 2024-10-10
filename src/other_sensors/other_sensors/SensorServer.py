#!/usr/bin/env python3
from __future__ import print_function
import rclpy
from rclpy.node import Node
from plantroid_msgs.srv import Sensors
import serial
from pymodbus.client import ModbusSerialClient

computer = 0


class SensorServer(Node):

    def __init__(self):
        super().__init__("sensor_service")
        self.srv = self.create_service(Sensors, "sensors_server",
                                       self.cb_function)
        self.NPK_port = "/dev/ttyNPK"
        #self.Ph_EC_port = "/dev/ttyUSB0"
        self.arduino_port = "/dev/ttyArduino"
        self.arduino = serial.Serial(self.arduino_port,9600,timeout=5)
        self.NPK_sensor = serial.Serial(self.NPK_port,9600,timeout=5)

    def cb_function(self, req, resp):
        sensor = req.sensor_number
        if sensor<=5:
            resp.sensor_reading = self.get_arduino(str.encode(str(sensor)))
        elif sensor == 6:
            resp.sensor_reading = self.get_NPK("EC")
        elif sensor == 7:
            resp.sensor_reading = self.get_NPK("pH")
        elif sensor == 8:
            resp.sensor_reading = self.get_NPK("N")
        elif sensor == 9:
            resp.sensor_reading = self.get_NPK("P")
        elif sensor == 10:
            resp.sensor_reading = self.get_NPK("K")            
        else:
            resp.sensor_reading = "0"
        return resp

    def get_arduino(self, sensor):
        self.arduino.write(sensor)
        return self.arduino.readline().decode("utf-8")[:-1]

    def get_NPK(self, value):

        response = ""
        client = ModbusSerialClient(self.NPK_port, baudrate=9600)
        client.connect()
        while response == "":
            response = str(client.read_holding_registers(address={"EC":0x0202,
                                                                  "pH":0x0203,
                                                                  "N":0x0204,
                                                                  "P":0x0205,
                                                                  "K":0x0206}\
                                                                  [value],
                                                         count=1,
                                                         slave=1).registers[0])
        client.close()

        # for older NPK only integrated soil sensor.
        # if value == "A":
        #     for msg in [[0x01,0x03, 0x00, 0x1e, 0x00, 0x01, 0xe4, 0x0c],
        #                 [0x01,0x03, 0x00, 0x1f, 0x00, 0x01, 0xb5, 0xcc],
        #                 [0x01,0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xc0]]:
        #         self.NPK_sensor.write(msg)
        #         ans = self.NPK_sensor.read(7)
        #         response += str(ans[4])+";"
        #
        # elif value == "N":
        #     get_nitrogen_msg = [0x01,0x03, 0x00, 0x1e, 0x00, 0x01, 0xe4, 0x0c]
        #     self.NPK_sensor.write(get_nitrogen_msg)
        #     ans = self.NPK_sensor.read(7)
        #     response = str(ans[4])
        #   
        # elif value == "P":
        #     get_phosphorus_msg = [0x01,0x03, 0x00, 0x1f, 0x00, 0x01, 0xb5,
        #                           0xcc]
        #     self.NPK_sensor.write(get_phosphorus_msg)
        #     ans = self.NPK_sensor.read(7)
        #     response = str(ans[4])
        #
        # elif value == "K":
        #     get_potassium_msg = [0x01,0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xc0]
        #     self.NPK_sensor.write(get_potassium_msg)
        #     ans = self.NPK_sensor.read(7)
        #     response = str(ans[4])

        return response

    def get_PH_EC(self,value):
        return "7"


def main():
    rclpy.init(args=None)
    s = SensorServer()
    print("Ready to read sensors")
    rclpy.spin(s)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
