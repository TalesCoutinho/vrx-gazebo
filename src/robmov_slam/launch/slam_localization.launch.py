import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_dir = get_package_share_directory('robmov_slam')
    ekf_config_path = os.path.join(pkg_dir, 'config', 'ekf_config.yaml')

    # Robot Localization EKF Node
    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config_path, {'use_sim_time': True, 'base_link_frame': 'wamv/wamv/base_link'}],
        remappings=[
            ('odometry/filtered', '/wamv/odom_filtered'),
        ]
    )

    # Navsat Transform Node (Converts GPS to local Odometry)
    navsat_node = Node(
        package='robot_localization',
        executable='navsat_transform_node',
        name='navsat_transform',
        output='screen',
        parameters=[ekf_config_path, {'use_sim_time': True, 'base_link_frame': 'wamv/wamv/base_link'}],
        remappings=[
            ('imu', '/wamv/sensors/imu/imu/data'),
            ('gps/fix', '/wamv/sensors/gps/gps/fix'),
            ('odometry/filtered', '/wamv/odom_filtered')
        ]
    )

    # Twist to Thrust Node
    twist2thrust_node = Node(
        package='robmov_slam',
        executable='twist2thrust.py',
        name='twist2thrust',
        output='screen'
    )

    # ROS-GZ Bridge for Sensors (IMU and GPS)
    ros_gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='sensor_bridge',
        output='screen',
        arguments=[
            '/world/bathymetry/model/wamv/link/wamv/base_link/sensor/imu_wamv_sensor/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
            '/world/bathymetry/model/wamv/link/wamv/base_link/sensor/navsat/navsat@sensor_msgs/msg/NavSatFix[gz.msgs.NavSat'
        ],
        remappings=[
            ('/world/bathymetry/model/wamv/link/wamv/base_link/sensor/imu_wamv_sensor/imu', '/wamv/sensors/imu/imu/data'),
            ('/world/bathymetry/model/wamv/link/wamv/base_link/sensor/navsat/navsat', '/wamv/sensors/gps/gps/fix')
        ]
    )

    # Nav2 Navigation Stack (Planner, Controller, BT Navigator)
    nav2_params_path = os.path.join(pkg_dir, 'config', 'nav2_params.yaml')
    
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_dir, 'launch', 'navigation_launch.py')),
        launch_arguments={'use_sim_time': 'true', 'params_file': nav2_params_path}.items()
    )

    # Static transform publisher to link map -> odom
    static_map_odom_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_map_to_odom',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']
    )

    from launch.actions import TimerAction

    return LaunchDescription([
        ekf_node,
        navsat_node,
        twist2thrust_node,
        ros_gz_bridge_node,
        static_map_odom_tf,
        TimerAction(
            period=10.0,
            actions=[nav2_launch]
        )
    ])

