import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    ExecuteProcess,
    LogInfo,
    RegisterEventHandler,
    TimerAction,
)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    nav_demo_dir = get_package_share_directory('yahboom_m3pro_nav_demo')
    world_bringup_dir = get_package_share_directory('m3pro_world_bringup')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    map_yaml_file = os.path.join(nav_demo_dir, 'maps', 'hospital_map_v2.yaml')
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

    spawn_controllers_cmd = (
        'ros2 run controller_manager spawner joint_state_broadcaster '
        '&& ros2 run controller_manager spawner diff_drive_controller'
    )
    spawn_controllers_process = ExecuteProcess(
        cmd=['bash', '-c', spawn_controllers_cmd],
        output='screen',
    )
    delayed_spawn_controllers = TimerAction(
        period=10.0,
        actions=[
            LogInfo(msg='[Nav2 Demo] 正在加载底层车轮控制器...'),
            spawn_controllers_process,
        ],
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

    # 必须在 joint_state_broadcaster + diff_drive_controller 加载完成（bash 退出）后再起 Nav2。
    # 若用固定 15s 定时器，Gazebo/插件较慢时会出现 odom 尚未发布、Nav2 已激活，导致 TF 与 progress 异常。
    start_nav2_after_controllers = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_controllers_process,
            on_exit=[
                LogInfo(msg='[Nav2 Demo] 正在唤醒 Nav2 自动驾驶系统...'),
                nav2_launch,
            ],
        )
    )

    return LaunchDescription([
        rviz_arg,
        hospital_env_launch,
        lidar_merger_node,
        ekf_node,
        delayed_spawn_controllers,
        start_nav2_after_controllers,
    ])
