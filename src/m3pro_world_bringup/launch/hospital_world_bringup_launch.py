"""
Base bringup: Gazebo hospital world + M3Pro spawn + RViz + optional keyboard teleop.
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
    """Get path to hospital.world from package or workspace."""
    try:
        pkg_path = get_package_share_path('aws_robomaker_hospital_world')
        p = pkg_path / 'worlds' / 'hospital.world'
        if p.exists():
            return p
    except Exception:
        pass

    current = Path(__file__).resolve().parent
    for _ in range(8):
        p1 = current / 'aws-robomaker-hospital-world' / 'worlds' / 'hospital.world'
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
        'Hospital world not found. Expected aws-robomaker-hospital-world with worlds/hospital.world.'
    )


def get_hospital_model_paths():
    """Get additional GAZEBO_MODEL_PATH entries from hospital world package."""
    world_path = get_hospital_world_path()
    hospital_pkg = world_path.parent.parent
    models_path = hospital_pkg / 'models'
    fuel_models_path = hospital_pkg / 'fuel_models'
    paths = []
    if models_path.exists():
        paths.append(str(models_path))
    if fuel_models_path.exists():
        paths.append(str(fuel_models_path))
    return os.pathsep.join(paths) if paths else ''


def generate_launch_description():
    bringup_share = get_package_share_path('m3pro_world_bringup')
    default_urdf = bringup_share / 'urdf' / 'M3Pro.urdf'
    default_rviz = bringup_share / 'rviz' / 'nav_demo.rviz'
    try:
        slam_demo_share = get_package_share_path('yahboom_m3pro_slam_demo')
        legacy_rviz = slam_demo_share / 'rviz' / 'nav_demo.rviz'
        if legacy_rviz.exists():
            default_rviz = legacy_rviz
    except Exception:
        slam_demo_share = None
    world_path = get_hospital_world_path()
    hospital_models = get_hospital_model_paths()

    gui_arg = DeclareLaunchArgument(
        'gui',
        default_value='true',
        description='Set to "false" to run Gazebo headless.',
    )
    model_arg = DeclareLaunchArgument(
        'model',
        default_value=str(default_urdf),
        description='Path to robot URDF/xacro file',
    )
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=str(world_path),
        description='Path to Gazebo world file',
    )
    rviz_arg = DeclareLaunchArgument(
        'rvizconfig',
        default_value=str(default_rviz),
        description='Path to RViz config file.',
    )
    x_arg = DeclareLaunchArgument('x', default_value='0.049177', description='Spawn X position')
    y_arg = DeclareLaunchArgument('y', default_value='11.755002', description='Spawn Y position')
    z_arg = DeclareLaunchArgument('z', default_value='0.01', description='Spawn Z position')
    keyboard_arg = DeclareLaunchArgument(
        'keyboard',
        default_value='true',
        description='If true, launch teleop_twist_keyboard in xterm.',
    )
    speed_arg = DeclareLaunchArgument(
        'speed',
        default_value='1.99999',
        description='Teleop linear speed (m/s).',
    )
    turn_arg = DeclareLaunchArgument(
        'turn',
        default_value='0.99999',
        description='Teleop angular speed (rad/s).',
    )

    # Gazebo converts some package mesh URIs to model://<pkg>/... during URDF->SDF.
    # Include ROS share root so model://m3pro_world_bringup/meshes/... can resolve.
    model_roots = [str(bringup_share.parent)]
    if hospital_models:
        model_roots.insert(0, hospital_models)
    existing = os.environ.get('GAZEBO_MODEL_PATH', '')
    new_path = os.pathsep.join(model_roots) + (os.pathsep + existing if existing else '')
    gazebo_model_path_actions = [SetEnvironmentVariable('GAZEBO_MODEL_PATH', new_path)]

    gazebo_launch_dir = Path(get_package_share_path('gazebo_ros')) / 'launch'

    gzserver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([str(gazebo_launch_dir / 'gzserver.launch.py')]),
        launch_arguments={
            'world': LaunchConfiguration('world'),
            'verbose': 'true',
        }.items(),
    )

    gzclient_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([str(gazebo_launch_dir / 'gzclient.launch.py')]),
        condition=IfCondition(LaunchConfiguration('gui')),
    )

    doc = xacro.process_file(str(default_urdf))
    robot_desc_raw = doc.toxml()
    if '<robot' in robot_desc_raw:
        robot_desc_raw = '<robot' + robot_desc_raw.split('<robot', 1)[1]
    robot_description = ParameterValue(robot_desc_raw, value_type=str)

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

    def create_keyboard_teleop(context, *args, **kwargs):
        speed = context.perform_substitution(LaunchConfiguration('speed'))
        turn = context.perform_substitution(LaunchConfiguration('turn'))
        teleop_cmd = (
            'ros2 run teleop_twist_keyboard teleop_twist_keyboard '
            '--ros-args -r cmd_vel:=/diff_drive_controller/cmd_vel_unstamped '
            f'-p speed:={speed} -p turn:={turn} -p repeat_rate:=20'
        )
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

    keyboard_hint = TimerAction(
        period=8.0,
        actions=[
            LogInfo(
                msg='[keyboard] Run manually in a new terminal if needed: '
                    'ros2 run teleop_twist_keyboard teleop_twist_keyboard '
                    '--ros-args -r cmd_vel:=/diff_drive_controller/cmd_vel_unstamped'
            ),
        ],
        condition=UnlessCondition(LaunchConfiguration('keyboard')),
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
        parameters=[{'use_sim_time': True}],
    )

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
            keyboard_teleop,
        ],
    )

    return LaunchDescription([
        gui_arg,
        model_arg,
        world_arg,
        rviz_arg,
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
        spawn_m3pro_rviz,
        keyboard_hint,
    ])
