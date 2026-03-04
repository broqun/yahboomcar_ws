"""
建图 launch：深度图转激光 + Cartographer 2D SLAM（与 depth_slam_launch 功能类似，使用 Cartographer 替代 SLAM Toolbox）.

与 hospital_m3pro_teleop_launch.py 配合使用：
  终端1: ros2 launch yahboom_M3Pro_description hospital_m3pro_teleop_launch.py
  终端2: ros2 launch yahboom_M3Pro_description depth_cartographer_launch.py

话题与 depth_slam_launch 一致：
  - 输入: /dabai_dcw2/depth/image_raw, /dabai_dcw2/depth/camera_info
  - 输出: /scan（虚拟激光）, /map（Cartographer 占据栅格）
  - 坐标系: map -> odom -> base_footprint
"""

from pathlib import Path

from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch_ros.actions import Node


def get_config_dir():
    """Get Cartographer config directory (works from source and install)."""
    try:
        pkg_share = get_package_share_path('yahboom_M3Pro_description')
        config_dir = Path(pkg_share) / 'config'
        if config_dir.exists():
            return str(config_dir)
    except Exception:
        pass
    # Fallback: relative to this launch file (source layout)
    launch_dir = Path(__file__).resolve().parent
    config_dir = launch_dir.parent / 'config'
    if config_dir.exists():
        return str(config_dir)
    raise FileNotFoundError(
        'Cartographer config not found. Build and source the workspace, '
        'or run from workspace root with config/ in yahboom_M3Pro_description.'
    )


def generate_launch_description():
    config_dir = get_config_dir()

    return LaunchDescription([
        # 1. 深度图转激光（与 depth_slam_launch.py 相同）
        Node(
            package='depthimage_to_laserscan',
            executable='depthimage_to_laserscan_node',
            name='depthimage_to_laserscan',
            remappings=[
                ('depth', '/dabai_dcw2/depth/image_raw'),
                ('depth_camera_info', '/dabai_dcw2/depth/camera_info'),
                ('scan', '/scan'),
            ],
            parameters=[{
                'use_sim_time': True,
                'scan_height': 25,
                'scan_time': 0.033,
                'range_min': 0.1,
                'range_max': 10.0,
                'output_frame': 'DCW2',
            }],
        ),

        # 2. Cartographer 2D SLAM（配置目录/文件名通过 gflags 命令行传入，不能用 ROS 参数）
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            arguments=[
                '-configuration_directory', config_dir,
                '-configuration_basename', 'cartographer_m3pro_2d.lua',
            ],
            parameters=[{'use_sim_time': True}],
        ),

        # 3. 占据栅格发布（发布 /map，供 RViz 与导航使用）
        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='cartographer_occupancy_grid_node',
            parameters=[{
                'use_sim_time': True,
                'resolution': 0.05,
            }],
        ),
    ])
