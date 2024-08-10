// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from plantroid_msgs:msg/Speed.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__MSG__DETAIL__SPEED__TRAITS_HPP_
#define PLANTROID_MSGS__MSG__DETAIL__SPEED__TRAITS_HPP_

#include "plantroid_msgs/msg/detail/speed__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<plantroid_msgs::msg::Speed>()
{
  return "plantroid_msgs::msg::Speed";
}

template<>
inline const char * name<plantroid_msgs::msg::Speed>()
{
  return "plantroid_msgs/msg/Speed";
}

template<>
struct has_fixed_size<plantroid_msgs::msg::Speed>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<plantroid_msgs::msg::Speed>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<plantroid_msgs::msg::Speed>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PLANTROID_MSGS__MSG__DETAIL__SPEED__TRAITS_HPP_
