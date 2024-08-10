// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from plantroid_msgs:msg/State.idl
// generated code does not contain a copyright notice
#include "plantroid_msgs/msg/detail/state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>


// Include directives for member types
// Member `pose`
#include "plantroid_msgs/msg/detail/pose__functions.h"
// Member `speed`
#include "plantroid_msgs/msg/detail/speed__functions.h"

bool
plantroid_msgs__msg__State__init(plantroid_msgs__msg__State * msg)
{
  if (!msg) {
    return false;
  }
  // pose
  if (!plantroid_msgs__msg__Pose__init(&msg->pose)) {
    plantroid_msgs__msg__State__fini(msg);
    return false;
  }
  // speed
  if (!plantroid_msgs__msg__Speed__init(&msg->speed)) {
    plantroid_msgs__msg__State__fini(msg);
    return false;
  }
  return true;
}

void
plantroid_msgs__msg__State__fini(plantroid_msgs__msg__State * msg)
{
  if (!msg) {
    return;
  }
  // pose
  plantroid_msgs__msg__Pose__fini(&msg->pose);
  // speed
  plantroid_msgs__msg__Speed__fini(&msg->speed);
}

plantroid_msgs__msg__State *
plantroid_msgs__msg__State__create()
{
  plantroid_msgs__msg__State * msg = (plantroid_msgs__msg__State *)malloc(sizeof(plantroid_msgs__msg__State));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(plantroid_msgs__msg__State));
  bool success = plantroid_msgs__msg__State__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
plantroid_msgs__msg__State__destroy(plantroid_msgs__msg__State * msg)
{
  if (msg) {
    plantroid_msgs__msg__State__fini(msg);
  }
  free(msg);
}


bool
plantroid_msgs__msg__State__Sequence__init(plantroid_msgs__msg__State__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  plantroid_msgs__msg__State * data = NULL;
  if (size) {
    data = (plantroid_msgs__msg__State *)calloc(size, sizeof(plantroid_msgs__msg__State));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = plantroid_msgs__msg__State__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        plantroid_msgs__msg__State__fini(&data[i - 1]);
      }
      free(data);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
plantroid_msgs__msg__State__Sequence__fini(plantroid_msgs__msg__State__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      plantroid_msgs__msg__State__fini(&array->data[i]);
    }
    free(array->data);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

plantroid_msgs__msg__State__Sequence *
plantroid_msgs__msg__State__Sequence__create(size_t size)
{
  plantroid_msgs__msg__State__Sequence * array = (plantroid_msgs__msg__State__Sequence *)malloc(sizeof(plantroid_msgs__msg__State__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = plantroid_msgs__msg__State__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
plantroid_msgs__msg__State__Sequence__destroy(plantroid_msgs__msg__State__Sequence * array)
{
  if (array) {
    plantroid_msgs__msg__State__Sequence__fini(array);
  }
  free(array);
}
