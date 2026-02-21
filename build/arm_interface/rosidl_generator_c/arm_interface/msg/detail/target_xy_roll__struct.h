// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from arm_interface:msg/TargetXYRoll.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__TARGET_XY_ROLL__STRUCT_H_
#define ARM_INTERFACE__MSG__DETAIL__TARGET_XY_ROLL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/TargetXYRoll in the package arm_interface.
typedef struct arm_interface__msg__TargetXYRoll
{
  float x;
  float y;
  float roll;
} arm_interface__msg__TargetXYRoll;

// Struct for a sequence of arm_interface__msg__TargetXYRoll.
typedef struct arm_interface__msg__TargetXYRoll__Sequence
{
  arm_interface__msg__TargetXYRoll * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_interface__msg__TargetXYRoll__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARM_INTERFACE__MSG__DETAIL__TARGET_XY_ROLL__STRUCT_H_
