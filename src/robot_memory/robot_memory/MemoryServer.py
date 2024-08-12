#!/usr/bin/env python3
import rclpy
import os
from rclpy.node import Node
from rooted_msgs.srv import *
from rooted_msgs.msg import *
from std_msgs.msg import String
import sqlite3 as sql 


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

    def __init__(self, database_folder=""):
        super().__init__("memory_server")
        self.srv = self.create_service(MemoryRequest, "memory_service", self.handle_request)
        self.database_folder =  database_folder

    def handle_request(self, req, resp):
        database_name = req.db_name
        command = req.command
        response = None 

        if "SELECT" in command or "INSERT" in command:
            try:
                assert os.path.isfile(f"{self.database_folder}/{database_name}")
            except AssertionError:
                self.get_logger().error(f"{database_name} could not be found in {self.database_folder}")
                response = "Failed"
            
            try:
                db = sql.connect(f"{self.database_folder}/{database_name}")
                cursor = db.cursor()
                cursor.execute(command)
            except:
                self.get_logger().error(f"There was a problem connecting to {database_name}.")
                response = "Failed"
            
            if "SELECT" in command:
                response = [i[0] for i in response.fetchall()]
            else:
                response = "Success"
            resp.result = response
        
        else:         
            self.get_logger().error(f"Command does not read or write from/in database {database_name}.")
            response = "Failed"

        return resp

def main():
    rclpy.init(args=None)
    memory_manager = MemoryServer
    rclpy.spin(memory_manager)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
