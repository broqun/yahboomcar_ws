# yahboomcar_ws 工作空间目录结构

```
yahboomcar_ws/
├── .git/
├── .gitignore
├── build/
├── install/
├── log/
├── src/
│   ├── arm_driver/
│   │   ├── arm_driver/
│   │   │   ├── __init__.py
│   │   │   └── arm_driver.py
│   │   ├── package.xml
│   │   ├── resource/
│   │   ├── setup.cfg
│   │   ├── setup.py
│   │   └── test/
│   │
│   ├── arm_interface/
│   │   ├── CMakeLists.txt
│   │   ├── msg/           # AprilTagInfo, ArmJoint, Position, ShapeInfo 等 .msg
│   │   ├── package.xml
│   │   └── srv/            # ArmKinemarics.srv
│   │
│   ├── arm_kin/
│   │   ├── CMakeLists.txt
│   │   ├── include/arm_kin/
│   │   ├── param/          # offset_value.yaml
│   │   ├── package.xml
│   │   └── src/            # fk_ik_kin.cpp, kin_srv.cpp
│   │
│   ├── arm_msgs/
│   │   ├── CMakeLists.txt
│   │   ├── msg/            # ArmJoint.msg, ArmJoints.msg
│   │   └── package.xml
│   │
│   ├── aws-robomaker-hospital-world/
│   │   ├── CMakeLists.txt
│   │   ├── docs/
│   │   ├── fuel_models/    # 医院场景 Gazebo 模型 (桌椅、病床、推车等)
│   │   ├── fuel_utility.py
│   │   ├── launch/         # hospital.launch, view_hospital.launch
│   │   ├── models/         # 医院建筑、电梯、窗帘等模型
│   │   ├── worlds/         # hospital.world 等
│   │   └── LICENSE, CODE_OF_CONDUCT.md, CONTRIBUTING.md
│   │
│   ├── learning_dds/
│   │   ├── learning_dds/   # dds_controller_pub.py, dds_robot_sub.py
│   │   ├── package.xml
│   │   ├── setup.py, setup.cfg
│   │   ├── resource/, test/
│   │   └── ...
│   │
│   ├── learning_time/
│   │   ├── learning_time/  # get_clock_demo, rate_demo, timer_demo 等
│   │   ├── package.xml
│   │   └── setup.py, resource/, test/
│   │
│   ├── learn_launch/
│   │   ├── launch/         # include_launch, multi_node_launch, remap_name_launch 等
│   │   ├── learn_launch/
│   │   ├── package.xml
│   │   └── setup.py, resource/, test/
│   │
│   ├── M3Pro_config/       # MoveIt 配置 (M3Pro)
│   │   ├── CMakeLists.txt
│   │   ├── config/         # M3Pro.urdf.xacro, M3Pro.srdf, kinematics, moveit 等
│   │   ├── launch/         # demo, move_group, moveit_rviz, rsp, spawn_controllers 等
│   │   └── package.xml
│   │
│   ├── M3Pro_demo/
│   │   ├── M3Pro_demo/     # apriltag/颜色/手势/抓取等 demo 脚本
│   │   ├── launch/         # camera_arm_kin.launch.py
│   │   ├── package.xml
│   │   └── setup.py, resource/, test/
│   │
│   ├── M3Pro_MoveIt_demo/
│   │   ├── M3Pro_MoveIt_demo/  # random_move.py, SimulationToMachine.py
│   │   ├── package.xml
│   │   └── setup.py, resource/, test/
│   │
│   ├── MoveIt_demo/
│   │   └── ...
│   │
│   ├── pkg_action/
│   │   ├── pkg_action/      # action_server_demo.py, action_client_demo.py
│   │   ├── package.xml
│   │   └── setup.py, resource/, test/
│   │
│   ├── pkg_helloworld_cpp/
│   │   └── ...
│   │
│   ├── pkg_helloworld_py/
│   │   ├── pkg_helloworld_py/  # helloworld.py
│   │   ├── package.xml
│   │   └── setup.py, resource/, test/
│   │
│   ├── pkg_interfaces/
│   │   └── ...
│   │
│   ├── pkg_metapackage/
│   │   └── ...
│   │
│   ├── pkg_param/
│   │   ├── pkg_param/      # param_demo.py
│   │   ├── package.xml
│   │   └── setup.py, resource/, test/
│   │
│   ├── pkg_service/
│   │   └── ...
│   │
│   ├── pkg_topic/
│   │   ├── pkg_topic/      # publisher_demo.py, subscriber_demo.py
│   │   ├── package.xml
│   │   └── setup.py, resource/, test/
│   │
│   ├── test_config/        # MoveIt 测试配置 (dofbot_pro)
│   │   ├── CMakeLists.txt
│   │   ├── config/         # dofbot_pro_descripton.*, moveit, kinematics 等
│   │   ├── launch/
│   │   └── package.xml
│   │
│   ├── test_moveit_config/ # MoveIt 测试配置 (M3Pro)
│   │   ├── CMakeLists.txt
│   │   ├── config/         # M3Pro.urdf.xacro, M3Pro.srdf, moveit 等
│   │   ├── launch/
│   │   └── package.xml
│   │
│   ├── yahboomcar_ctrl/
│   │   ├── yahboomcar_ctrl/  # yahboom_joy_M3Pro, yahboom_joy_R2, yahboom_keyboard
│   │   ├── launch/         # yahboomcar_joy_launch.py, keyboart_ctrl_launch
│   │   ├── package.xml
│   │   └── setup.py, resource/, test/
│   │
│   ├── yahboomcar_description/
│   │   ├── launch/         # display, description_multi_robot
│   │   ├── meshes/         # 底盘/相机/IMU 等 STL
│   │   ├── urdf/           # Muto.urdf, Muto_robot1/2.urdf
│   │   ├── rviz/
│   │   ├── package.xml
│   │   └── setup.py, resource/, test/
│   │
│   ├── yahboomcar_mediapipe/
│   │   ├── yahboomcar_mediapipe/  # 手势/手部/人脸检测等 (01_HandDetector ~ 16_GestureGrasp)
│   │   ├── launch/         # mediapipe_points.launch.py
│   │   ├── rviz/
│   │   ├── package.xml
│   │   └── setup.py, resource/, test/
│   │
│   ├── yahboomcar_msgs/
│   │   ├── CMakeLists.txt
│   │   ├── msg/            # ImageMsg, PointArray, Position, Target, TargetArray
│   │   └── package.xml
│   │
│   ├── yahboom_M3Pro_DepthCam/
│   │   ├── yahboom_M3Pro_DepthCam/  # GetDepthColor, Measure_Distance, Edge_Detection
│   │   ├── package.xml
│   │   └── setup.py, resource/, test/
│   │
│   ├── yahboom_M3Pro_description/   # M3Pro 机器人描述与仿真/SLAM
│   │   ├── config/         # Cartographer: cartographer_m3pro_2d.lua, map_builder, pose_graph, trajectory_builder_2d/3d
│   │   ├── launch/         # depth_cartographer, depth_slam, display, hospital_m3pro_teleop
│   │   ├── meshes/         # 机械臂/轮子/相机/底盘等 STL
│   │   ├── urdf/           # M3Pro.urdf
│   │   ├── rviz/           # yahboom_M3Pro, spen_M3Pro, spen_M3Pro_depth_slam 等
│   │   ├── package.xml
│   │   └── setup.py, resource/, test/
│   │
│   ├── yahboom_M3Pro_laser/
│   │   ├── yahboom_M3Pro_laser/  # laser_Avoidance, laser_Tracker, laser_Warning
│   │   ├── launch/         # laser_driver.launch.py
│   │   ├── package.xml
│   │   └── setup.py, resource/, test/
│   │
│   └── yahboom_yolov8/
│       ├── yahboom_yolov8/  # yolov8_detect, yolov8_track, Robot_Move, PID 等
│       ├── launch/         # yolov8_deep_track.launch.py
│       ├── package.xml
│       └── setup.py, resource/, test/
│
└── turtlesim.yaml
```

## 说明

- **build/**：colcon 编译输出目录  
- **install/**：安装目录，含各包 share/、lib/ 及 setup 脚本  
- **log/**：colcon 构建与运行日志  
- **src/**：ROS 2 源码包，包含机械臂接口/控制、M3Pro 描述与 SLAM、医院仿真世界、MoveIt 配置、示例包等。  
- 未展开的包（如 `MoveIt_demo`、`pkg_helloworld_cpp`、`pkg_interfaces`、`pkg_metapackage`、`pkg_service`）结构与上述 Python/launch 包类似（package.xml、setup.py 或 CMakeLists.txt、resource、test 等）。

*文档由工作空间扫描生成，已省略 `__pycache__`、`build`、`install`、`log` 及 `.git` 内部结构。*
