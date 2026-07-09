import os
def get_workspace_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.abspath(__file__))

import yaml

with open(os.path.join(get_workspace_root(), 'src/robmov_slam/config/nav2_params.yaml'), 'r') as f:
    content = f.read()

content = content.replace('base_link', 'wamv/base_link')
content = content.replace('robot_radius: 0.22', 'footprint: "[ [2.5, 1.2], [2.5, -1.2], [-2.5, -1.2], [-2.5, 1.2] ]"')
content = content.replace('topic: /scan', 'topic: /wamv/sensors/lidars/lidar_wamv_sensor/scan')
content = content.replace('raytrace_max_range: 3.0', 'raytrace_max_range: 30.0')
content = content.replace('obstacle_max_range: 2.5', 'obstacle_max_range: 30.0')

with open(os.path.join(get_workspace_root(), 'src/robmov_slam/config/nav2_params.yaml'), 'w') as f:
    f.write(content)
