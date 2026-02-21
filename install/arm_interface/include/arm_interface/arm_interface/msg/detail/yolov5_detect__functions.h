// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from arm_interface:msg/Yolov5Detect.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__YOLOV5_DETECT__FUNCTIONS_H_
#define ARM_INTERFACE__MSG__DETAIL__YOLOV5_DETECT__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "arm_interface/msg/rosidl_generator_c__visibility_control.h"

#include "arm_interface/msg/detail/yolov5_detect__struct.h"

/// Initialize msg/Yolov5Detect message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * arm_interface__msg__Yolov5Detect
 * )) before or use
 * arm_interface__msg__Yolov5Detect__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
bool
arm_interface__msg__Yolov5Detect__init(arm_interface__msg__Yolov5Detect * msg);

/// Finalize msg/Yolov5Detect message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
void
arm_interface__msg__Yolov5Detect__fini(arm_interface__msg__Yolov5Detect * msg);

/// Create msg/Yolov5Detect message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * arm_interface__msg__Yolov5Detect__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
arm_interface__msg__Yolov5Detect *
arm_interface__msg__Yolov5Detect__create();

/// Destroy msg/Yolov5Detect message.
/**
 * It calls
 * arm_interface__msg__Yolov5Detect__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
void
arm_interface__msg__Yolov5Detect__destroy(arm_interface__msg__Yolov5Detect * msg);

/// Check for msg/Yolov5Detect message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
bool
arm_interface__msg__Yolov5Detect__are_equal(const arm_interface__msg__Yolov5Detect * lhs, const arm_interface__msg__Yolov5Detect * rhs);

/// Copy a msg/Yolov5Detect message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
bool
arm_interface__msg__Yolov5Detect__copy(
  const arm_interface__msg__Yolov5Detect * input,
  arm_interface__msg__Yolov5Detect * output);

/// Initialize array of msg/Yolov5Detect messages.
/**
 * It allocates the memory for the number of elements and calls
 * arm_interface__msg__Yolov5Detect__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
bool
arm_interface__msg__Yolov5Detect__Sequence__init(arm_interface__msg__Yolov5Detect__Sequence * array, size_t size);

/// Finalize array of msg/Yolov5Detect messages.
/**
 * It calls
 * arm_interface__msg__Yolov5Detect__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
void
arm_interface__msg__Yolov5Detect__Sequence__fini(arm_interface__msg__Yolov5Detect__Sequence * array);

/// Create array of msg/Yolov5Detect messages.
/**
 * It allocates the memory for the array and calls
 * arm_interface__msg__Yolov5Detect__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
arm_interface__msg__Yolov5Detect__Sequence *
arm_interface__msg__Yolov5Detect__Sequence__create(size_t size);

/// Destroy array of msg/Yolov5Detect messages.
/**
 * It calls
 * arm_interface__msg__Yolov5Detect__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
void
arm_interface__msg__Yolov5Detect__Sequence__destroy(arm_interface__msg__Yolov5Detect__Sequence * array);

/// Check for msg/Yolov5Detect message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
bool
arm_interface__msg__Yolov5Detect__Sequence__are_equal(const arm_interface__msg__Yolov5Detect__Sequence * lhs, const arm_interface__msg__Yolov5Detect__Sequence * rhs);

/// Copy an array of msg/Yolov5Detect messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
bool
arm_interface__msg__Yolov5Detect__Sequence__copy(
  const arm_interface__msg__Yolov5Detect__Sequence * input,
  arm_interface__msg__Yolov5Detect__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // ARM_INTERFACE__MSG__DETAIL__YOLOV5_DETECT__FUNCTIONS_H_
