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
                'scan_height': 25,       # 提取深度图中中间 5 行像素
                'scan_time': 0.033,     # 对应 30fps
                'range_min': 0.1,       # 最小距离
                'range_max': 10.0,       # 最大距离（匹配你之前的设置）
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
                'scan_topic': '/scan',
                # --- 强制指定坐标系 ---
                'map_frame': 'map',
                'odom_frame': 'odom',
                'base_frame': 'base_footprint',  # <--- 重点！请确认你的小车根节点是不是叫 base_footprint
                'scan_queue_size': 50,      # 增大队列，给 TF 缓冲时间
                'transform_timeout': 0.5,   # 增加等待坐标转换的超时时间
                # --- 增大匹配搜索范围 ---
                'hubere_distance': 0.1,         # 容忍的小误差范围
                'minimum_travel_distance': 0.1,  # 走 10cm 更新一次，别太频繁
                'minimum_travel_heading': 0.1,   # 转 5-6 度更新一次
                'scan_buffer_size': 1000,          # 增加缓存，利于回环
                # --- 关键：提高扫描匹配的权重 ---
                'link_match_minimum_response_fine': 0.05, 
                'loop_search_maximum_distance': 15.0, # 在 5 米范围内寻找回环，防止走廊对不上
            }]
        )
    ])