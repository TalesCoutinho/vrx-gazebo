import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import time

class Tracker(Node):
    def __init__(self):
        super().__init__('tracker_node')
        self.sub_odom = self.create_subscription(Odometry, '/wamv/odom_filtered', self.odom_cb, 10)
        self.sub_cmd = self.create_subscription(Twist, '/cmd_vel', self.cmd_cb, 10)
        self.last_pose = None
        self.last_cmd = None
        self.start_time = time.time()
        self.timer = self.create_timer(5.0, self.timer_cb)
        
    def odom_cb(self, msg):
        self.last_pose = msg.pose.pose.position
        
    def cmd_cb(self, msg):
        self.last_cmd = msg
        
    def timer_cb(self):
        elapsed = time.time() - self.start_time
        if self.last_pose:
            print(f"[{elapsed:.1f}s] Pose: x={self.last_pose.x:.2f}, y={self.last_pose.y:.2f}")
        if self.last_cmd:
            print(f"[{elapsed:.1f}s] CmdVel: linear_x={self.last_cmd.linear.x:.2f}, angular_z={self.last_cmd.angular.z:.2f}")

def main():
    rclpy.init()
    node = Tracker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
