#!/bin/bash
trap "echo 'Encerrando processos...'; pkill -P $$; exit" SIGINT SIGTERM EXIT
source /home/tales/Source/ROS/robmov/install/setup.bash
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:/home/tales/Source/ROS/robmov/vrx/vrx_urdf:/home/tales/Source/ROS/robmov/vrx/vrx_gz/models

# Kill old processes to prevent conflicts
echo "Limpando processos antigos do ROS e Gazebo..."
pkill -9 -f "gz\|gazebo\|rviz2\|ros2\|ruby\|mission_coverage" || true
sleep 25

# Garantir que a pasta de logs existe
mkdir -p /home/tales/Source/ROS/robmov/log


echo "Pré-processando o URDF do WAM-V para converter juntas contínuas/revolutas em fixas (evitar time jump no TF)..."
export URDF_PATH=/tmp/wamv_fixed.urdf.xacro
xacro /home/tales/Source/ROS/robmov/vrx/vrx_urdf/wamv_gazebo/urdf/wamv_gazebo.urdf.xacro namespace:=wamv locked:=true vrx_sensors_enabled:=false gps_enabled:=true imu_enabled:=true lidar_enabled:=true bathymetry_enabled:=true thruster_config:=H > $URDF_PATH
sed -i 's/type="revolute"/type="fixed"/g' $URDF_PATH
sed -i 's/type="continuous"/type="fixed"/g' $URDF_PATH
sed -i 's/<joint name="wamv\/left_chassis_engine_joint" type="fixed">/<joint name="wamv\/left_chassis_engine_joint" type="revolute">/g' $URDF_PATH
sed -i 's/<joint name="wamv\/right_chassis_engine_joint" type="fixed">/<joint name="wamv\/right_chassis_engine_joint" type="revolute">/g' $URDF_PATH
sed -i 's/<joint name="wamv\/left_engine_propeller_joint" type="fixed">/<joint name="wamv\/left_engine_propeller_joint" type="continuous">/g' $URDF_PATH
sed -i 's/<joint name="wamv\/right_engine_propeller_joint" type="fixed">/<joint name="wamv\/right_engine_propeller_joint" type="continuous">/g' $URDF_PATH
# Forcing Gazebo to use the dedicated NVIDIA GPU (RTX 2050) instead of the integrated graphics
export __NV_PRIME_RENDER_OFFLOAD=1
export __GLX_VENDOR_LIBRARY_NAME=nvidia
export __VK_LAYER_NV_optimus=NVIDIA_only
export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json

ros2 launch vrx_gz competition.launch.py headless:=true world:=bathymetry urdf:=$URDF_PATH vrx_sensors_enabled:=false gps_enabled:=true imu_enabled:=true lidar_enabled:=true bathymetry_enabled:=true > /home/tales/Source/ROS/robmov/gazebo_log.txt 2>&1 &
SIM_PID=$!
echo "Aguardando 35 segundos para o Gazebo carregar minimamente..."
sleep 35

echo "Coletando árvore de TFs..."
ros2 run tf2_tools view_frames -o /home/tales/Source/ROS/robmov/tf_tree

echo "Iniciando SLAM e Navegação..."
# Fix Gazebo lumped frame_id mismatches by connecting them to the URDF links
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 wamv/wamv/imu_wamv_link "wamv/wamv/base_link/imu_wamv_sensor" --ros-args -p use_sim_time:=true &
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 wamv/wamv/gps_wamv_link "wamv/wamv/base_link/navsat" --ros-args -p use_sim_time:=true &
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 wamv/wamv/lidar_wamv_link "wamv/wamv/base_link/lidar_wamv_sensor" --ros-args -p use_sim_time:=true &
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 wamv/wamv/bathymetry_wamv_link "wamv/wamv/base_link/bathymetry_wamv_sensor" --ros-args -p use_sim_time:=true &

# Lança Fake Lidar para alimentar o SLAM Toolbox já que o Lidar real não funciona no Gazebo sem quebrar
# python3 /home/tales/Source/ROS/robmov/fake_lidar.py &

ros2 launch robmov_slam slam_localization.launch.py > /home/tales/Source/ROS/robmov/log/slam_log.txt 2>&1 &
SLAM_PID=$!
sleep 25

echo "Testando sensores (salvando em sensors_log.txt)..."
ros2 topic hz /wamv/sensors/imu/imu/data --window 5 > /home/tales/Source/ROS/robmov/log/sensors_log.txt 2>&1 &
ros2 topic hz /wamv/sensors/gps/gps/fix --window 5 >> /home/tales/Source/ROS/robmov/log/sensors_log.txt 2>&1 &
ros2 topic hz /wamv/sensors/lidars/lidar_wamv_sensor/scan --window 5 >> /home/tales/Source/ROS/robmov/log/sensors_log.txt 2>&1 &

echo "Iniciando RViz para acompanhamento da Navegação..."
#rviz2 -d /opt/ros/jazzy/share/nav2_bringup/rviz/nav2_default_view.rviz > /home/tales/Source/ROS/robmov/log/rviz_log.txt 2>&1 &
RVIZ_PID=$!

echo "Iniciando Coletor de Batimetria com Log e Anomalia..."
ros2 run robmov_slam software_bathymetry.py > /home/tales/Source/ROS/robmov/log/software_bathy.log 2>&1 &
MOCK_PID=$!
ros2 run robmov_slam bathymetry_mapper.py > /home/tales/Source/ROS/robmov/log/bathymetry_syslog.txt 2>&1 &
BATHY_PID=$!
sleep 25

echo "Iniciando Listener do Teclado em background..."
# Roda em background, mas ainda le do terminal
ros2 run robmov_slam keyboard_listener.py &
KEYBOARD_PID=$!

echo "Iniciando Missão Zigue-Zague..."
# Roda em foreground, bloqueando o script bash ate terminar ou ser cancelada
python3 -u /home/tales/Source/ROS/robmov/tracker.py > /home/tales/Source/ROS/robmov/log/tracker_log.txt 2>&1 &
ros2 run robmov_slam mission_coverage.py

echo "Processo finalizado com sucesso."
sleep infinity

