"""
一键启动：Gazebo 医院场景 + M3Pro 机器人 + 键盘遥操作 + SLAM 建图 + ros2_control 控制器。

等效于按顺序执行：
  1. ros2 launch yahboom_m3pro_slam_demo hospital_m3pro_teleop_launch.py
  2. ros2 launch yahboom_m3pro_slam_demo lidar_slam_launch.py
  3. (约 10s 后) ros2 run controller_manager spawner joint_state_broadcaster
  4. ros2 run controller_manager spawner diff_drive_controller

启动后可用键盘控制机器人在医院中行走并建图。
"""

from pathlib import Path

from ament_index_python.packages import get_package_share_path
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


def get_launch_path(package_name: str, launch_subpath: str) -> Path:
    """Return absolute path to a launch file in the given package."""
    pkg_share = get_package_share_path(package_name)
    return Path(pkg_share) / 'launch' / launch_subpath


def generate_launch_description():
    slam_pkg = 'yahboom_m3pro_slam_demo'
    world_pkg = 'm3pro_world_bringup'
    slam_share = get_package_share_path(slam_pkg)
    default_rviz = slam_share / 'rviz' / 'spen_m3pro_lidar_slam.rviz'

    rviz_arg = DeclareLaunchArgument(
        'rvizconfig',
        default_value=str(default_rviz),
        description='Path to RViz config file for SLAM demo.',
    )

    # 1. 医院场景 + Gazebo + 生成 M3Pro + RViz + 键盘遥操作
    hospital_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([str(get_launch_path(world_pkg, 'hospital_world_bringup_launch.py'))]),
        launch_arguments={
            'rvizconfig': LaunchConfiguration('rvizconfig'),
        }.items(),
    )

    # 2. 双雷达合并 + SLAM Toolbox
    lidar_slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([str(get_launch_path(slam_pkg, 'lidar_slam_launch.py'))]),
    )

    # 3. 在 Gazebo 和机器人生成后，加载 ros2_control 控制器（顺序执行）
    #    先 joint_state_broadcaster，再 diff_drive_controller，才能用键盘控制
    spawn_controllers_cmd = (
        'ros2 run controller_manager spawner joint_state_broadcaster '
        '&& ros2 run controller_manager spawner diff_drive_controller'
    )
    delayed_spawn_controllers = TimerAction(
        period=10.0,
        actions=[
            LogInfo(msg='[Gazebo Hospital SLAM Demo] 正在加载 joint_state_broadcaster 与 diff_drive_controller ...'),
            ExecuteProcess(
                cmd=['bash', '-c', spawn_controllers_cmd],
                output='screen',
            ),
        ],
    )

    return LaunchDescription([
        rviz_arg,
        hospital_launch,
        lidar_slam_launch,
        delayed_spawn_controllers,
    ])
