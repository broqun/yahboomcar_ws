cmake_minimum_required(VERSION 3.8)
project(arm_kin)
set(CMAKE_CXX_STANDARD 11)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ����������������� kdl_parser �� orocos_kdl��
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(arm_interface REQUIRED)
find_package(kdl_parser REQUIRED)  # ���� kdl_parser ��
find_package(orocos_kdl REQUIRED)

# �ֶ�ָ�� ROS 2 ��·�����ؼ����滻Ϊ��� ROS 2 �汾·����
link_directories(/opt/ros/humble/lib)  # ���� libkdl_parser.so ����Ŀ¼

# ͷ�ļ�·��
include_directories(
  include
  /usr/include/eigen3
  /opt/ros/humble/include  # ROS 2 ͷ�ļ�·��
)

# ������ִ���ļ�
add_executable(kin_srv src/kin_srv.cpp src/fk_ik_kin.cpp)

# ���� ROS 2 ����
ament_target_dependencies(kin_srv
  rclcpp
  std_msgs
  arm_interface
  kdl_parser
  orocos_kdl
)

# ���ӿ⣨���� kdl_parser ���Զ���⣩
target_link_libraries(kin_srv
  orocos-kdl  # KDL ��
  kdl_parser  # �������ҵ� libkdl_parser.so ��
)

# ��װ����
target_include_directories(kin_srv PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

install(
  DIRECTORY param
  DESTINATION share/${PROJECT_NAME}
)

install(TARGETS kin_srv
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()