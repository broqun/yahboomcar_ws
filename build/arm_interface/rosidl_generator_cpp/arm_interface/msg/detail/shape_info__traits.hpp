// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from arm_interface:msg/ShapeInfo.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__SHAPE_INFO__TRAITS_HPP_
#define ARM_INTERFACE__MSG__DETAIL__SHAPE_INFO__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "arm_interface/msg/detail/shape_info__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace arm_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const ShapeInfo & msg,
  std::ostream & out)
{
  out << "{";
  // member: value
  {
    if (msg.value.size() == 0) {
      out << "value: []";
    } else {
      out << "value: [";
      size_t pending_items = msg.value.size();
      for (auto item : msg.value) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ShapeInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.value.size() == 0) {
      out << "value: []\n";
    } else {
      out << "value:\n";
      for (auto item : msg.value) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ShapeInfo & msg, bool use_flow_style = false)
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
  const arm_interface::msg::ShapeInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const arm_interface::msg::ShapeInfo & msg)
{
  return arm_interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<arm_interface::msg::ShapeInfo>()
{
  return "arm_interface::msg::ShapeInfo";
}

template<>
inline const char * name<arm_interface::msg::ShapeInfo>()
{
  return "arm_interface/msg/ShapeInfo";
}

template<>
struct has_fixed_size<arm_interface::msg::ShapeInfo>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<arm_interface::msg::ShapeInfo>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<arm_interface::msg::ShapeInfo>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ARM_INTERFACE__MSG__DETAIL__SHAPE_INFO__TRAITS_HPP_
