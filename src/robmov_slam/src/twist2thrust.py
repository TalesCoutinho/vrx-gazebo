#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

class Twist2Thrust(Node):
    def __init__(self):
        super().__init__('twist2thrust')
        
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.left_pub = self.create_publisher(Float64, '/wamv/thrusters/left/thrust', 10)
        self.right_pub = self.create_publisher(Float64, '/wamv/thrusters/right/thrust', 10)
        
        # Parâmetro para ganho angular (ajuste de quão rápido o barco gira)
        self.declare_parameter('angular_gain', 5000.0)
        self.declare_parameter('linear_gain', 5000.0)

    def listener_callback(self, msg):
        angular_gain = self.get_parameter('angular_gain').value
        linear_gain = self.get_parameter('linear_gain').value
        
        v = msg.linear.x * linear_gain
        w = msg.angular.z * angular_gain
        
        left = Float64()
        right = Float64()
        
        # Cinemática Diferencial Básica
        # Girar à esquerda (w > 0) -> Motor direito acelera, esquerdo desacelera/recua
        left.data = v - w
        right.data = v + w
        
        # Os comandos de thrust do VRX não são velocidades exatas, mas sim
        # "ordens" ou rad/s da hélice (em algumas simulações vai de -X a X).
        # Para navegação segura, podemos limitar (clipping) a magnitude para evitar capotar o barco
        max_thrust = 5000.0  # Ajuste dependendo do plugin do VRX (às vezes é força em Newtons)
        left.data = max(-max_thrust, min(max_thrust, left.data))
        right.data = max(-max_thrust, min(max_thrust, right.data))

        self.get_logger().info(f"v: {v:.2f}, w: {w:.2f} -> L_thrust: {left.data:.2f}, R_thrust: {right.data:.2f}")

        self.left_pub.publish(left)
        self.right_pub.publish(right)

def main(args=None):
    rclpy.init(args=args)
    node = Twist2Thrust()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
