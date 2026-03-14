# `gazebo_hospital_slam_demo_launch.py` 使用说明

本文档基于当前仓库 `src/yahboom_M3Pro_description/` 下实际存在的 `launch/`、`scripts/`、`urdf/`、`config/` 文件进行整理，说明 `src/yahboom_M3Pro_description/launch/gazebo_hospital_slam_demo_launch.py` 的用途、启动流程、运行方法、可用参数，以及它所 `include` 的 `src/yahboom_M3Pro_description/launch/lidar_slam_launch.py` 中全部 SLAM 参数的含义与调参建议。

## 1. 文件作用

`gazebo_hospital_slam_demo_launch.py` 用于一键启动以下组件：

1. Gazebo 医院场景。
2. M3Pro 机器人模型与 `robot_state_publisher`。
3. RViz。
4. 键盘遥操作。
5. 双激光雷达数据合并节点。
6. `slam_toolbox` 异步建图节点。
7. `ros2_control` 控制器加载：
   - `joint_state_broadcaster`
   - `diff_drive_controller`

从代码注释看，它等价于按顺序执行下面几步：

```bash
ros2 launch yahboom_M3Pro_description hospital_m3pro_teleop_launch.py
ros2 launch yahboom_M3Pro_description lidar_slam_launch.py
ros2 run controller_manager spawner joint_state_broadcaster
ros2 run controller_manager spawner diff_drive_controller
```

其中控制器加载在主 launch 中通过 `TimerAction(period=10.0)` 延迟约 10 秒执行，避免 Gazebo 和机器人尚未完全就绪时加载失败。

## 2. 环境准备

### 2.1 依赖包（package.xml）

本包在 `src/yahboom_M3Pro_description/package.xml` 中声明的**运行依赖**（`exec_depend`）如下，运行本 launch 或同包内其它 launch 前需确保这些包已安装（如 `apt install ros-humble-<包名>` 或通过工作空间编译提供）：

| 依赖包 | 用途 |
|--------|------|
| **Launch / RViz / URDF** | |
| `ament_index_python` | Launch 中查找包路径（如 `get_package_share_path`）。 |
| `robot_state_publisher` | 发布机器人描述与 TF。 |
| `rviz2` | 可视化（本 launch 使用 `spen_M3Pro_lidar_slam.rviz`）。 |
| `xacro` | 解析 URDF 中的 xacro 表达式。 |
| `image_transport_plugins` | 图像传输插件（同包内其它 launch 可能使用）。 |
| **Gazebo** | |
| `gazebo_ros` | Gazebo 与 ROS 2 桥接、`gzserver`/`gzclient`、`spawn_entity`。 |
| `gazebo_ros2_control` | URDF 中 Gazebo 与 ros2_control 的插件。 |
| **ros2_control** | |
| `controller_manager` | 控制器管理，本 launch 用于 spawner 加载控制器。 |
| `diff_drive_controller` | 差速底盘控制，接收 `/diff_drive_controller/cmd_vel_unstamped`。 |
| `joint_state_broadcaster` | 发布关节状态到 `/joint_states`。 |
| **遥操作与 SLAM** | |
| `slam_toolbox` | 异步建图节点（本 launch 使用 `/scan_merged`）。 |
| `teleop_twist_keyboard` | 键盘遥操作。 |
| **深度图相关（其它 launch）** | |
| `cartographer_ros` | 深度图 + Cartographer 建图 launch 使用。 |
| `depthimage_to_laserscan` | 深度图转激光话题。 |
| **双雷达合并脚本** | |
| `message_filters` | `scripts/multi_lidar_merger.py` 中激光同步。 |
| `sensor_msgs` | `multi_lidar_merger.py` 中 `LaserScan` 消息。 |

仅运行本说明中的 `gazebo_hospital_slam_demo_launch.py` 时，与医院 + 双雷达 SLAM 直接相关的是：`gazebo_ros`、`gazebo_ros2_control`、`robot_state_publisher`、`rviz2`、`xacro`、`controller_manager`、`diff_drive_controller`、`joint_state_broadcaster`、`slam_toolbox`、`teleop_twist_keyboard`、`message_filters`、`sensor_msgs`；其余为同包其它 launch 或通用依赖。

### 2.2 建议先在 `~/.bashrc` 中配置环境变量

为了避免每次打开终端都重复执行 `source` 和相关环境变量导出，建议把下面内容写入 `~/.bashrc`：

