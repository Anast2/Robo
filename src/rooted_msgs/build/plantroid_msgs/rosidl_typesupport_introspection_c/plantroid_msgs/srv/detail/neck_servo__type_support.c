// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from plantroid_msgs:srv/NeckServo.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "plantroid_msgs/srv/detail/neck_servo__rosidl_typesupport_introspection_c.h"
#include "plantroid_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "plantroid_msgs/srv/detail/neck_servo__functions.h"
#include "plantroid_msgs/srv/detail/neck_servo__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void NeckServo_Request__rosidl_typesupport_introspection_c__NeckServo_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  plantroid_msgs__srv__NeckServo_Request__init(message_memory);
}

void NeckServo_Request__rosidl_typesupport_introspection_c__NeckServo_Request_fini_function(void * message_memory)
{
  plantroid_msgs__srv__NeckServo_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember NeckServo_Request__rosidl_typesupport_introspection_c__NeckServo_Request_message_member_array[1] = {
  {
    "angle",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(plantroid_msgs__srv__NeckServo_Request, angle),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers NeckServo_Request__rosidl_typesupport_introspection_c__NeckServo_Request_message_members = {
  "plantroid_msgs__srv",  // message namespace
  "NeckServo_Request",  // message name
  1,  // number of fields
  sizeof(plantroid_msgs__srv__NeckServo_Request),
  NeckServo_Request__rosidl_typesupport_introspection_c__NeckServo_Request_message_member_array,  // message members
  NeckServo_Request__rosidl_typesupport_introspection_c__NeckServo_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  NeckServo_Request__rosidl_typesupport_introspection_c__NeckServo_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t NeckServo_Request__rosidl_typesupport_introspection_c__NeckServo_Request_message_type_support_handle = {
  0,
  &NeckServo_Request__rosidl_typesupport_introspection_c__NeckServo_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_plantroid_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, srv, NeckServo_Request)() {
  if (!NeckServo_Request__rosidl_typesupport_introspection_c__NeckServo_Request_message_type_support_handle.typesupport_identifier) {
    NeckServo_Request__rosidl_typesupport_introspection_c__NeckServo_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &NeckServo_Request__rosidl_typesupport_introspection_c__NeckServo_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "plantroid_msgs/srv/detail/neck_servo__rosidl_typesupport_introspection_c.h"
// already included above
// #include "plantroid_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "plantroid_msgs/srv/detail/neck_servo__functions.h"
// already included above
// #include "plantroid_msgs/srv/detail/neck_servo__struct.h"


// Include directives for member types
// Member `status`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void NeckServo_Response__rosidl_typesupport_introspection_c__NeckServo_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  plantroid_msgs__srv__NeckServo_Response__init(message_memory);
}

void NeckServo_Response__rosidl_typesupport_introspection_c__NeckServo_Response_fini_function(void * message_memory)
{
  plantroid_msgs__srv__NeckServo_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember NeckServo_Response__rosidl_typesupport_introspection_c__NeckServo_Response_message_member_array[1] = {
  {
    "status",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(plantroid_msgs__srv__NeckServo_Response, status),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers NeckServo_Response__rosidl_typesupport_introspection_c__NeckServo_Response_message_members = {
  "plantroid_msgs__srv",  // message namespace
  "NeckServo_Response",  // message name
  1,  // number of fields
  sizeof(plantroid_msgs__srv__NeckServo_Response),
  NeckServo_Response__rosidl_typesupport_introspection_c__NeckServo_Response_message_member_array,  // message members
  NeckServo_Response__rosidl_typesupport_introspection_c__NeckServo_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  NeckServo_Response__rosidl_typesupport_introspection_c__NeckServo_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t NeckServo_Response__rosidl_typesupport_introspection_c__NeckServo_Response_message_type_support_handle = {
  0,
  &NeckServo_Response__rosidl_typesupport_introspection_c__NeckServo_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_plantroid_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, srv, NeckServo_Response)() {
  if (!NeckServo_Response__rosidl_typesupport_introspection_c__NeckServo_Response_message_type_support_handle.typesupport_identifier) {
    NeckServo_Response__rosidl_typesupport_introspection_c__NeckServo_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &NeckServo_Response__rosidl_typesupport_introspection_c__NeckServo_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "plantroid_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "plantroid_msgs/srv/detail/neck_servo__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers plantroid_msgs__srv__detail__neck_servo__rosidl_typesupport_introspection_c__NeckServo_service_members = {
  "plantroid_msgs__srv",  // service namespace
  "NeckServo",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // plantroid_msgs__srv__detail__neck_servo__rosidl_typesupport_introspection_c__NeckServo_Request_message_type_support_handle,
  NULL  // response message
  // plantroid_msgs__srv__detail__neck_servo__rosidl_typesupport_introspection_c__NeckServo_Response_message_type_support_handle
};

static rosidl_service_type_support_t plantroid_msgs__srv__detail__neck_servo__rosidl_typesupport_introspection_c__NeckServo_service_type_support_handle = {
  0,
  &plantroid_msgs__srv__detail__neck_servo__rosidl_typesupport_introspection_c__NeckServo_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, srv, NeckServo_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, srv, NeckServo_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_plantroid_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, srv, NeckServo)() {
  if (!plantroid_msgs__srv__detail__neck_servo__rosidl_typesupport_introspection_c__NeckServo_service_type_support_handle.typesupport_identifier) {
    plantroid_msgs__srv__detail__neck_servo__rosidl_typesupport_introspection_c__NeckServo_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)plantroid_msgs__srv__detail__neck_servo__rosidl_typesupport_introspection_c__NeckServo_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, srv, NeckServo_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, srv, NeckServo_Response)()->data;
  }

  return &plantroid_msgs__srv__detail__neck_servo__rosidl_typesupport_introspection_c__NeckServo_service_type_support_handle;
}
