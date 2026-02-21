// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from arm_interface:msg/CenterXY.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__CENTER_XY__STRUCT_H_
#define ARM_INTERFACE__MSG__DETAIL__CENTER_XY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/CenterXY in the package arm_interface.
typedef struct arm_interface__msg__CenterXY
{
  float center_x;
  float center_y;
} arm_interface__msg__CenterXY;

// Struct for a sequence of arm_interface__msg__CenterXY.
typedef struct arm_interface__msg__CenterXY__Sequence
{
  arm_interface__msg__CenterXY * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_interface__msg__CenterXY__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARM_INTERFACE__MSG__DETAIL__CENTER_XY__STRUCT_H_
