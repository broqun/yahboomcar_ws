"""
Compatibility wrapper.

基础环境（医院世界 + 机器人生成 + RViz + 键盘）已迁移到 m3pro_world_bringup。
保留本文件名，避免旧命令失效。
"""

from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    bringup_share = get_package_share_path('m3pro_world_bringup')

    passthrough_args = [
        DeclareLaunchArgument('gui', default_value='true'),
        DeclareLaunchArgument('model', default_value=str(bringup_share / 'urdf' / 'M3Pro.urdf')),
        DeclareLaunchArgument('x', default_value='0.049177'),
        DeclareLaunchArgument('y', default_value='11.755002'),
        DeclareLaunchArgument('z', default_value='0.01'),
        DeclareLaunchArgument('keyboard', default_value='true'),
        DeclareLaunchArgument('speed', default_value='1.99999'),
        DeclareLaunchArgument('turn', default_value='0.99999'),
    ]

    include_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [str(bringup_share / 'launch' / 'hospital_world_bringup_launch.py')]
        ),
        launch_arguments={
            'gui': LaunchConfiguration('gui'),
            'model': LaunchConfiguration('model'),
            'x': LaunchConfiguration('x'),
            'y': LaunchConfiguration('y'),
            'z': LaunchConfiguration('z'),
            'keyboard': LaunchConfiguration('keyboard'),
            'speed': LaunchConfiguration('speed'),
            'turn': LaunchConfiguration('turn'),
        }.items(),
    )

    return LaunchDescription([
        *passthrough_args,
        include_bringup,
    ])
