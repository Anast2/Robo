// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from plantroid_msgs:srv/Sensors.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__SRV__DETAIL__SENSORS__BUILDER_HPP_
#define PLANTROID_MSGS__SRV__DETAIL__SENSORS__BUILDER_HPP_

#include "plantroid_msgs/srv/detail/sensors__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace plantroid_msgs
{

namespace srv
{

namespace builder
{

class Init_Sensors_Request_sensor_number
{
public:
  Init_Sensors_Request_sensor_number()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::plantroid_msgs::srv::Sensors_Request sensor_number(::plantroid_msgs::srv::Sensors_Request::_sensor_number_type arg)
  {
    msg_.sensor_number = std::move(arg);
    return std::move(msg_);
  }

private:
  ::plantroid_msgs::srv::Sensors_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::plantroid_msgs::srv::Sensors_Request>()
{
  return plantroid_msgs::srv::builder::Init_Sensors_Request_sensor_number();
}

}  // namespace plantroid_msgs


namespace plantroid_msgs
{

namespace srv
{

namespace builder
{

class Init_Sensors_Response_sensor_reading
{
public:
  Init_Sensors_Response_sensor_reading()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::plantroid_msgs::srv::Sensors_Response sensor_reading(::plantroid_msgs::srv::Sensors_Response::_sensor_reading_type arg)
  {
    msg_.sensor_reading = std::move(arg);
    return std::move(msg_);
  }

private:
  ::plantroid_msgs::srv::Sensors_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::plantroid_msgs::srv::Sensors_Response>()
{
  return plantroid_msgs::srv::builder::Init_Sensors_Response_sensor_reading();
}

}  // namespace plantroid_msgs

#endif  // PLANTROID_MSGS__SRV__DETAIL__SENSORS__BUILDER_HPP_
