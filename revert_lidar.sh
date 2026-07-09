
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
sed -i 's/<max>130<\/max>/<max>40<\/max>/g' "$WORKSPACE_DIR"/vrx/vrx_urdf/wamv_gazebo/urdf/components/wamv_3d_lidar.xacro
colcon build --packages-select wamv_gazebo vrx_gz
