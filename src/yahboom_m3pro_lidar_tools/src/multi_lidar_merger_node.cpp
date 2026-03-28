#include <ament_index_cpp/get_package_share_directory.hpp>
#include <cmath>
#include <cstddef>
#include <fstream>
#include <functional>
#include <limits>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

#include "message_filters/subscriber.h"
#include "message_filters/sync_policies/approximate_time.h"
#include "message_filters/synchronizer.h"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "tinyxml2.h"

namespace
{

struct LaserOffset
{
  double x;
  double y;
  double yaw;
};

void replace_all(std::string * s, const std::string & from, const std::string & to)
{
  if (from.empty()) {
    return;
  }
  std::size_t pos = 0;
  while ((pos = s->find(from, pos)) != std::string::npos) {
    s->replace(pos, from.length(), to);
    pos += to.length();
  }
}

std::string expand_urdf_xacro_constants(std::string text)
{
  replace_all(&text, "${-pi/2}", std::to_string(-M_PI / 2.0));
  replace_all(&text, "${-pi/4}", std::to_string(-M_PI / 4.0));
  replace_all(&text, "${pi/2}", std::to_string(M_PI / 2.0));
  replace_all(&text, "${pi/4}", std::to_string(M_PI / 4.0));
  replace_all(&text, "${pi}", std::to_string(M_PI));
  return text;
}

std::string read_file(const std::string & path)
{
  std::ifstream in(path);
  if (!in) {
    throw std::runtime_error("failed to open URDF: " + path);
  }
  std::ostringstream buf;
  buf << in.rdbuf();
  return buf.str();
}

LaserOffset load_laser_mount_xy_yaw_from_urdf(
  const std::string & urdf_path, const char * joint_name)
{
  const std::string xml = expand_urdf_xacro_constants(read_file(urdf_path));
  tinyxml2::XMLDocument doc;
  if (doc.Parse(xml.c_str()) != tinyxml2::XML_SUCCESS) {
    throw std::runtime_error("URDF XML parse error: " + urdf_path);
  }
  const tinyxml2::XMLElement * robot = doc.FirstChildElement("robot");
  if (!robot) {
    throw std::runtime_error("no <robot> in " + urdf_path);
  }
  for (const tinyxml2::XMLElement * j = robot->FirstChildElement("joint"); j != nullptr;
    j = j->NextSiblingElement("joint"))
  {
    const char * name = j->Attribute("name");
    if (!name || std::string(name) != joint_name) {
      continue;
    }
    const tinyxml2::XMLElement * origin = j->FirstChildElement("origin");
    if (!origin) {
      throw std::runtime_error(
        std::string("joint \"") + joint_name + "\" has no <origin> in " + urdf_path);
    }
    const char * xyz_s = origin->Attribute("xyz");
    const char * rpy_s = origin->Attribute("rpy");
    if (!xyz_s || !rpy_s) {
      throw std::runtime_error(
        std::string("joint \"") + joint_name + "\" <origin> missing xyz/rpy in " + urdf_path);
    }
    double x = 0.0;
    double y = 0.0;
    double z = 0.0;
    double rr = 0.0;
    double pp = 0.0;
    double yy = 0.0;
    {
      std::istringstream iss(xyz_s);
      if (!(iss >> x >> y >> z)) {
        throw std::runtime_error("bad xyz on joint \"" + std::string(joint_name) + "\"");
      }
    }
    {
      std::istringstream iss(rpy_s);
      if (!(iss >> rr >> pp >> yy)) {
        throw std::runtime_error("bad rpy on joint \"" + std::string(joint_name) + "\"");
      }
    }
    return LaserOffset{x, y, yy};
  }
  throw std::runtime_error(
    std::string("joint \"") + joint_name + "\" not found in " + urdf_path);
}

std::string m3pro_urdf_path()
{
  const std::string share =
    ament_index_cpp::get_package_share_directory("m3pro_world_bringup");
  return share + "/urdf/M3Pro.urdf";
}

}  // namespace

// Merge front/rear 2D LaserScan into one virtual 360° scan on base_footprint for SLAM.
class MultiLidarMerger : public rclcpp::Node
{
public:
  MultiLidarMerger()
  : Node("multi_lidar_merger")
  {
    const std::string urdf_path = m3pro_urdf_path();
    try {
      front_ = load_laser_mount_xy_yaw_from_urdf(urdf_path, "laser_front_joint");
      rear_ = load_laser_mount_xy_yaw_from_urdf(urdf_path, "laser_rear_joint");
    } catch (const std::exception & e) {
      RCLCPP_FATAL(get_logger(), "%s", e.what());
      throw;
    }
    RCLCPP_INFO(
      get_logger(),
      "Laser mounts from URDF (%s): front (%.5f, %.5f, %.5f), rear (%.5f, %.5f, %.5f)",
      urdf_path.c_str(),
      front_.x, front_.y, front_.yaw,
      rear_.x, rear_.y, rear_.yaw);

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

  LaserOffset front_{};
  LaserOffset rear_{};
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