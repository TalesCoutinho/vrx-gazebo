
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
sed -i '/max_obstacle_height: 2.0/a \          min_obstacle_height: 0.5' "$WORKSPACE_DIR"/src/robmov_slam/config/nav2_params.yaml
colcon build --packages-select robmov_slam
