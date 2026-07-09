
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
sed -i '/global_frame: map/a \      rolling_window: true\n      width: 300\n      height: 300' "$WORKSPACE_DIR"/src/robmov_slam/config/nav2_params.yaml
colcon build --packages-select robmov_slam
