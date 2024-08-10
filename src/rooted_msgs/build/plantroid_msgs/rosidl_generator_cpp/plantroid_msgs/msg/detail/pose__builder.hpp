// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from plantroid_msgs:msg/Pose.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__MSG__DETAIL__POSE__BUILDER_HPP_
#define PLANTROID_MSGS__MSG__DETAIL__POSE__BUILDER_HPP_

#include "plantroid_msgs/msg/detail/pose__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace plantroid_msgs
{

namespace msg
{

namespace builder
{

class Init_Pose_theta
{
public:
  explicit Init_Pose_theta(::plantroid_msgs::msg::Pose & msg)
  : msg_(msg)
  {}
  ::plantroid_msgs::msg::Pose theta(::plantroid_msgs::msg::Pose::_theta_type arg)
  {
    msg_.theta = std::move(arg);
    return std::move(msg_);
  }

private:
  ::plantroid_msgs::msg::Pose msg_;
};

class Init_Pose_y
{
public:
  explicit Init_Pose_y(::plantroid_msgs::msg::Pose & msg)
  : msg_(msg)
  {}
  Init_Pose_theta y(::plantroid_msgs::msg::Pose::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Pose_theta(msg_);
  }

private:
  ::plantroid_msgs::msg::Pose msg_;
};

class Init_Pose_x
{
public:
  Init_Pose_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Pose_y x(::plantroid_msgs::msg::Pose::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Pose_y(msg_);
  }

private:
  ::plantroid_msgs::msg::Pose msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::plantroid_msgs::msg::Pose>()
{
  return plantroid_msgs::msg::builder::Init_Pose_x();
}

}  // namespace plantroid_msgs

#endif  // PLANTROID_MSGS__MSG__DETAIL__POSE__BUILDER_HPP_
