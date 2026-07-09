sed -i 's/<max>130<\/max>/<max>40<\/max>/g' /home/tales/Source/ROS/robmov/vrx/vrx_urdf/wamv_gazebo/urdf/components/wamv_3d_lidar.xacro
colcon build --packages-select wamv_gazebo vrx_gz
