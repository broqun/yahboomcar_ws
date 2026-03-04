# depth_cartographer_launch 说明

基于 **Cartographer** 的 2D 建图 launch，与 `depth_slam_launch.py` 功能等价，使用 Cartographer 替代 SLAM Toolbox，可与 `hospital_m3pro_teleop_launch.py` 配合进行仿真建图。

---

## 功能概览

| 项目 | 说明 |
|------|------|
| **输入** | 深度相机话题：`/dabai_dcw2/depth/image_raw`、`/dabai_dcw2/depth/camera_info` |
| **输出** | 虚拟激光 `/scan`、占据栅格地图 `/map` |
| **坐标系** | `map` → `odom` → `base_footprint`（与 SLAM Toolbox 方案一致） |
| **适用场景** | 仿真/实机建图，配合键盘或其它速度控制 |

---

## 与 depth_slam_launch 对比

| 对比项 | depth_slam_launch | depth_cartographer_launch |
|--------|-------------------|---------------------------|
| SLAM 后端 | SLAM Toolbox | Cartographer |
| 深度→激光 | depthimage_to_laserscan（相同） | 相同 |
| 地图话题 | `/map` | `/map` |
| 坐标系 | map → odom → base_footprint | 相同 |
| 配置方式 | 全在 launch 参数 | Lua 配置文件 |

两套方案二选一即可，无需同时启动。

---

## 文件结构

```
yahboom_M3Pro_description/
├── launch/
│   ├── depth_cartographer_launch.py   # 本 launch
│   ├── depth_cartographer_launch.md   # 本说明
│   ├── depth_slam_launch.py           # SLAM Toolbox 建图
│   └── hospital_m3pro_teleop_launch.py
└── config/                            # Cartographer 配置
    ├── cartographer_m3pro_2d.lua      # 主配置（坐标系、话题、频率等）
    ├── map_builder.lua                # 地图构建参数
    └── trajectory_builder_2d.lua      # 2D 轨迹与扫描匹配参数
```

---

## 使用方法

### 1. 依赖

- ROS 2（Humble / Iron / Rolling 等）
- `cartographer_ros`：`sudo apt install ros-$ROS_DISTRO-cartographer-ros`
- `depthimage_to_laserscan`：`sudo apt install ros-$ROS_DISTRO-depthimage-to-laserscan`

### 2. 编译与 source

```bash
cd /var/robotic/yahboomcar_ws
colcon build --packages-select yahboom_M3Pro_description
source install/setup.bash
```

### 3. 启动顺序（与 hospital 仿真配合）

**终端 1**：仿真 + 键盘遥控

```bash
ros2 launch yahboom_M3Pro_description hospital_m3pro_teleop_launch.py
```

**终端 2**：Cartographer 建图

```bash
ros2 launch yahboom_M3Pro_description depth_cartographer_launch.py
```

RViz 可继续使用 `spen_M3Pro_depth_slam.rviz`，固定坐标系选 `map`，添加 Map（`/map`）、LaserScan（`/scan`）和 TF 即可。

---

## 配置说明（Lua）

- **cartographer_m3pro_2d.lua**  
  主配置：坐标系（map / odom / base_footprint）、单线激光 `num_laser_scans = 1`、无里程计/无 IMU、扫描周期与距离范围与深度转激光一致。

- **map_builder.lua**  
  2D 建图开关、线程数、回环检测等。

- **trajectory_builder_2d.lua**  
  2D 轨迹与扫描匹配（`use_imu_data = false`，`min_range`/`max_range` 与深度图 range 一致）。

修改参数后需重新编译并 source，再重新启动 launch。

---

## 实现说明

- **为何用 `arguments` 传配置路径？**  
  `cartographer_node` 是 C++ 节点，通过 **gflags** 从命令行读取 `-configuration_directory` 和 `-configuration_basename`，不会从 ROS 2 的 parameter server 读取。因此 launch 中必须用 `arguments=[...]` 传入这两个选项，不能只写在 `parameters` 里，否则会报 `configuration_directory is missing` 并退出。

---

## 常见问题

- **找不到 config**：确保已执行 `colcon build` 并 `source install/setup.bash`，或从包含 `config/` 的源码目录运行。
- **无 /map**：确认 `cartographer_occupancy_grid_node` 已启动，且 Cartographer 已收到 `/scan` 与 TF（map–odom–base_footprint）。
- **TF 报错**：确保先启动 `hospital_m3pro_teleop_launch.py`，再启动本 launch，以保证 `base_footprint` 与相机帧（如 DCW2）的 TF 已发布。
