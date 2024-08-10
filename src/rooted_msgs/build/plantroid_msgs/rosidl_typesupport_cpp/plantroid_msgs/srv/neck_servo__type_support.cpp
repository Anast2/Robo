// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from plantroid_msgs:srv/NeckServo.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "plantroid_msgs/srv/detail/neck_servo__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace plantroid_msgs
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _NeckServo_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NeckServo_Request_type_support_ids_t;

static const _NeckServo_Request_type_support_ids_t _NeckServo_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _NeckServo_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NeckServo_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NeckServo_Request_type_support_symbol_names_t _NeckServo_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, plantroid_msgs, srv, NeckServo_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, plantroid_msgs, srv, NeckServo_Request)),
  }
};

typedef struct _NeckServo_Request_type_support_data_t
{
  void * data[2];
} _NeckServo_Request_type_support_data_t;

static _NeckServo_Request_type_support_data_t _NeckServo_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NeckServo_Request_message_typesupport_map = {
  2,
  "plantroid_msgs",
  &_NeckServo_Request_message_typesupport_ids.typesupport_identifier[0],
  &_NeckServo_Request_message_typesupport_symbol_names.symbol_name[0],
  &_NeckServo_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t NeckServo_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NeckServo_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace plantroid_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<plantroid_msgs::srv::NeckServo_Request>()
{
  return &::plantroid_msgs::srv::rosidl_typesupport_cpp::NeckServo_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, plantroid_msgs, srv, NeckServo_Request)() {
  return get_message_type_support_handle<plantroid_msgs::srv::NeckServo_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "plantroid_msgs/srv/detail/neck_servo__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace plantroid_msgs
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _NeckServo_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NeckServo_Response_type_support_ids_t;

static const _NeckServo_Response_type_support_ids_t _NeckServo_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _NeckServo_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NeckServo_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NeckServo_Response_type_support_symbol_names_t _NeckServo_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, plantroid_msgs, srv, NeckServo_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, plantroid_msgs, srv, NeckServo_Response)),
  }
};

typedef struct _NeckServo_Response_type_support_data_t
{
  void * data[2];
} _NeckServo_Response_type_support_data_t;

static _NeckServo_Response_type_support_data_t _NeckServo_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NeckServo_Response_message_typesupport_map = {
  2,
  "plantroid_msgs",
  &_NeckServo_Response_message_typesupport_ids.typesupport_identifier[0],
  &_NeckServo_Response_message_typesupport_symbol_names.symbol_name[0],
  &_NeckServo_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t NeckServo_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NeckServo_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace plantroid_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<plantroid_msgs::srv::NeckServo_Response>()
{
  return &::plantroid_msgs::srv::rosidl_typesupport_cpp::NeckServo_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, plantroid_msgs, srv, NeckServo_Response)() {
  return get_message_type_support_handle<plantroid_msgs::srv::NeckServo_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "plantroid_msgs/srv/detail/neck_servo__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace plantroid_msgs
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _NeckServo_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NeckServo_type_support_ids_t;

static const _NeckServo_type_support_ids_t _NeckServo_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _NeckServo_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NeckServo_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NeckServo_type_support_symbol_names_t _NeckServo_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, plantroid_msgs, srv, NeckServo)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, plantroid_msgs, srv, NeckServo)),
  }
};

typedef struct _NeckServo_type_support_data_t
{
  void * data[2];
} _NeckServo_type_support_data_t;

static _NeckServo_type_support_data_t _NeckServo_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NeckServo_service_typesupport_map = {
  2,
  "plantroid_msgs",
  &_NeckServo_service_typesupport_ids.typesupport_identifier[0],
  &_NeckServo_service_typesupport_symbol_names.symbol_name[0],
  &_NeckServo_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t NeckServo_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NeckServo_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace plantroid_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<plantroid_msgs::srv::NeckServo>()
{
  return &::plantroid_msgs::srv::rosidl_typesupport_cpp::NeckServo_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp
