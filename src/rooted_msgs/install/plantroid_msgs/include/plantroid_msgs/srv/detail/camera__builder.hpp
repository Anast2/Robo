// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from plantroid_msgs:srv/Camera.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__SRV__DETAIL__CAMERA__BUILDER_HPP_
#define PLANTROID_MSGS__SRV__DETAIL__CAMERA__BUILDER_HPP_

#include "plantroid_msgs/srv/detail/camera__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace plantroid_msgs
{

namespace srv
{

namespace builder
{

class Init_Camera_Request_imagetype
{
public:
  Init_Camera_Request_imagetype()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::plantroid_msgs::srv::Camera_Request imagetype(::plantroid_msgs::srv::Camera_Request::_imagetype_type arg)
  {
    msg_.imagetype = std::move(arg);
    return std::move(msg_);
  }

private:
  ::plantroid_msgs::srv::Camera_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::plantroid_msgs::srv::Camera_Request>()
{
  return plantroid_msgs::srv::builder::Init_Camera_Request_imagetype();
}

}  // namespace plantroid_msgs


namespace plantroid_msgs
{

namespace srv
{

namespace builder
{

class Init_Camera_Response_image
{
public:
  Init_Camera_Response_image()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::plantroid_msgs::srv::Camera_Response image(::plantroid_msgs::srv::Camera_Response::_image_type arg)
  {
    msg_.image = std::move(arg);
    return std::move(msg_);
  }

private:
  ::plantroid_msgs::srv::Camera_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::plantroid_msgs::srv::Camera_Response>()
{
  return plantroid_msgs::srv::builder::Init_Camera_Response_image();
}

}  // namespace plantroid_msgs

#endif  // PLANTROID_MSGS__SRV__DETAIL__CAMERA__BUILDER_HPP_
