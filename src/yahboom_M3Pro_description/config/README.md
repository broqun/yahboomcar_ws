# Cartographer 配置说明（config/*.lua）

本目录包含 **Cartographer 2D SLAM** 的 Lua 配置文件，供 `depth_cartographer_launch.py` 使用。Cartographer 启动时会加载**主配置**，主配置里通过 `include` 引入其余文件，共同决定建图与轨迹估计行为。

**配置与源码来源**：Lua 配置的“必填键”与结构由 **Cartographer 核心 C++ 库** 决定，配置示例来自 [cartographer-project/cartographer](https://github.com/cartographer-project/cartographer) 的 `configuration_files/`。ROS 侧封装与 launch 在 [cartographer-project/cartographer_ros](https://github.com/cartographer-project/cartographer_ros)（你安装的 `ros-humble-cartographer-ros` 即由此构建）。若某键放在错误的表里（例如把位姿图相关键放进 TRAJECTORY_BUILDER_2D），C++ 会报 `Key 'xxx' was used the wrong number of times`，需按核心库的配置结构放置。

---

## 文件关系与加载顺序

```
cartographer_m3pro_2d.lua   （主配置，launch 通过 -configuration_basename 指定）
    │
    ├── include "map_builder.lua"             → 定义 MAP_BUILDER
    │       └── include "pose_graph.lua"     → 定义 POSE_GRAPH（回环/优化）
    ├── include "trajectory_builder_2d.lua"  → 定义 TRAJECTORY_BUILDER_2D
    ├── include "trajectory_builder_3d.lua"  → 定义 TRAJECTORY_BUILDER_3D（2D 建图时未使用，但 C++ 要求 options.trajectory_builder 含此键）
    │
    └── 主配置中再设置 options（含 map_builder、trajectory_builder{2d,3d,collate_*）、以及 TRAJECTORY_BUILDER_2D 覆盖
```

- **主配置**：`cartographer_m3pro_2d.lua`（入口，包含 ROS 与传感器相关选项）。
- **子配置**：`map_builder.lua`（内嵌 include `pose_graph.lua`）、`trajectory_builder_2d.lua` 被主配置 include；主配置里可再对部分项做覆盖（例如 `min_range`、`max_range`）。

### C++ 端必填项（缺一报错）

以下为 Cartographer 官方实现中**必须存在**的键，否则会触发 `Key 'xxx' not in dictionary` 或类似错误：

| 位置 | 必填键 | 说明 |
|------|--------|------|
| 主配置返回值 | 整个表为 table，且含 `map_builder`、`trajectory_builder` | 主配置末尾需 `return options`；`options.trajectory_builder` 必须同时含 **trajectory_builder_2d** 与 **trajectory_builder_3d**（见官方 [trajectory_builder.lua](https://github.com/cartographer-project/cartographer/blob/master/configuration_files/trajectory_builder.lua)）。 |
| MAP_BUILDER | `pose_graph`、`collate_by_trajectory` | `map_builder.lua` 需 include `pose_graph.lua` 并设置 `pose_graph = POSE_GRAPH`。 |
| TRAJECTORY_BUILDER_2D | `use_online_correlative_scan_matching`、`pose_extrapolator`、`submaps`、`imu_gravity_time_constant` | 见 `trajectory_builder_2d.lua`。 |
| submaps.range_data_inserter | `tsdf_range_data_inserter` | 2D 概率栅格主要用 `probability_grid_range_data_inserter`，但 C++ 仍要求存在 `tsdf_range_data_inserter` 块。 |
| 键所在表 | 不要混放 | 位姿图相关（如里程计权重）只放在 `pose_graph.lua` 的 `optimization_problem`，不要放进 `TRAJECTORY_BUILDER_2D`，否则会触发 “used the wrong number of times”。 |

---

## 1. cartographer_m3pro_2d.lua（主配置）

**作用**：Cartographer 的**入口配置**，负责与 ROS 的对接和本机传感器设定。

| 内容 | 说明 |
|------|------|
| **include** | 引入 `map_builder.lua`、`trajectory_builder_2d.lua`，从而补全 `MAP_BUILDER` 与 `TRAJECTORY_BUILDER_2D`。 |
| **options** | ROS 与 SLAM 顶层选项。 |

### options 主要字段

| 字段 | 当前值 | 含义 |
|------|--------|------|
| `map_frame` | `"map"` | 地图坐标系，RViz 固定坐标系一般选它。 |
| `tracking_frame` | `"base_footprint"` | 被跟踪的机体坐标系（与 TF 树一致）。 |
| `published_frame` | `"odom"` | 作为 map 子帧发布的坐标系，通常为 odom。 |
| `odom_frame` | `"odom"` | 里程计/局部连续位姿的坐标系。 |
| `provide_odom_frame` | `true` | 是否发布 map→odom 的 TF（闭环前局部轨迹）。 |
| `use_odometry` | `false` | 不使用外部里程计，仅用激光做位姿估计。 |
| `num_laser_scans` | `1` | 使用 1 路 2D 激光（即 `/scan`，来自深度图转激光）。 |
| `num_subdivisions_per_laser_scan` | `1` | 每帧激光划分子段数，单路 2D 一般为 1。**必填**（cartographer_ros）。 |
| `num_multi_echo_laser_scans` | `0` | 无多回波激光。 |
| `num_point_clouds` | `0` | 不使用点云。 |
| `use_nav_sat` | `false` | 是否使用 NavSatFix（GPS）。**必填**（cartographer_ros NodeOptions）。 |
| `use_landmarks` | `false` | 是否使用 LandmarkList。**必填**（cartographer_ros NodeOptions）。 |
| `publish_frame_projected_to_2d` | `true` | 2D 时发布纯 2D 位姿（无 roll/pitch/z）。 |
| `rangefinder_sampling_ratio` | `1.0` | 测距数据采样比（1=全用）。**必填**（cartographer_ros）。 |
| `odometry_sampling_ratio` | `1.0` | 里程计采样比（use_odometry 时）。 |
| `imu_sampling_ratio` | `1.0` | IMU 采样比（use_imu 时）。 |
| `fixed_frame_pose_sampling_ratio` | `1.0` | 固定坐标系位姿采样比（外部定位时）。**必填**（cartographer_ros）。 |
| `landmarks_sampling_ratio` | `1.0` | 路标数据采样比（use_landmarks 时）。**必填**（cartographer_ros）。 |
| `lookup_transform_timeout_sec` | `0.2` | 查询 TF 的超时时间（秒）。 |
| `submap_publish_period_sec` | `0.3` | 子图发布周期。 |
| `pose_publish_period_sec` | `5e-3` | 位姿发布周期。 |
| `trajectory_publish_period_sec` | `0.03` | 轨迹发布周期。 |

主配置末尾还对 2D 轨迹做了少量覆盖，与深度图转激光一致：

- `TRAJECTORY_BUILDER_2D.min_range = 0.1`、`max_range = 10.0`（主配置中覆盖；勿在此覆盖 `scan_period`，当前 C++ 不读取会报错）

**重要**：  
1. 文件最后必须有 `return options`。Cartographer 的 C++ 端会把主配置脚本的**返回值**当作配置表；若不 return，会报错 `Topmost item on Lua stack is not a table`。  
2. `options` 表内必须包含 `map_builder` 与 `trajectory_builder`。`trajectory_builder` 必须同时含 `trajectory_builder_2d`、`trajectory_builder_3d`（及可选 `collate_fixed_frame`、`collate_landmarks`），否则报 `Key 'trajectory_builder_3d' not in dictionary`。

---

## 2. map_builder.lua（地图构建）

**作用**：配置 Cartographer 的**地图构建后端**（子图、回环、线程等）。会 `include "pose_graph.lua"` 并引用 `POSE_GRAPH`。

| 字段 | 当前值 | 含义 |
|------|--------|------|
| `use_trajectory_builder_2d` | `true` | 使用 2D 轨迹构建器（本方案为 2D 建图）。 |
| `use_trajectory_builder_3d` | `false` | 不使用 3D。 |
| `num_background_threads` | `4` | 后台用于优化/回环的线程数。 |
| `pose_graph` | `POSE_GRAPH` | 位姿图配置（回环约束、优化等），定义在 `pose_graph.lua`。**必填**。 |
| `collate_by_trajectory` | `false` | 是否按轨迹整编数据。**必填**。 |

## 3. pose_graph.lua（位姿图 / 回环）

**作用**：回环检测与全局优化（约束构建、采样比、Ceres 优化等）。由 `map_builder.lua` include，不直接被主配置引用。

---

## 4. trajectory_builder_3d.lua（3D 轨迹，仅占位）

**作用**：满足 C++ 对 `options.trajectory_builder.trajectory_builder_3d` 的必填要求。本方案为 2D 建图（`MAP_BUILDER.use_trajectory_builder_3d = false`），运行时不使用 3D 配置；内容与官方 [trajectory_builder_3d.lua](https://github.com/cartographer-project/cartographer/blob/master/configuration_files/trajectory_builder_3d.lua) 一致。

## 5. trajectory_builder_2d.lua（2D 轨迹与扫描匹配）

**作用**：配置 **2D 局部轨迹** 与 **单线激光的扫描匹配**，包括滤波、匹配器、运动过滤等。和“每一帧激光怎么用来估计位姿”直接相关。

### 传感器与范围

| 字段 | 值 | 含义 |
|------|-----|------|
| `use_imu_data` | `false` | 不使用 IMU（本机为深度转激光，无 IMU）。 |
| `min_range` / `max_range` | `0.1` / `10.0` | 激光有效距离（与 depthimage_to_laserscan 的 range_min/max 一致）。 |
| `min_z` / `max_z` | `-0.8` / `1.0` | 点云高度过滤（2D 时影响有限）。 |
| `missing_data_ray_length` | `5.0` | 缺失数据时的虚拟射线长度。 |
| `num_accumulated_range_data` | `1` | 累积多少帧再处理（1 即逐帧）。 |
| `voxel_filter_size` | `0.025` | 体素滤波格大小（米）。 |

### 滤波与匹配

| 块/字段 | 作用 |
|---------|------|
| **adaptive_voxel_filter** | 自适应体素滤波，控制降采样与范围。 |
| **loop_closure_adaptive_voxel_filter** | 回环时用的体素滤波，通常略宽松。 |
| **real_time_correlative_scan_matcher** | 实时相关扫描匹配：线性/角度搜索窗口、位移/旋转代价权重，用于初对齐。 |
| **ceres_scan_matcher** | Ceres 优化扫描匹配：占据权重、平移/旋转权重、迭代次数与线程数。 |

### 运动与约束

| 块/字段 | 作用 |
|---------|------|
| **motion_filter** | 运动过滤：时间、位移、转角阈值，避免过于频繁的位姿更新。 |
| **pose_extrapolator** | 位姿外推（匀速或 IMU），**必填**。 |
| **submaps** | 子图参数（栅格类型、分辨率、range_data_inserter，含 **tsdf_range_data_inserter** 占位），**必填**。 |
| **immutable_pose_min_observations** | 子图内至少观测次数。 |
| **pose_observation_continuous_estimation_duration** | 连续位姿估计时长。 |
| **pose_graph_odometry_translation/rotation_weight** | 位姿图中里程计边的平移/旋转权重。 |

---

## 修改建议

- **只改坐标系或话题相关**：改 `cartographer_m3pro_2d.lua` 里的 `options` 或末尾的 `TRAJECTORY_BUILDER_2D.*` 覆盖即可。
- **改回环、线程、2D/3D 开关**：改 `map_builder.lua`。
- **改回环约束、全局优化**：改 `pose_graph.lua`。
- **改扫描匹配、滤波、运动过滤、子图**：改 `trajectory_builder_2d.lua`。3D 相关仅当启用 3D 建图时改 `trajectory_builder_3d.lua`。

修改后需重新启动 `depth_cartographer_launch.py` 才能生效；若改了 `setup.py` 里安装的 config 文件，需重新 `colcon build` 并 `source install/setup.bash`。
