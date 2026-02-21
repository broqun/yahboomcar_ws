// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from pkg_interfaces:srv/Add.idl
// generated code does not contain a copyright notice

#ifndef PKG_INTERFACES__SRV__DETAIL__ADD__TRAITS_HPP_
#define PKG_INTERFACES__SRV__DETAIL__ADD__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "pkg_interfaces/srv/detail/add__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace pkg_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const Add_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: num1
  {
    out << "num1: ";
    rosidl_generator_traits::value_to_yaml(msg.num1, out);
    out << ", ";
  }

  // member: num2
  {
    out << "num2: ";
    rosidl_generator_traits::value_to_yaml(msg.num2, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Add_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: num1
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "num1: ";
    rosidl_generator_traits::value_to_yaml(msg.num1, out);
    out << "\n";
  }

  // member: num2
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "num2: ";
    rosidl_generator_traits::value_to_yaml(msg.num2, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Add_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace pkg_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use pkg_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const pkg_interfaces::srv::Add_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  pkg_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pkg_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const pkg_interfaces::srv::Add_Request & msg)
{
  return pkg_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<pkg_interfaces::srv::Add_Request>()
{
  return "pkg_interfaces::srv::Add_Request";
}

template<>
inline const char * name<pkg_interfaces::srv::Add_Request>()
{
  return "pkg_interfaces/srv/Add_Request";
}

template<>
struct has_fixed_size<pkg_interfaces::srv::Add_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<pkg_interfaces::srv::Add_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<pkg_interfaces::srv::Add_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace pkg_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const Add_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: sum
  {
    out << "sum: ";
    rosidl_generator_traits::value_to_yaml(msg.sum, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Add_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: sum
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sum: ";
    rosidl_generator_traits::value_to_yaml(msg.sum, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Add_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace pkg_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use pkg_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const pkg_interfaces::srv::Add_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  pkg_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pkg_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const pkg_interfaces::srv::Add_Response & msg)
{
  return pkg_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<pkg_interfaces::srv::Add_Response>()
{
  return "pkg_interfaces::srv::Add_Response";
}

template<>
inline const char * name<pkg_interfaces::srv::Add_Response>()
{
  return "pkg_interfaces/srv/Add_Response";
}

template<>
struct has_fixed_size<pkg_interfaces::srv::Add_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<pkg_interfaces::srv::Add_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<pkg_interfaces::srv::Add_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<pkg_interfaces::srv::Add>()
{
  return "pkg_interfaces::srv::Add";
}

template<>
inline const char * name<pkg_interfaces::srv::Add>()
{
  return "pkg_interfaces/srv/Add";
}

template<>
struct has_fixed_size<pkg_interfaces::srv::Add>
  : std::integral_constant<
    bool,
    has_fixed_size<pkg_interfaces::srv::Add_Request>::value &&
    has_fixed_size<pkg_interfaces::srv::Add_Response>::value
  >
{
};

template<>
struct has_bounded_size<pkg_interfaces::srv::Add>
  : std::integral_constant<
    bool,
    has_bounded_size<pkg_interfaces::srv::Add_Request>::value &&
    has_bounded_size<pkg_interfaces::srv::Add_Response>::value
  >
{
};

template<>
struct is_service<pkg_interfaces::srv::Add>
  : std::true_type
{
};

template<>
struct is_service_request<pkg_interfaces::srv::Add_Request>
  : std::true_type
{
};

template<>
struct is_service_response<pkg_interfaces::srv::Add_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // PKG_INTERFACES__SRV__DETAIL__ADD__TRAITS_HPP_
