from launch import LaunchDescription
from launch_ros.actions import Node
import os
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    laser_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
        get_package_share_directory('yahboom_M3Pro_laser'), 'launch'),
         '/laser_driver.launch.py'])
    )

    camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
        get_package_share_directory('orbbec_camera'), 'launch'),
         '/dabai_dcw2.launch.py'])
    )

    return LaunchDescription([laser_driver_launch,camera_launch])

