// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from plantroid_msgs:srv/Command.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "plantroid_msgs/srv/detail/command__rosidl_typesupport_introspection_c.h"
#include "plantroid_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "plantroid_msgs/srv/detail/command__functions.h"
#include "plantroid_msgs/srv/detail/command__struct.h"


// Include directives for member types
// Member `speed_command`
#include "plantroid_msgs/msg/speed.h"
// Member `speed_command`
#include "plantroid_msgs/msg/detail/speed__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void Command_Request__rosidl_typesupport_introspection_c__Command_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  plantroid_msgs__srv__Command_Request__init(message_memory);
}

void Command_Request__rosidl_typesupport_introspection_c__Command_Request_fini_function(void * message_memory)
{
  plantroid_msgs__srv__Command_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember Command_Request__rosidl_typesupport_introspection_c__Command_Request_message_member_array[1] = {
  {
    "speed_command",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(plantroid_msgs__srv__Command_Request, speed_command),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers Command_Request__rosidl_typesupport_introspection_c__Command_Request_message_members = {
  "plantroid_msgs__srv",  // message namespace
  "Command_Request",  // message name
  1,  // number of fields
  sizeof(plantroid_msgs__srv__Command_Request),
  Command_Request__rosidl_typesupport_introspection_c__Command_Request_message_member_array,  // message members
  Command_Request__rosidl_typesupport_introspection_c__Command_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  Command_Request__rosidl_typesupport_introspection_c__Command_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t Command_Request__rosidl_typesupport_introspection_c__Command_Request_message_type_support_handle = {
  0,
  &Command_Request__rosidl_typesupport_introspection_c__Command_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_plantroid_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, srv, Command_Request)() {
  Command_Request__rosidl_typesupport_introspection_c__Command_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, msg, Speed)();
  if (!Command_Request__rosidl_typesupport_introspection_c__Command_Request_message_type_support_handle.typesupport_identifier) {
    Command_Request__rosidl_typesupport_introspection_c__Command_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &Command_Request__rosidl_typesupport_introspection_c__Command_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "plantroid_msgs/srv/detail/command__rosidl_typesupport_introspection_c.h"
// already included above
// #include "plantroid_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "plantroid_msgs/srv/detail/command__functions.h"
// already included above
// #include "plantroid_msgs/srv/detail/command__struct.h"


// Include directives for member types
// Member `status`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void Command_Response__rosidl_typesupport_introspection_c__Command_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  plantroid_msgs__srv__Command_Response__init(message_memory);
}

void Command_Response__rosidl_typesupport_introspection_c__Command_Response_fini_function(void * message_memory)
{
  plantroid_msgs__srv__Command_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember Command_Response__rosidl_typesupport_introspection_c__Command_Response_message_member_array[1] = {
  {
    "status",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(plantroid_msgs__srv__Command_Response, status),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers Command_Response__rosidl_typesupport_introspection_c__Command_Response_message_members = {
  "plantroid_msgs__srv",  // message namespace
  "Command_Response",  // message name
  1,  // number of fields
  sizeof(plantroid_msgs__srv__Command_Response),
  Command_Response__rosidl_typesupport_introspection_c__Command_Response_message_member_array,  // message members
  Command_Response__rosidl_typesupport_introspection_c__Command_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  Command_Response__rosidl_typesupport_introspection_c__Command_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t Command_Response__rosidl_typesupport_introspection_c__Command_Response_message_type_support_handle = {
  0,
  &Command_Response__rosidl_typesupport_introspection_c__Command_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_plantroid_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, srv, Command_Response)() {
  if (!Command_Response__rosidl_typesupport_introspection_c__Command_Response_message_type_support_handle.typesupport_identifier) {
    Command_Response__rosidl_typesupport_introspection_c__Command_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &Command_Response__rosidl_typesupport_introspection_c__Command_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "plantroid_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "plantroid_msgs/srv/detail/command__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers plantroid_msgs__srv__detail__command__rosidl_typesupport_introspection_c__Command_service_members = {
  "plantroid_msgs__srv",  // service namespace
  "Command",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // plantroid_msgs__srv__detail__command__rosidl_typesupport_introspection_c__Command_Request_message_type_support_handle,
  NULL  // response message
  // plantroid_msgs__srv__detail__command__rosidl_typesupport_introspection_c__Command_Response_message_type_support_handle
};

static rosidl_service_type_support_t plantroid_msgs__srv__detail__command__rosidl_typesupport_introspection_c__Command_service_type_support_handle = {
  0,
  &plantroid_msgs__srv__detail__command__rosidl_typesupport_introspection_c__Command_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, srv, Command_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, srv, Command_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_plantroid_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, srv, Command)() {
  if (!plantroid_msgs__srv__detail__command__rosidl_typesupport_introspection_c__Command_service_type_support_handle.typesupport_identifier) {
    plantroid_msgs__srv__detail__command__rosidl_typesupport_introspection_c__Command_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)plantroid_msgs__srv__detail__command__rosidl_typesupport_introspection_c__Command_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, srv, Command_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, plantroid_msgs, srv, Command_Response)()->data;
  }

  return &plantroid_msgs__srv__detail__command__rosidl_typesupport_introspection_c__Command_service_type_support_handle;
}
