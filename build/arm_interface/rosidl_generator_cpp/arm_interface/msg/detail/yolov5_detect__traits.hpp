// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from arm_interface:msg/Yolov5Detect.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__YOLOV5_DETECT__TRAITS_HPP_
#define ARM_INTERFACE__MSG__DETAIL__YOLOV5_DETECT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "arm_interface/msg/detail/yolov5_detect__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace arm_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const Yolov5Detect & msg,
  std::ostream & out)
{
  out << "{";
  // member: result
  {
    out << "result: ";
    rosidl_generator_traits::value_to_yaml(msg.result, out);
    out << ", ";
  }

  // member: centerx
  {
    out << "centerx: ";
    rosidl_generator_traits::value_to_yaml(msg.centerx, out);
    out << ", ";
  }

  // member: centery
  {
    out << "centery: ";
    rosidl_generator_traits::value_to_yaml(msg.centery, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Yolov5Detect & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result: ";
    rosidl_generator_traits::value_to_yaml(msg.result, out);
    out << "\n";
  }

  // member: centerx
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "centerx: ";
    rosidl_generator_traits::value_to_yaml(msg.centerx, out);
    out << "\n";
  }

  // member: centery
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "centery: ";
    rosidl_generator_traits::value_to_yaml(msg.centery, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Yolov5Detect & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace arm_interface

namespace rosidl_generator_traits
{

[[deprecated("use arm_interface::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_interface::msg::Yolov5Detect & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const arm_interface::msg::Yolov5Detect & msg)
{
  return arm_interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<arm_interface::msg::Yolov5Detect>()
{
  return "arm_interface::msg::Yolov5Detect";
}

template<>
inline const char * name<arm_interface::msg::Yolov5Detect>()
{
  return "arm_interface/msg/Yolov5Detect";
}

template<>
struct has_fixed_size<arm_interface::msg::Yolov5Detect>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<arm_interface::msg::Yolov5Detect>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<arm_interface::msg::Yolov5Detect>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ARM_INTERFACE__MSG__DETAIL__YOLOV5_DETECT__TRAITS_HPP_
