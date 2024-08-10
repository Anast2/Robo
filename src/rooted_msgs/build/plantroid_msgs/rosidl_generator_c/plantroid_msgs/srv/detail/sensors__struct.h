// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from plantroid_msgs:srv/Sensors.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__SRV__DETAIL__SENSORS__STRUCT_H_
#define PLANTROID_MSGS__SRV__DETAIL__SENSORS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in srv/Sensors in the package plantroid_msgs.
typedef struct plantroid_msgs__srv__Sensors_Request
{
  int8_t sensor_number;
} plantroid_msgs__srv__Sensors_Request;

// Struct for a sequence of plantroid_msgs__srv__Sensors_Request.
typedef struct plantroid_msgs__srv__Sensors_Request__Sequence
{
  plantroid_msgs__srv__Sensors_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} plantroid_msgs__srv__Sensors_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'sensor_reading'
#include "rosidl_runtime_c/string.h"

// Struct defined in srv/Sensors in the package plantroid_msgs.
typedef struct plantroid_msgs__srv__Sensors_Response
{
  rosidl_runtime_c__String sensor_reading;
} plantroid_msgs__srv__Sensors_Response;

// Struct for a sequence of plantroid_msgs__srv__Sensors_Response.
typedef struct plantroid_msgs__srv__Sensors_Response__Sequence
{
  plantroid_msgs__srv__Sensors_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} plantroid_msgs__srv__Sensors_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PLANTROID_MSGS__SRV__DETAIL__SENSORS__STRUCT_H_
