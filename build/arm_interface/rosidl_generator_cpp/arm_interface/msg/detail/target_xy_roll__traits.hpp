// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from arm_interface:msg/TargetXYRoll.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__TARGET_XY_ROLL__TRAITS_HPP_
#define ARM_INTERFACE__MSG__DETAIL__TARGET_XY_ROLL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "arm_interface/msg/detail/target_xy_roll__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace arm_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const TargetXYRoll & msg,
  std::ostream & out)
{
  out << "{";
  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << ", ";
  }

  // member: roll
  {
    out << "roll: ";
    rosidl_generator_traits::value_to_yaml(msg.roll, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TargetXYRoll & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }

  // member: roll
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "roll: ";
    rosidl_generator_traits::value_to_yaml(msg.roll, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TargetXYRoll & msg, bool use_flow_style = false)
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
  const arm_interface::msg::TargetXYRoll & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const arm_interface::msg::TargetXYRoll & msg)
{
  return arm_interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<arm_interface::msg::TargetXYRoll>()
{
  return "arm_interface::msg::TargetXYRoll";
}

template<>
inline const char * name<arm_interface::msg::TargetXYRoll>()
{
  return "arm_interface/msg/TargetXYRoll";
}

template<>
struct has_fixed_size<arm_interface::msg::TargetXYRoll>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<arm_interface::msg::TargetXYRoll>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<arm_interface::msg::TargetXYRoll>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ARM_INTERFACE__MSG__DETAIL__TARGET_XY_ROLL__TRAITS_HPP_
