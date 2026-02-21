// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from arm_interface:msg/ShapeInfo.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "arm_interface/msg/detail/shape_info__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace arm_interface
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void ShapeInfo_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) arm_interface::msg::ShapeInfo(_init);
}

void ShapeInfo_fini_function(void * message_memory)
{
  auto typed_message = static_cast<arm_interface::msg::ShapeInfo *>(message_memory);
  typed_message->~ShapeInfo();
}

size_t size_function__ShapeInfo__value(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<float> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ShapeInfo__value(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<float> *>(untyped_member);
  return &member[index];
}

void * get_function__ShapeInfo__value(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<float> *>(untyped_member);
  return &member[index];
}

void fetch_function__ShapeInfo__value(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const float *>(
    get_const_function__ShapeInfo__value(untyped_member, index));
  auto & value = *reinterpret_cast<float *>(untyped_value);
  value = item;
}

void assign_function__ShapeInfo__value(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<float *>(
    get_function__ShapeInfo__value(untyped_member, index));
  const auto & value = *reinterpret_cast<const float *>(untyped_value);
  item = value;
}

void resize_function__ShapeInfo__value(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<float> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ShapeInfo_message_member_array[1] = {
  {
    "value",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_interface::msg::ShapeInfo, value),  // bytes offset in struct
    nullptr,  // default value
    size_function__ShapeInfo__value,  // size() function pointer
    get_const_function__ShapeInfo__value,  // get_const(index) function pointer
    get_function__ShapeInfo__value,  // get(index) function pointer
    fetch_function__ShapeInfo__value,  // fetch(index, &value) function pointer
    assign_function__ShapeInfo__value,  // assign(index, value) function pointer
    resize_function__ShapeInfo__value  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ShapeInfo_message_members = {
  "arm_interface::msg",  // message namespace
  "ShapeInfo",  // message name
  1,  // number of fields
  sizeof(arm_interface::msg::ShapeInfo),
  ShapeInfo_message_member_array,  // message members
  ShapeInfo_init_function,  // function to initialize message memory (memory has to be allocated)
  ShapeInfo_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ShapeInfo_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ShapeInfo_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace arm_interface


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<arm_interface::msg::ShapeInfo>()
{
  return &::arm_interface::msg::rosidl_typesupport_introspection_cpp::ShapeInfo_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, arm_interface, msg, ShapeInfo)() {
  return &::arm_interface::msg::rosidl_typesupport_introspection_cpp::ShapeInfo_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
