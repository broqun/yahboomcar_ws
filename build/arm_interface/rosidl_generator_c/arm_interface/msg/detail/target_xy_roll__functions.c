// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from arm_interface:msg/TargetXYRoll.idl
// generated code does not contain a copyright notice
#include "arm_interface/msg/detail/target_xy_roll__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
arm_interface__msg__TargetXYRoll__init(arm_interface__msg__TargetXYRoll * msg)
{
  if (!msg) {
    return false;
  }
  // x
  // y
  // roll
  return true;
}

void
arm_interface__msg__TargetXYRoll__fini(arm_interface__msg__TargetXYRoll * msg)
{
  if (!msg) {
    return;
  }
  // x
  // y
  // roll
}

bool
arm_interface__msg__TargetXYRoll__are_equal(const arm_interface__msg__TargetXYRoll * lhs, const arm_interface__msg__TargetXYRoll * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // roll
  if (lhs->roll != rhs->roll) {
    return false;
  }
  return true;
}

bool
arm_interface__msg__TargetXYRoll__copy(
  const arm_interface__msg__TargetXYRoll * input,
  arm_interface__msg__TargetXYRoll * output)
{
  if (!input || !output) {
    return false;
  }
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // roll
  output->roll = input->roll;
  return true;
}

arm_interface__msg__TargetXYRoll *
arm_interface__msg__TargetXYRoll__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  arm_interface__msg__TargetXYRoll * msg = (arm_interface__msg__TargetXYRoll *)allocator.allocate(sizeof(arm_interface__msg__TargetXYRoll), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(arm_interface__msg__TargetXYRoll));
  bool success = arm_interface__msg__TargetXYRoll__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
arm_interface__msg__TargetXYRoll__destroy(arm_interface__msg__TargetXYRoll * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    arm_interface__msg__TargetXYRoll__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
arm_interface__msg__TargetXYRoll__Sequence__init(arm_interface__msg__TargetXYRoll__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  arm_interface__msg__TargetXYRoll * data = NULL;

  if (size) {
    data = (arm_interface__msg__TargetXYRoll *)allocator.zero_allocate(size, sizeof(arm_interface__msg__TargetXYRoll), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = arm_interface__msg__TargetXYRoll__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        arm_interface__msg__TargetXYRoll__fini(&data[i - 1]);
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
arm_interface__msg__TargetXYRoll__Sequence__fini(arm_interface__msg__TargetXYRoll__Sequence * array)
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
      arm_interface__msg__TargetXYRoll__fini(&array->data[i]);
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

arm_interface__msg__TargetXYRoll__Sequence *
arm_interface__msg__TargetXYRoll__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  arm_interface__msg__TargetXYRoll__Sequence * array = (arm_interface__msg__TargetXYRoll__Sequence *)allocator.allocate(sizeof(arm_interface__msg__TargetXYRoll__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = arm_interface__msg__TargetXYRoll__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
arm_interface__msg__TargetXYRoll__Sequence__destroy(arm_interface__msg__TargetXYRoll__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    arm_interface__msg__TargetXYRoll__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
arm_interface__msg__TargetXYRoll__Sequence__are_equal(const arm_interface__msg__TargetXYRoll__Sequence * lhs, const arm_interface__msg__TargetXYRoll__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!arm_interface__msg__TargetXYRoll__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
arm_interface__msg__TargetXYRoll__Sequence__copy(
  const arm_interface__msg__TargetXYRoll__Sequence * input,
  arm_interface__msg__TargetXYRoll__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(arm_interface__msg__TargetXYRoll);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    arm_interface__msg__TargetXYRoll * data =
      (arm_interface__msg__TargetXYRoll *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!arm_interface__msg__TargetXYRoll__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          arm_interface__msg__TargetXYRoll__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!arm_interface__msg__TargetXYRoll__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
