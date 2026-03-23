# `yahboomcar_ws` 简要说明

当前工作空间的主要技术基础为：

- ROS 2
- ROS 2 Control
- Gazebo Classic

## 1. 依赖包安装

如果只想快速检查并安装工作区 `src/` 下当前功能包声明的依赖，建议在工作区根目录执行：

```bash
cd /var/robotic/yahboomcar_ws
rosdep install --from-paths src --ignore-src -r -y
```

如果你只想检查 Python Demo 包本身，也可以单独执行：

```bash
cd /var/robotic/yahboomcar_ws/src/yahboom_m3pro_slam_demo
rosdep install --from-paths . --ignore-src -r -y
```

说明：

- `gazebo_hospital_slam_demo_launch.py` 现在不仅依赖 `yahboom_m3pro_slam_demo`，还会启动 `yahboom_m3pro_lidar_tools` 中的 C++ 合并节点。
- 因此，只安装 / 编译 `yahboom_m3pro_slam_demo` 而没有准备好 `yahboom_m3pro_lidar_tools` 时，`/scan_merged` 不会出现。

## 2. 环境配置

建议把下面内容写入 `~/.bashrc`：

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

如果你的工作空间路径不是 `/var/robotic/yahboomcar_ws`，请把上面的工作空间 `source` 路径改成你自己的实际路径。

修改完成后执行：

```bash
source ~/.bashrc
```

## 3. 自动探索建图

当前工作区已经新增自动探索相关功能包：

- `yahboom_m3pro_exploration`

它会在现有医院 SLAM Demo 基础上继续启动：

- Nav2
- frontier exploration 节点

自动探索链路目前大致为：

```text
Gazebo / robot / ros2_control
-> /scan_front + /scan_rear
-> /scan_merged
-> slam_toolbox
-> Nav2
-> frontier_explorer
-> /diff_drive_controller/cmd_vel_unstamped
```

### 3.1 自动探索前的额外依赖

自动探索除了原有 SLAM Demo 依赖外，还需要系统中安装 Nav2，至少包括：

```bash
sudo apt update
sudo apt install -y ros-humble-navigation2 ros-humble-nav2-bringup
```

安装完成后可用下面命令快速检查：

```bash
source /opt/ros/humble/setup.bash
ros2 pkg prefix nav2_bringup
```

### 3.2 自动探索启动命令

假设环境变量、依赖包和 Nav2 都已经就绪，那么推荐在工作区根目录执行：

```bash
clear;clear && colcon build --packages-select yahboom_m3pro_exploration yahboom_m3pro_slam_demo yahboom_m3pro_lidar_tools && source install/setup.bash && ros2 launch yahboom_m3pro_exploration auto_explore_slam_launch.py
```

说明：

- 自动探索 launch 默认会把 `keyboard` 设为 `false`，不再依赖手动键盘控制。
- `auto_explore_slam_launch.py` 会先复用原有 Gazebo + SLAM Demo，再延迟拉起 Nav2 和 `frontier_explorer`。
- Nav2 的 `cmd_vel` 已经被重映射到 `/diff_drive_controller/cmd_vel_unstamped`，可直接驱动当前底盘控制器。

### 3.3 当前自动探索状态

根据最近一次实测，自动探索主链路已经可以跑通：

- Nav2 生命周期节点能够进入 `active`
- `frontier_explorer` 能收到 `/map`
- 节点会自动发送多个 frontier 目标
- 机器人已经多次成功自动到达探索目标并持续扩展地图

不过当前仍有一些已知问题：

- 偶尔会挑到不可规划或较差的 frontier 目标，导致局部规划失败或绕行时间过长
- 手动 `Ctrl-C` 停止时，`frontier_explorer` 还存在一次 `rclpy.shutdown()` 重复调用报错
- RViz 在当前图形环境下仍可能出现 GLSL 相关警告

更详细的最近一次运行结果与下一步建议，请参考：

```text
AUTO_EXPLORE_STATUS.md
```

## 4. 手动控制建图

如果你想先用最稳定的方式手动控制机器人建图，仍可使用原有手动 Demo：

```bash
clear;clear && colcon build --packages-select yahboom_m3pro_slam_demo yahboom_m3pro_lidar_tools && source install/setup.bash && ros2 launch yahboom_m3pro_slam_demo gazebo_hospital_slam_demo_launch.py
```

如果你当前不在工作区根目录，请先执行：

```bash
cd /var/robotic/yahboomcar_ws
```
