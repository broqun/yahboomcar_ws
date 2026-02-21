// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from pkg_interfaces:srv/Add.idl
// generated code does not contain a copyright notice
#include "pkg_interfaces/srv/detail/add__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
pkg_interfaces__srv__Add_Request__init(pkg_interfaces__srv__Add_Request * msg)
{
  if (!msg) {
    return false;
  }
  // num1
  // num2
  return true;
}

void
pkg_interfaces__srv__Add_Request__fini(pkg_interfaces__srv__Add_Request * msg)
{
  if (!msg) {
    return;
  }
  // num1
  // num2
}

bool
pkg_interfaces__srv__Add_Request__are_equal(const pkg_interfaces__srv__Add_Request * lhs, const pkg_interfaces__srv__Add_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // num1
  if (lhs->num1 != rhs->num1) {
    return false;
  }
  // num2
  if (lhs->num2 != rhs->num2) {
    return false;
  }
  return true;
}

bool
pkg_interfaces__srv__Add_Request__copy(
  const pkg_interfaces__srv__Add_Request * input,
  pkg_interfaces__srv__Add_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // num1
  output->num1 = input->num1;
  // num2
  output->num2 = input->num2;
  return true;
}

pkg_interfaces__srv__Add_Request *
pkg_interfaces__srv__Add_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pkg_interfaces__srv__Add_Request * msg = (pkg_interfaces__srv__Add_Request *)allocator.allocate(sizeof(pkg_interfaces__srv__Add_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(pkg_interfaces__srv__Add_Request));
  bool success = pkg_interfaces__srv__Add_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
pkg_interfaces__srv__Add_Request__destroy(pkg_interfaces__srv__Add_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    pkg_interfaces__srv__Add_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
pkg_interfaces__srv__Add_Request__Sequence__init(pkg_interfaces__srv__Add_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pkg_interfaces__srv__Add_Request * data = NULL;

  if (size) {
    data = (pkg_interfaces__srv__Add_Request *)allocator.zero_allocate(size, sizeof(pkg_interfaces__srv__Add_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = pkg_interfaces__srv__Add_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        pkg_interfaces__srv__Add_Request__fini(&data[i - 1]);
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
pkg_interfaces__srv__Add_Request__Sequence__fini(pkg_interfaces__srv__Add_Request__Sequence * array)
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
      pkg_interfaces__srv__Add_Request__fini(&array->data[i]);
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

pkg_interfaces__srv__Add_Request__Sequence *
pkg_interfaces__srv__Add_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pkg_interfaces__srv__Add_Request__Sequence * array = (pkg_interfaces__srv__Add_Request__Sequence *)allocator.allocate(sizeof(pkg_interfaces__srv__Add_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = pkg_interfaces__srv__Add_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
pkg_interfaces__srv__Add_Request__Sequence__destroy(pkg_interfaces__srv__Add_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    pkg_interfaces__srv__Add_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
pkg_interfaces__srv__Add_Request__Sequence__are_equal(const pkg_interfaces__srv__Add_Request__Sequence * lhs, const pkg_interfaces__srv__Add_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!pkg_interfaces__srv__Add_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
pkg_interfaces__srv__Add_Request__Sequence__copy(
  const pkg_interfaces__srv__Add_Request__Sequence * input,
  pkg_interfaces__srv__Add_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(pkg_interfaces__srv__Add_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    pkg_interfaces__srv__Add_Request * data =
      (pkg_interfaces__srv__Add_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!pkg_interfaces__srv__Add_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          pkg_interfaces__srv__Add_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!pkg_interfaces__srv__Add_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
pkg_interfaces__srv__Add_Response__init(pkg_interfaces__srv__Add_Response * msg)
{
  if (!msg) {
    return false;
  }
  // sum
  return true;
}

void
pkg_interfaces__srv__Add_Response__fini(pkg_interfaces__srv__Add_Response * msg)
{
  if (!msg) {
    return;
  }
  // sum
}

bool
pkg_interfaces__srv__Add_Response__are_equal(const pkg_interfaces__srv__Add_Response * lhs, const pkg_interfaces__srv__Add_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // sum
  if (lhs->sum != rhs->sum) {
    return false;
  }
  return true;
}

bool
pkg_interfaces__srv__Add_Response__copy(
  const pkg_interfaces__srv__Add_Response * input,
  pkg_interfaces__srv__Add_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // sum
  output->sum = input->sum;
  return true;
}

pkg_interfaces__srv__Add_Response *
pkg_interfaces__srv__Add_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pkg_interfaces__srv__Add_Response * msg = (pkg_interfaces__srv__Add_Response *)allocator.allocate(sizeof(pkg_interfaces__srv__Add_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(pkg_interfaces__srv__Add_Response));
  bool success = pkg_interfaces__srv__Add_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
pkg_interfaces__srv__Add_Response__destroy(pkg_interfaces__srv__Add_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    pkg_interfaces__srv__Add_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
pkg_interfaces__srv__Add_Response__Sequence__init(pkg_interfaces__srv__Add_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pkg_interfaces__srv__Add_Response * data = NULL;

  if (size) {
    data = (pkg_interfaces__srv__Add_Response *)allocator.zero_allocate(size, sizeof(pkg_interfaces__srv__Add_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = pkg_interfaces__srv__Add_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        pkg_interfaces__srv__Add_Response__fini(&data[i - 1]);
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
pkg_interfaces__srv__Add_Response__Sequence__fini(pkg_interfaces__srv__Add_Response__Sequence * array)
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
      pkg_interfaces__srv__Add_Response__fini(&array->data[i]);
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

pkg_interfaces__srv__Add_Response__Sequence *
pkg_interfaces__srv__Add_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pkg_interfaces__srv__Add_Response__Sequence * array = (pkg_interfaces__srv__Add_Response__Sequence *)allocator.allocate(sizeof(pkg_interfaces__srv__Add_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = pkg_interfaces__srv__Add_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
pkg_interfaces__srv__Add_Response__Sequence__destroy(pkg_interfaces__srv__Add_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    pkg_interfaces__srv__Add_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
pkg_interfaces__srv__Add_Response__Sequence__are_equal(const pkg_interfaces__srv__Add_Response__Sequence * lhs, const pkg_interfaces__srv__Add_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!pkg_interfaces__srv__Add_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
pkg_interfaces__srv__Add_Response__Sequence__copy(
  const pkg_interfaces__srv__Add_Response__Sequence * input,
  pkg_interfaces__srv__Add_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(pkg_interfaces__srv__Add_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    pkg_interfaces__srv__Add_Response * data =
      (pkg_interfaces__srv__Add_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!pkg_interfaces__srv__Add_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          pkg_interfaces__srv__Add_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!pkg_interfaces__srv__Add_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
