#include <cmath>
#include <limits>
#include <memory>
#include <vector>
#include <functional>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "message_filters/subscriber.h"
#include "message_filters/synchronizer.h"
#include "message_filters/sync_policies/approximate_time.h"

// 将车头/车尾两路 2D 激光统一投影到 base_footprint，
// 再重建成一条近似 360 度的虚拟 LaserScan，供 SLAM 直接使用。
class MultiLidarMerger : public rclcpp::Node
{
public:
  MultiLidarMerger()
  : Node("multi_lidar_merger")
  {
    auto qos = rclcpp::SensorDataQoS();

    // 两路雷达都使用传感器 QoS，尽量贴近底层激光数据的发布语义。
    sub_front_.subscribe(this, "/scan_front", qos.get_rmw_qos_profile());
    sub_rear_.subscribe(this, "/scan_rear", qos.get_rmw_qos_profile());

    // 使用近似时间同步，而不是严格同步。
    // 这样可以容忍前后雷达时间戳存在少量抖动，只要在 0.05s 窗口内就触发融合。
    sync_ = std::make_shared<message_filters::Synchronizer<SyncPolicy>>(
      SyncPolicy(10), sub_front_, sub_rear_);
    sync_->setMaxIntervalDuration(rclcpp::Duration::from_seconds(0.05));
    sync_->registerCallback(
      std::bind(&MultiLidarMerger::mergeCallback, this,
      std::placeholders::_1, std::placeholders::_2));

    // /scan_merged 是最终提供给 SLAM 的统一激光话题。
    pub_merged_ =
      create_publisher<sensor_msgs::msg::LaserScan>("/scan_merged", 10);

    RCLCPP_INFO(get_logger(), "C++ multi_lidar_merger started.");
  }

private:
  struct LaserOffset
  {
    double x;
    double y;
    double yaw;
  };

  using LaserScan = sensor_msgs::msg::LaserScan;
  using SyncPolicy = message_filters::sync_policies::ApproximateTime<
    LaserScan, LaserScan>;

  // 将某一路原始 LaserScan 投影到 base_footprint，并写入统一角度网格。
  //
  // 处理流程与 Python 版本保持一致：
  // 1. 用原始 scan 的极坐标恢复雷达局部笛卡尔点
  // 2. 结合雷达安装位姿 (x, y, yaw) 变换到 base_footprint
  // 3. 再将点转换回“虚拟 360 度雷达”的极坐标
  // 4. 将点落入对应角度 bin；若同一 bin 有多个点，保留最近量测
  void processScan(
    const LaserScan::ConstSharedPtr & msg,
    const LaserOffset & offset,
    LaserScan & merged,
    std::vector<float> & ranges)
  {
    for (size_t i = 0; i < msg->ranges.size(); ++i) {
      const float r = msg->ranges[i];
      // 只保留原雷达有效量程内的数据；无穷大、NaN 和超量程值都直接跳过。
      if (!(msg->range_min < r && r < msg->range_max)) {
        continue;
      }

      // 当前量测在“雷达自身坐标系”中的角度。
      const double local_theta =
        msg->angle_min + static_cast<double>(i) * msg->angle_increment;

      // 极坐标 -> 雷达局部笛卡尔坐标。
      const double lx = r * std::cos(local_theta);
      const double ly = r * std::sin(local_theta);

      const double cos_y = std::cos(offset.yaw);
      const double sin_y = std::sin(offset.yaw);

      // 雷达局部点 -> base_footprint。
      // 这里只考虑平面 2D 变换：先旋转，再平移。
      const double bx = lx * cos_y - ly * sin_y + offset.x;
      const double by = lx * sin_y + ly * cos_y + offset.y;

      // 再转换回统一虚拟雷达的极坐标表示。
      const double new_r = std::sqrt(bx * bx + by * by);
      const double new_theta = std::atan2(by, bx);

      // 根据角度计算应该写入哪一个角度 bin。
      // merged.angle_increment = pi / 360，对应总计 720 个 bin。
      const int idx = static_cast<int>(
        (new_theta - merged.angle_min) / merged.angle_increment);

      if (idx >= 0 && idx < static_cast<int>(ranges.size())) {
        // 同一个方向若前后雷达都命中，保留最近障碍物，避免被更远点覆盖。
        if (new_r < ranges[idx]) {
          ranges[idx] = static_cast<float>(new_r);
        }
      }
    }
  }

  // 当前后两路雷达在时间上匹配成功后，构造一条统一输出的 LaserScan。
  void mergeCallback(
    const LaserScan::ConstSharedPtr front_msg,
    const LaserScan::ConstSharedPtr rear_msg)
  {
    LaserScan merged;
    // 直接沿用前雷达时间戳，保证下游节点看到的是同一时刻的融合结果。
    merged.header.stamp = front_msg->header.stamp;
    // 统一输出到底盘中心坐标系，方便 SLAM 直接使用。
    merged.header.frame_id = "base_footprint";

    // 目标输出格式固定为 [-pi, pi] 的 360 度扫描，角分辨率 0.5 度。
    merged.angle_min = -M_PI;
    merged.angle_max = M_PI;
    merged.angle_increment = M_PI / 360.0;
    merged.range_min = 0.1;
    merged.range_max = 12.0;

    // 720 = 2pi / (pi / 360)，初始值为 inf，表示该方向暂时没有量测。
    std::vector<float> ranges(
      720, std::numeric_limits<float>::infinity());

    // 先后处理前后两路雷达，最终结果共同写入同一份 ranges。
    processScan(front_msg, front_, merged, ranges);
    processScan(rear_msg, rear_, merged, ranges);

    merged.ranges = ranges;
    pub_merged_->publish(merged);
  }

  message_filters::Subscriber<LaserScan> sub_front_;
  message_filters::Subscriber<LaserScan> sub_rear_;
  std::shared_ptr<message_filters::Synchronizer<SyncPolicy>> sync_;
  rclcpp::Publisher<LaserScan>::SharedPtr pub_merged_;

  // 与现有 Python 版本保持一致的雷达安装外参。
  // 若后续改 URDF 安装位姿，这里也必须同步更新，或者进一步改造成参数/TF 驱动。
  LaserOffset front_{0.12, -0.10, 0.0};
  LaserOffset rear_{-0.12, 0.10, M_PI};
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<MultiLidarMerger>();
  // 单线程 spin 已足够覆盖当前计算量与同步逻辑。
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}