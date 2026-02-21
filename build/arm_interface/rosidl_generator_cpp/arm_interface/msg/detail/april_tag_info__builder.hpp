// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_interface:msg/AprilTagInfo.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__APRIL_TAG_INFO__BUILDER_HPP_
#define ARM_INTERFACE__MSG__DETAIL__APRIL_TAG_INFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "arm_interface/msg/detail/april_tag_info__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace arm_interface
{

namespace msg
{

namespace builder
{

class Init_AprilTagInfo_z
{
public:
  explicit Init_AprilTagInfo_z(::arm_interface::msg::AprilTagInfo & msg)
  : msg_(msg)
  {}
  ::arm_interface::msg::AprilTagInfo z(::arm_interface::msg::AprilTagInfo::_z_type arg)
  {
    msg_.z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interface::msg::AprilTagInfo msg_;
};

class Init_AprilTagInfo_y
{
public:
  explicit Init_AprilTagInfo_y(::arm_interface::msg::AprilTagInfo & msg)
  : msg_(msg)
  {}
  Init_AprilTagInfo_z y(::arm_interface::msg::AprilTagInfo::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_AprilTagInfo_z(msg_);
  }

private:
  ::arm_interface::msg::AprilTagInfo msg_;
};

class Init_AprilTagInfo_x
{
public:
  explicit Init_AprilTagInfo_x(::arm_interface::msg::AprilTagInfo & msg)
  : msg_(msg)
  {}
  Init_AprilTagInfo_y x(::arm_interface::msg::AprilTagInfo::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_AprilTagInfo_y(msg_);
  }

private:
  ::arm_interface::msg::AprilTagInfo msg_;
};

class Init_AprilTagInfo_id
{
public:
  Init_AprilTagInfo_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AprilTagInfo_x id(::arm_interface::msg::AprilTagInfo::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_AprilTagInfo_x(msg_);
  }

private:
  ::arm_interface::msg::AprilTagInfo msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interface::msg::AprilTagInfo>()
{
  return arm_interface::msg::builder::Init_AprilTagInfo_id();
}

}  // namespace arm_interface

#endif  // ARM_INTERFACE__MSG__DETAIL__APRIL_TAG_INFO__BUILDER_HPP_
