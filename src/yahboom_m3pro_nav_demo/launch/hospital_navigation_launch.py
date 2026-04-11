import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    RegisterEventHandler,
    IncludeLaunchDescription,
    ExecuteProcess,
    LogInfo,
)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    nav_demo_dir = get_package_share_directory('yahboom_m3pro_nav_demo')
    world_bringup_dir = get_package_share_directory('m3pro_world_bringup')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    map_yaml_file = os.path.join(nav_demo_dir, 'maps', 'hospital_map_v3.yaml')
    nav2_params_file = os.path.join(nav_demo_dir, 'config', 'nav2_smac2d_mppi.yaml')
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

    joint_state_spawner = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'controller_manager', 'spawner', 'joint_state_broadcaster',
            '--controller-manager', '/controller_manager',
            '--controller-manager-timeout', '120',
        ],
        output='screen',
    )

    diff_drive_spawner = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'controller_manager', 'spawner', 'diff_drive_controller',
            '--controller-manager', '/controller_manager',
            '--controller-manager-timeout', '120',
        ],
        output='screen',
    )

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')),
        launch_arguments={
            'map': map_yaml_file,
            'use_sim_time': 'true',
            'params_file': nav2_params_file,
            'autostart': 'true',
            'use_composition': 'False',
        }.items()
    )

    start_diff_drive_after_joint_state = RegisterEventHandler(
        OnProcessExit(
            target_action=joint_state_spawner,
            on_exit=[
                LogInfo(msg='[Nav2 Demo] joint_state_broadcaster 完成，继续检查/加载 diff_drive_controller...'),
                diff_drive_spawner,
            ],
        )
    )

    start_nav2_after_spawners = RegisterEventHandler(
        OnProcessExit(
            target_action=diff_drive_spawner,
            on_exit=[
                LogInfo(msg='[Nav2 Demo] 控制器阶段结束，启动 Nav2...'),
                nav2_launch,
            ],
        )
    )

    return LaunchDescription([
        rviz_arg,
        hospital_env_launch,
        lidar_merger_node,
        ekf_node,
        LogInfo(msg='[Nav2 Demo] 使用 ROS2 spawner 顺序加载控制器，然后启动 Nav2...'),
        joint_state_spawner,
        start_diff_drive_after_joint_state,
        start_nav2_after_spawners,
    ])
