// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from plantroid_msgs:srv/Camera.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__SRV__DETAIL__CAMERA__STRUCT_HPP_
#define PLANTROID_MSGS__SRV__DETAIL__CAMERA__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__plantroid_msgs__srv__Camera_Request __attribute__((deprecated))
#else
# define DEPRECATED__plantroid_msgs__srv__Camera_Request __declspec(deprecated)
#endif

namespace plantroid_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Camera_Request_
{
  using Type = Camera_Request_<ContainerAllocator>;

  explicit Camera_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->imagetype = 0;
    }
  }

  explicit Camera_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->imagetype = 0;
    }
  }

  // field types and members
  using _imagetype_type =
    int8_t;
  _imagetype_type imagetype;

  // setters for named parameter idiom
  Type & set__imagetype(
    const int8_t & _arg)
  {
    this->imagetype = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    plantroid_msgs::srv::Camera_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const plantroid_msgs::srv::Camera_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<plantroid_msgs::srv::Camera_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<plantroid_msgs::srv::Camera_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      plantroid_msgs::srv::Camera_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<plantroid_msgs::srv::Camera_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      plantroid_msgs::srv::Camera_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<plantroid_msgs::srv::Camera_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<plantroid_msgs::srv::Camera_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<plantroid_msgs::srv::Camera_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__plantroid_msgs__srv__Camera_Request
    std::shared_ptr<plantroid_msgs::srv::Camera_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__plantroid_msgs__srv__Camera_Request
    std::shared_ptr<plantroid_msgs::srv::Camera_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Camera_Request_ & other) const
  {
    if (this->imagetype != other.imagetype) {
      return false;
    }
    return true;
  }
  bool operator!=(const Camera_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Camera_Request_

// alias to use template instance with default allocator
using Camera_Request =
  plantroid_msgs::srv::Camera_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace plantroid_msgs


#ifndef _WIN32
# define DEPRECATED__plantroid_msgs__srv__Camera_Response __attribute__((deprecated))
#else
# define DEPRECATED__plantroid_msgs__srv__Camera_Response __declspec(deprecated)
#endif

namespace plantroid_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Camera_Response_
{
  using Type = Camera_Response_<ContainerAllocator>;

  explicit Camera_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->image = "";
    }
  }

  explicit Camera_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : image(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->image = "";
    }
  }

  // field types and members
  using _image_type =
    std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other>;
  _image_type image;

  // setters for named parameter idiom
  Type & set__image(
    const std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other> & _arg)
  {
    this->image = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    plantroid_msgs::srv::Camera_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const plantroid_msgs::srv::Camera_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<plantroid_msgs::srv::Camera_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<plantroid_msgs::srv::Camera_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      plantroid_msgs::srv::Camera_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<plantroid_msgs::srv::Camera_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      plantroid_msgs::srv::Camera_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<plantroid_msgs::srv::Camera_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<plantroid_msgs::srv::Camera_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<plantroid_msgs::srv::Camera_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__plantroid_msgs__srv__Camera_Response
    std::shared_ptr<plantroid_msgs::srv::Camera_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__plantroid_msgs__srv__Camera_Response
    std::shared_ptr<plantroid_msgs::srv::Camera_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Camera_Response_ & other) const
  {
    if (this->image != other.image) {
      return false;
    }
    return true;
  }
  bool operator!=(const Camera_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Camera_Response_

// alias to use template instance with default allocator
using Camera_Response =
  plantroid_msgs::srv::Camera_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace plantroid_msgs

namespace plantroid_msgs
{

namespace srv
{

struct Camera
{
  using Request = plantroid_msgs::srv::Camera_Request;
  using Response = plantroid_msgs::srv::Camera_Response;
};

}  // namespace srv

}  // namespace plantroid_msgs

#endif  // PLANTROID_MSGS__SRV__DETAIL__CAMERA__STRUCT_HPP_
