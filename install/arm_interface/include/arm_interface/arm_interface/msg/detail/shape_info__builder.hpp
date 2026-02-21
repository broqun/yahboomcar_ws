// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_interface:msg/ShapeInfo.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__SHAPE_INFO__BUILDER_HPP_
#define ARM_INTERFACE__MSG__DETAIL__SHAPE_INFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "arm_interface/msg/detail/shape_info__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace arm_interface
{

namespace msg
{

namespace builder
{

class Init_ShapeInfo_value
{
public:
  Init_ShapeInfo_value()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::arm_interface::msg::ShapeInfo value(::arm_interface::msg::ShapeInfo::_value_type arg)
  {
    msg_.value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interface::msg::ShapeInfo msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interface::msg::ShapeInfo>()
{
  return arm_interface::msg::builder::Init_ShapeInfo_value();
}

}  // namespace arm_interface

#endif  // ARM_INTERFACE__MSG__DETAIL__SHAPE_INFO__BUILDER_HPP_
