// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from plantroid_msgs:msg/Speed.idl
// generated code does not contain a copyright notice
#include "plantroid_msgs/msg/detail/speed__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>


bool
plantroid_msgs__msg__Speed__init(plantroid_msgs__msg__Speed * msg)
{
  if (!msg) {
    return false;
  }
  // linear
  // angular
  return true;
}

void
plantroid_msgs__msg__Speed__fini(plantroid_msgs__msg__Speed * msg)
{
  if (!msg) {
    return;
  }
  // linear
  // angular
}

plantroid_msgs__msg__Speed *
plantroid_msgs__msg__Speed__create()
{
  plantroid_msgs__msg__Speed * msg = (plantroid_msgs__msg__Speed *)malloc(sizeof(plantroid_msgs__msg__Speed));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(plantroid_msgs__msg__Speed));
  bool success = plantroid_msgs__msg__Speed__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
plantroid_msgs__msg__Speed__destroy(plantroid_msgs__msg__Speed * msg)
{
  if (msg) {
    plantroid_msgs__msg__Speed__fini(msg);
  }
  free(msg);
}


bool
plantroid_msgs__msg__Speed__Sequence__init(plantroid_msgs__msg__Speed__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  plantroid_msgs__msg__Speed * data = NULL;
  if (size) {
    data = (plantroid_msgs__msg__Speed *)calloc(size, sizeof(plantroid_msgs__msg__Speed));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = plantroid_msgs__msg__Speed__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        plantroid_msgs__msg__Speed__fini(&data[i - 1]);
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
plantroid_msgs__msg__Speed__Sequence__fini(plantroid_msgs__msg__Speed__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      plantroid_msgs__msg__Speed__fini(&array->data[i]);
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

plantroid_msgs__msg__Speed__Sequence *
plantroid_msgs__msg__Speed__Sequence__create(size_t size)
{
  plantroid_msgs__msg__Speed__Sequence * array = (plantroid_msgs__msg__Speed__Sequence *)malloc(sizeof(plantroid_msgs__msg__Speed__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = plantroid_msgs__msg__Speed__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
plantroid_msgs__msg__Speed__Sequence__destroy(plantroid_msgs__msg__Speed__Sequence * array)
{
  if (array) {
    plantroid_msgs__msg__Speed__Sequence__fini(array);
  }
  free(array);
}
