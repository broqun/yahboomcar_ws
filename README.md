# `yahboomcar_ws` 简要说明

当前工作空间保留 `src/aws-robomaker-hospital-world/`，主要是为了给下面这个医院 SLAM Demo 提供 Gazebo 场景：

```text
src/yahboom_m3pro_slam_demo/launch/gazebo_hospital_slam_demo_launch.py
```

当前这套演示链路由两个自维护功能包组成：

- `yahboom_m3pro_slam_demo`
  - 负责 Gazebo 医院场景、机器人生成、RViz、键盘遥操作、`slam_toolbox` 启动
- `yahboom_m3pro_lidar_tools`
  - 负责 C++ 双雷达融合节点 `multi_lidar_merger_node`

也就是说，当前开发和验证的重点主要是：

- `yahboom_m3pro_slam_demo`
- `yahboom_m3pro_lidar_tools`
- `gazebo_hospital_slam_demo_launch.py`
- 基于医院场景的 Gazebo + M3Pro + 双雷达 SLAM 演示

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
export LD_LIBRARY_PATH=/usr/lib/wsl/lib:$LD_LIBRARY_PATH
export GALLIUM_DRIVER=d3d12
export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA

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

## 3. 快速启动

假设环境变量和依赖包都已经就绪，那么最直接的启动方式是在工作区根目录执行：

```bash
clear;clear && colcon build --packages-select yahboom_m3pro_slam_demo yahboom_m3pro_lidar_tools && source install/setup.bash && ros2 launch yahboom_m3pro_slam_demo gazebo_hospital_slam_demo_launch.py
```

如果你当前不在工作区根目录，请先执行：

```bash
cd /var/robotic/yahboomcar_ws
```

## 4. 更详细说明

更完整的启动流程、参数说明、常见问题和调试方法，请参考：

```text
src/yahboom_m3pro_slam_demo/launch/gazebo_hospital_slam_demo_launch.md
```
