// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from plantroid_msgs:srv/Sensors.idl
// generated code does not contain a copyright notice
#include "plantroid_msgs/srv/detail/sensors__rosidl_typesupport_fastrtps_cpp.hpp"
#include "plantroid_msgs/srv/detail/sensors__struct.hpp"

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

namespace plantroid_msgs
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
cdr_serialize(
  const plantroid_msgs::srv::Sensors_Request & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: sensor_number
  cdr << ros_message.sensor_number;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  plantroid_msgs::srv::Sensors_Request & ros_message)
{
  // Member: sensor_number
  cdr >> ros_message.sensor_number;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
get_serialized_size(
  const plantroid_msgs::srv::Sensors_Request & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: sensor_number
  {
    size_t item_size = sizeof(ros_message.sensor_number);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
max_serialized_size_Sensors_Request(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;


  // Member: sensor_number
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  return current_alignment - initial_alignment;
}

static bool _Sensors_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const plantroid_msgs::srv::Sensors_Request *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _Sensors_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<plantroid_msgs::srv::Sensors_Request *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _Sensors_Request__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const plantroid_msgs::srv::Sensors_Request *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _Sensors_Request__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_Sensors_Request(full_bounded, 0);
}

static message_type_support_callbacks_t _Sensors_Request__callbacks = {
  "plantroid_msgs::srv",
  "Sensors_Request",
  _Sensors_Request__cdr_serialize,
  _Sensors_Request__cdr_deserialize,
  _Sensors_Request__get_serialized_size,
  _Sensors_Request__max_serialized_size
};

static rosidl_message_type_support_t _Sensors_Request__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Sensors_Request__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace plantroid_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_plantroid_msgs
const rosidl_message_type_support_t *
get_message_type_support_handle<plantroid_msgs::srv::Sensors_Request>()
{
  return &plantroid_msgs::srv::typesupport_fastrtps_cpp::_Sensors_Request__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, plantroid_msgs, srv, Sensors_Request)() {
  return &plantroid_msgs::srv::typesupport_fastrtps_cpp::_Sensors_Request__handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include <limits>
// already included above
// #include <stdexcept>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
// already included above
// #include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace plantroid_msgs
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
cdr_serialize(
  const plantroid_msgs::srv::Sensors_Response & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: sensor_reading
  cdr << ros_message.sensor_reading;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  plantroid_msgs::srv::Sensors_Response & ros_message)
{
  // Member: sensor_reading
  cdr >> ros_message.sensor_reading;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
get_serialized_size(
  const plantroid_msgs::srv::Sensors_Response & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: sensor_reading
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.sensor_reading.size() + 1);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
max_serialized_size_Sensors_Response(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;


  // Member: sensor_reading
  {
    size_t array_size = 1;

    full_bounded = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  return current_alignment - initial_alignment;
}

static bool _Sensors_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const plantroid_msgs::srv::Sensors_Response *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _Sensors_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<plantroid_msgs::srv::Sensors_Response *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _Sensors_Response__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const plantroid_msgs::srv::Sensors_Response *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _Sensors_Response__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_Sensors_Response(full_bounded, 0);
}

static message_type_support_callbacks_t _Sensors_Response__callbacks = {
  "plantroid_msgs::srv",
  "Sensors_Response",
  _Sensors_Response__cdr_serialize,
  _Sensors_Response__cdr_deserialize,
  _Sensors_Response__get_serialized_size,
  _Sensors_Response__max_serialized_size
};

static rosidl_message_type_support_t _Sensors_Response__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Sensors_Response__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace plantroid_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_plantroid_msgs
const rosidl_message_type_support_t *
get_message_type_support_handle<plantroid_msgs::srv::Sensors_Response>()
{
  return &plantroid_msgs::srv::typesupport_fastrtps_cpp::_Sensors_Response__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, plantroid_msgs, srv, Sensors_Response)() {
  return &plantroid_msgs::srv::typesupport_fastrtps_cpp::_Sensors_Response__handle;
}

#ifdef __cplusplus
}
#endif

#include "rmw/error_handling.h"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/service_type_support_decl.hpp"

namespace plantroid_msgs
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

static service_type_support_callbacks_t _Sensors__callbacks = {
  "plantroid_msgs::srv",
  "Sensors",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, plantroid_msgs, srv, Sensors_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, plantroid_msgs, srv, Sensors_Response)(),
};

static rosidl_service_type_support_t _Sensors__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Sensors__callbacks,
  get_service_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace plantroid_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_plantroid_msgs
const rosidl_service_type_support_t *
get_service_type_support_handle<plantroid_msgs::srv::Sensors>()
{
  return &plantroid_msgs::srv::typesupport_fastrtps_cpp::_Sensors__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, plantroid_msgs, srv, Sensors)() {
  return &plantroid_msgs::srv::typesupport_fastrtps_cpp::_Sensors__handle;
}

#ifdef __cplusplus
}
#endif
