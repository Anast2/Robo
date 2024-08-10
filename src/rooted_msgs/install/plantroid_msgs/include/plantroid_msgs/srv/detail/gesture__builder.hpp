// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from plantroid_msgs:srv/Gesture.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__SRV__DETAIL__GESTURE__BUILDER_HPP_
#define PLANTROID_MSGS__SRV__DETAIL__GESTURE__BUILDER_HPP_

#include "plantroid_msgs/srv/detail/gesture__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace plantroid_msgs
{

namespace srv
{

namespace builder
{

class Init_Gesture_Request_gesture
{
public:
  Init_Gesture_Request_gesture()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::plantroid_msgs::srv::Gesture_Request gesture(::plantroid_msgs::srv::Gesture_Request::_gesture_type arg)
  {
    msg_.gesture = std::move(arg);
    return std::move(msg_);
  }

private:
  ::plantroid_msgs::srv::Gesture_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::plantroid_msgs::srv::Gesture_Request>()
{
  return plantroid_msgs::srv::builder::Init_Gesture_Request_gesture();
}

}  // namespace plantroid_msgs


namespace plantroid_msgs
{

namespace srv
{

namespace builder
{

class Init_Gesture_Response_result
{
public:
  Init_Gesture_Response_result()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::plantroid_msgs::srv::Gesture_Response result(::plantroid_msgs::srv::Gesture_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::plantroid_msgs::srv::Gesture_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::plantroid_msgs::srv::Gesture_Response>()
{
  return plantroid_msgs::srv::builder::Init_Gesture_Response_result();
}

}  // namespace plantroid_msgs

#endif  // PLANTROID_MSGS__SRV__DETAIL__GESTURE__BUILDER_HPP_
