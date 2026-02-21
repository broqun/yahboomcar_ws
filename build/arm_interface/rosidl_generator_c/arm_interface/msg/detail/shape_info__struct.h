// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from arm_interface:msg/ShapeInfo.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__SHAPE_INFO__STRUCT_H_
#define ARM_INTERFACE__MSG__DETAIL__SHAPE_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'value'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/ShapeInfo in the package arm_interface.
typedef struct arm_interface__msg__ShapeInfo
{
  rosidl_runtime_c__float__Sequence value;
} arm_interface__msg__ShapeInfo;

// Struct for a sequence of arm_interface__msg__ShapeInfo.
typedef struct arm_interface__msg__ShapeInfo__Sequence
{
  arm_interface__msg__ShapeInfo * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_interface__msg__ShapeInfo__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARM_INTERFACE__MSG__DETAIL__SHAPE_INFO__STRUCT_H_
