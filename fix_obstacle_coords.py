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

for path in file_paths:
    with open(path, 'r') as f:
        content = f.read()

    # Substitui 40 40 por -492 202 na pose da estaca
    content = re.sub(r'<pose>40 40 0 0 0 0</pose>', '<pose>-492 202 0 0 0 0</pose>', content)
    
    with open(path, 'w') as f:
        f.write(content)

print("Obstacle coordinates fixed.")