```bash
# --- ROS2 & Gazebo Environment Setup ---
source /usr/share/gazebo/setup.bash
source /opt/ros/humble/setup.bash
# 替换为你的工作空间路径
source /var/robotic/yahboomcar_ws/install/setup.bash

# --- NVIDIA RTX 4090 D WSL2 Hard-Decoding ---
export LD_LIBRARY_PATH=/usr/lib/wsl/lib:$LD_LIBRARY_PATH
export GALLIUM_DRIVER=d3d12
export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA

# --- Gazebo Path Fixes ---
# 禁用在线模型下载，防止卡顿
export GAZEBO_MODEL_DATABASE_URI=""
```

如果你的工作空间路径不是 `/var/robotic/yahboomcar_ws`，请把上面的 `source /var/robotic/yahboomcar_ws/install/setup.bash` 改成你自己的实际路径。

需要特别注意的是，当前仓库里的 `src/yahboom_M3Pro_description/urdf/M3Pro.urdf` 还把控制器配置文件写成了绝对路径：

```text
/var/robotic/yahboomcar_ws/src/yahboom_M3Pro_description/config/controllers.yaml
```

因此，如果你把整个工作空间移动到别的位置，仅修改 `~/.bashrc` 里的 `source .../install/setup.bash` 还不够，还需要同步修改 `M3Pro.urdf` 中这条 `controllers.yaml` 的绝对路径。

修改完成后执行：

```bash
source ~/.bashrc
```

这样之后再运行 `ros2 launch yahboom_M3Pro_description gazebo_hospital_slam_demo_launch.py` 时，ROS 2、Gazebo 和 WSL2 下的图形相关环境会自动生效。这里的 `GAZEBO_MODEL_DATABASE_URI=""` 只是禁止在线模型库下载，不会影响本地 `GAZEBO_MODEL_PATH` 的设置。

### 2.3 启动前快速检查

运行本 launch 前，建议确认以下条件：

1. 工作区已编译，并且当前终端已经 `source install/setup.bash`。
2. `aws_robomaker_hospital_world` 要么已经安装到 ROS 2 环境中，要么存在于当前工作区的 `src/aws-robomaker-hospital-world`。
3. Gazebo 能找到医院场景模型和 `yahboom_M3Pro_description` 的机器人资源。
4. `teleop_twist_keyboard`、`gazebo_ros`、`robot_state_publisher`、`xacro`、`slam_toolbox`、`controller_manager` 可用。
5. 如果使用 `keyboard:=true`，系统中还需要有 `xterm`，否则自动弹出的键盘控制终端无法启动。
6. 若使用 GUI，WSL2 或远程桌面环境的 OpenGL / Gazebo GUI 兼容性正常。

建议在工作区根目录运行。可分步执行，或用一条 `&&` 整合命令一次完成：

```bash
cd /var/robotic/yahboomcar_ws
colcon build --packages-select yahboom_M3Pro_description
source install/setup.bash
ros2 launch yahboom_M3Pro_description gazebo_hospital_slam_demo_launch.py
```

或一条命令（编译 + source + 启动）：

```bash
cd /var/robotic/yahboomcar_ws && colcon build --packages-select yahboom_M3Pro_description && source install/setup.bash && ros2 launch yahboom_M3Pro_description gazebo_hospital_slam_demo_launch.py
```

## 3. 启动流程

本 launch 的执行逻辑如下：

### 3.1 启动医院 Gazebo 场景

主 launch 先 `include` `hospital_m3pro_teleop_launch.py`，由后者负责：

1. 优先从已安装的 `aws_robomaker_hospital_world` 包中查找 `worlds/hospital.world`。
2. 如果安装包中找不到，再从当前工作区向上回溯，尝试查找：
   - `aws-robomaker-hospital-world/worlds/hospital.world`
   - `src/aws-robomaker-hospital-world/worlds/hospital.world`
3. 设置 `GAZEBO_MODEL_PATH`，包含：
   - 医院场景的 `models/`
   - 医院场景的 `fuel_models/`
   - `yahboom_M3Pro_description` 的 package share 上级目录，用于解析 `package://yahboom_M3Pro_description/meshes/...`
4. 启动 `gzserver`。
5. 视 `gui` 参数决定是否启动 `gzclient`。

### 3.2 发布机器人描述并生成机器人

`hospital_m3pro_teleop_launch.py` 会：

