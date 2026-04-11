from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 获取 ekf 配置文件路径
    ekf_config_path = os.path.join(
        get_package_share_directory('yahboom_m3pro_slam_demo'), 
        'config', 
        'ekf.yaml'
    )

    return LaunchDescription([
        # 1. 启动 C++ 双雷达合并节点
        Node(
            package='yahboom_m3pro_lidar_tools',
            executable='multi_lidar_merger_node',
            name='multi_lidar_merger',
            output='screen'
        ),
        # 如需切回 Python 合并器，可使用下面注释模板：
        # from launch.actions import ExecuteProcess
        # merger_script = os.path.join(
        #     get_package_share_directory('yahboom_m3pro_slam_demo'),
        #     'scripts',
        #     'multi_lidar_merger.py'
        # )
        # ExecuteProcess(
        #     cmd=['python3', merger_script],
        #     output='screen'
        # ),

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
                'link_match_minimum_response_fine': 0.15,
            }]
        ),

        # 3. 👑 新增：启动 robot_localization (EKF 融合)
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[ekf_config_path, {'use_sim_time': True}]
        )
    ])