#!/usr/bin/env python3
import rclpy
import os
from rclpy.node import Node
from rooted_msgs.srv import *
from rooted_msgs.msg import *
from std_msgs.msg import String
import sqlite3 as sql 
from queue import Queue
import threading


insert_queue = Queue()


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


class MemoryServer(Node):

    def __init__(self, database_folder="."):
        super().__init__("memory_server")
        self.srv = self.create_service(MemoryRequest, "memory_service", self.handle_request)
        self.database_folder =  database_folder

    def handle_request(self, req, resp):
        database_name = req.db_name
        command = req.command
        response = None 
        db, cursor = None, None 

        if "SELECT" in command or "INSERT" in command:
            try:
                assert os.path.isfile(f"{self.database_folder}/{database_name}")
            except AssertionError:
                self.get_logger().error(f"{database_name} could not be found in {self.database_folder}")
                response = "Failed"
            
            try:
                db = sql.connect(f"{self.database_folder}/{database_name}")
                cursor = db.cursor()
            except:
                self.get_logger().error(f"There was a problem connecting to {database_name}.")
                response = "Failed"

            if "INSERT" in command:
                global insert_queue
                insert_queue.put([database_name, command])
                response = "Success"

            elif "SELECT" in command:
                cursor.execute(command)
                response = str([i[0] for i in cursor.fetchall()])
            else:
                response = "Success"
            resp.result = response

        else:         
            self.get_logger().error(f"Command does not read or write from/in database {database_name}.")
            response = "Failed"

        return resp


class MemoryWriter:
    def __init__(self, database_folder="."):
        self.database_folder =  database_folder #TODO: convert to rosparam db_folder_path.  
        self.main_routine()
         
    def main_routine(self):
        global insert_queue
        while 1:
            while not insert_queue.empty():
                current_insertion = insert_queue.get()
                db_name = current_insertion[0]
                command = current_insertion[1]
                try:
                    db = sql.connect(f"{self.database_folder}/{db_name}")
                    cursor = db.cursor()
                    cursor.execute(command)
                except Exception as e:
                    print("Failed to perform insertion operation due to: ", e)


def memory_server_start():
    memory_manager = MemoryServer
    rclpy.spin(memory_manager)


def memory_writer_start():
    writer = MemoryWriter()


def main():
    rclpy.init(args=None)
    server_thread = threading.Thread(target=memory_server_start, args=())
    writer_thread = threading.Thread(target=memory_writer_start, args=())
    server_thread.start()
    writer_thread.start()
    rclpy.shutdown()

  
if __name__ == "__main__":
    main()
