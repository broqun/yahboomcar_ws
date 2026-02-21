// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_interface:msg/Position.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__POSITION__BUILDER_HPP_
#define ARM_INTERFACE__MSG__DETAIL__POSITION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "arm_interface/msg/detail/position__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace arm_interface
{

namespace msg
{

namespace builder
{

class Init_Position_z
{
public:
  explicit Init_Position_z(::arm_interface::msg::Position & msg)
  : msg_(msg)
  {}
  ::arm_interface::msg::Position z(::arm_interface::msg::Position::_z_type arg)
  {
    msg_.z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interface::msg::Position msg_;
};

class Init_Position_y
{
public:
  explicit Init_Position_y(::arm_interface::msg::Position & msg)
  : msg_(msg)
  {}
  Init_Position_z y(::arm_interface::msg::Position::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Position_z(msg_);
  }

private:
  ::arm_interface::msg::Position msg_;
};

class Init_Position_x
{
public:
  Init_Position_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Position_y x(::arm_interface::msg::Position::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Position_y(msg_);
  }

private:
  ::arm_interface::msg::Position msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interface::msg::Position>()
{
  return arm_interface::msg::builder::Init_Position_x();
}

}  // namespace arm_interface

#endif  // ARM_INTERFACE__MSG__DETAIL__POSITION__BUILDER_HPP_
