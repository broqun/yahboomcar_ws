# yahboomcar_ws

Yahboom M3Pro 机器人 ROS 2 仿真工作空间——在 Gazebo Classic 医院场景中完成建图与导航。

**技术栈**：ROS 2 Humble · Gazebo Classic 11 · ros2_control · Nav2 · SLAM Toolbox

---

## 工作空间目录与功能包

### 功能包职责

| 源码目录 | ROS 包名（`package.xml` 的 `<name>`） | 构建类型 | 说明 |
|----------|----------------------------------------|----------|------|
| `src/aws-robomaker-hospital-world/` | `aws_robomaker_hospital_world` | `ament_cmake` | AWS RoboMaker 医院 Gazebo 世界：建筑/房间与家具模型资源，并向 Gazebo 导出模型搜索路径。 |
| `src/m3pro_world_bringup/` | `m3pro_world_bringup` | `ament_python` | 基础 bringup：加载医院世界、Gazebo 中生成 M3Pro、`ros2_control`、RViz、键盘遥控等。 |
| `src/yahboom_m3pro_lidar_tools/` | `yahboom_m3pro_lidar_tools` | `ament_cmake` | M3Pro 用 C++ 雷达工具（如双雷达合并节点 `multi_lidar_merger_node`）。 |
| `src/yahboom_m3pro_slam_demo/` | `yahboom_m3pro_slam_demo` | `ament_python` | 手动遥控 SLAM：`slam_toolbox`、可选 Cartographer、EKF、多雷达合并脚本与 launch。 |
| `src/yahboom_m3pro_nav_demo/` | `yahboom_m3pro_nav_demo` | `ament_python` | 静态地图 + Nav2 自主导航；EKF、Nav2 参数（含 Smac2D + MPPI）、医院地图与命名航点 YAML；`waypoint_recorder` / `waypoint_patrol` 控制台入口。 |
| `src/yahboom_m3pro_exploration/` | `yahboom_m3pro_exploration` | `ament_python` | 自主探索脚手架：前沿探索节点与 `auto_explore_slam` 类 launch（依赖 SLAM demo 与 Nav2）。 |

### 工作空间根目录

`build/`、`install/`、`log/` 为 colcon 构建产物；根目录下的 `hospital_map_v3.*` 为便于使用的地图副本（包内亦有地图）。

```text
yahboomcar_ws/
├── README.md
├── AUTO_EXPLORE_STATUS.md
├── WORKSPACE_FILES.md
├── hospital_map_v3.yaml
├── hospital_map_v3.pgm
├── src/                    # 源码（见下）
├── build/                  # colcon build
├── install/                # colcon install（source install/setup.bash）
└── log/                    # colcon 日志
```

### `src/` 总览

```text
src/
├── aws-robomaker-hospital-world/
├── m3pro_world_bringup/
├── yahboom_m3pro_lidar_tools/
├── yahboom_m3pro_slam_demo/
├── yahboom_m3pro_nav_demo/
├── yahboom_m3pro_exploration/
├── build/                  # 若存在：误在 src 内执行 colcon 时的残留，可清理
└── log/                    # 同上
```

### 各包目录结构（摘要）

#### `aws-robomaker-hospital-world`

`fuel_models/`（约 43 个子目录）与 `models/`（约 37 个子目录）为大量 SDF/模型资源，此处不逐条列出。

```text
aws-robomaker-hospital-world/
├── CMakeLists.txt
├── package.xml
├── launch/
│   ├── hospital.launch
│   └── view_hospital.launch
├── worlds/
│   ├── hospital.world
│   ├── hospital_original.world
│   ├── hospital_two_floors.world
│   └── hospital_three_floors.world
├── fuel_models/            # Fuel 风格道具/家具模型（多子目录）
├── models/                 # 医院建筑与场景构件（多子目录）
├── docs/                   # 文档与图片
├── photos/
├── fuel_utility.py
├── setup.sh
└── requirements.txt
```

#### `m3pro_world_bringup`

```text
m3pro_world_bringup/
├── package.xml
├── setup.py
├── config/
│   └── controllers.yaml
├── launch/
│   └── hospital_world_bringup_launch.py
├── urdf/
│   └── M3Pro.urdf
├── meshes/                 # 车体/臂/轮等 *.STL
└── rviz/
    └── default_demo.rviz
```

#### `yahboom_m3pro_lidar_tools`

```text
yahboom_m3pro_lidar_tools/
├── package.xml
├── CMakeLists.txt
└── src/
    └── multi_lidar_merger_node.cpp
```

#### `yahboom_m3pro_slam_demo`

```text
yahboom_m3pro_slam_demo/
├── package.xml
├── setup.py
├── config/                 # EKF、Cartographer *.lua 等
├── launch/
│   ├── display_launch.py
│   ├── gazebo_hospital_slam_demo_launch.py
│   ├── hospital_cartographer_demo_launch.py
│   ├── hospital_m3pro_teleop_launch.py
│   └── lidar_slam_launch.py
├── scripts/
│   └── multi_lidar_merger.py
├── maps/
├── rviz/
└── test/
```

#### `yahboom_m3pro_nav_demo`

