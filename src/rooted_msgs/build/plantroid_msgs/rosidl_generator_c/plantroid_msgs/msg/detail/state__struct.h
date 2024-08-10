// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from plantroid_msgs:msg/State.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__MSG__DETAIL__STATE__STRUCT_H_
#define PLANTROID_MSGS__MSG__DETAIL__STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'pose'
#include "plantroid_msgs/msg/detail/pose__struct.h"
// Member 'speed'
#include "plantroid_msgs/msg/detail/speed__struct.h"

// Struct defined in msg/State in the package plantroid_msgs.
typedef struct plantroid_msgs__msg__State
{
  plantroid_msgs__msg__Pose pose;
  plantroid_msgs__msg__Speed speed;
} plantroid_msgs__msg__State;

// Struct for a sequence of plantroid_msgs__msg__State.
typedef struct plantroid_msgs__msg__State__Sequence
{
  plantroid_msgs__msg__State * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} plantroid_msgs__msg__State__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PLANTROID_MSGS__MSG__DETAIL__STATE__STRUCT_H_
