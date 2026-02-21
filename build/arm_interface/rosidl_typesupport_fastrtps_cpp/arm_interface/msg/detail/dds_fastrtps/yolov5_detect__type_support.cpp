// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from arm_interface:msg/Yolov5Detect.idl
// generated code does not contain a copyright notice
#include "arm_interface/msg/detail/yolov5_detect__rosidl_typesupport_fastrtps_cpp.hpp"
#include "arm_interface/msg/detail/yolov5_detect__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace arm_interface
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_arm_interface
cdr_serialize(
  const arm_interface::msg::Yolov5Detect & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: result
  cdr << ros_message.result;
  // Member: centerx
  cdr << ros_message.centerx;
  // Member: centery
  cdr << ros_message.centery;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_arm_interface
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  arm_interface::msg::Yolov5Detect & ros_message)
{
  // Member: result
  cdr >> ros_message.result;

  // Member: centerx
  cdr >> ros_message.centerx;

  // Member: centery
  cdr >> ros_message.centery;

  return true;
}  // NOLINT(readability/fn_size)

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_arm_interface
get_serialized_size(
  const arm_interface::msg::Yolov5Detect & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: result
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.result.size() + 1);
  // Member: centerx
  {
    size_t item_size = sizeof(ros_message.centerx);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: centery
  {
    size_t item_size = sizeof(ros_message.centery);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_arm_interface
max_serialized_size_Yolov5Detect(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: result
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Member: centerx
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: centery
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = arm_interface::msg::Yolov5Detect;
    is_plain =
      (
      offsetof(DataType, centery) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _Yolov5Detect__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const arm_interface::msg::Yolov5Detect *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _Yolov5Detect__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<arm_interface::msg::Yolov5Detect *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _Yolov5Detect__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const arm_interface::msg::Yolov5Detect *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _Yolov5Detect__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_Yolov5Detect(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _Yolov5Detect__callbacks = {
  "arm_interface::msg",
  "Yolov5Detect",
  _Yolov5Detect__cdr_serialize,
  _Yolov5Detect__cdr_deserialize,
  _Yolov5Detect__get_serialized_size,
  _Yolov5Detect__max_serialized_size
};

static rosidl_message_type_support_t _Yolov5Detect__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Yolov5Detect__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace arm_interface

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_arm_interface
const rosidl_message_type_support_t *
get_message_type_support_handle<arm_interface::msg::Yolov5Detect>()
{
  return &arm_interface::msg::typesupport_fastrtps_cpp::_Yolov5Detect__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, arm_interface, msg, Yolov5Detect)() {
  return &arm_interface::msg::typesupport_fastrtps_cpp::_Yolov5Detect__handle;
}

#ifdef __cplusplus
}
#endif
