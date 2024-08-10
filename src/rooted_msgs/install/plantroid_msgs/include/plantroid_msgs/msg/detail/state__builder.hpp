// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from plantroid_msgs:msg/State.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__MSG__DETAIL__STATE__BUILDER_HPP_
#define PLANTROID_MSGS__MSG__DETAIL__STATE__BUILDER_HPP_

#include "plantroid_msgs/msg/detail/state__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace plantroid_msgs
{

namespace msg
{

namespace builder
{

class Init_State_speed
{
public:
  explicit Init_State_speed(::plantroid_msgs::msg::State & msg)
  : msg_(msg)
  {}
  ::plantroid_msgs::msg::State speed(::plantroid_msgs::msg::State::_speed_type arg)
  {
    msg_.speed = std::move(arg);
    return std::move(msg_);
  }

private:
  ::plantroid_msgs::msg::State msg_;
};

class Init_State_pose
{
public:
  Init_State_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_State_speed pose(::plantroid_msgs::msg::State::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_State_speed(msg_);
  }

private:
  ::plantroid_msgs::msg::State msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::plantroid_msgs::msg::State>()
{
  return plantroid_msgs::msg::builder::Init_State_pose();
}

}  // namespace plantroid_msgs

#endif  // PLANTROID_MSGS__MSG__DETAIL__STATE__BUILDER_HPP_