```text
yahboom_m3pro_nav_demo/
├── package.xml
├── setup.py
├── STARTUP_SEQUENCE.md
├── config/
│   ├── ekf.yaml
│   ├── nav2_smac2d_mppi.yaml    # hospital_navigation_launch 默认 Nav2 参数（Smac2D + MPPI）
│   ├── nav2_navigation.yaml    # 备选（RPP 等），launch 未默认引用时可手工指定
│   └── recorded_waypoints.yaml   # 随包安装的固定命名航点（医院房间等）
├── launch/
│   └── hospital_navigation_launch.py
├── maps/                     # hospital_map_v1 / v2 / v3（launch 当前默认 v2）
├── rviz/
│   ├── nav_demo.rviz
│   └── nav2_smac2d_mppi_debug.rviz
├── yahboom_m3pro_nav_demo/   # Python 包
│   ├── waypoint_storage.py   # YAML 读写与默认路径（~/.ros/...）
│   ├── waypoint_recorder.py  # 订阅 /goal_pose，交互命名并写入航点文件
│   └── waypoint_patrol.py    # 按 YAML 顺序 NavigateToPose 巡检
└── test/
```

#### `yahboom_m3pro_exploration`

```text
yahboom_m3pro_exploration/
├── package.xml
├── setup.py
├── config/
│   └── nav2_params.yaml
├── launch/
│   └── auto_explore_slam_launch.py
└── yahboom_m3pro_exploration/
    └── frontier_explorer.py
```

### 包依赖关系（示意）

```text
aws_robomaker_hospital_world
        │
        ▼
m3pro_world_bringup ◄── yahboom_m3pro_lidar_tools
   │         │                    │
   ▼         ▼                    ▼
yahboom_m3pro_slam_demo   yahboom_m3pro_nav_demo
   │
   ▼
yahboom_m3pro_exploration
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

基于预建静态地图，使用 Nav2 进行自主导航。在 RViz 中点击 "2D Goal Pose" 设置目标。命名航点 YAML、录制工具与按点巡检见第 5 节。

```bash
ros2 launch yahboom_m3pro_nav_demo hospital_navigation_launch.py
```

启动内容：Gazebo 医院场景 → M3Pro spawn → ros2_control → 双雷达合并 → EKF 里程计融合 → Nav2（AMCL + Planner + Controller + Recovery）→ RViz

关键配置文件：

| 文件 | 说明 |
|------|------|
| `config/nav2_smac2d_mppi.yaml` | **`hospital_navigation_launch.py` 默认**：Nav2 全栈（AMCL、`nav2_smac_planner/SmacPlanner2D`、`nav2_mppi_controller::MPPIController`、costmap、recovery 等） |
| `config/nav2_navigation.yaml` | 备选 Nav2 参数（例如 **RegulatedPurePursuitController**）；需要时可自定义 launch 或手工加载 |
| `config/ekf.yaml` | robot_localization EKF 参数（odom → base_footprint TF） |
| `maps/hospital_map_v2.yaml` | `hospital_navigation_launch.py` 当前绑定的静态地图 |
| `maps/hospital_map_v3.yaml` | 更新的医院地图资源（根目录亦有 `hospital_map_v3.*` 副本便于取用） |
| `config/recorded_waypoints.yaml` | 随包安装的命名航点（房间等）；运行时亦可被 `~/.ros/...` 下的录制文件覆盖（见下文「航点」） |
| `rviz/nav_demo.rviz` | RViz 导航显示配置 |

RViz 默认使用 `yahboom_m3pro_nav_demo/rviz/nav_demo.rviz`，可通过参数覆盖：

```bash
ros2 launch yahboom_m3pro_nav_demo hospital_navigation_launch.py rvizconfig:=/path/to/your.rviz
```

---

## 5. 航点：录制、保存位置与巡检

工作空间提供三个协作模块（均在 `yahboom_m3pro_nav_demo` 包内）：

| 组件 | 作用 |
|------|------|
| `waypoint_storage` | 读写 `frame_id` + `waypoints` 结构的 YAML；默认路径为 **`$ROS_HOME/yahboom_m3pro_nav_demo/recorded_waypoints.yaml`**（未设置 `ROS_HOME` 时一般为 **`~/.ros/...`**）。 |
| `waypoint_recorder` | 订阅 RViz **「2D Goal Pose」** 发布的 `/goal_pose`，终端输入航点名称后**追加**写入文件（可用参数改输出路径）。 |
| `waypoint_patrol` | 从 YAML 按顺序调用 Nav2 **NavigateToPose** 访问各命名点（无需 `waypoint_follower`）。 |

**`waypoint_patrol` 选择文件的优先级**（未指定 `waypoints_file` 时）：若存在用户录制文件则用 **`~/.ros/.../recorded_waypoints.yaml`**，否则使用安装后的 **`share/yahboom_m3pro_nav_demo/config/recorded_waypoints.yaml`**（源码即 `config/recorded_waypoints.yaml`，含医院固定房间等航点）。

录制并写入**包内固定文件**（便于提交版本库、随 `colcon build` 安装），例如：

```bash
ros2 run yahboom_m3pro_nav_demo waypoint_recorder --ros-args \
  -p waypoints_output_file:=/var/robotic/yahboomcar_ws/src/yahboom_m3pro_nav_demo/config/recorded_waypoints.yaml
```

在 RViz 中使用 **2D Goal Pose** 点击地图并拖拽设定朝向后，在终端为每个点输入名称即可。

导航栈已运行后，按 YAML 顺序巡检（可按需加 `patrol_loop`、`waypoint_order`）：

```bash
ros2 run yahboom_m3pro_nav_demo waypoint_patrol --ros-args -p use_sim_time:=true
```

显式指定航点文件：

```bash
ros2 run yahboom_m3pro_nav_demo waypoint_patrol --ros-args \
  -p use_sim_time:=true \
  -p waypoints_file:=/var/robotic/yahboomcar_ws/src/yahboom_m3pro_nav_demo/config/recorded_waypoints.yaml
```

常用参数：`patrol_loop`（是否循环）、`waypoint_order`（逗号分隔名称列表，缺省则按名称排序）。

---

## 6. 仅启动仿真环境（不含建图/导航）

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
