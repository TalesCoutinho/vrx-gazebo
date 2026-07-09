import re

file_paths = [
    '/home/tales/Source/ROS/robmov/vrx/vrx_gz/worlds/bathymetry.sdf',
    '/home/tales/Source/ROS/robmov/install/vrx_gz/share/vrx_gz/worlds/bathymetry.sdf'
]

obstacle_xml = """    <model name="estaca_desafio">
      <pose>40 40 0 0 0 0</pose>
      <static>true</static>
      <link name="link">
        <visual name="visual">
          <pose>0 0 2 0 0 0</pose>
          <geometry>
            <cylinder>
              <radius>2.0</radius>
              <length>8.0</length>
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
              <radius>2.0</radius>
              <length>8.0</length>
            </cylinder>
          </geometry>
        </collision>
      </link>
    </model>
"""

for path in file_paths:
    with open(path, 'r') as f:
        content = f.read()

    # Remove any old estacas
    content = re.sub(r'<!-- Custom Obstacle for Lidar Avoidance -->.*?estaca_central.*?</model>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- Custom Obstacle for Lidar Avoidance -->.*?estaca_gigante.*?</model>', '', content, flags=re.DOTALL)
    content = re.sub(r'<model name="estaca_desafio">.*?</model>', '', content, flags=re.DOTALL)

    content = content.replace("<!-- Antenna for communication with the WAM-V -->", obstacle_xml + "    <!-- Antenna for communication with the WAM-V -->")

    with open(path, 'w') as f:
        f.write(content)

print("Obstacle fixed.")
