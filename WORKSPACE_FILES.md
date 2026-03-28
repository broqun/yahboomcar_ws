# yahboomcar_ws 文件目录与说明

本文档根据工作区根目录 [`.gitignore`](.gitignore) 规则，列出 **未被 Git 忽略** 的路径（`git ls-files` 与 `git ls-files --others --exclude-standard` 的并集），共 **877** 个路径条目；其中 `src/aws-robomaker-hospital-world/` 在第 4 节按**目录**合并为 7 条说明，其余路径仍逐条列出（第 4 节表格共 **71** 行）。  
**不包含**：`build/`、`install/`、`log/`、`.vscode/`、`__pycache__/`、根 `.gitignore` 中列出的其它 `src/` 子目录、以及 `*.dat` / `*.pyc` 等被忽略类型。

**生成方式**：下文 **第 3 节** 对各包作结构化说明；**第 4 节** 为路径—说明对照表（`aws-robomaker-hospital-world` 仅按目录合并，其余路径逐条列出）。

---

## 1. 根目录 `.gitignore` 排除范围摘要

| 模式 | 含义 |
|------|------|
| `**/build/`、`**/install/`、`**/log/` | ROS 2 / colcon 构建产物与日志，不纳入清单 |
| `src/` 下除 `aws-robomaker-hospital-world`、`yahboom_m3pro_slam_demo` 等以外的多个目录 | 按仓库策略忽略的教学包、其它车型等（详见根 `.gitignore`） |
| `.vscode/` | 编辑器配置 |
| `**/__pycache__/`、`*.pyc` | Python 缓存 |
| `*.dat`、`*.whl`、`*.pth`、`*.onnx` | 数据与大模型权重等 |

> **说明**：磁盘上若存在未跟踪且未被忽略的目录（例如本地拷贝的其它包），会出现在清单中；若某路径已被忽略则**不会**出现在本文档中。  
> 例如 `src/yahboom_M3Pro_description/` 若在根 `.gitignore` 中被排除，则**不会**出现在下文第 4 节表格中，尽管工作目录里可能仍有该文件夹。

---

## 2. 工作空间目录树（逻辑结构，仅含清单内包）

```
yahboomcar_ws/
├── .gitignore
├── README.md
├── AUTO_EXPLORE_STATUS.md
└── src/
    ├── aws-robomaker-hospital-world/    # 医院 Gazebo 世界与模型（CMake / ROS 2）
    ├── yahboom_m3pro_exploration/       # 前沿探索 + Nav2 参数（Python ament）
    ├── yahboom_m3pro_lidar_tools/       # 多激光合并 C++ 节点
    └── yahboom_m3pro_slam_demo/         # M3Pro 医院仿真 + Cartographer 等（Python ament）
```

---

## 3. 各包与关键文件说明（详细）

### 3.1 工作区根

- **`.gitignore`**  
  定义 Git 与工作区文档统计时排除的内容：编译目录、大量教学用 `src` 子包、IDE、缓存及二进制模型权重后缀等。

- **`README.md`**  
  工作空间总览：`rosdep`、环境变量顺序（ROS 2 → Gazebo → 工作空间）、编译与典型 launch 说明。

- **`AUTO_EXPLORE_STATUS.md`**  
  与自动探索或 SLAM 实验相关的状态记录类 Markdown。

---

### 3.2 `src/aws-robomaker-hospital-world`

基于 AWS RoboMaker 的医院仿真世界，供 Gazebo Classic 使用。以下**只说明目录用途**；具体模型名、网格与贴图文件名见仓库内树形结构，本文不再逐文件列举。

