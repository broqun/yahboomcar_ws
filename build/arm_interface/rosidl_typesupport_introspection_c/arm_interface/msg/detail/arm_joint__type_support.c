// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from arm_interface:msg/ArmJoint.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "arm_interface/msg/detail/arm_joint__rosidl_typesupport_introspection_c.h"
#include "arm_interface/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "arm_interface/msg/detail/arm_joint__functions.h"
#include "arm_interface/msg/detail/arm_joint__struct.h"


// Include directives for member types
// Member `joints`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__ArmJoint_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  arm_interface__msg__ArmJoint__init(message_memory);
}

void arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__ArmJoint_fini_function(void * message_memory)
{
  arm_interface__msg__ArmJoint__fini(message_memory);
}

size_t arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__size_function__ArmJoint__joints(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__get_const_function__ArmJoint__joints(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__get_function__ArmJoint__joints(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__fetch_function__ArmJoint__joints(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__get_const_function__ArmJoint__joints(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__assign_function__ArmJoint__joints(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__get_function__ArmJoint__joints(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__resize_function__ArmJoint__joints(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__ArmJoint_message_member_array[4] = {
  {
    "id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_interface__msg__ArmJoint, id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "run_time",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_interface__msg__ArmJoint, run_time),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "angle",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_interface__msg__ArmJoint, angle),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "joints",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_interface__msg__ArmJoint, joints),  // bytes offset in struct
    NULL,  // default value
    arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__size_function__ArmJoint__joints,  // size() function pointer
    arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__get_const_function__ArmJoint__joints,  // get_const(index) function pointer
    arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__get_function__ArmJoint__joints,  // get(index) function pointer
    arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__fetch_function__ArmJoint__joints,  // fetch(index, &value) function pointer
    arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__assign_function__ArmJoint__joints,  // assign(index, value) function pointer
    arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__resize_function__ArmJoint__joints  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__ArmJoint_message_members = {
  "arm_interface__msg",  // message namespace
  "ArmJoint",  // message name
  4,  // number of fields
  sizeof(arm_interface__msg__ArmJoint),
  arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__ArmJoint_message_member_array,  // message members
  arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__ArmJoint_init_function,  // function to initialize message memory (memory has to be allocated)
  arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__ArmJoint_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__ArmJoint_message_type_support_handle = {
  0,
  &arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__ArmJoint_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_arm_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_interface, msg, ArmJoint)() {
  if (!arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__ArmJoint_message_type_support_handle.typesupport_identifier) {
    arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__ArmJoint_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &arm_interface__msg__ArmJoint__rosidl_typesupport_introspection_c__ArmJoint_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
