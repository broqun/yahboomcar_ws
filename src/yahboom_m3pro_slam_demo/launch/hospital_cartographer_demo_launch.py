"""
One-click demo: Gazebo hospital world + M3Pro + keyboard teleop + Cartographer mapping.

Sequence:
  1) Include hospital_world_bringup_launch.py
  2) Feed Cartographer directly with /scan_front and /scan_rear
  3) Start cartographer_node + occupancy grid publishing
  4) Delay-load ros2_control controllers for driving
"""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory, get_package_share_path
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    LogInfo,
    TimerAction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def get_launch_path(package_name: str, launch_subpath: str) -> Path:
    pkg_share = get_package_share_path(package_name)
    return Path(pkg_share) / 'launch' / launch_subpath


def generate_launch_description():
    slam_pkg = 'yahboom_m3pro_slam_demo'
    world_pkg = 'm3pro_world_bringup'
    slam_share = get_package_share_path(slam_pkg)
    ekf_config_path = (
        Path(get_package_share_directory(slam_pkg)) / 'config' / 'ekf.yaml'
    )
    default_rviz = slam_share / 'rviz' / 'spen_m3pro_lidar_slam.rviz'
    config_dir = slam_share / 'config'

    rviz_arg = DeclareLaunchArgument(
        'rvizconfig',
        default_value=str(default_rviz),
        description='Path to RViz config file.',
    )
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time for all SLAM nodes.',
    )
    resolution_arg = DeclareLaunchArgument(
        'resolution',
        default_value='0.05',
        description='Occupancy grid resolution (meters).',
    )
    publish_period_arg = DeclareLaunchArgument(
        'publish_period_sec',
        default_value='1.0',
        description='Occupancy grid publish period in seconds.',
    )

    hospital_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [str(get_launch_path(world_pkg, 'hospital_world_bringup_launch.py'))]
        ),
        launch_arguments={
            'rvizconfig': LaunchConfiguration('rvizconfig'),
        }.items(),
    )

    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        output='screen',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        arguments=[
            '-configuration_directory',
            str(config_dir),
            '-configuration_basename',
            'cartographer_m3pro_2d.lua',
        ],
        remappings=[
            ('scan_1', '/scan_front'),
            ('scan_2', '/scan_rear'),
            ('imu', '/imu/data'),
            ('odom', '/odometry/filtered'),
        ],
    )

    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[str(ekf_config_path), {'use_sim_time': LaunchConfiguration('use_sim_time')}],
    )

    occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        name='cartographer_occupancy_grid_node',
        output='screen',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        arguments=[
            '-resolution',
            LaunchConfiguration('resolution'),
            '-publish_period_sec',
            LaunchConfiguration('publish_period_sec'),
        ],
    )

    spawn_controllers_cmd = (
        'ros2 run controller_manager spawner joint_state_broadcaster '
        '&& ros2 run controller_manager spawner diff_drive_controller'
    )
    delayed_spawn_controllers = TimerAction(
        period=10.0,
        actions=[
            LogInfo(
                msg=(
                    '[Gazebo Hospital Cartographer Demo] '
                    'Loading joint_state_broadcaster and diff_drive_controller ...'
                )
            ),
            ExecuteProcess(
                cmd=['bash', '-c', spawn_controllers_cmd],
                output='screen',
            ),
        ],
    )

    return LaunchDescription([
        rviz_arg,
        use_sim_time_arg,
        resolution_arg,
        publish_period_arg,
        hospital_launch,
        ekf_node,
        cartographer_node,
        occupancy_grid_node,
        delayed_spawn_controllers,
    ])
