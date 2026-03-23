cmake_minimum_required(VERSION 3.8)
project(yahboom_m3pro_lidar_tools)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(message_filters REQUIRED)

add_executable(multi_lidar_merger_node
  src/multi_lidar_merger_node.cpp
)

ament_target_dependencies(multi_lidar_merger_node
  rclcpp
  sensor_msgs
  message_filters
)

install(TARGETS
  multi_lidar_merger_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()