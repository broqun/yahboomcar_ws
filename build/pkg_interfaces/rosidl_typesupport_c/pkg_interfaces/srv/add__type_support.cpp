// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from pkg_interfaces:srv/Add.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "pkg_interfaces/srv/detail/add__struct.h"
#include "pkg_interfaces/srv/detail/add__type_support.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace pkg_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _Add_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Add_Request_type_support_ids_t;

static const _Add_Request_type_support_ids_t _Add_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Add_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Add_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Add_Request_type_support_symbol_names_t _Add_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, pkg_interfaces, srv, Add_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pkg_interfaces, srv, Add_Request)),
  }
};

typedef struct _Add_Request_type_support_data_t
{
  void * data[2];
} _Add_Request_type_support_data_t;

static _Add_Request_type_support_data_t _Add_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Add_Request_message_typesupport_map = {
  2,
  "pkg_interfaces",
  &_Add_Request_message_typesupport_ids.typesupport_identifier[0],
  &_Add_Request_message_typesupport_symbol_names.symbol_name[0],
  &_Add_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Add_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Add_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace pkg_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, pkg_interfaces, srv, Add_Request)() {
  return &::pkg_interfaces::srv::rosidl_typesupport_c::Add_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "pkg_interfaces/srv/detail/add__struct.h"
// already included above
// #include "pkg_interfaces/srv/detail/add__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace pkg_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _Add_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Add_Response_type_support_ids_t;

static const _Add_Response_type_support_ids_t _Add_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Add_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Add_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Add_Response_type_support_symbol_names_t _Add_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, pkg_interfaces, srv, Add_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pkg_interfaces, srv, Add_Response)),
  }
};

typedef struct _Add_Response_type_support_data_t
{
  void * data[2];
} _Add_Response_type_support_data_t;

static _Add_Response_type_support_data_t _Add_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Add_Response_message_typesupport_map = {
  2,
  "pkg_interfaces",
  &_Add_Response_message_typesupport_ids.typesupport_identifier[0],
  &_Add_Response_message_typesupport_symbol_names.symbol_name[0],
  &_Add_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Add_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Add_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace pkg_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, pkg_interfaces, srv, Add_Response)() {
  return &::pkg_interfaces::srv::rosidl_typesupport_c::Add_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "pkg_interfaces/srv/detail/add__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace pkg_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _Add_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Add_type_support_ids_t;

static const _Add_type_support_ids_t _Add_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Add_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Add_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Add_type_support_symbol_names_t _Add_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, pkg_interfaces, srv, Add)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pkg_interfaces, srv, Add)),
  }
};

typedef struct _Add_type_support_data_t
{
  void * data[2];
} _Add_type_support_data_t;

static _Add_type_support_data_t _Add_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Add_service_typesupport_map = {
  2,
  "pkg_interfaces",
  &_Add_service_typesupport_ids.typesupport_identifier[0],
  &_Add_service_typesupport_symbol_names.symbol_name[0],
  &_Add_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t Add_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Add_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace pkg_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, pkg_interfaces, srv, Add)() {
  return &::pkg_interfaces::srv::rosidl_typesupport_c::Add_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif
