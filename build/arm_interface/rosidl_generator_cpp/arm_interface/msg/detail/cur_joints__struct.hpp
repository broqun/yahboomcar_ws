// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from arm_interface:msg/CurJoints.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__CUR_JOINTS__STRUCT_HPP_
#define ARM_INTERFACE__MSG__DETAIL__CUR_JOINTS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__arm_interface__msg__CurJoints __attribute__((deprecated))
#else
# define DEPRECATED__arm_interface__msg__CurJoints __declspec(deprecated)
#endif

namespace arm_interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CurJoints_
{
  using Type = CurJoints_<ContainerAllocator>;

  explicit CurJoints_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit CurJoints_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _joints_type =
    std::vector<int16_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int16_t>>;
  _joints_type joints;

  // setters for named parameter idiom
  Type & set__joints(
    const std::vector<int16_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int16_t>> & _arg)
  {
    this->joints = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    arm_interface::msg::CurJoints_<ContainerAllocator> *;
  using ConstRawPtr =
    const arm_interface::msg::CurJoints_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<arm_interface::msg::CurJoints_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<arm_interface::msg::CurJoints_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      arm_interface::msg::CurJoints_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<arm_interface::msg::CurJoints_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      arm_interface::msg::CurJoints_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<arm_interface::msg::CurJoints_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<arm_interface::msg::CurJoints_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<arm_interface::msg::CurJoints_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__arm_interface__msg__CurJoints
    std::shared_ptr<arm_interface::msg::CurJoints_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__arm_interface__msg__CurJoints
    std::shared_ptr<arm_interface::msg::CurJoints_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CurJoints_ & other) const
  {
    if (this->joints != other.joints) {
      return false;
    }
    return true;
  }
  bool operator!=(const CurJoints_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CurJoints_

// alias to use template instance with default allocator
using CurJoints =
  arm_interface::msg::CurJoints_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace arm_interface

#endif  // ARM_INTERFACE__MSG__DETAIL__CUR_JOINTS__STRUCT_HPP_