1. 读取 `M3Pro.urdf`。
2. 使用 `xacro.process_file()` 处理表达式。
3. 将结果作为 `robot_description` 参数传给 `robot_state_publisher`。
4. 延迟约 5.5 秒调用 `gazebo_ros/spawn_entity.py` 将机器人生成到 Gazebo。

补充说明：

- 虽然该 launch 声明了 `model` 参数，但当前代码实际仍固定使用默认的 `M3Pro.urdf` 路径进行 `xacro.process_file()`，所以传入 `model:=...` 目前大概率不会真正替换机器人模型。

### 3.3 启动键盘控制与 RViz

机器人生成时还会一并启动：

1. `rviz2`，默认加载 `rviz/spen_M3Pro_lidar_slam.rviz`。
2. 如果 `keyboard:=true`，通过 `xterm` 启动 `teleop_twist_keyboard`。
3. 键盘控制会把速度指令重映射到：

```text
/diff_drive_controller/cmd_vel_unstamped
```

4. 键盘控制默认还会带上：
   - `speed:=1.99999`
   - `turn:=0.99999`
   - `repeat_rate:=20`
5. 如果 `keyboard:=false`，launch 不会自动创建遥控终端，只会在约 8 秒后打印一条手动启动提示。

### 3.4 启动双雷达 SLAM

主 launch 同时 `include` `lidar_slam_launch.py`，后者会依次启动：

1. `multi_lidar_merger.py`
2. `slam_toolbox` 的 `async_slam_toolbox_node`

#### 双雷达合并节点的数据流

`multi_lidar_merger.py` 订阅：

- `/scan_front`
- `/scan_rear`

然后根据两个雷达在车体上的安装位姿，把点云统一投影到 `base_footprint` 坐标系，发布：

- `/scan_merged`

这个 `/scan_merged` 就是 SLAM 使用的激光输入。

### 3.5 延迟加载 ros2_control 控制器

主 launch 在 10 秒后执行：

```bash
ros2 run controller_manager spawner joint_state_broadcaster
ros2 run controller_manager spawner diff_drive_controller
```

加载顺序不能反过来。通常必须先有 `joint_state_broadcaster`，再加载 `diff_drive_controller`，否则遥操作可能无法生效。

## 4. 常用启动命令

### 4.1 默认启动

```bash
ros2 launch yahboom_M3Pro_description gazebo_hospital_slam_demo_launch.py
```

### 4.2 无 Gazebo GUI 启动

适合 WSL2 或图形不稳定环境：

```bash
ros2 launch yahboom_M3Pro_description gazebo_hospital_slam_demo_launch.py gui:=false
```

### 4.3 指定初始生成位置

```bash
ros2 launch yahboom_M3Pro_description gazebo_hospital_slam_demo_launch.py x:=0.0 y:=10.0 z:=0.01
```

### 4.4 不自动打开键盘控制终端

```bash
ros2 launch yahboom_M3Pro_description gazebo_hospital_slam_demo_launch.py keyboard:=false
```

