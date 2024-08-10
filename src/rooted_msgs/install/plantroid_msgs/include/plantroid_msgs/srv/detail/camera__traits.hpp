// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from plantroid_msgs:srv/Camera.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__SRV__DETAIL__CAMERA__TRAITS_HPP_
#define PLANTROID_MSGS__SRV__DETAIL__CAMERA__TRAITS_HPP_

#include "plantroid_msgs/srv/detail/camera__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<plantroid_msgs::srv::Camera_Request>()
{
  return "plantroid_msgs::srv::Camera_Request";
}

template<>
inline const char * name<plantroid_msgs::srv::Camera_Request>()
{
  return "plantroid_msgs/srv/Camera_Request";
}

template<>
struct has_fixed_size<plantroid_msgs::srv::Camera_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<plantroid_msgs::srv::Camera_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<plantroid_msgs::srv::Camera_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<plantroid_msgs::srv::Camera_Response>()
{
  return "plantroid_msgs::srv::Camera_Response";
}

template<>
inline const char * name<plantroid_msgs::srv::Camera_Response>()
{
  return "plantroid_msgs/srv/Camera_Response";
}

template<>
struct has_fixed_size<plantroid_msgs::srv::Camera_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<plantroid_msgs::srv::Camera_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<plantroid_msgs::srv::Camera_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<plantroid_msgs::srv::Camera>()
{
  return "plantroid_msgs::srv::Camera";
}

template<>
inline const char * name<plantroid_msgs::srv::Camera>()
{
  return "plantroid_msgs/srv/Camera";
}

template<>
struct has_fixed_size<plantroid_msgs::srv::Camera>
  : std::integral_constant<
    bool,
    has_fixed_size<plantroid_msgs::srv::Camera_Request>::value &&
    has_fixed_size<plantroid_msgs::srv::Camera_Response>::value
  >
{
};

template<>
struct has_bounded_size<plantroid_msgs::srv::Camera>
  : std::integral_constant<
    bool,
    has_bounded_size<plantroid_msgs::srv::Camera_Request>::value &&
    has_bounded_size<plantroid_msgs::srv::Camera_Response>::value
  >
{
};

template<>
struct is_service<plantroid_msgs::srv::Camera>
  : std::true_type
{
};

template<>
struct is_service_request<plantroid_msgs::srv::Camera_Request>
  : std::true_type
{
};

template<>
struct is_service_response<plantroid_msgs::srv::Camera_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // PLANTROID_MSGS__SRV__DETAIL__CAMERA__TRAITS_HPP_
