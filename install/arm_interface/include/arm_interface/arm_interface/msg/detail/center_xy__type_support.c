// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from arm_interface:msg/CenterXY.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "arm_interface/msg/detail/center_xy__rosidl_typesupport_introspection_c.h"
#include "arm_interface/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "arm_interface/msg/detail/center_xy__functions.h"
#include "arm_interface/msg/detail/center_xy__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void arm_interface__msg__CenterXY__rosidl_typesupport_introspection_c__CenterXY_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  arm_interface__msg__CenterXY__init(message_memory);
}

void arm_interface__msg__CenterXY__rosidl_typesupport_introspection_c__CenterXY_fini_function(void * message_memory)
{
  arm_interface__msg__CenterXY__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember arm_interface__msg__CenterXY__rosidl_typesupport_introspection_c__CenterXY_message_member_array[2] = {
  {
    "center_x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_interface__msg__CenterXY, center_x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "center_y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_interface__msg__CenterXY, center_y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers arm_interface__msg__CenterXY__rosidl_typesupport_introspection_c__CenterXY_message_members = {
  "arm_interface__msg",  // message namespace
  "CenterXY",  // message name
  2,  // number of fields
  sizeof(arm_interface__msg__CenterXY),
  arm_interface__msg__CenterXY__rosidl_typesupport_introspection_c__CenterXY_message_member_array,  // message members
  arm_interface__msg__CenterXY__rosidl_typesupport_introspection_c__CenterXY_init_function,  // function to initialize message memory (memory has to be allocated)
  arm_interface__msg__CenterXY__rosidl_typesupport_introspection_c__CenterXY_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t arm_interface__msg__CenterXY__rosidl_typesupport_introspection_c__CenterXY_message_type_support_handle = {
  0,
  &arm_interface__msg__CenterXY__rosidl_typesupport_introspection_c__CenterXY_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_arm_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_interface, msg, CenterXY)() {
  if (!arm_interface__msg__CenterXY__rosidl_typesupport_introspection_c__CenterXY_message_type_support_handle.typesupport_identifier) {
    arm_interface__msg__CenterXY__rosidl_typesupport_introspection_c__CenterXY_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &arm_interface__msg__CenterXY__rosidl_typesupport_introspection_c__CenterXY_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
