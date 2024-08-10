// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from plantroid_msgs:msg/Speed.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__MSG__DETAIL__SPEED__BUILDER_HPP_
#define PLANTROID_MSGS__MSG__DETAIL__SPEED__BUILDER_HPP_

#include "plantroid_msgs/msg/detail/speed__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace plantroid_msgs
{

namespace msg
{

namespace builder
{

class Init_Speed_angular
{
public:
  explicit Init_Speed_angular(::plantroid_msgs::msg::Speed & msg)
  : msg_(msg)
  {}
  ::plantroid_msgs::msg::Speed angular(::plantroid_msgs::msg::Speed::_angular_type arg)
  {
    msg_.angular = std::move(arg);
    return std::move(msg_);
  }

private:
  ::plantroid_msgs::msg::Speed msg_;
};

class Init_Speed_linear
{
public:
  Init_Speed_linear()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Speed_angular linear(::plantroid_msgs::msg::Speed::_linear_type arg)
  {
    msg_.linear = std::move(arg);
    return Init_Speed_angular(msg_);
  }

private:
  ::plantroid_msgs::msg::Speed msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::plantroid_msgs::msg::Speed>()
{
  return plantroid_msgs::msg::builder::Init_Speed_linear();
}

}  // namespace plantroid_msgs

#endif  // PLANTROID_MSGS__MSG__DETAIL__SPEED__BUILDER_HPP_
