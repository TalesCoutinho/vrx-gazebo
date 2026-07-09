import os
def get_workspace_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(get_workspace_root(), 'vrx/vrx_gz/worlds/bathymetry.sdf'), 'r') as f:
    content = f.read()

waypoints = [
    ("wp_1", -522, 182),
    ("wp_2", -442, 182),
    ("wp_3", -442, 202),
    ("wp_4", -522, 202),
    ("wp_5", -522, 222),
    ("wp_6", -442, 222),
    ("wp_7", -442, 242),
    ("wp_8", -522, 242),
    ("wp_9", -522, 262),
    ("wp_10", -442, 262),
]

new_elements = ""
for name, ex, ey in waypoints:
    new_elements += f"""    <model name="{name}">
      <pose>{ex} {ey} 4.0 0 0 0</pose>
      <static>true</static>
      <link name="link">
        <visual name="visual">
          <geometry>
            <sphere>
              <radius>1.5</radius>
            </sphere>
          </geometry>
          <material>
            <ambient>0 1 0 1</ambient>
            <diffuse>0 1 0 1</diffuse>
          </material>
        </visual>
      </link>
    </model>
"""

content = content.replace("<!-- Antenna for communication with the WAM-V -->", new_elements + "    <!-- Antenna for communication with the WAM-V -->")

with open(os.path.join(get_workspace_root(), 'vrx/vrx_gz/worlds/bathymetry.sdf'), 'w') as f:
    f.write(content)

