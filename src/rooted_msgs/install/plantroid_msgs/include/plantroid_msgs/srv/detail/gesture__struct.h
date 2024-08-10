// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from plantroid_msgs:srv/Gesture.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__SRV__DETAIL__GESTURE__STRUCT_H_
#define PLANTROID_MSGS__SRV__DETAIL__GESTURE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'gesture'
#include "rosidl_runtime_c/string.h"

// Struct defined in srv/Gesture in the package plantroid_msgs.
typedef struct plantroid_msgs__srv__Gesture_Request
{
  rosidl_runtime_c__String gesture;
} plantroid_msgs__srv__Gesture_Request;

// Struct for a sequence of plantroid_msgs__srv__Gesture_Request.
typedef struct plantroid_msgs__srv__Gesture_Request__Sequence
{
  plantroid_msgs__srv__Gesture_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} plantroid_msgs__srv__Gesture_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "rosidl_runtime_c/string.h"

// Struct defined in srv/Gesture in the package plantroid_msgs.
typedef struct plantroid_msgs__srv__Gesture_Response
{
  rosidl_runtime_c__String result;
} plantroid_msgs__srv__Gesture_Response;

// Struct for a sequence of plantroid_msgs__srv__Gesture_Response.
typedef struct plantroid_msgs__srv__Gesture_Response__Sequence
{
  plantroid_msgs__srv__Gesture_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} plantroid_msgs__srv__Gesture_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PLANTROID_MSGS__SRV__DETAIL__GESTURE__STRUCT_H_
