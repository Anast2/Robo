// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from plantroid_msgs:srv/NeckServo.idl
// generated code does not contain a copyright notice
#include "plantroid_msgs/srv/detail/neck_servo__rosidl_typesupport_fastrtps_cpp.hpp"
#include "plantroid_msgs/srv/detail/neck_servo__struct.hpp"

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
  const plantroid_msgs::srv::NeckServo_Request & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: angle
  cdr << ros_message.angle;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  plantroid_msgs::srv::NeckServo_Request & ros_message)
{
  // Member: angle
  cdr >> ros_message.angle;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
get_serialized_size(
  const plantroid_msgs::srv::NeckServo_Request & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: angle
  {
    size_t item_size = sizeof(ros_message.angle);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
max_serialized_size_NeckServo_Request(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;


  // Member: angle
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  return current_alignment - initial_alignment;
}

static bool _NeckServo_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const plantroid_msgs::srv::NeckServo_Request *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _NeckServo_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<plantroid_msgs::srv::NeckServo_Request *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _NeckServo_Request__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const plantroid_msgs::srv::NeckServo_Request *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _NeckServo_Request__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_NeckServo_Request(full_bounded, 0);
}

static message_type_support_callbacks_t _NeckServo_Request__callbacks = {
  "plantroid_msgs::srv",
  "NeckServo_Request",
  _NeckServo_Request__cdr_serialize,
  _NeckServo_Request__cdr_deserialize,
  _NeckServo_Request__get_serialized_size,
  _NeckServo_Request__max_serialized_size
};

static rosidl_message_type_support_t _NeckServo_Request__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_NeckServo_Request__callbacks,
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
get_message_type_support_handle<plantroid_msgs::srv::NeckServo_Request>()
{
  return &plantroid_msgs::srv::typesupport_fastrtps_cpp::_NeckServo_Request__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, plantroid_msgs, srv, NeckServo_Request)() {
  return &plantroid_msgs::srv::typesupport_fastrtps_cpp::_NeckServo_Request__handle;
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
  const plantroid_msgs::srv::NeckServo_Response & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: status
  cdr << ros_message.status;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  plantroid_msgs::srv::NeckServo_Response & ros_message)
{
  // Member: status
  cdr >> ros_message.status;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
get_serialized_size(
  const plantroid_msgs::srv::NeckServo_Response & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: status
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.status.size() + 1);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
max_serialized_size_NeckServo_Response(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;


  // Member: status
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

static bool _NeckServo_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const plantroid_msgs::srv::NeckServo_Response *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _NeckServo_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<plantroid_msgs::srv::NeckServo_Response *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _NeckServo_Response__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const plantroid_msgs::srv::NeckServo_Response *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _NeckServo_Response__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_NeckServo_Response(full_bounded, 0);
}

static message_type_support_callbacks_t _NeckServo_Response__callbacks = {
  "plantroid_msgs::srv",
  "NeckServo_Response",
  _NeckServo_Response__cdr_serialize,
  _NeckServo_Response__cdr_deserialize,
  _NeckServo_Response__get_serialized_size,
  _NeckServo_Response__max_serialized_size
};

static rosidl_message_type_support_t _NeckServo_Response__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_NeckServo_Response__callbacks,
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
get_message_type_support_handle<plantroid_msgs::srv::NeckServo_Response>()
{
  return &plantroid_msgs::srv::typesupport_fastrtps_cpp::_NeckServo_Response__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, plantroid_msgs, srv, NeckServo_Response)() {
  return &plantroid_msgs::srv::typesupport_fastrtps_cpp::_NeckServo_Response__handle;
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

static service_type_support_callbacks_t _NeckServo__callbacks = {
  "plantroid_msgs::srv",
  "NeckServo",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, plantroid_msgs, srv, NeckServo_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, plantroid_msgs, srv, NeckServo_Response)(),
};

static rosidl_service_type_support_t _NeckServo__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_NeckServo__callbacks,
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
get_service_type_support_handle<plantroid_msgs::srv::NeckServo>()
{
  return &plantroid_msgs::srv::typesupport_fastrtps_cpp::_NeckServo__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, plantroid_msgs, srv, NeckServo)() {
  return &plantroid_msgs::srv::typesupport_fastrtps_cpp::_NeckServo__handle;
}

#ifdef __cplusplus
}
#endif
