import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import FollowWaypoints

def main():
    rclpy.init()
    node = rclpy.create_node('check_nav2_client')
    client = ActionClient(node, FollowWaypoints, 'follow_waypoints')
    if not client.wait_for_server(timeout_sec=2.0):
        print("Nav2 server not available")
    else:
        print("Nav2 server is running")
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
