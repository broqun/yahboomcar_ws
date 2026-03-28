import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.actions import SetRemap

def generate_launch_description():
    # --- 1. 获取各个包的绝对路径 ---
    nav_demo_dir = get_package_share_directory('yahboom_m3pro_nav_demo')
    slam_demo_dir = get_package_share_directory('yahboom_m3pro_slam_demo')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    # --- 2. 定义关键文件路径 ---
    map_yaml_file = os.path.join(nav_demo_dir, 'maps', 'hospital_map_v1.yaml')
    nav2_params_file = os.path.join(nav_demo_dir, 'config', 'nav2_navigation.yaml')

    # --- 3. 基础环境：加载 Gazebo、医院世界、机器人模型与 RViz ---
    # 完美复用你之前的 launch，但通过参数关闭 xterm 键盘遥控终端
    hospital_env_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(slam_demo_dir, 'launch', 'hospital_m3pro_teleop_launch.py')),
        launch_arguments={'keyboard': 'false'}.items()
    )

    # --- 4. 启动双雷达合并节点 ---
    # 为 Nav2 提供 360 度无死角的 /scan_merged 视野
    lidar_merger_node = Node(
        package='yahboom_m3pro_lidar_tools',
        executable='multi_lidar_merger_node',
        name='multi_lidar_merger',
        output='screen'
    )

    # --- 5. 延迟加载底层轮子控制器 ---
    # 等待 Gazebo 物理引擎稳定后，挂载 diff_drive_controller
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

    # --- 6. 核心：启动 Nav2 导航栈 ---
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')),
        launch_arguments={
            'map': map_yaml_file,
            'use_sim_time': 'true',
            'params_file': nav2_params_file,
            'autostart': 'true',
            'cmd_vel_topic': '/diff_drive_controller/cmd_vel_unstamped',
            'use_velocity_smoother': 'False'
        }.items()
    )

    remappings = [('/cmd_vel', '/diff_drive_controller/cmd_vel_unstamped')]

    # --- 7. 返回总的 Launch 描述 (采用架构师推荐的阶梯启动) ---
    return LaunchDescription([
        SetRemap(src='/cmd_vel', dst='/diff_drive_controller/cmd_vel_unstamped'),
        hospital_env_launch,
        lidar_merger_node,
        delayed_spawn_controllers,
        # 延迟 15 秒启动 Nav2，确保控制器和雷达都已就绪，避免 TF 报错狂刷屏
        TimerAction(
            period=15.0,
            actions=[
                LogInfo(msg='[Nav2 Demo] 正在唤醒 Nav2 自动驾驶系统...'),
                nav2_launch
            ]
        )
    ])
