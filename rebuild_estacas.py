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

pattern_old_estacas = r"<model name=\"estaca_[ABC]\">[\s\S]*?</model>"
content = re.sub(pattern_old_estacas, "", content)

new_estacas = [
    ("estaca_A", -502, 197),
    ("estaca_B", -482, 227),
    ("estaca_C", -462, 247),
]

new_elements = ""
for name, ex, ey in new_estacas:
    new_elements += f"""    <model name="{name}">
      <pose>{ex} {ey} 0 0 0 0</pose>
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
            <ambient>1 0.5 0 1</ambient>
            <diffuse>1 0.5 0 1</diffuse>
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

content = content.replace("<!-- Antenna for communication with the WAM-V -->", new_elements + "    <!-- Antenna for communication with the WAM-V -->")

with open(os.path.join(get_workspace_root(), 'vrx/vrx_gz/worlds/bathymetry.sdf'), 'w') as f:
    f.write(content)

