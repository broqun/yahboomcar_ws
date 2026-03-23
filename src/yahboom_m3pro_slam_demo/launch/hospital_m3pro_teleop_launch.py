"""
Launch Gazebo with hospital world, spawn M3Pro robot, and start keyboard teleop.

Launches:
- Gazebo with aws-robomaker-hospital-world
- M3Pro robot model (robot_state_publisher + spawn_entity)
- teleop_twist_keyboard for keyboard control
"""

import os
from pathlib import Path

from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    LogInfo,
    OpaqueFunction,
    SetEnvironmentVariable,
    TimerAction,
)
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
import xacro


def get_hospital_world_path():
    """Get path to hospital.world. Works from both source and install layout."""
    # Try 1: ament/ROS2 package (if aws_robomaker_hospital_world is installed)
    try:
        pkg_path = get_package_share_path('aws_robomaker_hospital_world')
        p = pkg_path / 'worlds' / 'hospital.world'
        if p.exists():
            return p
    except Exception:
        pass
    # Try 2: 从当前文件向上查找 workspace，支持 source 与 install 两种布局
    # source:  src/yahboom_m3pro_slam_demo/launch/xxx.py
    # install: install/yahboom_m3pro_slam_demo/share/yahboom_m3pro_slam_demo/launch/xxx.py
    current = Path(__file__).resolve().parent
    for _ in range(8):
        # 当前层级下的 aws-robomaker-hospital-world（如在 src/ 内）
        p1 = current / 'aws-robomaker-hospital-world' / 'worlds' / 'hospital.world'
        # workspace 根下的 src/aws-robomaker-hospital-world
        p2 = current / 'src' / 'aws-robomaker-hospital-world' / 'worlds' / 'hospital.world'
        if p1.exists():
            return p1
        if p2.exists():
            return p2
        parent = current.parent
        if parent == current:
            break
        current = parent
    raise FileNotFoundError(
        'Hospital world not found. Run this launch from workspace root, '
        'with aws-robomaker-hospital-world in src/'
    )


def get_hospital_model_paths():
    """Get GAZEBO_MODEL_PATH additions for hospital world models."""
    # 先找到 hospital.world 所在包，models 和 fuel_models 与其同目录
    world_path = get_hospital_world_path()
    hospital_pkg = world_path.parent.parent  # worlds -> aws-robomaker-hospital-world
    models_path = hospital_pkg / 'models'
    fuel_models_path = hospital_pkg / 'fuel_models'
    paths = []
    if models_path.exists():
        paths.append(str(models_path))
    if fuel_models_path.exists():
        paths.append(str(fuel_models_path))
    return os.pathsep.join(paths) if paths else ''


