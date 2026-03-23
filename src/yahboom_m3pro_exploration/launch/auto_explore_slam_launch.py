from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription, LogInfo, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, SetRemap
from ament_index_python.packages import get_package_share_path


def generate_launch_description():
    # 这里不重复实现 Gazebo / SLAM / 控制器链路，而是直接复用现有 Demo launch。
    slam_demo_share = get_package_share_path('yahboom_m3pro_slam_demo')
    exploration_share = get_package_share_path('yahboom_m3pro_exploration')
    nav2_bringup_share = get_package_share_path('nav2_bringup')

    keyboard = LaunchConfiguration('keyboard')
    gui = LaunchConfiguration('gui')
    autostart = LaunchConfiguration('autostart')
    use_sim_time = LaunchConfiguration('use_sim_time')
    params_file = LaunchConfiguration('params_file')

    base_demo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [str(slam_demo_share / 'launch' / 'gazebo_hospital_slam_demo_launch.py')]
        ),
        launch_arguments={
            'keyboard': keyboard,
            'gui': gui,
        }.items(),
    )

    # Nav2 默认输出 /cmd_vel，而当前底盘控制器实际监听
    # /diff_drive_controller/cmd_vel_unstamped，因此这里统一做 remap。
    nav2_launch = GroupAction([
        SetRemap(src='cmd_vel', dst='/diff_drive_controller/cmd_vel_unstamped'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [str(nav2_bringup_share / 'launch' / 'navigation_launch.py')]
            ),
            launch_arguments={
                'use_sim_time': use_sim_time,
                'autostart': autostart,
                'params_file': params_file,
            }.items(),
        ),
    ])

    # 当前 explorer 还只是“占位节点”，用于验证自动探索包本身的接线。
    # 下一步会在这里补 frontier 检测与 NavigateToPose action 调用。
    frontier_explorer = Node(
        package='yahboom_m3pro_exploration',
        executable='frontier_explorer',
        name='frontier_explorer',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
        }],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'keyboard',
            default_value='false',
            description='Keep false for autonomous exploration; true keeps manual teleop available.',
        ),
        DeclareLaunchArgument(
            'gui',
            default_value='true',
            description='Whether to launch Gazebo GUI.',
        ),
        DeclareLaunchArgument(
            'autostart',
            default_value='true',
            description='Automatically transition Nav2 lifecycle nodes to active.',
        ),
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use Gazebo simulation time.',
        ),
        DeclareLaunchArgument(
            'params_file',
            default_value=str(exploration_share / 'config' / 'nav2_params.yaml'),
            description='Nav2 parameter file.',
        ),
        # 先启动现有 SLAM Demo，让 Gazebo、机器人、控制器、/scan_merged、/map 先稳定起来。
        LogInfo(msg='[auto_explore_slam_launch] Starting base SLAM demo.'),
        base_demo_launch,
        # Nav2 依赖 map / odom / scan / controller 等链路，因此延迟拉起更稳妥。
        TimerAction(
            period=12.0,
            actions=[
                LogInfo(msg='[auto_explore_slam_launch] Starting Nav2 navigation stack.'),
                nav2_launch,
            ],
        ),
        # explorer 需要在 Nav2 生命周期节点进入 active 后再启动，避免一上来就发目标失败。
        TimerAction(
            period=14.0,
            actions=[
                LogInfo(msg='[auto_explore_slam_launch] Starting frontier explorer scaffold.'),
                frontier_explorer,
            ],
        ),
    ])
