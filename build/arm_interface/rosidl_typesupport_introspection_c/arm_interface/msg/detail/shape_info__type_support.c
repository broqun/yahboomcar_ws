// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from arm_interface:msg/ShapeInfo.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "arm_interface/msg/detail/shape_info__rosidl_typesupport_introspection_c.h"
#include "arm_interface/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "arm_interface/msg/detail/shape_info__functions.h"
#include "arm_interface/msg/detail/shape_info__struct.h"


// Include directives for member types
// Member `value`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__ShapeInfo_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  arm_interface__msg__ShapeInfo__init(message_memory);
}

void arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__ShapeInfo_fini_function(void * message_memory)
{
  arm_interface__msg__ShapeInfo__fini(message_memory);
}

size_t arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__size_function__ShapeInfo__value(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__get_const_function__ShapeInfo__value(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__get_function__ShapeInfo__value(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__fetch_function__ShapeInfo__value(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__get_const_function__ShapeInfo__value(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__assign_function__ShapeInfo__value(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__get_function__ShapeInfo__value(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__resize_function__ShapeInfo__value(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__ShapeInfo_message_member_array[1] = {
  {
    "value",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_interface__msg__ShapeInfo, value),  // bytes offset in struct
    NULL,  // default value
    arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__size_function__ShapeInfo__value,  // size() function pointer
    arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__get_const_function__ShapeInfo__value,  // get_const(index) function pointer
    arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__get_function__ShapeInfo__value,  // get(index) function pointer
    arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__fetch_function__ShapeInfo__value,  // fetch(index, &value) function pointer
    arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__assign_function__ShapeInfo__value,  // assign(index, value) function pointer
    arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__resize_function__ShapeInfo__value  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__ShapeInfo_message_members = {
  "arm_interface__msg",  // message namespace
  "ShapeInfo",  // message name
  1,  // number of fields
  sizeof(arm_interface__msg__ShapeInfo),
  arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__ShapeInfo_message_member_array,  // message members
  arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__ShapeInfo_init_function,  // function to initialize message memory (memory has to be allocated)
  arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__ShapeInfo_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__ShapeInfo_message_type_support_handle = {
  0,
  &arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__ShapeInfo_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_arm_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_interface, msg, ShapeInfo)() {
  if (!arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__ShapeInfo_message_type_support_handle.typesupport_identifier) {
    arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__ShapeInfo_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &arm_interface__msg__ShapeInfo__rosidl_typesupport_introspection_c__ShapeInfo_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
