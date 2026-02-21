#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <geometry_msgs/msg/pose.hpp>
#include <random>

class SetTargetPosition : public rclcpp::Node
{
public:
  SetTargetPosition()
    : Node("set_target_position")
  {
    // 初始化其他内容
    RCLCPP_INFO(this->get_logger(), "Initializing RandomMoveIt2Control.");
  }

  void initialize()
  {
    // 在此函数中初始化 move_group_interface_ 和 planning_scene_interface_
    move_group_interface_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(shared_from_this(), "arm_group");
    planning_scene_interface_ = std::make_shared<moveit::planning_interface::PlanningSceneInterface>();

    move_group_interface_->setNumPlanningAttempts(10);  // 设置最大规划尝试次数为 10
    move_group_interface_->setPlanningTime(5.0);         // 设置每次规划的最大时间为 5 秒

    // 设置随机数生成器
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(-0.1, 0.1);

    //std::vector<double> target_joints = {0.79, 0.79, -1.57, -1.57, 0}; // 目标关节角度（单位：弧度）

        // 设置目标关节空间值
    //move_group_interface_->setJointValueTarget(target_joints);
    // 设置目标位置
    geometry_msgs::msg::Pose target_pose;
    target_pose.orientation.x = 4.10678e-05;
    target_pose.orientation.y = 0.713247;
    target_pose.orientation.z = 2.25082e-05;
    target_pose.orientation.w = 0.700913;
    target_pose.position.x = 0.0830882;
    target_pose.position.y = -1.92146e-05;
    target_pose.position.z = 0.354935;

    // 设置目标位置
    move_group_interface_->setPoseTarget(target_pose);

    // 规划路径
    moveit::planning_interface::MoveGroupInterface::Plan my_plan;
    bool success = (move_group_interface_->plan(my_plan) == moveit::core::MoveItErrorCode::SUCCESS);

    if (success)
    {
      RCLCPP_INFO(this->get_logger(), "Planning succeeded, moving the arm.");
      move_group_interface_->execute(my_plan);


    }
    else
    {
      RCLCPP_ERROR(this->get_logger(), "Planning failed!");
    }
    auto current_pose = move_group_interface_->getCurrentPose();
    RCLCPP_INFO(this->get_logger(), "Current Pose: x=%f, y=%f, z=%f",
            current_pose.pose.position.x,
            current_pose.pose.position.y,
            current_pose.pose.position.z);
  }

private:
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface_;
  std::shared_ptr<moveit::planning_interface::PlanningSceneInterface> planning_scene_interface_;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<SetTargetPosition>();
  
  // 延迟初始化
  node->initialize();

  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
