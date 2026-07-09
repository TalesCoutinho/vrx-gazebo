import re

with open('/home/tales/Source/ROS/robmov/vrx/vrx_gz/worlds/bathymetry.sdf', 'r') as f:
    content = f.read()

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

content = content.replace("<!-- Antenna for communication with the WAM-V -->", new_elements + "\n    <!-- Antenna for communication with the WAM-V -->")

with open('/home/tales/Source/ROS/robmov/vrx/vrx_gz/worlds/bathymetry.sdf', 'w') as f:
    f.write(content)
