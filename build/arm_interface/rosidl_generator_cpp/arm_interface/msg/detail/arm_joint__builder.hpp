// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_interface:msg/ArmJoint.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__ARM_JOINT__BUILDER_HPP_
#define ARM_INTERFACE__MSG__DETAIL__ARM_JOINT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "arm_interface/msg/detail/arm_joint__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace arm_interface
{

namespace msg
{

namespace builder
{

class Init_ArmJoint_joints
{
public:
  explicit Init_ArmJoint_joints(::arm_interface::msg::ArmJoint & msg)
  : msg_(msg)
  {}
  ::arm_interface::msg::ArmJoint joints(::arm_interface::msg::ArmJoint::_joints_type arg)
  {
    msg_.joints = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interface::msg::ArmJoint msg_;
};

class Init_ArmJoint_angle
{
public:
  explicit Init_ArmJoint_angle(::arm_interface::msg::ArmJoint & msg)
  : msg_(msg)
  {}
  Init_ArmJoint_joints angle(::arm_interface::msg::ArmJoint::_angle_type arg)
  {
    msg_.angle = std::move(arg);
    return Init_ArmJoint_joints(msg_);
  }

private:
  ::arm_interface::msg::ArmJoint msg_;
};

class Init_ArmJoint_run_time
{
public:
  explicit Init_ArmJoint_run_time(::arm_interface::msg::ArmJoint & msg)
  : msg_(msg)
  {}
  Init_ArmJoint_angle run_time(::arm_interface::msg::ArmJoint::_run_time_type arg)
  {
    msg_.run_time = std::move(arg);
    return Init_ArmJoint_angle(msg_);
  }

private:
  ::arm_interface::msg::ArmJoint msg_;
};

class Init_ArmJoint_id
{
public:
  Init_ArmJoint_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ArmJoint_run_time id(::arm_interface::msg::ArmJoint::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_ArmJoint_run_time(msg_);
  }

private:
  ::arm_interface::msg::ArmJoint msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interface::msg::ArmJoint>()
{
  return arm_interface::msg::builder::Init_ArmJoint_id();
}

}  // namespace arm_interface

#endif  // ARM_INTERFACE__MSG__DETAIL__ARM_JOINT__BUILDER_HPP_
