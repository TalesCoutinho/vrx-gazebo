import os
def get_workspace_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.abspath(__file__))

#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Simulating the ZigZag mission path
waypoints = [
    [-525.0, 150.0],
    [-525.0, 185.0],
    [-515.0, 185.0],
    [-515.0, 150.0],
    [-505.0, 150.0],
    [-505.0, 185.0],
    [-495.0, 185.0],
    [-495.0, 150.0]
]

points_x = []
points_y = []
depths = []

# Interpolate points along the path
for i in range(len(waypoints) - 1):
    start = np.array(waypoints[i])
    end = np.array(waypoints[i+1])
    dist = np.linalg.norm(end - start)
    num_points = int(dist * 2) # 2 points per meter
    
    xs = np.linspace(start[0], end[0], num_points)
    ys = np.linspace(start[1], end[1], num_points)
    
    for x, y in zip(xs, ys):
        points_x.append(x)
        points_y.append(y)
        
        # Simulating bathymetry: deeper in the middle, some random noise
        # Base depth around -10 meters, plus some hills and noise
        z = -10.0 + np.sin(x/5.0)*2.0 + np.cos(y/5.0)*3.0 + np.random.normal(0, 0.2)
        depths.append(z)

points_x = np.array(points_x)
points_y = np.array(points_y)
depths = np.array(depths)

# Create grid
xi = np.linspace(points_x.min() - 5, points_x.max() + 5, 200)
yi = np.linspace(points_y.min() - 5, points_y.max() + 5, 200)
xi, yi = np.meshgrid(xi, yi)

# Interpolate
zi = griddata((points_x, points_y), depths, (xi, yi), method='cubic', fill_value=depths.min())

# Plot
plt.figure(figsize=(10, 8))
# Create filled contours
contour = plt.contourf(xi, yi, zi, levels=30, cmap='ocean')
plt.colorbar(contour, label='Profundidade (Z em metros)')

# Plot the simulated boat trajectory
plt.plot(points_x, points_y, 'r--', alpha=0.3, label='Trajetória Autônoma do Barco')
plt.scatter(points_x[::20], points_y[::20], color='red', s=5, alpha=0.5) # Some markers

# Mark the posts
posts = [
    [-520, 170],
    [-510, 175],
    [-505, 165],
    [-515, 160],
    [-525, 180]
]
for px, py in posts:
    plt.plot(px, py, 'y^', markersize=10, markeredgecolor='black', label='Estaca (Obstáculo)' if px == -520 else "")

plt.title('Mapa Batimétrico (Simulação Sintética)')
plt.xlabel('Coordenada X (metros)')
plt.ylabel('Coordenada Y (metros)')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)

output_path = os.path.join(get_workspace_root(), 'bathymetry_map.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f'Mapa gerado com sucesso em {output_path}')
