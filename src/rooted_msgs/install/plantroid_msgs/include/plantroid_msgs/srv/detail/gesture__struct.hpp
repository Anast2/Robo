// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from plantroid_msgs:srv/Gesture.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__SRV__DETAIL__GESTURE__STRUCT_HPP_
#define PLANTROID_MSGS__SRV__DETAIL__GESTURE__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__plantroid_msgs__srv__Gesture_Request __attribute__((deprecated))
#else
# define DEPRECATED__plantroid_msgs__srv__Gesture_Request __declspec(deprecated)
#endif

namespace plantroid_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Gesture_Request_
{
  using Type = Gesture_Request_<ContainerAllocator>;

  explicit Gesture_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->gesture = "";
    }
  }

  explicit Gesture_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : gesture(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->gesture = "";
    }
  }

  // field types and members
  using _gesture_type =
    std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other>;
  _gesture_type gesture;

  // setters for named parameter idiom
  Type & set__gesture(
    const std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other> & _arg)
  {
    this->gesture = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    plantroid_msgs::srv::Gesture_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const plantroid_msgs::srv::Gesture_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<plantroid_msgs::srv::Gesture_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<plantroid_msgs::srv::Gesture_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      plantroid_msgs::srv::Gesture_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<plantroid_msgs::srv::Gesture_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      plantroid_msgs::srv::Gesture_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<plantroid_msgs::srv::Gesture_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<plantroid_msgs::srv::Gesture_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<plantroid_msgs::srv::Gesture_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__plantroid_msgs__srv__Gesture_Request
    std::shared_ptr<plantroid_msgs::srv::Gesture_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__plantroid_msgs__srv__Gesture_Request
    std::shared_ptr<plantroid_msgs::srv::Gesture_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Gesture_Request_ & other) const
  {
    if (this->gesture != other.gesture) {
      return false;
    }
    return true;
  }
  bool operator!=(const Gesture_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Gesture_Request_

// alias to use template instance with default allocator
using Gesture_Request =
  plantroid_msgs::srv::Gesture_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace plantroid_msgs


#ifndef _WIN32
# define DEPRECATED__plantroid_msgs__srv__Gesture_Response __attribute__((deprecated))
#else
# define DEPRECATED__plantroid_msgs__srv__Gesture_Response __declspec(deprecated)
#endif

namespace plantroid_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Gesture_Response_
{
  using Type = Gesture_Response_<ContainerAllocator>;

  explicit Gesture_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->result = "";
    }
  }

  explicit Gesture_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->result = "";
    }
  }

  // field types and members
  using _result_type =
    std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__result(
    const std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    plantroid_msgs::srv::Gesture_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const plantroid_msgs::srv::Gesture_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<plantroid_msgs::srv::Gesture_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<plantroid_msgs::srv::Gesture_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      plantroid_msgs::srv::Gesture_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<plantroid_msgs::srv::Gesture_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      plantroid_msgs::srv::Gesture_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<plantroid_msgs::srv::Gesture_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<plantroid_msgs::srv::Gesture_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<plantroid_msgs::srv::Gesture_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__plantroid_msgs__srv__Gesture_Response
    std::shared_ptr<plantroid_msgs::srv::Gesture_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__plantroid_msgs__srv__Gesture_Response
    std::shared_ptr<plantroid_msgs::srv::Gesture_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Gesture_Response_ & other) const
  {
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const Gesture_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Gesture_Response_

// alias to use template instance with default allocator
using Gesture_Response =
  plantroid_msgs::srv::Gesture_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace plantroid_msgs

namespace plantroid_msgs
{

namespace srv
{

struct Gesture
{
  using Request = plantroid_msgs::srv::Gesture_Request;
  using Response = plantroid_msgs::srv::Gesture_Response;
};

}  // namespace srv

}  // namespace plantroid_msgs

#endif  // PLANTROID_MSGS__SRV__DETAIL__GESTURE__STRUCT_HPP_
