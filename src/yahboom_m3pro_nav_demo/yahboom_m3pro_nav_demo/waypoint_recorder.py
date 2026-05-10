import math
import queue
import threading
from pathlib import Path

import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.node import Node

from yahboom_m3pro_nav_demo.waypoint_storage import default_record_path, merge_waypoint


def euler_from_quaternion(x, y, z, w):
    """Return yaw in radians from quaternion components x, y, z, w."""
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y - z * z)
    return math.atan2(t3, t4)


class WaypointRecorderNode(Node):
    def __init__(self, pose_queue):
        super().__init__('waypoint_recorder_node')
        self.declare_parameter('waypoints_output_file', '')
        self.pose_queue = pose_queue
        # 订阅 RViz2 的 2D Goal Pose
        self.subscription = self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        # 将接收到的 Pose 立即放入队列，绝不阻塞 ROS 2 线程
        self.pose_queue.put(msg)


def main(args=None):
    rclpy.init(args=args)

    # 创建一个线程安全的队列
    pose_queue = queue.Queue()
    recorder_node = WaypointRecorderNode(pose_queue)
    out_override = (
        recorder_node.get_parameter('waypoints_output_file')
        .get_parameter_value()
        .string_value.strip()
    )
    storage_path = Path(out_override).expanduser() if out_override else default_record_path()

    # 核心：将 ROS 2 的 spin (事件循环) 扔进后台子线程运行
    spin_thread = threading.Thread(target=rclpy.spin, args=(recorder_node,), daemon=True)
    spin_thread.start()

    print("\n" + "="*50)
    print("📍 交互式航点记录仪 (Interactive Waypoint Recorder) 已启动！")
    print("👉 请切换到 RViz2，使用 '2D Goal Pose' 工具点击目标并拖拽。")
    print(f"💾 航点将追加保存到: {storage_path}")
    print("="*50 + "\n")

    try:
        # 主线程：专门负责与用户通过终端交互
        while rclpy.ok():
            # 这里的 get() 会阻塞主线程等待，但不会影响后台的 ROS 2 节点
            msg = pose_queue.get()

            # 当 RViz 传来新坐标时，响铃并提醒用户输入
            print("\n" + "🛎️" * 20)
            wp_name = input("✨ 捕获到新航点！请给它起个名字 (如 room_1, charger): ").strip()

            if not wp_name:
                wp_name = "unnamed_wp"

            # 提取坐标并计算
            x = round(msg.pose.position.x, 3)
            y = round(msg.pose.position.y, 3)
            yaw = round(euler_from_quaternion(
                msg.pose.orientation.x,
                msg.pose.orientation.y,
                msg.pose.orientation.z,
                msg.pose.orientation.w), 3)

            frame_id = msg.header.frame_id.strip() or 'map'
            merge_waypoint(storage_path, wp_name, x, y, yaw, frame_id=frame_id)

            # 仍打印一行 Python 片段，便于手工粘贴到自定义脚本（可选）
            print(f"✅ 记录成功: [{wp_name}]（已写入磁盘）")
            print(f"        '{wp_name}': create_pose(navigator, {x}, {y}, {yaw}),")
            print("-" * 50)
            print("👉 等待下一个航点输入...")

    except KeyboardInterrupt:
        print("\n🛑 收到中断信号，程序退出。")
    finally:
        recorder_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
