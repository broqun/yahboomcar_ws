// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from arm_interface:msg/CenterXY.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__CENTER_XY__TRAITS_HPP_
#define ARM_INTERFACE__MSG__DETAIL__CENTER_XY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "arm_interface/msg/detail/center_xy__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace arm_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const CenterXY & msg,
  std::ostream & out)
{
  out << "{";
  // member: center_x
  {
    out << "center_x: ";
    rosidl_generator_traits::value_to_yaml(msg.center_x, out);
    out << ", ";
  }

  // member: center_y
  {
    out << "center_y: ";
    rosidl_generator_traits::value_to_yaml(msg.center_y, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CenterXY & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: center_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center_x: ";
    rosidl_generator_traits::value_to_yaml(msg.center_x, out);
    out << "\n";
  }

  // member: center_y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center_y: ";
    rosidl_generator_traits::value_to_yaml(msg.center_y, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CenterXY & msg, bool use_flow_style = false)
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
  const arm_interface::msg::CenterXY & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const arm_interface::msg::CenterXY & msg)
{
  return arm_interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<arm_interface::msg::CenterXY>()
{
  return "arm_interface::msg::CenterXY";
}

template<>
inline const char * name<arm_interface::msg::CenterXY>()
{
  return "arm_interface/msg/CenterXY";
}

template<>
struct has_fixed_size<arm_interface::msg::CenterXY>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<arm_interface::msg::CenterXY>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<arm_interface::msg::CenterXY>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ARM_INTERFACE__MSG__DETAIL__CENTER_XY__TRAITS_HPP_
