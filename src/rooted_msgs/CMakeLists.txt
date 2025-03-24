cmake_minimum_required(VERSION 3.8)
project(rooted_msgs)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Pose.msg"
  "msg/Speed.msg"
  "msg/State.msg"
  "srv/Camera.srv"
  "srv/NeckServo.srv"
  "srv/NavigationOrder.srv"
  "srv/LLM.srv"
  "srv/MemoryRequest.srv"
  "srv/Sensors.srv"
  "srv/Command.srv"
  "srv/Busy.srv"
  "srv/Gesture.srv"
  "action/HighLevelAction.action"  # Added action file
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()