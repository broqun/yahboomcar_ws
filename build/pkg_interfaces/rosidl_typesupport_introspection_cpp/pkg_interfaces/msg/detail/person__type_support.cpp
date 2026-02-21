// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from pkg_interfaces:msg/Person.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "pkg_interfaces/msg/detail/person__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace pkg_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void Person_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) pkg_interfaces::msg::Person(_init);
}

void Person_fini_function(void * message_memory)
{
  auto typed_message = static_cast<pkg_interfaces::msg::Person *>(message_memory);
  typed_message->~Person();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Person_message_member_array[3] = {
  {
    "name",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pkg_interfaces::msg::Person, name),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "age",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pkg_interfaces::msg::Person, age),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "height",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pkg_interfaces::msg::Person, height),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Person_message_members = {
  "pkg_interfaces::msg",  // message namespace
  "Person",  // message name
  3,  // number of fields
  sizeof(pkg_interfaces::msg::Person),
  Person_message_member_array,  // message members
  Person_init_function,  // function to initialize message memory (memory has to be allocated)
  Person_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Person_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Person_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace pkg_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<pkg_interfaces::msg::Person>()
{
  return &::pkg_interfaces::msg::rosidl_typesupport_introspection_cpp::Person_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, pkg_interfaces, msg, Person)() {
  return &::pkg_interfaces::msg::rosidl_typesupport_introspection_cpp::Person_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