| 目录 | 说明 |
|------|------|
| `docs/` | 文档资源；其下 `images/` 为 README/说明用配图与占位。 |
| `launch/` | 启动 Gazebo 并加载医院世界的 `.launch` 文件。 |
| `models/` | 包内自带的 Gazebo 模型：建筑构件（墙/地/顶、电梯、护士站等）、家具与装饰画等；每个子目录为一个模型，通常含 `model.config`、`model.sdf`、`meshes/`、`materials/` 等。 |
| `fuel_models/` | 通过 Gazebo Fuel 拉取的道具与人物模型；根目录可有 `database.config`；每个子目录为一种模型，常见结构为 `model.config`、`model.sdf`、`meshes/`（OBJ/MTL/贴图）、`thumbnails/`。 |
| `photos/` | 装饰画等用的 JPEG 贴图，由部分 DAE 以相对路径引用。 |
| `worlds/` | 医院场景的 `.world` 主文件及多楼层等变体。 |
| （包根目录） | 散落的构建与元数据文件：`CMakeLists.txt`（构建与 `install` 规则）、`package.xml`、`requirements.txt`、`fuel_utility.py`（Fuel 批量下载）、`setup.sh`、`LICENSE`、`NOTICE`、`README.md`、`CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`.gitignore` 等；不单独逐文件展开。 |

---

### 3.3 `src/yahboom_m3pro_exploration`

| 路径 | 说明 |
|------|------|
| `package.xml` / `setup.py` / `setup.cfg` | ament_python 包元数据与安装配置。 |
| `resource/yahboom_m3pro_exploration` | 包资源标记文件。 |
| `config/nav2_params.yaml` | Nav2 栈参数：代价地图、规划器、行为树等，供自动探索使用。 |
| `launch/auto_explore_slam_launch.py` | 启动探索节点、SLAM、Nav2 等的组合 launch。 |
| `yahboom_m3pro_exploration/frontier_explorer.py` | 前沿（frontier）探索逻辑实现。 |
| `yahboom_m3pro_exploration/__init__.py` | 包初始化。 |

---

### 3.4 `src/yahboom_m3pro_lidar_tools`

| 路径 | 说明 |
|------|------|
| `CMakeLists.txt` | 定义 C++ 可执行文件 `multi_lidar_merger_node` 的编译与安装。 |
| `package.xml` | 声明 `rclcpp`、`sensor_msgs` 等依赖。 |
| `src/multi_lidar_merger_node.cpp` | 订阅多路激光（或类似 `LaserScan`），发布合并后的 `/scan_merged`（具体话题名以源码为准）。 |

---

### 3.5 `src/yahboom_m3pro_slam_demo`

M3Pro 在医院场景中的仿真、遥控、Cartographer、显示与桥接配置。

| 路径 | 说明 |
|------|------|
| `src/aws-robomaker-hospital-world/docs/` | 文档配图目录：`images/` 下为 README/说明用截图与示意图。 |
| `src/aws-robomaker-hospital-world/launch/` | Gazebo Classic 启动文件（如加载医院世界）。 |
| `src/aws-robomaker-hospital-world/models/` | 内置 Gazebo 模型：医院建筑构件、电梯、家具、装饰画等；各子目录为独立模型，内含 `model.config`、`model.sdf`、`meshes/`、`materials/` 等。 |
| `src/aws-robomaker-hospital-world/fuel_models/` | 通过 Fuel 下载的道具/人物模型库；根目录含 `database.config`；各子目录为一种模型，一般含 `model.config`、`model.sdf`、`meshes/`（OBJ/MTL/贴图）、`thumbnails/`。 |
| `src/aws-robomaker-hospital-world/photos/` | Portrait 等装饰画所用 JPEG 贴图，供部分 DAE 引用。 |
| `src/aws-robomaker-hospital-world/worlds/` | Gazebo `.world` 医院场景主文件及多楼层变体。 |
| `src/aws-robomaker-hospital-world/`（包根目录零散文件） | `CMakeLists.txt`、`package.xml`、`requirements.txt`、`fuel_utility.py`、`setup.sh`、`LICENSE`、`NOTICE`、`README.md`、`CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`.gitignore`：构建与安装、ROS 依赖声明、Python 依赖、Fuel 批量下载脚本、环境脚本、许可证与社区文档、包内忽略规则。 |
| `package.xml` / `setup.py` / `setup.cfg` | ament_python 包定义与测试入口。 |
| `resource/yahboom_m3pro_slam_demo` | 资源标记。 |
| `launch/gazebo_hospital_slam_demo_launch.py` | 医院世界 + 机器人 spawn + 传感器桥接 + 合并激光等主 demo。 |
| `launch/hospital_m3pro_teleop_launch.py` | 键盘/遥控与医院场景组合。 |
| `launch/display_launch.py` | RViz/机器人模型显示类启动。 |
| `launch/lidar_slam_launch.py` | 激光 SLAM 相关启动。 |
| `launch/gazebo_hospital_slam_demo_launch.md` | 上述 launch 的说明文档。 |
| `config/cartographer_m3pro_2d.lua` 等 `*.lua` | Google Cartographer 2D/3D、轨迹与位姿图参数。 |
| `config/controllers.yaml` | `ros2_control` 控制器参数。 |
| `config/ros_gz_bridge_hospital.yaml` | ROS 2 ↔ Gazebo 经典 桥接映射配置。 |
| `config/README.md` | 配置目录说明。 |
| `urdf/M3Pro.urdf` | 机器人链路、关节、Gazebo 插件引用；网格多来自 `meshes/`。 |
| `meshes/*.STL` | 各连杆、轮子、机械臂、相机等 STL 网格文件名与 URDF 中 `mesh filename` 对应。 |
| `maps/hospital_map_v1.yaml` + `.pgm` | 预保存医院栅格地图及元数据。 |
| `rviz/*.rviz` | RViz2 布局（激光、地图、TF、机器人模型等）。 |
| `scripts/multi_lidar_merger.py` | Python 版多激光合并脚本（若与 C++ 节点二选一或并存）。 |
| `test/test_*.py` | ament 版权、flake8、docstring 风格测试。 |
| `yahboom_m3pro_slam_demo/__init__.py` | 包初始化。 |
| `diagnosis.log` | 某次运行的终端日志存档；非源代码，可清理。 |
| `launch/.ipynb_checkpoints/`、`urdf/.ipynb_checkpoints/` | Jupyter 自动保存；建议日后加入 `.gitignore`。 |

