#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math

class FakeLidar(Node):
    def __init__(self):
        super().__init__('fake_lidar')
        self.publisher_ = self.create_publisher(LaserScan, '/wamv/sensors/lidars/lidar_wamv_sensor/scan', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        # Use the ROS frame_id, because ros_gz_bridge bridges to this, or static transform does.
        msg.header.frame_id = 'wamv/wamv/base_link/lidar_wamv_sensor'
        
        num_readings = 360
        msg.angle_min = -math.pi
        msg.angle_max = math.pi
        msg.angle_increment = 2 * math.pi / num_readings
        msg.time_increment = 0.0
        msg.scan_time = 0.1
        msg.range_min = 0.1
        msg.range_max = 130.0
        
        msg.ranges = [float('inf')] * num_readings
        msg.intensities = [0.0] * num_readings
        
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = FakeLidar()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
