// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_interface:msg/Yolov5Detect.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__YOLOV5_DETECT__BUILDER_HPP_
#define ARM_INTERFACE__MSG__DETAIL__YOLOV5_DETECT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "arm_interface/msg/detail/yolov5_detect__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace arm_interface
{

namespace msg
{

namespace builder
{

class Init_Yolov5Detect_centery
{
public:
  explicit Init_Yolov5Detect_centery(::arm_interface::msg::Yolov5Detect & msg)
  : msg_(msg)
  {}
  ::arm_interface::msg::Yolov5Detect centery(::arm_interface::msg::Yolov5Detect::_centery_type arg)
  {
    msg_.centery = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interface::msg::Yolov5Detect msg_;
};

class Init_Yolov5Detect_centerx
{
public:
  explicit Init_Yolov5Detect_centerx(::arm_interface::msg::Yolov5Detect & msg)
  : msg_(msg)
  {}
  Init_Yolov5Detect_centery centerx(::arm_interface::msg::Yolov5Detect::_centerx_type arg)
  {
    msg_.centerx = std::move(arg);
    return Init_Yolov5Detect_centery(msg_);
  }

private:
  ::arm_interface::msg::Yolov5Detect msg_;
};

class Init_Yolov5Detect_result
{
public:
  Init_Yolov5Detect_result()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Yolov5Detect_centerx result(::arm_interface::msg::Yolov5Detect::_result_type arg)
  {
    msg_.result = std::move(arg);
    return Init_Yolov5Detect_centerx(msg_);
  }

private:
  ::arm_interface::msg::Yolov5Detect msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interface::msg::Yolov5Detect>()
{
  return arm_interface::msg::builder::Init_Yolov5Detect_result();
}

}  // namespace arm_interface

#endif  // ARM_INTERFACE__MSG__DETAIL__YOLOV5_DETECT__BUILDER_HPP_
