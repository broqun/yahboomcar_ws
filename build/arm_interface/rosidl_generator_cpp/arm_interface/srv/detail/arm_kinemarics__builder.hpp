// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_interface:srv/ArmKinemarics.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACE__SRV__DETAIL__ARM_KINEMARICS__BUILDER_HPP_
#define ARM_INTERFACE__SRV__DETAIL__ARM_KINEMARICS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "arm_interface/srv/detail/arm_kinemarics__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace arm_interface
{

namespace srv
{

namespace builder
{

class Init_ArmKinemarics_Request_kin_name
{
public:
  explicit Init_ArmKinemarics_Request_kin_name(::arm_interface::srv::ArmKinemarics_Request & msg)
  : msg_(msg)
  {}
  ::arm_interface::srv::ArmKinemarics_Request kin_name(::arm_interface::srv::ArmKinemarics_Request::_kin_name_type arg)
  {
    msg_.kin_name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Request msg_;
};

class Init_ArmKinemarics_Request_cur_joint6
{
public:
  explicit Init_ArmKinemarics_Request_cur_joint6(::arm_interface::srv::ArmKinemarics_Request & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Request_kin_name cur_joint6(::arm_interface::srv::ArmKinemarics_Request::_cur_joint6_type arg)
  {
    msg_.cur_joint6 = std::move(arg);
    return Init_ArmKinemarics_Request_kin_name(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Request msg_;
};

class Init_ArmKinemarics_Request_cur_joint5
{
public:
  explicit Init_ArmKinemarics_Request_cur_joint5(::arm_interface::srv::ArmKinemarics_Request & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Request_cur_joint6 cur_joint5(::arm_interface::srv::ArmKinemarics_Request::_cur_joint5_type arg)
  {
    msg_.cur_joint5 = std::move(arg);
    return Init_ArmKinemarics_Request_cur_joint6(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Request msg_;
};

class Init_ArmKinemarics_Request_cur_joint4
{
public:
  explicit Init_ArmKinemarics_Request_cur_joint4(::arm_interface::srv::ArmKinemarics_Request & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Request_cur_joint5 cur_joint4(::arm_interface::srv::ArmKinemarics_Request::_cur_joint4_type arg)
  {
    msg_.cur_joint4 = std::move(arg);
    return Init_ArmKinemarics_Request_cur_joint5(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Request msg_;
};

class Init_ArmKinemarics_Request_cur_joint3
{
public:
  explicit Init_ArmKinemarics_Request_cur_joint3(::arm_interface::srv::ArmKinemarics_Request & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Request_cur_joint4 cur_joint3(::arm_interface::srv::ArmKinemarics_Request::_cur_joint3_type arg)
  {
    msg_.cur_joint3 = std::move(arg);
    return Init_ArmKinemarics_Request_cur_joint4(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Request msg_;
};

class Init_ArmKinemarics_Request_cur_joint2
{
public:
  explicit Init_ArmKinemarics_Request_cur_joint2(::arm_interface::srv::ArmKinemarics_Request & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Request_cur_joint3 cur_joint2(::arm_interface::srv::ArmKinemarics_Request::_cur_joint2_type arg)
  {
    msg_.cur_joint2 = std::move(arg);
    return Init_ArmKinemarics_Request_cur_joint3(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Request msg_;
};

class Init_ArmKinemarics_Request_cur_joint1
{
public:
  explicit Init_ArmKinemarics_Request_cur_joint1(::arm_interface::srv::ArmKinemarics_Request & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Request_cur_joint2 cur_joint1(::arm_interface::srv::ArmKinemarics_Request::_cur_joint1_type arg)
  {
    msg_.cur_joint1 = std::move(arg);
    return Init_ArmKinemarics_Request_cur_joint2(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Request msg_;
};

class Init_ArmKinemarics_Request_yaw
{
public:
  explicit Init_ArmKinemarics_Request_yaw(::arm_interface::srv::ArmKinemarics_Request & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Request_cur_joint1 yaw(::arm_interface::srv::ArmKinemarics_Request::_yaw_type arg)
  {
    msg_.yaw = std::move(arg);
    return Init_ArmKinemarics_Request_cur_joint1(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Request msg_;
};

class Init_ArmKinemarics_Request_pitch
{
public:
  explicit Init_ArmKinemarics_Request_pitch(::arm_interface::srv::ArmKinemarics_Request & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Request_yaw pitch(::arm_interface::srv::ArmKinemarics_Request::_pitch_type arg)
  {
    msg_.pitch = std::move(arg);
    return Init_ArmKinemarics_Request_yaw(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Request msg_;
};

class Init_ArmKinemarics_Request_roll
{
public:
  explicit Init_ArmKinemarics_Request_roll(::arm_interface::srv::ArmKinemarics_Request & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Request_pitch roll(::arm_interface::srv::ArmKinemarics_Request::_roll_type arg)
  {
    msg_.roll = std::move(arg);
    return Init_ArmKinemarics_Request_pitch(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Request msg_;
};

class Init_ArmKinemarics_Request_tar_z
{
public:
  explicit Init_ArmKinemarics_Request_tar_z(::arm_interface::srv::ArmKinemarics_Request & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Request_roll tar_z(::arm_interface::srv::ArmKinemarics_Request::_tar_z_type arg)
  {
    msg_.tar_z = std::move(arg);
    return Init_ArmKinemarics_Request_roll(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Request msg_;
};

class Init_ArmKinemarics_Request_tar_y
{
public:
  explicit Init_ArmKinemarics_Request_tar_y(::arm_interface::srv::ArmKinemarics_Request & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Request_tar_z tar_y(::arm_interface::srv::ArmKinemarics_Request::_tar_y_type arg)
  {
    msg_.tar_y = std::move(arg);
    return Init_ArmKinemarics_Request_tar_z(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Request msg_;
};

class Init_ArmKinemarics_Request_tar_x
{
public:
  Init_ArmKinemarics_Request_tar_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ArmKinemarics_Request_tar_y tar_x(::arm_interface::srv::ArmKinemarics_Request::_tar_x_type arg)
  {
    msg_.tar_x = std::move(arg);
    return Init_ArmKinemarics_Request_tar_y(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interface::srv::ArmKinemarics_Request>()
{
  return arm_interface::srv::builder::Init_ArmKinemarics_Request_tar_x();
}

}  // namespace arm_interface


namespace arm_interface
{

namespace srv
{

namespace builder
{

class Init_ArmKinemarics_Response_yaw
{
public:
  explicit Init_ArmKinemarics_Response_yaw(::arm_interface::srv::ArmKinemarics_Response & msg)
  : msg_(msg)
  {}
  ::arm_interface::srv::ArmKinemarics_Response yaw(::arm_interface::srv::ArmKinemarics_Response::_yaw_type arg)
  {
    msg_.yaw = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Response msg_;
};

class Init_ArmKinemarics_Response_pitch
{
public:
  explicit Init_ArmKinemarics_Response_pitch(::arm_interface::srv::ArmKinemarics_Response & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Response_yaw pitch(::arm_interface::srv::ArmKinemarics_Response::_pitch_type arg)
  {
    msg_.pitch = std::move(arg);
    return Init_ArmKinemarics_Response_yaw(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Response msg_;
};

class Init_ArmKinemarics_Response_roll
{
public:
  explicit Init_ArmKinemarics_Response_roll(::arm_interface::srv::ArmKinemarics_Response & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Response_pitch roll(::arm_interface::srv::ArmKinemarics_Response::_roll_type arg)
  {
    msg_.roll = std::move(arg);
    return Init_ArmKinemarics_Response_pitch(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Response msg_;
};

class Init_ArmKinemarics_Response_z
{
public:
  explicit Init_ArmKinemarics_Response_z(::arm_interface::srv::ArmKinemarics_Response & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Response_roll z(::arm_interface::srv::ArmKinemarics_Response::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_ArmKinemarics_Response_roll(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Response msg_;
};

class Init_ArmKinemarics_Response_y
{
public:
  explicit Init_ArmKinemarics_Response_y(::arm_interface::srv::ArmKinemarics_Response & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Response_z y(::arm_interface::srv::ArmKinemarics_Response::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_ArmKinemarics_Response_z(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Response msg_;
};

class Init_ArmKinemarics_Response_x
{
public:
  explicit Init_ArmKinemarics_Response_x(::arm_interface::srv::ArmKinemarics_Response & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Response_y x(::arm_interface::srv::ArmKinemarics_Response::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_ArmKinemarics_Response_y(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Response msg_;
};

class Init_ArmKinemarics_Response_joint6
{
public:
  explicit Init_ArmKinemarics_Response_joint6(::arm_interface::srv::ArmKinemarics_Response & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Response_x joint6(::arm_interface::srv::ArmKinemarics_Response::_joint6_type arg)
  {
    msg_.joint6 = std::move(arg);
    return Init_ArmKinemarics_Response_x(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Response msg_;
};

class Init_ArmKinemarics_Response_joint5
{
public:
  explicit Init_ArmKinemarics_Response_joint5(::arm_interface::srv::ArmKinemarics_Response & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Response_joint6 joint5(::arm_interface::srv::ArmKinemarics_Response::_joint5_type arg)
  {
    msg_.joint5 = std::move(arg);
    return Init_ArmKinemarics_Response_joint6(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Response msg_;
};

class Init_ArmKinemarics_Response_joint4
{
public:
  explicit Init_ArmKinemarics_Response_joint4(::arm_interface::srv::ArmKinemarics_Response & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Response_joint5 joint4(::arm_interface::srv::ArmKinemarics_Response::_joint4_type arg)
  {
    msg_.joint4 = std::move(arg);
    return Init_ArmKinemarics_Response_joint5(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Response msg_;
};

class Init_ArmKinemarics_Response_joint3
{
public:
  explicit Init_ArmKinemarics_Response_joint3(::arm_interface::srv::ArmKinemarics_Response & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Response_joint4 joint3(::arm_interface::srv::ArmKinemarics_Response::_joint3_type arg)
  {
    msg_.joint3 = std::move(arg);
    return Init_ArmKinemarics_Response_joint4(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Response msg_;
};

class Init_ArmKinemarics_Response_joint2
{
public:
  explicit Init_ArmKinemarics_Response_joint2(::arm_interface::srv::ArmKinemarics_Response & msg)
  : msg_(msg)
  {}
  Init_ArmKinemarics_Response_joint3 joint2(::arm_interface::srv::ArmKinemarics_Response::_joint2_type arg)
  {
    msg_.joint2 = std::move(arg);
    return Init_ArmKinemarics_Response_joint3(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Response msg_;
};

class Init_ArmKinemarics_Response_joint1
{
public:
  Init_ArmKinemarics_Response_joint1()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ArmKinemarics_Response_joint2 joint1(::arm_interface::srv::ArmKinemarics_Response::_joint1_type arg)
  {
    msg_.joint1 = std::move(arg);
    return Init_ArmKinemarics_Response_joint2(msg_);
  }

private:
  ::arm_interface::srv::ArmKinemarics_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interface::srv::ArmKinemarics_Response>()
{
  return arm_interface::srv::builder::Init_ArmKinemarics_Response_joint1();
}

}  // namespace arm_interface

#endif  // ARM_INTERFACE__SRV__DETAIL__ARM_KINEMARICS__BUILDER_HPP_
