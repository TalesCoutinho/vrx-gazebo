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

# Define the new large estacas for slalom
new_elements = """
    <!-- Custom Large Estacas for Slalom Navigation -->
"""

estaca_coords = [
    (1, -512, 182),
    (2, -492, 202),
    (3, -472, 222),
    (4, -452, 242),
    (5, -432, 262),
    (6, -412, 282),
    (7, -392, 302),
    (8, -372, 322),
    (9, -352, 342),
    (10, -332, 362),
]

for estaca in estaca_coords:
    new_elements += f"""
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

new_elements += """
    <!-- Visual Markers for Waypoints -->
"""

waypoint_coords = [
    (2, -510.5, 200.5),
    (3, -473.5, 203.5),
    (4, -470.5, 240.5),
    (5, -433.5, 243.5),
    (6, -430.5, 280.5),
    (7, -393.5, 283.5),
    (8, -390.5, 320.5),
    (9, -353.5, 323.5),
    (10, -350.5, 360.5),
    (11, -312.0, 382.0),
]

for wp in waypoint_coords:
    new_elements += f"""
    <model name="waypoint_marker_{wp[0]}">
      <pose>{wp[1]} {wp[2]} 1.5 0 0 0</pose>
      <static>true</static>
      <link name="link">
        <visual name="visual">
          <geometry>
            <sphere>
              <radius>1.0</radius>
            </sphere>
          </geometry>
          <material>
            <ambient>0 1 0 1</ambient>
            <diffuse>0 1 0 1</diffuse>
            <emissive>0 1 0 1</emissive>
          </material>
        </visual>
      </link>
    </model>
"""

# Remove old estacas
pattern = r"<!-- Custom Large Estacas for Navigation -->.*?(?=<!-- Antenna for communication with the WAM-V -->)|<!-- Custom Large Estacas for Slalom Navigation -->.*?(?=<!-- Antenna for communication with the WAM-V -->)"
content = re.sub(pattern, new_elements, content, flags=re.DOTALL)

with open(os.path.join(get_workspace_root(), 'vrx/vrx_gz/worlds/bathymetry.sdf'), 'w') as f:
    f.write(content)
