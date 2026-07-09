#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from rclpy.qos import qos_profile_sensor_data
from PIL import Image
import numpy as np

class SoftwareBathymetry(Node):
    def __init__(self):
        super().__init__('software_bathymetry')
        
        # Load heightmap image
        self.heightmap_path = '/home/tales/Source/ROS/robmov/vrx/vrx_gz/models/seabed/materials/textures/heightmap.png'
        try:
            img = Image.open(self.heightmap_path).convert('L')
            self.heightmap = np.array(img)
            self.height, self.width = self.heightmap.shape
            self.get_logger().info(f"Loaded heightmap: {self.width}x{self.height}")
        except Exception as e:
            self.get_logger().error(f"Failed to load heightmap: {e}")
            self.heightmap = None

        self.last_x = None
        self.last_y = None
        self.last_header = None
        
        self.odom_sub = self.create_subscription(
            Odometry,
            '/wamv/odom_filtered',
            self.odom_callback,
            10
        )
        
        self.scan_pub = self.create_publisher(
            LaserScan,
            '/world/bathymetry/model/wamv/link/wamv/base_link/sensor/bathymetry_wamv_sensor/scan',
            qos_profile_sensor_data
        )

        # 20 Hz timer for publishing
        self.timer = self.create_timer(0.05, self.timer_callback)

        self.get_logger().info('Software Bathymetry Sensor Started at 20Hz.')

    def odom_callback(self, msg):
        self.last_x = msg.pose.pose.position.x
        self.last_y = msg.pose.pose.position.y
        self.last_header = msg.header

    def timer_callback(self):
        if self.heightmap is None or self.last_x is None:
            return

        x = self.last_x
        y = self.last_y
        
        # Map Gazebo (x, y) to image (u, v)
        u = int((x + 250.0) / 500.0 * (self.width - 1))
        v = int((-y + 250.0) / 500.0 * (self.height - 1))
        
        # Clamp coordinates
        u = max(0, min(self.width - 1, u))
        v = max(0, min(self.height - 1, v))
        
        pixel_val = self.heightmap[v, u]
        
        # Height map scaling: size 500 500 20, pos 0 0 -25
        z_seabed = -25.0 + (pixel_val / 255.0) * 20.0
        
        # Sensor is at z = -1.0
        z_sensor = -1.0
        
        # Distance from sensor to seabed
        depth = z_sensor - z_seabed
        
        # Add some gaussian noise to simulate a real sonar
        noise = np.random.normal(0, 0.05)
        depth += noise
        
        if depth < 0.1:
            depth = float('inf') # invalid
            
        scan_msg = LaserScan()
        scan_msg.header = self.last_header
        scan_msg.header.frame_id = 'wamv/bathymetry_wamv_sensor_link'
        scan_msg.angle_min = 0.0
        scan_msg.angle_max = 0.0
        scan_msg.angle_increment = 0.0
        scan_msg.time_increment = 0.0
        scan_msg.range_min = 0.1
        scan_msg.range_max = 100.0
        scan_msg.ranges = [float(depth)]
        
        self.scan_pub.publish(scan_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SoftwareBathymetry()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
