// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from plantroid_msgs:srv/Gesture.idl
// generated code does not contain a copyright notice
#include "plantroid_msgs/srv/detail/gesture__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "plantroid_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "plantroid_msgs/srv/detail/gesture__struct.h"
#include "plantroid_msgs/srv/detail/gesture__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // gesture
#include "rosidl_runtime_c/string_functions.h"  // gesture

// forward declare type support functions


using _Gesture_Request__ros_msg_type = plantroid_msgs__srv__Gesture_Request;

static bool _Gesture_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _Gesture_Request__ros_msg_type * ros_message = static_cast<const _Gesture_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: gesture
  {
    const rosidl_runtime_c__String * str = &ros_message->gesture;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _Gesture_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _Gesture_Request__ros_msg_type * ros_message = static_cast<_Gesture_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: gesture
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->gesture.data) {
      rosidl_runtime_c__String__init(&ros_message->gesture);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->gesture,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'gesture'\n");
      return false;
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_plantroid_msgs
size_t get_serialized_size_plantroid_msgs__srv__Gesture_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _Gesture_Request__ros_msg_type * ros_message = static_cast<const _Gesture_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name gesture
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->gesture.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _Gesture_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_plantroid_msgs__srv__Gesture_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_plantroid_msgs
size_t max_serialized_size_plantroid_msgs__srv__Gesture_Request(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;

  // member: gesture
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

static size_t _Gesture_Request__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_plantroid_msgs__srv__Gesture_Request(
    full_bounded, 0);
}


static message_type_support_callbacks_t __callbacks_Gesture_Request = {
  "plantroid_msgs::srv",
  "Gesture_Request",
  _Gesture_Request__cdr_serialize,
  _Gesture_Request__cdr_deserialize,
  _Gesture_Request__get_serialized_size,
  _Gesture_Request__max_serialized_size
};

static rosidl_message_type_support_t _Gesture_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_Gesture_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, plantroid_msgs, srv, Gesture_Request)() {
  return &_Gesture_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "plantroid_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "plantroid_msgs/srv/detail/gesture__struct.h"
// already included above
// #include "plantroid_msgs/srv/detail/gesture__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

// already included above
// #include "rosidl_runtime_c/string.h"  // result
// already included above
// #include "rosidl_runtime_c/string_functions.h"  // result

// forward declare type support functions


using _Gesture_Response__ros_msg_type = plantroid_msgs__srv__Gesture_Response;

static bool _Gesture_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _Gesture_Response__ros_msg_type * ros_message = static_cast<const _Gesture_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: result
  {
    const rosidl_runtime_c__String * str = &ros_message->result;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _Gesture_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _Gesture_Response__ros_msg_type * ros_message = static_cast<_Gesture_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: result
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->result.data) {
      rosidl_runtime_c__String__init(&ros_message->result);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->result,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'result'\n");
      return false;
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_plantroid_msgs
size_t get_serialized_size_plantroid_msgs__srv__Gesture_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _Gesture_Response__ros_msg_type * ros_message = static_cast<const _Gesture_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name result
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->result.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _Gesture_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_plantroid_msgs__srv__Gesture_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_plantroid_msgs
size_t max_serialized_size_plantroid_msgs__srv__Gesture_Response(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;

  // member: result
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

static size_t _Gesture_Response__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_plantroid_msgs__srv__Gesture_Response(
    full_bounded, 0);
}


static message_type_support_callbacks_t __callbacks_Gesture_Response = {
  "plantroid_msgs::srv",
  "Gesture_Response",
  _Gesture_Response__cdr_serialize,
  _Gesture_Response__cdr_deserialize,
  _Gesture_Response__get_serialized_size,
  _Gesture_Response__max_serialized_size
};

static rosidl_message_type_support_t _Gesture_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_Gesture_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, plantroid_msgs, srv, Gesture_Response)() {
  return &_Gesture_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "plantroid_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "plantroid_msgs/srv/gesture.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t Gesture__callbacks = {
  "plantroid_msgs::srv",
  "Gesture",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, plantroid_msgs, srv, Gesture_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, plantroid_msgs, srv, Gesture_Response)(),
};

static rosidl_service_type_support_t Gesture__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &Gesture__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, plantroid_msgs, srv, Gesture)() {
  return &Gesture__handle;
}

#if defined(__cplusplus)
}
#endif
