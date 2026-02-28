"""
/dabai_dcw2/camera_info
/dabai_dcw2/depth/camera_info
/dabai_dcw2/depth/image_raw
/dabai_dcw2/depth/image_raw/compressed
/dabai_dcw2/depth/image_raw/compressedDepth
/dabai_dcw2/depth/image_raw/theora
/dabai_dcw2/image_raw
/dabai_dcw2/image_raw/compressed
/dabai_dcw2/image_raw/compressedDepth
/dabai_dcw2/image_raw/theora
/dabai_dcw2/points
"""

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. 深度图转激光雷达节点
        Node(
            package='depthimage_to_laserscan',
            executable='depthimage_to_laserscan_node',
            name='depthimage_to_laserscan',
            remappings=[
                ('depth', '/dabai_dcw2/depth/image_raw'), # 你的深度图话题
                ('depth_camera_info', '/dabai_dcw2/depth/camera_info'),
                ('scan', '/scan') # 输出的虚拟激光话题
            ],
            parameters=[{
                'use_sim_time': True,
                'scan_height': 5,       # 提取深度图中中间 5 行像素
                'scan_time': 0.033,     # 对应 30fps
                'range_min': 0.1,       # 最小距离
                'range_max': 6.0,       # 最大距离（匹配你之前的设置）
                'output_frame': 'DCW2' # 必须与相机 Link 一致
            }]
        ),

        # 2. 启动 SLAM Toolbox
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            parameters=[{
                'use_sim_time': True,
                'max_laser_range': 6.0,
                'minimum_time_interval': 0.01,
                'mode': 'mapping',
                'scan_topic': '/scan'
            }]
        )
    ])