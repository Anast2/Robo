// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from plantroid_msgs:srv/NeckServo.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__SRV__DETAIL__NECK_SERVO__BUILDER_HPP_
#define PLANTROID_MSGS__SRV__DETAIL__NECK_SERVO__BUILDER_HPP_

#include "plantroid_msgs/srv/detail/neck_servo__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace plantroid_msgs
{

namespace srv
{

namespace builder
{

class Init_NeckServo_Request_angle
{
public:
  Init_NeckServo_Request_angle()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::plantroid_msgs::srv::NeckServo_Request angle(::plantroid_msgs::srv::NeckServo_Request::_angle_type arg)
  {
    msg_.angle = std::move(arg);
    return std::move(msg_);
  }

private:
  ::plantroid_msgs::srv::NeckServo_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::plantroid_msgs::srv::NeckServo_Request>()
{
  return plantroid_msgs::srv::builder::Init_NeckServo_Request_angle();
}

}  // namespace plantroid_msgs


namespace plantroid_msgs
{

namespace srv
{

namespace builder
{

class Init_NeckServo_Response_status
{
public:
  Init_NeckServo_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::plantroid_msgs::srv::NeckServo_Response status(::plantroid_msgs::srv::NeckServo_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return std::move(msg_);
  }

private:
  ::plantroid_msgs::srv::NeckServo_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::plantroid_msgs::srv::NeckServo_Response>()
{
  return plantroid_msgs::srv::builder::Init_NeckServo_Response_status();
}

}  // namespace plantroid_msgs

#endif  // PLANTROID_MSGS__SRV__DETAIL__NECK_SERVO__BUILDER_HPP_
