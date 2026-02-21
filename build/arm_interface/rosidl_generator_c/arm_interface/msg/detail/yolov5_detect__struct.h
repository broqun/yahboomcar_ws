// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from arm_interface:msg/Yolov5Detect.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__YOLOV5_DETECT__STRUCT_H_
#define ARM_INTERFACE__MSG__DETAIL__YOLOV5_DETECT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'result'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/Yolov5Detect in the package arm_interface.
typedef struct arm_interface__msg__Yolov5Detect
{
  rosidl_runtime_c__String result;
  float centerx;
  float centery;
} arm_interface__msg__Yolov5Detect;

// Struct for a sequence of arm_interface__msg__Yolov5Detect.
typedef struct arm_interface__msg__Yolov5Detect__Sequence
{
  arm_interface__msg__Yolov5Detect * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_interface__msg__Yolov5Detect__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARM_INTERFACE__MSG__DETAIL__YOLOV5_DETECT__STRUCT_H_
