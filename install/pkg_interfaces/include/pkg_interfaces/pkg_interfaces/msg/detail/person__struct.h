// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from pkg_interfaces:msg/Person.idl
// generated code does not contain a copyright notice

#ifndef PKG_INTERFACES__MSG__DETAIL__PERSON__STRUCT_H_
#define PKG_INTERFACES__MSG__DETAIL__PERSON__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/Person in the package pkg_interfaces.
typedef struct pkg_interfaces__msg__Person
{
  rosidl_runtime_c__String name;
  int32_t age;
  double height;
} pkg_interfaces__msg__Person;

// Struct for a sequence of pkg_interfaces__msg__Person.
typedef struct pkg_interfaces__msg__Person__Sequence
{
  pkg_interfaces__msg__Person * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pkg_interfaces__msg__Person__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PKG_INTERFACES__MSG__DETAIL__PERSON__STRUCT_H_
