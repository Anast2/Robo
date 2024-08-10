// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from plantroid_msgs:msg/Speed.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__MSG__DETAIL__SPEED__STRUCT_H_
#define PLANTROID_MSGS__MSG__DETAIL__SPEED__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/Speed in the package plantroid_msgs.
typedef struct plantroid_msgs__msg__Speed
{
  double linear;
  double angular;
} plantroid_msgs__msg__Speed;

// Struct for a sequence of plantroid_msgs__msg__Speed.
typedef struct plantroid_msgs__msg__Speed__Sequence
{
  plantroid_msgs__msg__Speed * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} plantroid_msgs__msg__Speed__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PLANTROID_MSGS__MSG__DETAIL__SPEED__STRUCT_H_