---

## 4. 完整文件路径与说明对照表

下表在合并 `aws-robomaker-hospital-world` 为目录级条目后共 **71** 行；其中该包仅占 7 行，其余为其它包逐文件说明。非 aws 路径的说明仍按 **文件类型与路径模式** 归类生成。

| 路径 | 说明 |
|------|------|
| `AUTO_EXPLORE_STATUS.md` | 自动探索 / SLAM 相关状态或笔记类文档。 |
| `.gitignore` | Git 忽略规则：指定不纳入版本管理或不在本清单统计范围内的路径与文件类型。 |
| `README.md` | 工作空间根说明：依赖安装、环境变量、编译与启动方式等。 |
| `src/aws-robomaker-hospital-world/docs/` | 文档配图目录：`images/` 下为 README/说明用截图与示意图。 |
| `src/aws-robomaker-hospital-world/launch/` | Gazebo Classic 启动文件（如加载医院世界）。 |
| `src/aws-robomaker-hospital-world/models/` | 内置 Gazebo 模型：医院建筑构件、电梯、家具、装饰画等；各子目录为独立模型，内含 `model.config`、`model.sdf`、`meshes/`、`materials/` 等。 |
| `src/aws-robomaker-hospital-world/fuel_models/` | 通过 Fuel 下载的道具/人物模型库；根目录含 `database.config`；各子目录为一种模型，一般含 `model.config`、`model.sdf`、`meshes/`（OBJ/MTL/贴图）、`thumbnails/`。 |
| `src/aws-robomaker-hospital-world/photos/` | Portrait 等装饰画所用 JPEG 贴图，供部分 DAE 引用。 |
| `src/aws-robomaker-hospital-world/worlds/` | Gazebo `.world` 医院场景主文件及多楼层变体。 |
| `src/aws-robomaker-hospital-world/`（包根目录零散文件） | `CMakeLists.txt`、`package.xml`、`requirements.txt`、`fuel_utility.py`、`setup.sh`、`LICENSE`、`NOTICE`、`README.md`、`CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`.gitignore`：构建与安装、ROS 依赖声明、Python 依赖、Fuel 批量下载脚本、环境脚本、许可证与社区文档、包内忽略规则。 |
| `src/yahboom_m3pro_exploration/config/nav2_params.yaml` | YAML 配置：Nav2、Gazebo–ROS 桥、地图元数据等。 |
| `src/yahboom_m3pro_exploration/launch/auto_explore_slam_launch.py` | ROS 2 Python Launch：启动节点、参数与包含其它 launch。 |
| `src/yahboom_m3pro_exploration/package.xml` | ROS 包清单：包名、依赖、构建类型（ament_cmake 或 ament_python）。 |
| `src/yahboom_m3pro_exploration/resource/yahboom_m3pro_exploration` | ament 资源标记文件：与包名同名，用于 `ros2 pkg prefix` 等识别。 |
| `src/yahboom_m3pro_exploration/setup.cfg` | Python 打包与测试工具配置（如 pytest、flake8 等）。 |
| `src/yahboom_m3pro_exploration/setup.py` | Python 包 setuptools 入口：声明可安装模块与 entry_points（若有）。 |
| `src/yahboom_m3pro_exploration/yahboom_m3pro_exploration/frontier_explorer.py` | Python 源码模块或脚本。 |
| `src/yahboom_m3pro_exploration/yahboom_m3pro_exploration/__init__.py` | Python 包标识：使目录成为可导入的包。 |
| `src/yahboom_m3pro_lidar_tools/CMakeLists.txt` | CMake 构建脚本：编译 `multi_lidar_merger_node` 等 C++ 节点。 |
| `src/yahboom_m3pro_lidar_tools/package.xml` | ROS 包清单：包名、依赖、构建类型（ament_cmake 或 ament_python）。 |
| `src/yahboom_m3pro_lidar_tools/src/multi_lidar_merger_node.cpp` | C++ 源码：ROS 2 节点实现（如多激光合并）。 |
| `src/yahboom_m3pro_slam_demo/config/cartographer_m3pro_2d.lua` | Cartographer 2D/3D 或轨迹构建器 Lua 配置。 |
| `src/yahboom_m3pro_slam_demo/config/controllers.yaml` | YAML 配置：Nav2、Gazebo–ROS 桥、地图元数据等。 |
| `src/yahboom_m3pro_slam_demo/config/map_builder.lua` | Cartographer 2D/3D 或轨迹构建器 Lua 配置。 |
| `src/yahboom_m3pro_slam_demo/config/pose_graph.lua` | Cartographer 2D/3D 或轨迹构建器 Lua 配置。 |
| `src/yahboom_m3pro_slam_demo/config/README.md` | Markdown 文档：说明、教程或设计笔记。 |
| `src/yahboom_m3pro_slam_demo/config/ros_gz_bridge_hospital.yaml` | YAML 配置：Nav2、Gazebo–ROS 桥、地图元数据等。 |
| `src/yahboom_m3pro_slam_demo/config/trajectory_builder_2d.lua` | Cartographer 2D/3D 或轨迹构建器 Lua 配置。 |
| `src/yahboom_m3pro_slam_demo/config/trajectory_builder_3d.lua` | Cartographer 2D/3D 或轨迹构建器 Lua 配置。 |
| `src/yahboom_m3pro_slam_demo/diagnosis.log` | 运行诊断日志（终端输出重定向）；可删除或加入忽略，不宜作为长期版本内容。 |
| `src/yahboom_m3pro_slam_demo/launch/display_launch.py` | ROS 2 Python Launch：启动节点、参数与包含其它 launch。 |
| `src/yahboom_m3pro_slam_demo/launch/gazebo_hospital_slam_demo_launch.md` | Markdown 文档：说明、教程或设计笔记。 |
| `src/yahboom_m3pro_slam_demo/launch/gazebo_hospital_slam_demo_launch.py` | ROS 2 Python Launch：启动节点、参数与包含其它 launch。 |
| `src/yahboom_m3pro_slam_demo/launch/hospital_m3pro_teleop_launch.py` | ROS 2 Python Launch：启动节点、参数与包含其它 launch。 |
| `src/yahboom_m3pro_slam_demo/launch/.ipynb_checkpoints/display_launch-checkpoint.py` | ROS 2 Python Launch：启动节点、参数与包含其它 launch。 |
| `src/yahboom_m3pro_slam_demo/launch/lidar_slam_launch.py` | ROS 2 Python Launch：启动节点、参数与包含其它 launch。 |
| `src/yahboom_m3pro_slam_demo/maps/hospital_map_v1.pgm` | 占用栅格地图图像（与 `.yaml` 配对）。 |
| `src/yahboom_m3pro_slam_demo/maps/hospital_map_v1.yaml` | YAML 配置：Nav2、Gazebo–ROS 桥、地图元数据等。 |
| `src/yahboom_m3pro_slam_demo/meshes/arm1.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/arm2.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/arm3.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/arm4.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/arm5.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/arm_base_Link.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/base_link.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/Camera.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/DCW2.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/Gripping.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/llink1.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/llink2.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/llink3.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/lwheel1.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/lwheel2.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/rlink1.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/rlink2.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/rlink3.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/rwheel1.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/meshes/rwheel2.STL` | STL 三角网格：M3Pro 机器人连杆/相机等部件的可视化网格。 |
| `src/yahboom_m3pro_slam_demo/package.xml` | ROS 包清单：包名、依赖、构建类型（ament_cmake 或 ament_python）。 |
| `src/yahboom_m3pro_slam_demo/resource/yahboom_m3pro_slam_demo` | ament 资源标记文件：与包名同名，用于 `ros2 pkg prefix` 等识别。 |
| `src/yahboom_m3pro_slam_demo/rviz/spen_M3Pro_lidar_slam.rviz` | RViz2 显示配置：话题、TF、地图与机器人模型等。 |
| `src/yahboom_m3pro_slam_demo/rviz/yahboom_M3Pro.rviz` | RViz2 显示配置：话题、TF、地图与机器人模型等。 |
| `src/yahboom_m3pro_slam_demo/scripts/multi_lidar_merger.py` | Python 源码模块或脚本。 |
| `src/yahboom_m3pro_slam_demo/setup.cfg` | Python 打包与测试工具配置（如 pytest、flake8 等）。 |
| `src/yahboom_m3pro_slam_demo/setup.py` | Python 包 setuptools 入口：声明可安装模块与 entry_points（若有）。 |
| `src/yahboom_m3pro_slam_demo/test/test_copyright.py` | ament 测试：版权、flake8、pep257 等。 |
| `src/yahboom_m3pro_slam_demo/test/test_flake8.py` | ament 测试：版权、flake8、pep257 等。 |
| `src/yahboom_m3pro_slam_demo/test/test_pep257.py` | ament 测试：版权、flake8、pep257 等。 |
| `src/yahboom_m3pro_slam_demo/urdf/.ipynb_checkpoints/M3Pro-checkpoint.urdf` | URDF：M3Pro 机器人关节、连杆与 Gazebo 插件等描述。 |
| `src/yahboom_m3pro_slam_demo/urdf/M3Pro.urdf` | URDF：M3Pro 机器人关节、连杆与 Gazebo 插件等描述。 |
| `src/yahboom_m3pro_slam_demo/yahboom_m3pro_slam_demo/__init__.py` | Python 包标识：使目录成为可导入的包。 |