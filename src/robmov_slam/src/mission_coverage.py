#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Empty
import math
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from transforms3d.euler import euler2quat
from visualization_msgs.msg import Marker, MarkerArray
from rclpy.qos import QoSProfile, DurabilityPolicy

class CoverageMission(Node):
    def __init__(self):
        super().__init__('coverage_mission')
        self.abort_requested = False
        
        qos_profile = QoSProfile(depth=10, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.marker_pub = self.create_publisher(MarkerArray, 'waypoints_markers', qos_profile)

        self.shutdown_sub = self.create_subscription(
            Empty,
            '/system/shutdown',
            self.shutdown_callback,
            10)

        # Waypoints for slalom course
        self.waypoints = [
            [60.0, 10.0],
            [60.0, 20.0],
            [20.0, 20.0],
            [20.0, 30.0],
            [60.0, 30.0],
            [60.0, 40.0],
            [20.0, 40.0],
            [20.0, 50.0],
            [60.0, 50.0]
        ]

    def shutdown_callback(self, msg):
        self.get_logger().warn('Sinal de parada recebido! Abortando a missão...')
        self.abort_requested = True

    def publish_markers(self, clock):
        marker_array = MarkerArray()
        for i, (x, y) in enumerate(self.waypoints):
            marker = Marker()
            marker.header.frame_id = 'odom'
            marker.header.stamp = clock.now().to_msg()
            marker.ns = 'waypoints'
            marker.id = i
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD
            marker.pose.position.x = float(x)
            marker.pose.position.y = float(y)
            marker.pose.position.z = 2.0
            marker.pose.orientation.w = 1.0
            marker.scale.x = 0.8
            marker.scale.y = 0.8
            marker.scale.z = 0.8
            marker.color.a = 0.8
            fraction = i / (len(self.waypoints) - 1)
            marker.color.r = float(fraction)
            marker.color.g = float(1.0 - fraction)
            marker.color.b = 0.0
            marker_array.markers.append(marker)
        self.marker_pub.publish(marker_array)

def main(args=None):
    rclpy.init(args=args)
    node = CoverageMission()

    navigator = BasicNavigator()

    node.get_logger().info('Aguardando inicializacao completa do Nav2...')
    navigator.waitUntilNav2Active(localizer="robot_localization")
    node.get_logger().info('Nav2 inicializado e pronto!')

    # Publish markers
    node.publish_markers(navigator.get_clock())

    poses = []
    
    # Generate poses with correct heading towards the next waypoint
    for i in range(len(node.waypoints)):
        x, y = node.waypoints[i]
        
        # Calculate yaw to look at the next waypoint (or keep same if last)
        if i < len(node.waypoints) - 1:
            nx, ny = node.waypoints[i+1]
            yaw = math.atan2(ny - y, nx - x)
        else:
            yaw = 0.0

        pose = PoseStamped()
        pose.header.frame_id = 'odom'
        pose.header.stamp = navigator.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0
        
        q = euler2quat(0, 0, yaw) # returns [w, x, y, z]
        pose.pose.orientation.w = q[0]
        pose.pose.orientation.x = q[1]
        pose.pose.orientation.y = q[2]
        pose.pose.orientation.z = q[3]
        
        poses.append(pose)

    node.get_logger().info(f'Enviando {len(poses)} waypoints para o Nav2...')
    navigator.followWaypoints(poses)

    while not navigator.isTaskComplete():
        rclpy.spin_once(node, timeout_sec=0.1)
        if node.abort_requested:
            node.get_logger().warn('Cancelando waypoints no Nav2...')
            navigator.cancelTask()
            break

        feedback = navigator.getFeedback()
        if feedback:
            node.get_logger().info(f'Navegando para o waypoint {feedback.current_waypoint}...', throttle_duration_sec=2.0)

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        node.get_logger().info('Missao finalizada com sucesso!')
    elif result == TaskResult.CANCELED:
        node.get_logger().info('Missao cancelada.')
    elif result == TaskResult.FAILED:
        node.get_logger().error('Falha na missao.')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
