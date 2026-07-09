import sys
import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    urdf_path = os.environ.get('URDF_PATH', '/home/tales/Source/ROS/robmov/vrx/vrx_urdf/wamv_gazebo/urdf/wamv_gazebo.urdf')
    with open(urdf_path, 'r') as f:
        robot_desc = f.read()
    
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': True, 'frame_prefix': 'wamv/', 'robot_description': robot_desc}]
        )
    ])
