import os
def get_workspace_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.abspath(__file__))

import re

with open(os.path.join(get_workspace_root(), 'vrx/vrx_gz/worlds/bathymetry.sdf'), 'r') as f:
    content = f.read()

# Define the new large estacas
new_estacas = """
    <!-- Custom Large Estacas for Navigation -->
"""

estaca_coords = [
    (1, -517, 147),
    (2, -517, 177),
    (3, -497, 147),
    (4, -497, 177),
    (5, -477, 147),
    (6, -477, 177),
]

for estaca in estaca_coords:
    new_estacas += f"""
    <model name="estaca_{estaca[0]}">
      <pose>{estaca[1]} {estaca[2]} 0 0 0 0</pose>
      <static>true</static>
      <link name="link">
        <visual name="visual">
          <pose>0 0 2 0 0 0</pose>
          <geometry>
            <cylinder>
              <radius>1.5</radius>
              <length>4.0</length>
            </cylinder>
          </geometry>
          <material>
            <ambient>1 0 0 1</ambient>
            <diffuse>1 0 0 1</diffuse>
          </material>
        </visual>
        <collision name="collision">
          <pose>0 0 2 0 0 0</pose>
          <geometry>
            <cylinder>
              <radius>1.5</radius>
              <length>4.0</length>
            </cylinder>
          </geometry>
        </collision>
      </link>
    </model>
"""

# Remove old slam_post_0 to slam_post_4
pattern = r"<!-- Posts for SLAM/Bathymetry testing -->.*?(?=<!-- Antenna for communication with the WAM-V -->)"
content = re.sub(pattern, new_estacas, content, flags=re.DOTALL)

with open(os.path.join(get_workspace_root(), 'vrx/vrx_gz/worlds/bathymetry.sdf'), 'w') as f:
    f.write(content)

