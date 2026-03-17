# `yahboomcar_ws` 简要说明

当前工作空间中保留 `src/aws-robomaker-hospital-world/`，主要目的不是单独维护这个医院场景包本身，而是为了给下面这个 Demo 提供 Gazebo 医院仿真环境：

```text
src/yahboom_M3Pro_description/launch/gazebo_hospital_slam_demo_launch.py
```

也就是说，当前开发和验证的重点主要是：

- `yahboom_M3Pro_description`
- `gazebo_hospital_slam_demo_launch.py`
- 基于医院场景的 Gazebo + M3Pro + 双雷达 SLAM 演示

## 1. 依赖包安装

如果只想快速检查并安装 `yahboom_M3Pro_description` 当前声明的依赖，可进入功能包目录执行：

```bash
cd /var/robotic/yahboomcar_ws/src/yahboom_M3Pro_description
rosdep install --from-paths . --ignore-src -r -y
```

说明：

- 这条命令会基于当前目录下功能包的 `package.xml` 解析缺失依赖。
- `xterm` 不在 `package.xml` 中，因此通常不会被 `rosdep` 自动安装。
- 即使没有安装 `xterm`，Demo 仍可运行；只是 `keyboard:=true` 时不会自动弹出键盘遥控终端，可改用 `keyboard:=false` 后手动运行遥控命令。

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
clear;clear && colcon build --packages-select yahboom_M3Pro_description && source install/setup.bash && ros2 launch yahboom_M3Pro_description gazebo_hospital_slam_demo_launch.py
```

如果你当前不在工作区根目录，请先执行：

```bash
cd /var/robotic/yahboomcar_ws
```

## 4. 更详细说明

更完整的启动流程、参数说明、常见问题和调试方法，请参考：

```text
src/yahboom_M3Pro_description/launch/gazebo_hospital_slam_demo_launch.md
```
