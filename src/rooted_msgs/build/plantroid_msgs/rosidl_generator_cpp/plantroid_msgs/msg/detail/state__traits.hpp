// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from plantroid_msgs:msg/State.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__MSG__DETAIL__STATE__TRAITS_HPP_
#define PLANTROID_MSGS__MSG__DETAIL__STATE__TRAITS_HPP_

#include "plantroid_msgs/msg/detail/state__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

// Include directives for member types
// Member 'pose'
#include "plantroid_msgs/msg/detail/pose__traits.hpp"
// Member 'speed'
#include "plantroid_msgs/msg/detail/speed__traits.hpp"

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<plantroid_msgs::msg::State>()
{
  return "plantroid_msgs::msg::State";
}

template<>
inline const char * name<plantroid_msgs::msg::State>()
{
  return "plantroid_msgs/msg/State";
}

template<>
struct has_fixed_size<plantroid_msgs::msg::State>
  : std::integral_constant<bool, has_fixed_size<plantroid_msgs::msg::Pose>::value && has_fixed_size<plantroid_msgs::msg::Speed>::value> {};

template<>
struct has_bounded_size<plantroid_msgs::msg::State>
  : std::integral_constant<bool, has_bounded_size<plantroid_msgs::msg::Pose>::value && has_bounded_size<plantroid_msgs::msg::Speed>::value> {};

template<>
struct is_message<plantroid_msgs::msg::State>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PLANTROID_MSGS__MSG__DETAIL__STATE__TRAITS_HPP_
