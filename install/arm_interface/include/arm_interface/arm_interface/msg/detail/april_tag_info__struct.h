// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from arm_interface:msg/AprilTagInfo.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__APRIL_TAG_INFO__STRUCT_H_
#define ARM_INTERFACE__MSG__DETAIL__APRIL_TAG_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/AprilTagInfo in the package arm_interface.
typedef struct arm_interface__msg__AprilTagInfo
{
  int16_t id;
  float x;
  float y;
  float z;
} arm_interface__msg__AprilTagInfo;

// Struct for a sequence of arm_interface__msg__AprilTagInfo.
typedef struct arm_interface__msg__AprilTagInfo__Sequence
{
  arm_interface__msg__AprilTagInfo * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_interface__msg__AprilTagInfo__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARM_INTERFACE__MSG__DETAIL__APRIL_TAG_INFO__STRUCT_H_