然后手动在新终端运行：

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/diff_drive_controller/cmd_vel_unstamped
```

### 4.5 调整遥操作速度

```bash
ros2 launch yahboom_M3Pro_description gazebo_hospital_slam_demo_launch.py speed:=1.0 turn:=0.5
```

## 5. 可用 Launch 参数

这些参数由被 `include` 的 `hospital_m3pro_teleop_launch.py` 声明，因此在启动 `gazebo_hospital_slam_demo_launch.py` 时也可直接传入。

| 参数 | 默认值 | 作用 |
|---|---:|---|
| `gui` | `true` | 是否启动 Gazebo 图形界面。`false` 时只起 `gzserver`。 |
| `model` | `M3Pro.urdf` 绝对路径 | 已声明的机器人 URDF / xacro 路径参数，但当前代码并没有真正按该参数切换模型，基本仍固定读取默认 `M3Pro.urdf`。 |
| `x` | `0.049177` | 机器人生成的 X 坐标。 |
| `y` | `11.755002` | 机器人生成的 Y 坐标。 |
| `z` | `0.01` | 机器人生成的 Z 坐标。 |
| `keyboard` | `true` | 是否自动使用 `xterm` 打开键盘遥控终端。 |
| `speed` | `1.99999` | 键盘遥操作线速度。 |
| `turn` | `0.99999` | 键盘遥操作角速度。 |

## 6. 运行后应该看到的关键节点与话题

### 6.1 关键节点与控制器状态

可用以下命令检查：

```bash
ros2 node list
ros2 control list_controllers
```

正常情况下应先在 `ros2 node list` 中看到类似节点：

- `/robot_state_publisher`
- `/spawn_m3pro`
- `/rviz2`
- `/slam_toolbox`
- `/multi_lidar_merger`
- `/controller_manager`

然后在 `ros2 control list_controllers` 中确认至少有以下控制器处于 `active`：

- `joint_state_broadcaster`
- `diff_drive_controller`

### 6.2 关键话题

可用以下命令检查：

```bash
ros2 topic list
```

重点关注：

- `/clock`
- `/scan_front`
- `/scan_rear`
- `/scan_merged`
- `/map`
- `/odom`
- `/tf`
- `/tf_static`
- `/diff_drive_controller/cmd_vel_unstamped`
- `/joint_states`

### 6.3 推荐验证顺序

1. 先确认 Gazebo 场景与机器人已经生成。
2. 确认 `/scan_front` 和 `/scan_rear` 有数据。
3. 确认 `/scan_merged` 有数据。
4. 确认 `/map` 已发布。
5. 用键盘遥控机器人移动，观察 RViz 中地图是否逐步增长。

## 7. `lidar_slam_launch.py` 的完整说明

`lidar_slam_launch.py` 只做两件事：

1. 启动双雷达合并节点。
2. 启动 `slam_toolbox/async_slam_toolbox_node`。

### 7.1 双雷达合并节点说明

脚本路径：

```text
src/yahboom_M3Pro_description/scripts/multi_lidar_merger.py
```

该节点的核心行为：

1. 使用 `ApproximateTimeSynchronizer` 同步前后两个 `LaserScan`。
2. 前雷达安装位姿固定为：
   - `x=0.12`
   - `y=-0.10`
   - `yaw=0.0`
3. 后雷达安装位姿固定为：
   - `x=-0.12`
   - `y=0.10`
   - `yaw=pi`
4. 将两路数据统一投影到 `base_footprint`。
5. 发布角度范围 `[-pi, pi]`、长度 720 的 `/scan_merged`。

因此，SLAM 实际使用的激光雷达并不是原始单个雷达话题，而是该脚本拼接后的虚拟 360 度激光。

## 8. `slam_toolbox` 全部参数解释

`lidar_slam_launch.py` 中的 `slam_toolbox` 参数均以内联字典形式传入，没有额外 YAML 文件。下面按代码顺序解释每一项。

### 8.1 时间与输入输出坐标系

#### `use_sim_time: True`

作用：

- 让 `slam_toolbox` 使用 Gazebo 提供的仿真时间 `/clock`。

何时需要改：

- 在真实机器人上运行时，通常改为 `False`。
- 在 Gazebo 中一般必须为 `True`，否则时间轴会不一致。

#### `scan_topic: /scan_merged`

作用：

- 指定 SLAM 订阅的激光雷达话题。

当前配置含义：

- SLAM 使用双雷达融合后的 `/scan_merged`。

何时需要改：

- 如果只用单雷达，可改为 `/scan_front` 或其他真实雷达话题。

#### `map_frame: map`

作用：

- 设置全局地图坐标系名称。

当前配置含义：

- SLAM 会生成 `map -> odom` 变换，并发布地图到 `map` 坐标系。

#### `odom_frame: odom`

作用：

- 指定里程计坐标系名称。

当前配置含义：

- 机器人底盘里程计使用 `odom` 作为局部连续坐标系。

#### `base_frame: base_footprint`

作用：

- 指定机器人主体参考坐标系。

当前配置含义：

- SLAM 以 `base_footprint` 作为机器人位姿参考，而不是 `base_link`。

为什么这样配置：

- 对地面移动机器人来说，`base_footprint` 更适合 2D 建图，因为它通常剔除了俯仰和翻滚影响。

### 8.2 激光范围与更新频率

#### `max_laser_range: 12.0`

作用：

- 指定 SLAM 处理的最大有效激光距离。

当前配置含义：

- 只使用 12 米以内的回波。

调参建议：

- 若雷达真实量程更短，可以减小。
- 若环境较大但噪声较多，过大的范围可能降低匹配稳定性。

#### `minimum_time_interval: 0.25`

作用：

- 控制 SLAM 两次处理扫描数据之间的最小时间间隔。

当前配置含义：

- 最快约每 0.25 秒处理一次，也就是约 4 Hz。

影响：

- 值更小：处理更频繁，CPU 占用更高，地图更新更快。
- 值更大：处理更稀疏，CPU 压力更低，但快速运动时可能丢失细节。

### 8.3 建图模式与地图分辨率

#### `mode: mapping`

作用：

- 设定 SLAM Toolbox 的工作模式。

当前配置含义：

- 处于建图模式，会持续扩展和优化地图。

常见替代值：

- 保存好地图后，在定位场景中通常使用 localization 模式，而不是 mapping。

#### `resolution: 0.05`

作用：

- 地图分辨率，单位米 / 像素。

当前配置含义：

- 每个栅格代表 5 cm。

调参建议：

- 更小，例如 `0.02`：地图更精细，但内存和计算开销更高。
- 更大，例如 `0.10`：计算更省，但墙体和狭窄通道会更粗糙。

### 8.4 关键帧 / 触发更新阈值

#### `minimum_travel_distance: 0.25`

作用：

- 机器人至少移动多少距离后，SLAM 才会认为值得进行一次新的关键更新。

当前配置含义：

- 机器人移动 25 cm 后会更积极地更新位姿 / 地图。

调参建议：

- 小环境、低速建图可适当减小。
- 高噪声里程计或高速运动时过小会导致更新过密。

#### `minimum_travel_heading: 0.2`

作用：

- 机器人至少转过多少角度后，SLAM 才触发新的关键更新。

当前配置含义：

- 约等于 11.5 度。

调参建议：

- 原地转弯建图较多时，可适当减小。
- 若角度更新太敏感导致计算负担重，可适当增大。

### 8.5 扫描匹配搜索窗口

#### `correlation_search_space_dimension: 0.8`

作用：

- 相关性匹配时，在平移方向上搜索的空间范围。

当前配置含义：

- 算法会在更大的平移范围内尝试把当前激光扫描和已有地图对齐。

为什么这里偏大：

- 代码注释明确说明，这是为了在轮式里程计打滑或漂移时，给激光匹配更大“找回正确位置”的机会。

调参影响：

- 更大：更能容忍漂移，但计算量更大，也更容易出现错误匹配。
- 更小：更快，但对里程计依赖更强。

#### `correlation_search_space_resolution: 0.02`

作用：

- 相关性搜索时的平移采样步长。

当前配置含义：

- 按 2 cm 精度在搜索空间内尝试不同位姿。

调参影响：

- 更小：搜索更精细，计算量增加。
- 更大：更快，但可能错过最优匹配点。

### 8.6 匹配惩罚与匹配策略

#### `angle_variance_penalty: 1.0`

作用：

- 对旋转偏差进行惩罚，抑制不合理的大角度匹配。

当前配置含义：

- 倾向于接受角度变化更平滑、更保守的匹配结果。

调参建议：

- 地图中长直走廊较多时，适当的角度惩罚有利于稳定方向估计。
- 太大可能导致真实转弯时匹配不够灵活。

#### `use_scan_matching: True`

作用：

- 是否启用激光扫描匹配。

当前配置含义：

- 启用，是建图质量的关键。

一般建议：

- 在 2D 激光建图中通常应保持开启。

#### `use_scan_barycenter: True`

作用：

- 在匹配时使用扫描数据的重心信息辅助估计。

当前配置含义：

- 对当前扫描的整体几何分布更敏感，有助于改善部分场景中的初始匹配。

调参说明：

- 该参数属于匹配策略细节，通常不需要频繁修改。
- 若遇到特殊环境中的匹配异常，可尝试切换为 `False` 做对比。

### 8.7 扫描缓存与回环检测

#### `scan_buffer_size: 150`

作用：

- 设置内部用于匹配 / 优化的扫描缓存大小。

当前配置含义：

- 保留最近 150 帧左右的扫描历史供算法使用。

调参影响：

- 更大：历史更多，可能利于匹配与闭环，但内存更高。
- 更小：内存更省，但历史上下文更少。

#### `loop_search_maximum_distance: 12.0`

作用：

- 回环检测时允许搜索的最大空间距离。

当前配置含义：

- 仅在 12 米范围内积极搜索回环候选。

为什么这样设置：

- 代码注释说明与雷达量程一致，避免搜索远超传感器有效范围的闭环候选。

#### `loop_match_minimum_chain_size: 3`

作用：

- 回环匹配需要满足的最小连续匹配链长度。

当前配置含义：

- 至少有 3 个连续关系支持，回环才更容易被接受。

调参影响：

- 更大：更保守，误回环更少，但可能漏检。
- 更小：更敏感，但误检风险更高。

#### `link_match_minimum_response_fine: 0.1`

作用：

- 精细匹配阶段接受匹配结果所需的最低响应值。

当前配置含义：

- 只要细匹配得分达到 0.1，就可作为有效链接候选。

调参影响：

- 更高：更严格，更不容易接受弱匹配。
- 更低：更宽松，但错误匹配概率增加。

## 9. 当前参数组合的整体特点

这组参数整体偏向下面的调参思路：

1. 面向 Gazebo 仿真，因此强制 `use_sim_time=True`。
2. 使用双雷达拼接结果 `/scan_merged`，获得接近 360 度感知。
3. 对轮式里程计漂移有一定容忍度：
   - 较大的 `correlation_search_space_dimension`
   - 开启 `use_scan_matching`
   - 较保守的角度惩罚
4. 地图分辨率适中：
   - `resolution=0.05`
5. 更新频率不算太激进：
   - `minimum_time_interval=0.25`
   - `minimum_travel_distance=0.25`
   - `minimum_travel_heading=0.2`

如果你在医院长走廊中发现地图“拉扯”、重影或闭环效果一般，优先考虑围绕以下参数微调：

- `correlation_search_space_dimension`
- `correlation_search_space_resolution`
- `minimum_travel_distance`
- `minimum_travel_heading`
- `loop_search_maximum_distance`
- `link_match_minimum_response_fine`

## 10. 常见问题

### 10.1 启动后 Gazebo GUI 崩溃，但 `gzserver` 正常

这在 WSL2 中比较常见，通常是 Gazebo Classic 的 GUI / Ogre 渲染兼容问题。可尝试：

**方案一：无 GUI 启动**

```bash
ros2 launch yahboom_M3Pro_description gazebo_hospital_slam_demo_launch.py gui:=false
```

用 `RViz` 观察数据，先不依赖 `gzclient`。

**方案二：重启 WSL 后再试 GUI**

若仍希望使用 Gazebo 图形界面，可在 Windows 端重启 WSL 后重试，有时能恢复 GUI 渲染：在 **Windows PowerShell**（非 WSL 内）中依次执行：

```powershell
wsl --shutdown
```

关闭后重新进入 WSL，在开始菜单或终端中再次启动「Windows 终端」或输入 `wsl` 即可。然后再在 WSL 里重新执行本 launch（可先 `gui:=false` 确认无 GUI 时正常，再去掉该参数试 GUI）。

### 10.2 键盘控制无法生效

检查项：

1. `ros2 control list_controllers` 中 `joint_state_broadcaster` 是否为 `active`。
2. `ros2 control list_controllers` 中 `diff_drive_controller` 是否为 `active`。
3. 键盘指令是否发往 `/diff_drive_controller/cmd_vel_unstamped`。
4. `xterm` 是否存在，若不存在请使用 `keyboard:=false` 手动开终端运行遥控。
5. 若工作空间不在 `/var/robotic/yahboomcar_ws`，检查 `M3Pro.urdf` 中 `controllers.yaml` 的绝对路径是否已经同步修改。

### 10.3 没有地图或地图不更新

建议按顺序检查：

1. `/scan_front`、`/scan_rear` 是否有数据。
2. `/scan_merged` 是否有数据。
3. `/slam_toolbox` 节点是否存在。
4. `tf` 中是否存在 `map -> odom -> base_footprint` 链路。

### 10.4 机器人生成失败

检查：

1. `hospital.world` 是否能被找到。
2. Gazebo 是否已完全启动。
3. `robot_description` 是否正确发布。
4. URDF 中是否包含不兼容的 XML 声明或解析错误。

## 11. 推荐调试命令

```bash
ros2 node list
ros2 topic list
ros2 topic echo /scan_merged
ros2 topic echo /map --once
ros2 run tf2_tools view_frames
ros2 control list_controllers
```

## 12. 适用场景

该 launch 更适合以下用途：

1. 在 Gazebo 医院环境中做 2D 建图演示。
2. 验证双雷达融合建图链路是否稳定。
3. 联调 `ros2_control` 差速底盘与 SLAM。
4. 在导航功能接入前，先完成地图构建和传感器验证。

如果后续你还要补“保存地图”“加载地图定位”“接 Nav2 导航”的说明，建议另外再拆分文档，避免这个启动说明过于臃肿。
