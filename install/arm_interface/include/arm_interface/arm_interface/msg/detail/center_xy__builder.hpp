// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_interface:msg/CenterXY.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__CENTER_XY__BUILDER_HPP_
#define ARM_INTERFACE__MSG__DETAIL__CENTER_XY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "arm_interface/msg/detail/center_xy__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace arm_interface
{

namespace msg
{

namespace builder
{

class Init_CenterXY_center_y
{
public:
  explicit Init_CenterXY_center_y(::arm_interface::msg::CenterXY & msg)
  : msg_(msg)
  {}
  ::arm_interface::msg::CenterXY center_y(::arm_interface::msg::CenterXY::_center_y_type arg)
  {
    msg_.center_y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interface::msg::CenterXY msg_;
};

class Init_CenterXY_center_x
{
public:
  Init_CenterXY_center_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CenterXY_center_y center_x(::arm_interface::msg::CenterXY::_center_x_type arg)
  {
    msg_.center_x = std::move(arg);
    return Init_CenterXY_center_y(msg_);
  }

private:
  ::arm_interface::msg::CenterXY msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interface::msg::CenterXY>()
{
  return arm_interface::msg::builder::Init_CenterXY_center_x();
}

}  // namespace arm_interface

#endif  // ARM_INTERFACE__MSG__DETAIL__CENTER_XY__BUILDER_HPP_
