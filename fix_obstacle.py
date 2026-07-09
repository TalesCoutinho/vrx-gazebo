import os
def get_workspace_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.abspath(__file__))

import re

file_paths = [
    os.path.join(get_workspace_root(), 'vrx/vrx_gz/worlds/bathymetry.sdf'),
    os.path.join(get_workspace_root(), 'install/vrx_gz/share/vrx_gz/worlds/bathymetry.sdf')
]

obstacle_xml = """
    <!-- Custom Obstacle for Lidar Avoidance -->
    <model name="estaca_gigante">
      <pose>40 40 5 0 0 0</pose>
      <static>true</static>
      <link name="link">
        <visual name="visual">
          <pose>0 0 10 0 0 0</pose>
          <geometry>
            <cylinder>
              <radius>3.0</radius>
              <length>20.0</length>
            </cylinder>
          </geometry>
          <material>
            <ambient>1 0 0 1</ambient>
            <diffuse>1 0 0 1</diffuse>
            <specular>0.1 0.1 0.1 1</specular>
          </material>
        </visual>
        <collision name="collision">
          <pose>0 0 10 0 0 0</pose>
          <geometry>
            <cylinder>
              <radius>3.0</radius>
              <length>20.0</length>
            </cylinder>
          </geometry>
        </collision>
      </link>
    </model>
"""

for path in file_paths:
    with open(path, 'r') as f:
        content = f.read()

    # Remove the old estaca_central if it exists
    content = re.sub(r'<!-- Custom Obstacle for Lidar Avoidance -->.*?estaca_central.*?</model>', '', content, flags=re.DOTALL)
    
    # Also remove any estaca_gigante if it exists
    content = re.sub(r'<!-- Custom Obstacle for Lidar Avoidance -->.*?estaca_gigante.*?</model>', '', content, flags=re.DOTALL)

    # Insert before the antenna
    content = content.replace("<!-- Antenna for communication with the WAM-V -->", obstacle_xml + "\n    <!-- Antenna for communication with the WAM-V -->")

    with open(path, 'w') as f:
        f.write(content)

print("Giant Obstacle inserted.")
