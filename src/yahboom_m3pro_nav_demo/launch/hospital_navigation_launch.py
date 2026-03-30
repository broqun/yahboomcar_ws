import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess, TimerAction, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.actions import SetRemap

def generate_launch_description():
    nav_demo_dir = get_package_share_directory('yahboom_m3pro_nav_demo')
    world_bringup_dir = get_package_share_directory('m3pro_world_bringup')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    map_yaml_file = os.path.join(nav_demo_dir, 'maps', 'hospital_map_v2.yaml')
    nav2_params_file = os.path.join(nav_demo_dir, 'config', 'nav2_navigation.yaml')
    ekf_config_file = os.path.join(nav_demo_dir, 'config', 'ekf.yaml')
    default_rviz = os.path.join(nav_demo_dir, 'rviz', 'nav_demo.rviz')

    rviz_arg = DeclareLaunchArgument(
        'rvizconfig',
        default_value=default_rviz,
        description='Path to RViz config file for Nav2 demo.',
    )

    hospital_env_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(world_bringup_dir, 'launch', 'hospital_world_bringup_launch.py')),
        launch_arguments={
            'keyboard': 'false',
            'rvizconfig': LaunchConfiguration('rvizconfig'),
        }.items()
    )

    lidar_merger_node = Node(
        package='yahboom_m3pro_lidar_tools',
        executable='multi_lidar_merger_node',
        name='multi_lidar_merger',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config_file, {'use_sim_time': True}]
    )

    spawn_controllers_cmd = (
        'ros2 run controller_manager spawner joint_state_broadcaster '
        '&& ros2 run controller_manager spawner diff_drive_controller'
    )
    delayed_spawn_controllers = TimerAction(
        period=10.0,
        actions=[
            LogInfo(msg='[Nav2 Demo] 正在加载底层车轮控制器...'),
            ExecuteProcess(cmd=['bash', '-c', spawn_controllers_cmd], output='screen'),
        ]
    )

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')),
        launch_arguments={
            'map': map_yaml_file,
            'use_sim_time': 'true',
            'params_file': nav2_params_file,
            'autostart': 'true',
        }.items()
    )

    return LaunchDescription([
        rviz_arg,
        SetRemap(src='/cmd_vel', dst='/diff_drive_controller/cmd_vel_unstamped'),
        hospital_env_launch,
        lidar_merger_node,
        ekf_node,
        delayed_spawn_controllers,

        TimerAction(
            period=15.0,
            actions=[
                LogInfo(msg='[Nav2 Demo] 正在唤醒 Nav2 自动驾驶系统...'),
                nav2_launch
            ]
        )
    ])
