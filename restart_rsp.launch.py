import os
def get_workspace_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.abspath(__file__))

import sys
import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    urdf_path = os.environ.get('URDF_PATH', os.path.join(get_workspace_root(), 'vrx/vrx_urdf/wamv_gazebo/urdf/wamv_gazebo.urdf'))
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
