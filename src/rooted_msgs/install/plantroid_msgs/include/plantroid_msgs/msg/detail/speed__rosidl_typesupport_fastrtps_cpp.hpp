// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from plantroid_msgs:msg/Speed.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__MSG__DETAIL__SPEED__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define PLANTROID_MSGS__MSG__DETAIL__SPEED__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "plantroid_msgs/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "plantroid_msgs/msg/detail/speed__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace plantroid_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
cdr_serialize(
  const plantroid_msgs::msg::Speed & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  plantroid_msgs::msg::Speed & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
get_serialized_size(
  const plantroid_msgs::msg::Speed & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
max_serialized_size_Speed(
  bool & full_bounded,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace plantroid_msgs

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_plantroid_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, plantroid_msgs, msg, Speed)();

#ifdef __cplusplus
}
#endif

#endif  // PLANTROID_MSGS__MSG__DETAIL__SPEED__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
