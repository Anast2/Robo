#!/usr/bin/env python3
"""Virtual encoder node for PC simulation (no hardware)."""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class VirtualEncoder(Node):
    """Virtual encoder that simulates odometry without hardware."""

    def __init__(self):
        super().__init__('virtual_encoder_node')
        self.declare_parameter('DEVICENAME', '/dev/ttyServo')
        self.declare_parameter('BAUDRATE', '1000000')

        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.cmd_sub = self.create_subscription(
            Twist, 'cmd_vel', self.cmd_callback, 10)

        self.timer = self.create_timer(0.1, self.publish_odom)
        self.get_logger().info('Virtual encoder started (simulation mode)')

    def cmd_callback(self, msg):
        pass  # Ignore commands in virtual mode

    def publish_odom(self):
        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        self.odom_pub.publish(odom)


class VirtualController(Node):
    """Virtual controller that accepts velocity commands without hardware."""

    def __init__(self):
        super().__init__('virtual_controller_node')
        self.declare_parameter('DEVICENAME', '/dev/ttyServo')
        self.declare_parameter('BAUDRATE', '1000000')

        self.cmd_sub = self.create_subscription(
            Twist, 'cmd_vel', self.cmd_callback, 10)

        self.get_logger().info('Virtual controller started (simulation mode)')

    def cmd_callback(self, msg):
        pass  # Ignore commands in virtual mode


def main_encoder(args=None):
    rclpy.init(args=args)
    node = VirtualEncoder()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


def main_controller(args=None):
    rclpy.init(args=args)
    node = VirtualController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main_encoder()
