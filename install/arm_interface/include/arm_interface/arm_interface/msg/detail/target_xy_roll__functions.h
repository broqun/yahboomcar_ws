// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from arm_interface:msg/TargetXYRoll.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__TARGET_XY_ROLL__FUNCTIONS_H_
#define ARM_INTERFACE__MSG__DETAIL__TARGET_XY_ROLL__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "arm_interface/msg/rosidl_generator_c__visibility_control.h"

#include "arm_interface/msg/detail/target_xy_roll__struct.h"

/// Initialize msg/TargetXYRoll message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * arm_interface__msg__TargetXYRoll
 * )) before or use
 * arm_interface__msg__TargetXYRoll__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
bool
arm_interface__msg__TargetXYRoll__init(arm_interface__msg__TargetXYRoll * msg);

/// Finalize msg/TargetXYRoll message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
void
arm_interface__msg__TargetXYRoll__fini(arm_interface__msg__TargetXYRoll * msg);

/// Create msg/TargetXYRoll message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * arm_interface__msg__TargetXYRoll__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
arm_interface__msg__TargetXYRoll *
arm_interface__msg__TargetXYRoll__create();

/// Destroy msg/TargetXYRoll message.
/**
 * It calls
 * arm_interface__msg__TargetXYRoll__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
void
arm_interface__msg__TargetXYRoll__destroy(arm_interface__msg__TargetXYRoll * msg);

/// Check for msg/TargetXYRoll message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
bool
arm_interface__msg__TargetXYRoll__are_equal(const arm_interface__msg__TargetXYRoll * lhs, const arm_interface__msg__TargetXYRoll * rhs);

/// Copy a msg/TargetXYRoll message.
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
arm_interface__msg__TargetXYRoll__copy(
  const arm_interface__msg__TargetXYRoll * input,
  arm_interface__msg__TargetXYRoll * output);

/// Initialize array of msg/TargetXYRoll messages.
/**
 * It allocates the memory for the number of elements and calls
 * arm_interface__msg__TargetXYRoll__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
bool
arm_interface__msg__TargetXYRoll__Sequence__init(arm_interface__msg__TargetXYRoll__Sequence * array, size_t size);

/// Finalize array of msg/TargetXYRoll messages.
/**
 * It calls
 * arm_interface__msg__TargetXYRoll__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
void
arm_interface__msg__TargetXYRoll__Sequence__fini(arm_interface__msg__TargetXYRoll__Sequence * array);

/// Create array of msg/TargetXYRoll messages.
/**
 * It allocates the memory for the array and calls
 * arm_interface__msg__TargetXYRoll__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
arm_interface__msg__TargetXYRoll__Sequence *
arm_interface__msg__TargetXYRoll__Sequence__create(size_t size);

/// Destroy array of msg/TargetXYRoll messages.
/**
 * It calls
 * arm_interface__msg__TargetXYRoll__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
void
arm_interface__msg__TargetXYRoll__Sequence__destroy(arm_interface__msg__TargetXYRoll__Sequence * array);

/// Check for msg/TargetXYRoll message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_interface
bool
arm_interface__msg__TargetXYRoll__Sequence__are_equal(const arm_interface__msg__TargetXYRoll__Sequence * lhs, const arm_interface__msg__TargetXYRoll__Sequence * rhs);

/// Copy an array of msg/TargetXYRoll messages.
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
arm_interface__msg__TargetXYRoll__Sequence__copy(
  const arm_interface__msg__TargetXYRoll__Sequence * input,
  arm_interface__msg__TargetXYRoll__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // ARM_INTERFACE__MSG__DETAIL__TARGET_XY_ROLL__FUNCTIONS_H_
