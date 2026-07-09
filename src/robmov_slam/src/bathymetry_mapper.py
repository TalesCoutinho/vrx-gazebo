#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Empty
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os

from rclpy.qos import qos_profile_sensor_data
import signal
import sys

class BathymetryMapper(Node):
    def __init__(self):
        super().__init__('bathymetry_mapper')
        
        self.odom_sub = self.create_subscription(
            Odometry,
            '/wamv/odom_filtered',
            self.odom_callback,
            qos_profile_sensor_data)
            
        self.sonar_sub = self.create_subscription(
            LaserScan,
            '/world/bathymetry/model/wamv/link/wamv/base_link/sensor/bathymetry_wamv_sensor/scan',
            self.sonar_callback,
            qos_profile_sensor_data)
            
        self.shutdown_sub = self.create_subscription(
            Empty,
            '/system/shutdown',
            self.shutdown_callback,
            10)
            
        self.current_x = None
        self.current_y = None
        self.current_z = None
        self.pos_uncertainty = 0.0
        
        self.points_x = []
        self.points_y = []
        self.depths = []
        
        self.last_depth = None
        
        # Abre o arquivo de log para gravacao
        self.log_file = open('/home/tales/Source/ROS/robmov/bathymetry_log.txt', 'w')
        # Formato: <profundidade> <incerteza_sonar> <coord_x> <coord_y> <coord_z> <incerteza_posicao>
        
        self.get_logger().info('Bathymetry Mapper Started. Logging to bathymetry_log.txt')

    def odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        self.current_z = msg.pose.pose.position.z
        
        # A covariancia e um array 36 (6x6). Index 0 = Var(X), Index 7 = Var(Y)
        cov = msg.pose.covariance
        var_x = cov[0]
        var_y = cov[7]
        # Incerteza basica estimada pela media das variancias em X e Y
        self.pos_uncertainty = (var_x + var_y) / 2.0

    def sonar_callback(self, msg):
        if self.current_x is not None and self.current_y is not None:
            depth = None
            for r in msg.ranges:
                if not np.isinf(r) and not np.isnan(r) and r > 0.0:
                    depth = r
                    break
            
            if depth is not None:
                # Deteccao de Anomalia (Risco de Encalhe)
                # Se a profundidade diminui rapidamente, o fundo subiu
                if self.last_depth is not None:
                    diff = self.last_depth - depth
                    if diff > 1.5: # Fundo subiu mais de 1.5m de uma vez
                        self.get_logger().error(f'[ALERTA DE ANOMALIA] Risco de encalhe detectado! Posição atual: X={self.current_x:.2f}, Y={self.current_y:.2f}, Profundidade={depth:.2f}m')
                self.last_depth = depth
                
                # Z na perspectiva batimetrica (profundidade negativa ou positiva, dependendo da convencao)
                z = -depth
                sonar_uncertainty = 0.1 # Fixo, conforme especificado
                
                self.points_x.append(self.current_x)
                self.points_y.append(self.current_y)
                self.depths.append(z)
                
                # Formato: <profundidade> <incerteza_sonar> <coord_x> <coord_y> <coord_z> <incerteza_posicao>
                log_line = f"{depth:.4f} {sonar_uncertainty:.4f} {self.current_x:.4f} {self.current_y:.4f} {self.current_z:.4f} {self.pos_uncertainty:.6f}\n"
                self.log_file.write(log_line)
                self.log_file.flush()
                
                # Generate map periodically to survive SIGKILL from run_all.sh
                if len(self.depths) % 50 == 0:
                    self.generate_map()

    def shutdown_callback(self, msg):
        self.get_logger().info('Recebido sinal de encerramento! Finalizando...')
        self.generate_map()
        self.log_file.close()
        # Encerra o ROS
        raise SystemExit

    def generate_map(self):
        self.get_logger().info(f'Generating map with {len(self.depths)} points from log...')
        if len(self.depths) < 2:
            self.get_logger().warning('Not enough points to generate a map.')
            return
            
        x = np.array(self.points_x)
        y = np.array(self.points_y)
        z = np.array(self.depths)
        
        # Create grid
        xi = np.linspace(x.min() - 5, x.max() + 5, 100)
        yi = np.linspace(y.min() - 5, y.max() + 5, 100)
        xi, yi = np.meshgrid(xi, yi)
        
        # Interpolate
        zi = griddata((x, y), z, (xi, yi), method='cubic', fill_value=z.min())
        
        # Plot
        plt.figure(figsize=(10, 8))
        plt.contourf(xi, yi, zi, levels=20, cmap='viridis')
        plt.colorbar(label='Profundidade (Z)')
        
        # Overlay the boat trajectory
        plt.plot(x, y, 'r--', alpha=0.5, label='Trajetória do Barco')
        
        plt.title('Mapa Batimétrico (Relevo Subaquático)')
        plt.xlabel('X (metros)')
        plt.ylabel('Y (metros)')
        plt.legend()
        
        # Save to file
        output_path = '/home/tales/Source/ROS/robmov/bathymetry_map.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.get_logger().info(f'Bathymetric map saved successfully to {output_path} !')

def main(args=None):
    rclpy.init(args=args)
    node = BathymetryMapper()
    
    def signal_handler(sig, frame):
        node.get_logger().info('Encerrando... Gerando mapa batimétrico antes de sair.')
        node.generate_map()
        node.log_file.close()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        rclpy.spin(node)
    except Exception as e:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
