// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from plantroid_msgs:srv/Command.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__SRV__DETAIL__COMMAND__STRUCT_HPP_
#define PLANTROID_MSGS__SRV__DETAIL__COMMAND__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


// Include directives for member types
// Member 'speed_command'
#include "plantroid_msgs/msg/detail/speed__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__plantroid_msgs__srv__Command_Request __attribute__((deprecated))
#else
# define DEPRECATED__plantroid_msgs__srv__Command_Request __declspec(deprecated)
#endif

namespace plantroid_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Command_Request_
{
  using Type = Command_Request_<ContainerAllocator>;

  explicit Command_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : speed_command(_init)
  {
    (void)_init;
  }

  explicit Command_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : speed_command(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _speed_command_type =
    plantroid_msgs::msg::Speed_<ContainerAllocator>;
  _speed_command_type speed_command;

  // setters for named parameter idiom
  Type & set__speed_command(
    const plantroid_msgs::msg::Speed_<ContainerAllocator> & _arg)
  {
    this->speed_command = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    plantroid_msgs::srv::Command_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const plantroid_msgs::srv::Command_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<plantroid_msgs::srv::Command_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<plantroid_msgs::srv::Command_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      plantroid_msgs::srv::Command_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<plantroid_msgs::srv::Command_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      plantroid_msgs::srv::Command_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<plantroid_msgs::srv::Command_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<plantroid_msgs::srv::Command_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<plantroid_msgs::srv::Command_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__plantroid_msgs__srv__Command_Request
    std::shared_ptr<plantroid_msgs::srv::Command_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__plantroid_msgs__srv__Command_Request
    std::shared_ptr<plantroid_msgs::srv::Command_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Command_Request_ & other) const
  {
    if (this->speed_command != other.speed_command) {
      return false;
    }
    return true;
  }
  bool operator!=(const Command_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Command_Request_

// alias to use template instance with default allocator
using Command_Request =
  plantroid_msgs::srv::Command_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace plantroid_msgs


#ifndef _WIN32
# define DEPRECATED__plantroid_msgs__srv__Command_Response __attribute__((deprecated))
#else
# define DEPRECATED__plantroid_msgs__srv__Command_Response __declspec(deprecated)
#endif

namespace plantroid_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Command_Response_
{
  using Type = Command_Response_<ContainerAllocator>;

  explicit Command_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = "";
    }
  }

  explicit Command_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : status(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = "";
    }
  }

  // field types and members
  using _status_type =
    std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other>;
  _status_type status;

  // setters for named parameter idiom
  Type & set__status(
    const std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other> & _arg)
  {
    this->status = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    plantroid_msgs::srv::Command_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const plantroid_msgs::srv::Command_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<plantroid_msgs::srv::Command_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<plantroid_msgs::srv::Command_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      plantroid_msgs::srv::Command_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<plantroid_msgs::srv::Command_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      plantroid_msgs::srv::Command_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<plantroid_msgs::srv::Command_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<plantroid_msgs::srv::Command_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<plantroid_msgs::srv::Command_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__plantroid_msgs__srv__Command_Response
    std::shared_ptr<plantroid_msgs::srv::Command_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__plantroid_msgs__srv__Command_Response
    std::shared_ptr<plantroid_msgs::srv::Command_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Command_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    return true;
  }
  bool operator!=(const Command_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Command_Response_

// alias to use template instance with default allocator
using Command_Response =
  plantroid_msgs::srv::Command_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace plantroid_msgs

namespace plantroid_msgs
{

namespace srv
{

struct Command
{
  using Request = plantroid_msgs::srv::Command_Request;
  using Response = plantroid_msgs::srv::Command_Response;
};

}  // namespace srv

}  // namespace plantroid_msgs

#endif  // PLANTROID_MSGS__SRV__DETAIL__COMMAND__STRUCT_HPP_
