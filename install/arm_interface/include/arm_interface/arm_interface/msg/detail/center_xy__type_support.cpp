// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from arm_interface:msg/CenterXY.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "arm_interface/msg/detail/center_xy__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace arm_interface
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void CenterXY_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) arm_interface::msg::CenterXY(_init);
}

void CenterXY_fini_function(void * message_memory)
{
  auto typed_message = static_cast<arm_interface::msg::CenterXY *>(message_memory);
  typed_message->~CenterXY();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember CenterXY_message_member_array[2] = {
  {
    "center_x",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_interface::msg::CenterXY, center_x),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "center_y",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_interface::msg::CenterXY, center_y),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers CenterXY_message_members = {
  "arm_interface::msg",  // message namespace
  "CenterXY",  // message name
  2,  // number of fields
  sizeof(arm_interface::msg::CenterXY),
  CenterXY_message_member_array,  // message members
  CenterXY_init_function,  // function to initialize message memory (memory has to be allocated)
  CenterXY_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t CenterXY_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &CenterXY_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace arm_interface


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<arm_interface::msg::CenterXY>()
{
  return &::arm_interface::msg::rosidl_typesupport_introspection_cpp::CenterXY_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, arm_interface, msg, CenterXY)() {
  return &::arm_interface::msg::rosidl_typesupport_introspection_cpp::CenterXY_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
