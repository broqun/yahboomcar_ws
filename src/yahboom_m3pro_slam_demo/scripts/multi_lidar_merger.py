#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET

import message_filters
import math
import rclpy
from ament_index_python.packages import get_package_share_directory
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan


def _expand_urdf_xacro_constants(urdf_text: str) -> str:
    """Minimal substitutions so ElementTree can parse numeric rpy/xyz."""
    repl = (
        ('${-pi/2}', str(-math.pi / 2)),
        ('${-pi/4}', str(-math.pi / 4)),
        ('${pi/2}', str(math.pi / 2)),
        ('${pi/4}', str(math.pi / 4)),
        ('${pi}', str(math.pi)),
    )
    for old, new in repl:
        urdf_text = urdf_text.replace(old, new)
    return urdf_text


def load_laser_mount_xy_yaw_from_urdf(urdf_path: str, joint_name: str) -> dict:
    """
    Read fixed joint origin relative to parent (base_link in M3Pro.urdf).
    Returns offset for merge into base_footprint: same x,y as base_link (base_joint is z-only).
    yaw is URDF rpy third component (planar lidar, roll=pitch=0).
    """
    with open(urdf_path, encoding='utf-8') as f:
        root = ET.fromstring(_expand_urdf_xacro_constants(f.read()))
    joint = None
    for j in root.findall('joint'):
        if j.get('name') == joint_name:
            joint = j
            break
    if joint is None:
        raise ValueError(f'joint "{joint_name}" not found in {urdf_path}')
    origin = joint.find('origin')
    if origin is None:
        raise ValueError(f'joint "{joint_name}" has no <origin> in {urdf_path}')
    xyz = [float(v) for v in origin.get('xyz', '0 0 0').split()]
    rpy = [float(v) for v in origin.get('rpy', '0 0 0').split()]
    if len(xyz) < 2 or len(rpy) < 3:
        raise ValueError(f'invalid origin on "{joint_name}" in {urdf_path}')
    return {'x': xyz[0], 'y': xyz[1], 'yaw': rpy[2]}


class MultiLidarMerger(Node):
    def __init__(self):
        super().__init__('multi_lidar_merger')
        
        # 1. 设置同步订阅器
        self.sub_front = message_filters.Subscriber(self, LaserScan, '/scan_front', qos_profile=qos_profile_sensor_data)
        self.sub_rear = message_filters.Subscriber(self, LaserScan, '/scan_rear', qos_profile=qos_profile_sensor_data)
        
        # 2. 建立时间同步器：容忍度 0.05秒
        self.ts = message_filters.ApproximateTimeSynchronizer([self.sub_front, self.sub_rear], 10, 0.05)
        self.ts.registerCallback(self.merge_callback)
        
        self.pub_merged = self.create_publisher(LaserScan, '/scan_merged', 10)
        
        urdf_path = os.path.join(
            get_package_share_directory('m3pro_world_bringup'),
            'urdf',
            'M3Pro.urdf',
        )
        self.p_front = load_laser_mount_xy_yaw_from_urdf(urdf_path, 'laser_front_joint')
        self.p_rear = load_laser_mount_xy_yaw_from_urdf(urdf_path, 'laser_rear_joint')
        self.get_logger().info(
            f'Laser mounts from URDF ({urdf_path}): '
            f'front xyz_yaw=({self.p_front["x"]:.5f}, {self.p_front["y"]:.5f}, {self.p_front["yaw"]:.5f}), '
            f'rear=({self.p_rear["x"]:.5f}, {self.p_rear["y"]:.5f}, {self.p_rear["yaw"]:.5f})'
        )

        self.get_logger().info(
            'Dual lidar merger started (approx. time sync + pose transform); '
            'publishing merged 360° LaserScan on base_footprint.'
        )

    def merge_callback(self, front_msg, rear_msg):
        merged = LaserScan()
        merged.header.stamp = front_msg.header.stamp
        merged.header.frame_id = 'base_footprint' # 统一投影到底盘中心
        
        merged.angle_min = -math.pi
        merged.angle_max = math.pi
        # 将分母改为 360.0，使角分辨率变成 0.5度
        merged.angle_increment = math.pi / 360.0
        merged.range_min = 0.1
        merged.range_max = 12.0
        
        # 将数组长度翻倍到 720，用来装填更高密度的激光点
        ranges = [float('inf')] * 720
        
        def process(msg, offset):
            for i, r in enumerate(msg.ranges):
                if msg.range_min < r < msg.range_max:
                    # 坐标变换：1. 获取局部角度 + 安装角偏置
                    local_theta = msg.angle_min + i * msg.angle_increment
                    
                    # 2. 局部极坐标 -> 局部笛卡尔坐标
                    lx = r * math.cos(local_theta)
                    ly = r * math.sin(local_theta)
                    
                    # 3. 考虑安装角 (Yaw) 旋转 + 平移，投影到 base_footprint 坐标系
                    cos_y = math.cos(offset['yaw'])
                    sin_y = math.sin(offset['yaw'])
                    bx = lx * cos_y - ly * sin_y + offset['x']
                    by = lx * sin_y + ly * cos_y + offset['y']
                    
                    # 4. 将底盘坐标转换回虚拟极坐标
                    new_r = math.sqrt(bx**2 + by**2)
                    new_theta = math.atan2(by, bx)
                    
                    # 5. 计算在 720 度数组中的索引位 (修正之前的变量名错误)
                    idx = int((new_theta - merged.angle_min) / merged.angle_increment)
                    # 因为数组变成了 720 大小，所以索引的上限也要改成 720
                    if 0 <= idx < 720:
                        if new_r < ranges[idx]:
                            ranges[idx] = new_r

        process(front_msg, self.p_front)
        process(rear_msg, self.p_rear)
        
        merged.ranges = ranges
        self.pub_merged.publish(merged)

def main(args=None):
    rclpy.init(args=args)
    node = MultiLidarMerger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()