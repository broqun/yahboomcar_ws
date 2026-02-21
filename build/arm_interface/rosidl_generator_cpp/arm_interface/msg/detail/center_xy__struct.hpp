// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from arm_interface:msg/CenterXY.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__MSG__DETAIL__CENTER_XY__STRUCT_HPP_
#define ARM_INTERFACE__MSG__DETAIL__CENTER_XY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__arm_interface__msg__CenterXY __attribute__((deprecated))
#else
# define DEPRECATED__arm_interface__msg__CenterXY __declspec(deprecated)
#endif

namespace arm_interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CenterXY_
{
  using Type = CenterXY_<ContainerAllocator>;

  explicit CenterXY_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->center_x = 0.0f;
      this->center_y = 0.0f;
    }
  }

  explicit CenterXY_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->center_x = 0.0f;
      this->center_y = 0.0f;
    }
  }

  // field types and members
  using _center_x_type =
    float;
  _center_x_type center_x;
  using _center_y_type =
    float;
  _center_y_type center_y;

  // setters for named parameter idiom
  Type & set__center_x(
    const float & _arg)
  {
    this->center_x = _arg;
    return *this;
  }
  Type & set__center_y(
    const float & _arg)
  {
    this->center_y = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    arm_interface::msg::CenterXY_<ContainerAllocator> *;
  using ConstRawPtr =
    const arm_interface::msg::CenterXY_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<arm_interface::msg::CenterXY_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<arm_interface::msg::CenterXY_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      arm_interface::msg::CenterXY_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<arm_interface::msg::CenterXY_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      arm_interface::msg::CenterXY_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<arm_interface::msg::CenterXY_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<arm_interface::msg::CenterXY_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<arm_interface::msg::CenterXY_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__arm_interface__msg__CenterXY
    std::shared_ptr<arm_interface::msg::CenterXY_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__arm_interface__msg__CenterXY
    std::shared_ptr<arm_interface::msg::CenterXY_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CenterXY_ & other) const
  {
    if (this->center_x != other.center_x) {
      return false;
    }
    if (this->center_y != other.center_y) {
      return false;
    }
    return true;
  }
  bool operator!=(const CenterXY_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CenterXY_

// alias to use template instance with default allocator
using CenterXY =
  arm_interface::msg::CenterXY_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace arm_interface

#endif  // ARM_INTERFACE__MSG__DETAIL__CENTER_XY__STRUCT_HPP_
