// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from arm_interface:msg/Yolov5Detect.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "arm_interface/msg/detail/yolov5_detect__struct.hpp"
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

void Yolov5Detect_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) arm_interface::msg::Yolov5Detect(_init);
}

void Yolov5Detect_fini_function(void * message_memory)
{
  auto typed_message = static_cast<arm_interface::msg::Yolov5Detect *>(message_memory);
  typed_message->~Yolov5Detect();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Yolov5Detect_message_member_array[3] = {
  {
    "result",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_interface::msg::Yolov5Detect, result),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "centerx",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_interface::msg::Yolov5Detect, centerx),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "centery",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_interface::msg::Yolov5Detect, centery),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Yolov5Detect_message_members = {
  "arm_interface::msg",  // message namespace
  "Yolov5Detect",  // message name
  3,  // number of fields
  sizeof(arm_interface::msg::Yolov5Detect),
  Yolov5Detect_message_member_array,  // message members
  Yolov5Detect_init_function,  // function to initialize message memory (memory has to be allocated)
  Yolov5Detect_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Yolov5Detect_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Yolov5Detect_message_members,
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
get_message_type_support_handle<arm_interface::msg::Yolov5Detect>()
{
  return &::arm_interface::msg::rosidl_typesupport_introspection_cpp::Yolov5Detect_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, arm_interface, msg, Yolov5Detect)() {
  return &::arm_interface::msg::rosidl_typesupport_introspection_cpp::Yolov5Detect_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
