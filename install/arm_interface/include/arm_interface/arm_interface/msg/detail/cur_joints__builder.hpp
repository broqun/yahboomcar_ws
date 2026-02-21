// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_interface:msg/CurJoints.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__CUR_JOINTS__BUILDER_HPP_
#define ARM_INTERFACE__MSG__DETAIL__CUR_JOINTS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "arm_interface/msg/detail/cur_joints__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace arm_interface
{

namespace msg
{

namespace builder
{

class Init_CurJoints_joints
{
public:
  Init_CurJoints_joints()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::arm_interface::msg::CurJoints joints(::arm_interface::msg::CurJoints::_joints_type arg)
  {
    msg_.joints = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interface::msg::CurJoints msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interface::msg::CurJoints>()
{
  return arm_interface::msg::builder::Init_CurJoints_joints();
}

}  // namespace arm_interface

#endif  // ARM_INTERFACE__MSG__DETAIL__CUR_JOINTS__BUILDER_HPP_
