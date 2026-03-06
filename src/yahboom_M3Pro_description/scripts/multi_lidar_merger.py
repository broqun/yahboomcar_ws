#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data
import message_filters
import math

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
        
        # 3. 物理偏移量与安装角 (必须与 URDF 中的 laser_rear_left_joint rpy 保持一致)
        # 前雷达朝前 (yaw=0)，后雷达在 URDF 中已转 180度 (yaw=pi)
        self.p_front = {'x': 0.12, 'y': -0.10, 'yaw': 0.0}
        self.p_rear = {'x': -0.12, 'y': 0.10, 'yaw': math.pi}
        
        self.get_logger().info("🚀 双雷达【同步纠偏修正版】已启动！正在缝合 360° 点云...")

    def merge_callback(self, front_msg, rear_msg):
        merged = LaserScan()
        merged.header.stamp = front_msg.header.stamp
        merged.header.frame_id = 'base_footprint' # 统一投影到底盘中心
        
        merged.angle_min = -math.pi
        merged.angle_max = math.pi
        merged.angle_increment = math.pi / 180.0
        merged.range_min = 0.1
        merged.range_max = 12.0
        
        # 初始化 360 个索引位
        ranges = [float('inf')] * 360
        
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
                    
                    # 5. 计算在 360 度数组中的索引位 (修正之前的变量名错误)
                    idx = int((new_theta - merged.angle_min) / merged.angle_increment)
                    if 0 <= idx < 360:
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