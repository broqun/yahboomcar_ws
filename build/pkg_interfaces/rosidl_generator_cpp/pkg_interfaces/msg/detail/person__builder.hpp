// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from pkg_interfaces:msg/Person.idl
// generated code does not contain a copyright notice

#ifndef PKG_INTERFACES__MSG__DETAIL__PERSON__BUILDER_HPP_
#define PKG_INTERFACES__MSG__DETAIL__PERSON__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "pkg_interfaces/msg/detail/person__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace pkg_interfaces
{

namespace msg
{

namespace builder
{

class Init_Person_height
{
public:
  explicit Init_Person_height(::pkg_interfaces::msg::Person & msg)
  : msg_(msg)
  {}
  ::pkg_interfaces::msg::Person height(::pkg_interfaces::msg::Person::_height_type arg)
  {
    msg_.height = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pkg_interfaces::msg::Person msg_;
};

class Init_Person_age
{
public:
  explicit Init_Person_age(::pkg_interfaces::msg::Person & msg)
  : msg_(msg)
  {}
  Init_Person_height age(::pkg_interfaces::msg::Person::_age_type arg)
  {
    msg_.age = std::move(arg);
    return Init_Person_height(msg_);
  }

private:
  ::pkg_interfaces::msg::Person msg_;
};

class Init_Person_name
{
public:
  Init_Person_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Person_age name(::pkg_interfaces::msg::Person::_name_type arg)
  {
    msg_.name = std::move(arg);
    return Init_Person_age(msg_);
  }

private:
  ::pkg_interfaces::msg::Person msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::pkg_interfaces::msg::Person>()
{
  return pkg_interfaces::msg::builder::Init_Person_name();
}

}  // namespace pkg_interfaces

#endif  // PKG_INTERFACES__MSG__DETAIL__PERSON__BUILDER_HPP_
