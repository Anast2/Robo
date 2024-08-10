// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from plantroid_msgs:msg/Pose.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__MSG__DETAIL__POSE__TRAITS_HPP_
#define PLANTROID_MSGS__MSG__DETAIL__POSE__TRAITS_HPP_

#include "plantroid_msgs/msg/detail/pose__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<plantroid_msgs::msg::Pose>()
{
  return "plantroid_msgs::msg::Pose";
}

template<>
inline const char * name<plantroid_msgs::msg::Pose>()
{
  return "plantroid_msgs/msg/Pose";
}

template<>
struct has_fixed_size<plantroid_msgs::msg::Pose>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<plantroid_msgs::msg::Pose>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<plantroid_msgs::msg::Pose>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PLANTROID_MSGS__MSG__DETAIL__POSE__TRAITS_HPP_
