# yahboomcar_ws

Yahboom M3Pro 机器人 ROS 2 仿真工作空间——在 Gazebo Classic 医院场景中完成建图与导航。

**技术栈**：ROS 2 Humble · Gazebo Classic 11 · ros2_control · Nav2 · SLAM Toolbox

---

## 功能包一览

```
src/
├── aws-robomaker-hospital-world   # 医院 Gazebo 世界模型（纯资源包，ament_cmake）
├── m3pro_world_bringup            # 基础 bringup：Gazebo + M3Pro spawn + RViz + 键盘遥控
├── yahboom_m3pro_lidar_tools      # 双雷达合并节点（C++，ament_cmake）
├── yahboom_m3pro_slam_demo        # 手动遥控 SLAM 建图演示
└── yahboom_m3pro_nav_demo         # 基于静态地图的 Nav2 自主导航演示
```

**依赖关系**：

```
aws-robomaker-hospital-world
        │
        ▼
m3pro_world_bringup ◄── yahboom_m3pro_lidar_tools
   │         │                    │
   ▼         ▼                    ▼
yahboom_m3pro_slam_demo   yahboom_m3pro_nav_demo
```

---

## 1. 环境配置

### 1.1 系统依赖

```bash
sudo apt update
sudo apt install -y \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-ros2-control \
  ros-humble-ros2-controllers \
  ros-humble-robot-localization \
  ros-humble-slam-toolbox \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-teleop-twist-keyboard \
  ros-humble-xacro \
  xterm
```

### 1.2 工作空间依赖（一键检查）

```bash
cd /var/robotic/yahboomcar_ws
rosdep install --from-paths src --ignore-src -r -y
```

### 1.3 bashrc 推荐配置

```bash
# ==========================================
# 1. 基础环境加载 (ROS 2 & 底层工作空间)
# 注：顺序很重要！先刷 ROS 2，再刷 Gazebo，最后刷自己的工作空间
# ==========================================
source /opt/ros/humble/setup.bash
source /usr/share/gazebo/setup.bash
source /var/robotic/yahboomcar_ws/install/setup.bash

# ==========================================
# 2. 硬件加速 (NVIDIA RTX 4090D in WSL2)
# 以下 3 项属于可选优化，不是启动 Demo 的必需条件
# 只有当你发现 Gazebo / RViz 没有正确使用 NVIDIA 显卡渲染，
# 或怀疑当前仍在走软件渲染、界面卡顿明显时，再尝试启用
# 如果当前显示和性能都正常，也可以先不加，避免引入额外图形兼容性变量
# ==========================================
# export LD_LIBRARY_PATH=/usr/lib/wsl/lib:$LD_LIBRARY_PATH
# export GALLIUM_DRIVER=d3d12
# export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA

# ==========================================
# 3. Gazebo 仿真器优化配置
# ==========================================
# 禁用在线模型下载，防止启动卡顿
export GAZEBO_MODEL_DATABASE_URI=""
```

如果工作空间路径不同，请替换上面的路径。修改完成后执行 `source ~/.bashrc`。

---

## 2. 编译

```bash
cd /var/robotic/yahboomcar_ws
colcon build
source install/setup.bash
```

如果只想编译特定包：

```bash
colcon build --packages-select m3pro_world_bringup yahboom_m3pro_slam_demo
```

---

## 3. 手动遥控 SLAM 建图

使用键盘控制机器人在医院场景中手动建图。

```bash
ros2 launch yahboom_m3pro_slam_demo gazebo_hospital_slam_demo_launch.py
```

启动内容：Gazebo 医院场景 → M3Pro spawn → ros2_control → 键盘遥控 → 双雷达合并 → SLAM Toolbox → RViz

RViz 默认使用 `yahboom_m3pro_slam_demo/rviz/spen_m3pro_lidar_slam.rviz`，可通过参数覆盖：

```bash
ros2 launch yahboom_m3pro_slam_demo gazebo_hospital_slam_demo_launch.py rvizconfig:=/path/to/your.rviz
```

---

## 4. Nav2 自主导航

基于预建静态地图，使用 Nav2 进行自主导航。在 RViz 中点击 "2D Goal Pose" 设置目标。

```bash
ros2 launch yahboom_m3pro_nav_demo hospital_navigation_launch.py
```

启动内容：Gazebo 医院场景 → M3Pro spawn → ros2_control → 双雷达合并 → EKF 里程计融合 → Nav2（AMCL + Planner + Controller + Recovery）→ RViz

关键配置文件：

| 文件 | 说明 |
|------|------|
| `config/nav2_navigation.yaml` | Nav2 全栈参数（AMCL、costmap、RPP controller、velocity_smoother 等） |
| `config/ekf.yaml` | robot_localization EKF 参数（odom → base_footprint TF） |
| `maps/hospital_map_v2.yaml` | 静态地图 |
| `rviz/nav_demo.rviz` | RViz 导航显示配置 |

Nav2 控制器使用 **RegulatedPurePursuitController**，当前配置为纯弧线转弯模式（`use_rotate_to_heading: False` + `allow_reversing: False`）。

RViz 默认使用 `yahboom_m3pro_nav_demo/rviz/nav_demo.rviz`，可通过参数覆盖：

```bash
ros2 launch yahboom_m3pro_nav_demo hospital_navigation_launch.py rvizconfig:=/path/to/your.rviz
```

---

## 5. 仅启动仿真环境（不含建图/导航）

如果只想加载 Gazebo 医院场景 + 机器人 + 键盘遥控 + RViz：

```bash
ros2 launch m3pro_world_bringup hospital_world_bringup_launch.py
```

可选参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `gui` | `true` | 是否启动 Gazebo GUI |
| `keyboard` | `true` | 是否启动键盘遥控（xterm） |
| `rvizconfig` | `m3pro_world_bringup/rviz/default_demo.rviz` | RViz 配置文件路径 |
| `world` | `hospital.world` | Gazebo 世界文件路径 |
| `x` / `y` / `z` | `0.049 / 11.755 / 0.01` | 机器人 spawn 位置 |
