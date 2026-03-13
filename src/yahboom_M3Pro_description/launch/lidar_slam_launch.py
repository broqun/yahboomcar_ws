from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        
        # 1. 启动打好补丁的 360° 双雷达合并 Python 节点
        ExecuteProcess(
            cmd=['python3', '/var/robotic/yahboomcar_ws/src/yahboom_M3Pro_description/scripts/multi_lidar_merger.py'],
            output='screen'
        ),

        # 2. 启动 SLAM Toolbox
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[{
                'use_sim_time': True,  # 强制使用仿真时间
                'scan_topic': '/scan_merged', 
                'map_frame': 'map',
                'odom_frame': 'odom',
                'base_frame': 'base_footprint',
                
                'max_laser_range': 12.0,
                'minimum_time_interval': 0.25,
                
                'mode': 'mapping',
                'resolution': 0.05,
                
                'minimum_travel_distance': 0.25,
                'minimum_travel_heading': 0.2,
                
                # 👈 [修改] 扩大相关性搜索空间！如果里程计漂移了，给算法更大的范围去把墙壁“拉”回来
                'correlation_search_space_dimension': 0.8,
                'correlation_search_space_resolution': 0.02,
                
                # 惩罚参数。强迫算法更信任激光雷达的直线匹配，而不是盲目相信打滑的轮子
                'angle_variance_penalty': 1.0, 
                'use_scan_matching': True,
                'use_scan_barycenter': True,
                
                'scan_buffer_size': 150,
                'loop_search_maximum_distance': 12.0, # T-mini Plus 激光雷达测距范围为0.05m至12m
                'loop_match_minimum_chain_size': 3,
                'link_match_minimum_response_fine': 0.1,
            }]
        )
    ])