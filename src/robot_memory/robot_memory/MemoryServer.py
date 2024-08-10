#!/usr/bin/env python3
import os
import subprocess
from plantroid_msgs.srv import *
from plantroid_msgs.msg import *
from std_msgs.msg import String
import subprocess 
from ast import literal_eval
import cv2
from PIL import Image 
import face_recognition
import io
import numpy as np
import sqlite3
import sys
import rclpy
from rclpy.node import Node


#sys.path.insert(1, './OKAO')
#from OKAO_vision_interface import get_image_array

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def get_all(conn, table, column):
	c = conn.cursor()
	response = c.execute("SELECT {} FROM {}".format(column, table))
	response = [i[0] for i in response.fetchall()]
	return response
	

def crop_face(img_array):
	blob = img_to_blob(img_array)
	full_img = face_recognition.load_image_file(blob)
	face_locations = face_recognition.face_locations(full_img)
	top, right, bottom, left = face_locations[0]
	face_image = full_img[top:bottom, left:right]
	cropped_pil_img = Image.fromarray(face_image)
	cropped_np_img = np.asarray(cropped_pil_img) 
	return cropped_np_img


def img_to_blob(img_array):
    blob = None
    pil_img = Image.fromarray(np.array(img_array).astype("uint8"))
    blob = io.BytesIO()
    pil_img.save(img_byte_arr, format='PNG')
    blob = img_byte_arr.getvalue()
    return blob


def blob_to_array(blob):
    img = Image.open(io.BytesIO(blob))
    return np.asarray(img)


def write_sql(dbLoc, sql_command, values):
    import sqlite3 as sql
    db = sql.connect(dbLoc)
    cursor = db.cursor()
    cursor.execute(sql_command, values)
    db.commit()
    db.close()


class Cameras(Node):

    def __init__(self):
        super().__init__('memory_camera_service')
        self.cli = self.create_client(Camera, 'camera')
        while not self.cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Camera.Request()

    def send_request(self, type):
        self.req.imagetype = type
        self.future = self.cli.call_async(self.req)
        

class MemoryServer(Node):

    def __init__(self):
        super().__init__("memory_server")
        self.srv = self.create_service(Gesture, "memory_service", self.handle_memory)
        self.nc = NeckCommander()
        self.mc = MotorCommander()

    def handle_memory(self, req, resp):
        memory_request = req.gesture.split(";")
        
        if memory_request[0] == "face_check":
            resp.result = "Unknown"
            face = self.get_crop_face()
            face_encoded = face_recognition.face_encodings(face_recognition.load_image_file(img_to_blob(face))[0])
            saved_faces = get_all("ID.db","face_img")
            saved_faces_encoded = [face_recognition.face_encodings(face_recognition.load_image_file(f))[0]
                                  for f in saved_faces]
            names = get_all("ID.db","name")    
            result = face_recognition.compare_faces([f], face_encoded)
            if True in result:
                match_index = result.index()                
                resp.result = names[match_index]
    
        elif memory_request[0] == "register_face":
            name, gender, age = memory_request[1:]
            face = self.get_crop_face()
            face_blob = img_to_blob(face)
            write_sql("ID.db","""
              INSERT INTO face_id
              (name, gender, age, face_img)
              VALUES (?,?,?,?)
            """, [name.  gender, age, face_blob])
            resp.result = "Done."

        return resp

    def get_crop_face():
        camera_client = Cameras()
        camera_client.send_request(3)
        face_img = None
        while rclpy.ok():
            rclpy.spin_once(camera_client)
            if camera_client.future.done():
                try:
                    response = camera_client.future.result().image
                except Exception as e:
                    camera_client.get_logger().info(
		                'Service call failed %r' % (e,))
                else:
                    face_img = literal_eval(response)
                break

        face = crop_face(face_img)
