// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from pkg_interfaces:srv/Add.idl
// generated code does not contain a copyright notice

#ifndef PKG_INTERFACES__SRV__DETAIL__ADD__STRUCT_HPP_
#define PKG_INTERFACES__SRV__DETAIL__ADD__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__pkg_interfaces__srv__Add_Request __attribute__((deprecated))
#else
# define DEPRECATED__pkg_interfaces__srv__Add_Request __declspec(deprecated)
#endif

namespace pkg_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Add_Request_
{
  using Type = Add_Request_<ContainerAllocator>;

  explicit Add_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->num1 = 0l;
      this->num2 = 0l;
    }
  }

  explicit Add_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->num1 = 0l;
      this->num2 = 0l;
    }
  }

  // field types and members
  using _num1_type =
    int32_t;
  _num1_type num1;
  using _num2_type =
    int32_t;
  _num2_type num2;

  // setters for named parameter idiom
  Type & set__num1(
    const int32_t & _arg)
  {
    this->num1 = _arg;
    return *this;
  }
  Type & set__num2(
    const int32_t & _arg)
  {
    this->num2 = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pkg_interfaces::srv::Add_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const pkg_interfaces::srv::Add_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pkg_interfaces::srv::Add_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pkg_interfaces::srv::Add_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pkg_interfaces::srv::Add_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pkg_interfaces::srv::Add_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pkg_interfaces::srv::Add_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pkg_interfaces::srv::Add_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pkg_interfaces::srv::Add_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pkg_interfaces::srv::Add_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pkg_interfaces__srv__Add_Request
    std::shared_ptr<pkg_interfaces::srv::Add_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pkg_interfaces__srv__Add_Request
    std::shared_ptr<pkg_interfaces::srv::Add_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Add_Request_ & other) const
  {
    if (this->num1 != other.num1) {
      return false;
    }
    if (this->num2 != other.num2) {
      return false;
    }
    return true;
  }
  bool operator!=(const Add_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Add_Request_

// alias to use template instance with default allocator
using Add_Request =
  pkg_interfaces::srv::Add_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace pkg_interfaces


#ifndef _WIN32
# define DEPRECATED__pkg_interfaces__srv__Add_Response __attribute__((deprecated))
#else
# define DEPRECATED__pkg_interfaces__srv__Add_Response __declspec(deprecated)
#endif

namespace pkg_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Add_Response_
{
  using Type = Add_Response_<ContainerAllocator>;

  explicit Add_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->sum = 0l;
    }
  }

  explicit Add_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->sum = 0l;
    }
  }

  // field types and members
  using _sum_type =
    int32_t;
  _sum_type sum;

  // setters for named parameter idiom
  Type & set__sum(
    const int32_t & _arg)
  {
    this->sum = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pkg_interfaces::srv::Add_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const pkg_interfaces::srv::Add_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pkg_interfaces::srv::Add_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pkg_interfaces::srv::Add_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pkg_interfaces::srv::Add_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pkg_interfaces::srv::Add_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pkg_interfaces::srv::Add_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pkg_interfaces::srv::Add_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pkg_interfaces::srv::Add_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pkg_interfaces::srv::Add_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pkg_interfaces__srv__Add_Response
    std::shared_ptr<pkg_interfaces::srv::Add_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pkg_interfaces__srv__Add_Response
    std::shared_ptr<pkg_interfaces::srv::Add_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Add_Response_ & other) const
  {
    if (this->sum != other.sum) {
      return false;
    }
    return true;
  }
  bool operator!=(const Add_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Add_Response_

// alias to use template instance with default allocator
using Add_Response =
  pkg_interfaces::srv::Add_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace pkg_interfaces

namespace pkg_interfaces
{

namespace srv
{

struct Add
{
  using Request = pkg_interfaces::srv::Add_Request;
  using Response = pkg_interfaces::srv::Add_Response;
};

}  // namespace srv

}  // namespace pkg_interfaces

#endif  // PKG_INTERFACES__SRV__DETAIL__ADD__STRUCT_HPP_
