// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from plantroid_msgs:srv/Command.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__SRV__DETAIL__COMMAND__STRUCT_H_
#define PLANTROID_MSGS__SRV__DETAIL__COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'speed_command'
#include "plantroid_msgs/msg/detail/speed__struct.h"

// Struct defined in srv/Command in the package plantroid_msgs.
typedef struct plantroid_msgs__srv__Command_Request
{
  plantroid_msgs__msg__Speed speed_command;
} plantroid_msgs__srv__Command_Request;

// Struct for a sequence of plantroid_msgs__srv__Command_Request.
typedef struct plantroid_msgs__srv__Command_Request__Sequence
{
  plantroid_msgs__srv__Command_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} plantroid_msgs__srv__Command_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'status'
#include "rosidl_runtime_c/string.h"

// Struct defined in srv/Command in the package plantroid_msgs.
typedef struct plantroid_msgs__srv__Command_Response
{
  rosidl_runtime_c__String status;
} plantroid_msgs__srv__Command_Response;

// Struct for a sequence of plantroid_msgs__srv__Command_Response.
typedef struct plantroid_msgs__srv__Command_Response__Sequence
{
  plantroid_msgs__srv__Command_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} plantroid_msgs__srv__Command_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PLANTROID_MSGS__SRV__DETAIL__COMMAND__STRUCT_H_
