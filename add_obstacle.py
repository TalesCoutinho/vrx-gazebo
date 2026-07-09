import re

file_path = '/home/tales/Source/ROS/robmov/vrx/vrx_gz/worlds/bathymetry.sdf'

with open(file_path, 'r') as f:
    content = f.read()

# Remove the old comment if it exists to keep it clean
content = content.replace("<!-- Custom Large Estacas for Slalom Navigation -->", "")

obstacle_xml = """
    <!-- Custom Obstacle for Lidar Avoidance -->
    <model name="estaca_central">
      <pose>40 30 0 0 0 0</pose>
      <static>true</static>
      <link name="link">
        <visual name="visual">
          <pose>0 0 2 0 0 0</pose>
          <geometry>
            <cylinder>
              <radius>2.0</radius>
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
              <radius>2.0</radius>
              <length>4.0</length>
            </cylinder>
          </geometry>
        </collision>
      </link>
    </model>
"""

# Insert before the antenna
content = content.replace("<!-- Antenna for communication with the WAM-V -->", obstacle_xml + "\n    <!-- Antenna for communication with the WAM-V -->")

with open(file_path, 'w') as f:
    f.write(content)

print("Obstacle inserted at (40, 30).")
