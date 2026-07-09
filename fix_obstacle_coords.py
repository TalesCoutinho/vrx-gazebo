import re

file_paths = [
    '/home/tales/Source/ROS/robmov/vrx/vrx_gz/worlds/bathymetry.sdf',
    '/home/tales/Source/ROS/robmov/install/vrx_gz/share/vrx_gz/worlds/bathymetry.sdf'
]

for path in file_paths:
    with open(path, 'r') as f:
        content = f.read()

    # Substitui 40 40 por -492 202 na pose da estaca
    content = re.sub(r'<pose>40 40 0 0 0 0</pose>', '<pose>-492 202 0 0 0 0</pose>', content)
    
    with open(path, 'w') as f:
        f.write(content)

print("Obstacle coordinates fixed.")