def generate_launch_description():
    # Paths
    m3pro_share = get_package_share_path('yahboom_m3pro_slam_demo')
    default_urdf = m3pro_share / 'urdf' / 'M3Pro.urdf'
    world_path = get_hospital_world_path()
    hospital_models = get_hospital_model_paths()

    # Arguments
    gui_arg = DeclareLaunchArgument(
        'gui',
        default_value='true',
        description='Set to "false" to run Gazebo headless.'
    )
    model_arg = DeclareLaunchArgument(
        'model',
        default_value=str(default_urdf),
        description='Path to robot URDF/xacro file'
    )
    # -x 2.049177 -y 11.755002 -z 0.01
    x_arg = DeclareLaunchArgument('x', default_value='0.049177', description='Spawn X position')
    y_arg = DeclareLaunchArgument('y', default_value='11.755002', description='Spawn Y position')
    z_arg = DeclareLaunchArgument('z', default_value='0.01', description='Spawn Z position')
    keyboard_arg = DeclareLaunchArgument(
        'keyboard',
        default_value='true',
        description='If true, open new terminal for keyboard control (requires xterm). '
                    'If false, run manually: ros2 run teleop_twist_keyboard teleop_twist_keyboard',
    )
    speed_arg = DeclareLaunchArgument(
        'speed',
        default_value='1.99999',
        description='Linear speed (m/s) for forward/backward. Default 0.5 in teleop_twist_keyboard.',
    )
    turn_arg = DeclareLaunchArgument(
        'turn',
        default_value='0.99999',
        description='Angular speed (rad/s) for turning. Default 1.0 in teleop_twist_keyboard.',
    )

    # Set GAZEBO_MODEL_PATH: hospital models + M3Pro package (用于解析 package:///model://)
    # Gazebo 需要在此路径下找到 yahboom_m3pro_slam_demo/meshes/xxx.STL
    m3pro_model_path = str(m3pro_share.parent)  # .../share，下有 yahboom_m3pro_slam_demo/
    print(f"m3pro_model_path: {m3pro_model_path}")
    all_model_paths = [m3pro_model_path]
    if hospital_models:
        all_model_paths.insert(0, hospital_models)
    existing = os.environ.get('GAZEBO_MODEL_PATH', '')
    new_path = os.pathsep.join(all_model_paths) + (os.pathsep + existing if existing else '')
    print(f"new_path: {new_path}")
    gazebo_model_path_actions = [SetEnvironmentVariable('GAZEBO_MODEL_PATH', new_path)]
    print(f"GAZEBO_MODEL_PATH: {existing}")

    gazebo_launch_dir = Path(get_package_share_path('gazebo_ros')) / 'launch'

    # Gazebo server with hospital world
    gzserver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([str(gazebo_launch_dir / 'gzserver.launch.py')]),
        launch_arguments={
            'world': str(world_path),
            'verbose': 'true',
        }.items(),
    )

    # Gazebo client (GUI)
    gzclient_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([str(gazebo_launch_dir / 'gzclient.launch.py')]),
        condition=IfCondition(LaunchConfiguration('gui')),
    )

    # Robot description - 拦截并切除 XML 声明的终极方案
    try:
        # 1. 用 xacro 库在后台解析公式 (比如 ${pi})
        doc = xacro.process_file(str(default_urdf))
        robot_desc_raw = doc.toxml()
        
        # 2. 暴力切除：无视前面的声明和注释，强制从 <robot 标签开始截取！
        if '<robot' in robot_desc_raw:
            robot_desc_raw = '<robot' + robot_desc_raw.split('<robot', 1)[1]
            
        robot_description = ParameterValue(robot_desc_raw, value_type=str)
    except Exception as e:
        print(f"解析 URDF 失败: {e}")
        robot_description = ParameterValue("", value_type=str)

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': robot_description},
            {'use_sim_time': True},
        ],
    )

    # Keyboard teleop: 在新终端中运行（需 TTY，launch 子进程无 stdin）
    # speed: 线速度(m/s)，turn: 角速度(rad/s)。可用 launch 参数调整
    def create_keyboard_teleop(context, *args, **kwargs):
        speed = context.perform_substitution(LaunchConfiguration('speed'))
        turn = context.perform_substitution(LaunchConfiguration('turn'))
        teleop_cmd = f'ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p speed:={speed} -p turn:={turn} -p repeat_rate:=20'
        teleop_cmd = f'ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/diff_drive_controller/cmd_vel_unstamped -p speed:={speed} -p turn:={turn} -p repeat_rate:=20'
        return [
            ExecuteProcess(
                cmd=['xterm', '-geometry', '110x28', '-hold', '-e', teleop_cmd],
                output='screen',
            )
        ]

    keyboard_teleop = OpaqueFunction(
        function=create_keyboard_teleop,
        condition=IfCondition(LaunchConfiguration('keyboard')),
    )

    # 若禁用 xterm，延时提示用户手动运行
    keyboard_hint = TimerAction(
        period=8.0,
        actions=[
            LogInfo(msg='[键盘控制] 请在新终端运行: ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p speed:=1.0 -p turn:=0.5'),
        ],
        condition=UnlessCondition(LaunchConfiguration('keyboard')),
    )

    rviz_config_path = os.path.join(m3pro_share, 'rviz', 'spen_M3Pro_lidar_slam.rviz')
    # 定义 RViz2 节点
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        # 关键：通过参数加载预设好的界面布局
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': True}]
    )

    # Spawn robot in Gazebo (delayed to wait for Gazebo and robot_description)
    spawn_m3pro_rviz = TimerAction(
        period=5.5,
        actions=[
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                name='spawn_m3pro',
                output='screen',
                arguments=[
                    '-topic', 'robot_description',
                    '-entity', 'M3Pro',
                    '-x', LaunchConfiguration('x'),
                    '-y', LaunchConfiguration('y'),
                    '-z', LaunchConfiguration('z'),
                ],
            ),
            rviz_node,
            keyboard_teleop
        ],
    )

    ld = [
        gui_arg,
        model_arg,
        x_arg,
        y_arg,
        z_arg,
        keyboard_arg,
        speed_arg,
        turn_arg,
        *gazebo_model_path_actions,
        gzserver_launch,
        gzclient_launch,
        robot_state_publisher,
        # joint_state_publisher,
        spawn_m3pro_rviz,
        keyboard_hint,
    ]
    return LaunchDescription(ld)
