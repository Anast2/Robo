// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from plantroid_msgs:srv/Command.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__SRV__DETAIL__COMMAND__BUILDER_HPP_
#define PLANTROID_MSGS__SRV__DETAIL__COMMAND__BUILDER_HPP_

#include "plantroid_msgs/srv/detail/command__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace plantroid_msgs
{

namespace srv
{

namespace builder
{

class Init_Command_Request_speed_command
{
public:
  Init_Command_Request_speed_command()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::plantroid_msgs::srv::Command_Request speed_command(::plantroid_msgs::srv::Command_Request::_speed_command_type arg)
  {
    msg_.speed_command = std::move(arg);
    return std::move(msg_);
  }

private:
  ::plantroid_msgs::srv::Command_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::plantroid_msgs::srv::Command_Request>()
{
  return plantroid_msgs::srv::builder::Init_Command_Request_speed_command();
}

}  // namespace plantroid_msgs


namespace plantroid_msgs
{

namespace srv
{

namespace builder
{

class Init_Command_Response_status
{
public:
  Init_Command_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::plantroid_msgs::srv::Command_Response status(::plantroid_msgs::srv::Command_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return std::move(msg_);
  }

private:
  ::plantroid_msgs::srv::Command_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::plantroid_msgs::srv::Command_Response>()
{
  return plantroid_msgs::srv::builder::Init_Command_Response_status();
}

}  // namespace plantroid_msgs

#endif  // PLANTROID_MSGS__SRV__DETAIL__COMMAND__BUILDER_HPP_
