// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from plantroid_msgs:msg/Speed.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "plantroid_msgs/msg/detail/speed__rosidl_typesupport_introspection_c.h"
#include "plantroid_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "plantroid_msgs/msg/detail/speed__functions.h"
#include "plantroid_msgs/msg/detail/speed__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void Speed__rosidl_typesupport_introspection_c__Speed_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  plantroid_msgs__msg__Speed__init(message_memory);
}

void Speed__rosidl_typesupport_introspection_c__Speed_fini_function(void * message_memory)
{
  plantroid_msgs__msg__Speed__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember Speed__rosidl_typesupport_introspection_c__Speed_message_member_array[2] = {
  {
    "linear",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(plantroid_msgs__msg__Speed, linear),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "angular",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(plantroid_msgs__msg__Speed, angular),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers Speed__rosidl_typesupport_introspection_c__Speed_message_members = {
  "plantroid_msgs__msg",  // message namespace
  "Speed",  // message name
  2,  // number of fields
  sizeof(plantroid_msgs__msg__Speed),
  Speed__rosidl_typesupport_introspection_c__Speed_message_member_array,  // message members
  Speed__rosidl_typesupport_introspection_c__Speed_init_function,  // function to initialize message memory (memory has to be allocated)
  Speed__rosidl_typesupport_introspection_c__Speed_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t Speed__rosidl_typesupport_introspection_c__Speed_message_type_support_handle = {
  0,
  &Speed__rosidl_typesupport_introspection_c__Speed_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_plantroid_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, msg, Speed)() {
  if (!Speed__rosidl_typesupport_introspection_c__Speed_message_type_support_handle.typesupport_identifier) {
    Speed__rosidl_typesupport_introspection_c__Speed_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &Speed__rosidl_typesupport_introspection_c__Speed_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
