import re

with open('/home/tales/Source/ROS/robmov/vrx/vrx_gz/worlds/bathymetry.sdf', 'r') as f:
    content = f.read()

# Apagar as esferas antigas (wp_1 até wp_10)
pattern_old_wps = r"<model name=\"wp_[0-9]+\">[\s\S]*?</model>"
content = re.sub(pattern_old_wps, "", content)

waypoints = [
    ("wp_2", -472, 172),  # X=60, Y=10
    ("wp_3", -472, 182),  # X=60, Y=20
    ("wp_4", -512, 182),  # X=20, Y=20
    ("wp_5", -512, 192),  # X=20, Y=30
    ("wp_6", -472, 192),  # X=60, Y=30
    ("wp_7", -472, 202),  # X=60, Y=40
    ("wp_8", -512, 202),  # X=20, Y=40
    ("wp_9", -512, 212),  # X=20, Y=50
    ("wp_10", -472, 212)  # X=60, Y=50
]

new_elements = ""
for i, (name, ex, ey) in enumerate(waypoints):
    # Progressão de Verde (0, 1, 0) para Vermelho (1, 0, 0)
    fraction = i / (len(waypoints) - 1)
    r = fraction
    g = 1.0 - fraction
    b = 0.0
    
    new_elements += f"""    <model name="{name}">
      <pose>{ex} {ey} 4.0 0 0 0</pose>
      <static>true</static>
      <link name="link">
        <visual name="visual">
          <geometry>
            <sphere>
              <radius>0.8</radius>
            </sphere>
          </geometry>
          <material>
            <ambient>{r:.2f} {g:.2f} {b:.2f} 1</ambient>
            <diffuse>{r:.2f} {g:.2f} {b:.2f} 1</diffuse>
          </material>
        </visual>
      </link>
    </model>
"""

content = content.replace("<!-- Antenna for communication with the WAM-V -->", new_elements + "    <!-- Antenna for communication with the WAM-V -->")

with open('/home/tales/Source/ROS/robmov/vrx/vrx_gz/worlds/bathymetry.sdf', 'w') as f:
    f.write(content)

