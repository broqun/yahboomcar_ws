// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from arm_interface:msg/CurJoints.idl
// generated code does not contain a copyright notice
#include "arm_interface/msg/detail/cur_joints__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `joints`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
arm_interface__msg__CurJoints__init(arm_interface__msg__CurJoints * msg)
{
  if (!msg) {
    return false;
  }
  // joints
  if (!rosidl_runtime_c__int16__Sequence__init(&msg->joints, 0)) {
    arm_interface__msg__CurJoints__fini(msg);
    return false;
  }
  return true;
}

void
arm_interface__msg__CurJoints__fini(arm_interface__msg__CurJoints * msg)
{
  if (!msg) {
    return;
  }
  // joints
  rosidl_runtime_c__int16__Sequence__fini(&msg->joints);
}

bool
arm_interface__msg__CurJoints__are_equal(const arm_interface__msg__CurJoints * lhs, const arm_interface__msg__CurJoints * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // joints
  if (!rosidl_runtime_c__int16__Sequence__are_equal(
      &(lhs->joints), &(rhs->joints)))
  {
    return false;
  }
  return true;
}

bool
arm_interface__msg__CurJoints__copy(
  const arm_interface__msg__CurJoints * input,
  arm_interface__msg__CurJoints * output)
{
  if (!input || !output) {
    return false;
  }
  // joints
  if (!rosidl_runtime_c__int16__Sequence__copy(
      &(input->joints), &(output->joints)))
  {
    return false;
  }
  return true;
}

arm_interface__msg__CurJoints *
arm_interface__msg__CurJoints__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  arm_interface__msg__CurJoints * msg = (arm_interface__msg__CurJoints *)allocator.allocate(sizeof(arm_interface__msg__CurJoints), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(arm_interface__msg__CurJoints));
  bool success = arm_interface__msg__CurJoints__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
arm_interface__msg__CurJoints__destroy(arm_interface__msg__CurJoints * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    arm_interface__msg__CurJoints__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
arm_interface__msg__CurJoints__Sequence__init(arm_interface__msg__CurJoints__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  arm_interface__msg__CurJoints * data = NULL;

  if (size) {
    data = (arm_interface__msg__CurJoints *)allocator.zero_allocate(size, sizeof(arm_interface__msg__CurJoints), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = arm_interface__msg__CurJoints__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        arm_interface__msg__CurJoints__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
arm_interface__msg__CurJoints__Sequence__fini(arm_interface__msg__CurJoints__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      arm_interface__msg__CurJoints__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

arm_interface__msg__CurJoints__Sequence *
arm_interface__msg__CurJoints__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  arm_interface__msg__CurJoints__Sequence * array = (arm_interface__msg__CurJoints__Sequence *)allocator.allocate(sizeof(arm_interface__msg__CurJoints__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = arm_interface__msg__CurJoints__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
arm_interface__msg__CurJoints__Sequence__destroy(arm_interface__msg__CurJoints__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    arm_interface__msg__CurJoints__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
arm_interface__msg__CurJoints__Sequence__are_equal(const arm_interface__msg__CurJoints__Sequence * lhs, const arm_interface__msg__CurJoints__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!arm_interface__msg__CurJoints__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
arm_interface__msg__CurJoints__Sequence__copy(
  const arm_interface__msg__CurJoints__Sequence * input,
  arm_interface__msg__CurJoints__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(arm_interface__msg__CurJoints);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    arm_interface__msg__CurJoints * data =
      (arm_interface__msg__CurJoints *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!arm_interface__msg__CurJoints__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          arm_interface__msg__CurJoints__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!arm_interface__msg__CurJoints__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
