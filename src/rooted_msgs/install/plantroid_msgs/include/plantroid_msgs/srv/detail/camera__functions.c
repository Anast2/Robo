// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from plantroid_msgs:srv/Camera.idl
// generated code does not contain a copyright notice
#include "plantroid_msgs/srv/detail/camera__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

bool
plantroid_msgs__srv__Camera_Request__init(plantroid_msgs__srv__Camera_Request * msg)
{
  if (!msg) {
    return false;
  }
  // imagetype
  return true;
}

void
plantroid_msgs__srv__Camera_Request__fini(plantroid_msgs__srv__Camera_Request * msg)
{
  if (!msg) {
    return;
  }
  // imagetype
}

plantroid_msgs__srv__Camera_Request *
plantroid_msgs__srv__Camera_Request__create()
{
  plantroid_msgs__srv__Camera_Request * msg = (plantroid_msgs__srv__Camera_Request *)malloc(sizeof(plantroid_msgs__srv__Camera_Request));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(plantroid_msgs__srv__Camera_Request));
  bool success = plantroid_msgs__srv__Camera_Request__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
plantroid_msgs__srv__Camera_Request__destroy(plantroid_msgs__srv__Camera_Request * msg)
{
  if (msg) {
    plantroid_msgs__srv__Camera_Request__fini(msg);
  }
  free(msg);
}


bool
plantroid_msgs__srv__Camera_Request__Sequence__init(plantroid_msgs__srv__Camera_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  plantroid_msgs__srv__Camera_Request * data = NULL;
  if (size) {
    data = (plantroid_msgs__srv__Camera_Request *)calloc(size, sizeof(plantroid_msgs__srv__Camera_Request));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = plantroid_msgs__srv__Camera_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        plantroid_msgs__srv__Camera_Request__fini(&data[i - 1]);
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
plantroid_msgs__srv__Camera_Request__Sequence__fini(plantroid_msgs__srv__Camera_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      plantroid_msgs__srv__Camera_Request__fini(&array->data[i]);
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

plantroid_msgs__srv__Camera_Request__Sequence *
plantroid_msgs__srv__Camera_Request__Sequence__create(size_t size)
{
  plantroid_msgs__srv__Camera_Request__Sequence * array = (plantroid_msgs__srv__Camera_Request__Sequence *)malloc(sizeof(plantroid_msgs__srv__Camera_Request__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = plantroid_msgs__srv__Camera_Request__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
plantroid_msgs__srv__Camera_Request__Sequence__destroy(plantroid_msgs__srv__Camera_Request__Sequence * array)
{
  if (array) {
    plantroid_msgs__srv__Camera_Request__Sequence__fini(array);
  }
  free(array);
}


// Include directives for member types
// Member `image`
#include "rosidl_runtime_c/string_functions.h"

bool
plantroid_msgs__srv__Camera_Response__init(plantroid_msgs__srv__Camera_Response * msg)
{
  if (!msg) {
    return false;
  }
  // image
  if (!rosidl_runtime_c__String__init(&msg->image)) {
    plantroid_msgs__srv__Camera_Response__fini(msg);
    return false;
  }
  return true;
}

void
plantroid_msgs__srv__Camera_Response__fini(plantroid_msgs__srv__Camera_Response * msg)
{
  if (!msg) {
    return;
  }
  // image
  rosidl_runtime_c__String__fini(&msg->image);
}

plantroid_msgs__srv__Camera_Response *
plantroid_msgs__srv__Camera_Response__create()
{
  plantroid_msgs__srv__Camera_Response * msg = (plantroid_msgs__srv__Camera_Response *)malloc(sizeof(plantroid_msgs__srv__Camera_Response));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(plantroid_msgs__srv__Camera_Response));
  bool success = plantroid_msgs__srv__Camera_Response__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
plantroid_msgs__srv__Camera_Response__destroy(plantroid_msgs__srv__Camera_Response * msg)
{
  if (msg) {
    plantroid_msgs__srv__Camera_Response__fini(msg);
  }
  free(msg);
}


bool
plantroid_msgs__srv__Camera_Response__Sequence__init(plantroid_msgs__srv__Camera_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  plantroid_msgs__srv__Camera_Response * data = NULL;
  if (size) {
    data = (plantroid_msgs__srv__Camera_Response *)calloc(size, sizeof(plantroid_msgs__srv__Camera_Response));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = plantroid_msgs__srv__Camera_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        plantroid_msgs__srv__Camera_Response__fini(&data[i - 1]);
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
plantroid_msgs__srv__Camera_Response__Sequence__fini(plantroid_msgs__srv__Camera_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      plantroid_msgs__srv__Camera_Response__fini(&array->data[i]);
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

plantroid_msgs__srv__Camera_Response__Sequence *
plantroid_msgs__srv__Camera_Response__Sequence__create(size_t size)
{
  plantroid_msgs__srv__Camera_Response__Sequence * array = (plantroid_msgs__srv__Camera_Response__Sequence *)malloc(sizeof(plantroid_msgs__srv__Camera_Response__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = plantroid_msgs__srv__Camera_Response__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
plantroid_msgs__srv__Camera_Response__Sequence__destroy(plantroid_msgs__srv__Camera_Response__Sequence * array)
{
  if (array) {
    plantroid_msgs__srv__Camera_Response__Sequence__fini(array);
  }
  free(array);
}
