// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_interface:msg/TargetXYRoll.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__TARGET_XY_ROLL__BUILDER_HPP_
#define ARM_INTERFACE__MSG__DETAIL__TARGET_XY_ROLL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "arm_interface/msg/detail/target_xy_roll__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace arm_interface
{

namespace msg
{

namespace builder
{

class Init_TargetXYRoll_roll
{
public:
  explicit Init_TargetXYRoll_roll(::arm_interface::msg::TargetXYRoll & msg)
  : msg_(msg)
  {}
  ::arm_interface::msg::TargetXYRoll roll(::arm_interface::msg::TargetXYRoll::_roll_type arg)
  {
    msg_.roll = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interface::msg::TargetXYRoll msg_;
};

class Init_TargetXYRoll_y
{
public:
  explicit Init_TargetXYRoll_y(::arm_interface::msg::TargetXYRoll & msg)
  : msg_(msg)
  {}
  Init_TargetXYRoll_roll y(::arm_interface::msg::TargetXYRoll::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_TargetXYRoll_roll(msg_);
  }

private:
  ::arm_interface::msg::TargetXYRoll msg_;
};

class Init_TargetXYRoll_x
{
public:
  Init_TargetXYRoll_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TargetXYRoll_y x(::arm_interface::msg::TargetXYRoll::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_TargetXYRoll_y(msg_);
  }

private:
  ::arm_interface::msg::TargetXYRoll msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interface::msg::TargetXYRoll>()
{
  return arm_interface::msg::builder::Init_TargetXYRoll_x();
}

}  // namespace arm_interface

#endif  // ARM_INTERFACE__MSG__DETAIL__TARGET_XY_ROLL__BUILDER_HPP_
