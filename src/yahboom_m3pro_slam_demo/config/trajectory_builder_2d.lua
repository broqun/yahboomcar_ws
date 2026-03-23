-- 2D trajectory builder for Cartographer (depth-to-laserscan, no IMU).
-- Aligns with depth_slam_launch: range_min 0.1, range_max 10.0.

TRAJECTORY_BUILDER_2D = {
  -- 是否使用 IMU。无 IMU 时设为 false，仅靠激光做位姿估计。
  -- 例：实机有 IMU 可设为 true 并配置 tracking_frame 为 imu_link。
  use_imu_data = false,

  -- 激光有效最小/最大距离（米）。超出范围的测距会被丢弃。
  -- 例：0.1~10 与 depthimage_to_laserscan 的 range_min/max 一致，避免无效点。
  min_range = 0.1,
  max_range = 10.0,

  -- 点云高度过滤（米）。2D 激光一般忽略；若用 3D 点云则只保留 [min_z, max_z] 内的点。
  min_z = -0.8,
  max_z = 1.0,

  -- 当某束激光无有效测距时，在占用栅格中当作“射线长度”的默认值（米）。
  -- 例：5.0 表示“无数据”的射线按 5 米长画，用于区分未知与自由空间。
  missing_data_ray_length = 5.0,

  -- 累积多少帧激光后再做一次扫描匹配。1 表示每帧都匹配，实时性最好。
  -- 例：设为 2 可略降计算量但会稍增加延迟。
  num_accumulated_range_data = 1,

  -- 体素滤波格子边长（米）。同一格子内的点会合并，用于降采样、减少计算量。
  -- 例：0.025 即 2.5cm，室内建图常用；室外可试 0.05。
  voxel_filter_size = 0.025,

  -- 是否启用在线相关扫描匹配（在 Ceres 优化前先用 real_time_correlative_scan_matcher 做初对齐）。C++ 端必填。
  use_online_correlative_scan_matching = true,

  -- 自适应体素滤波（用于构造局部子图时的降采样）
  adaptive_voxel_filter = {
    max_length = 0.5,   -- 体素最大边长（米）。例：0.5 表示格子最大 50cm。
    min_num_points = 200,  -- 至少保留点数，不足则缩小体素以保证点数。
    max_range = 50.0,   -- 超过此距离（米）的点不参与此滤波。
  },

  -- 回环检测时的体素滤波（通常比上面略宽松，以保留更多特征）
  loop_closure_adaptive_voxel_filter = {
    max_length = 0.9,   -- 例：0.9 比 0.5 更粗，回环时计算更快。
    min_num_points = 100,
    max_range = 50.0,
  },

  -- 实时相关扫描匹配：在局部窗口内做平移/旋转搜索，得到初对齐位姿。
  real_time_correlative_scan_matcher = {
    linear_search_window = 0.1,       -- 平移搜索范围（米），例：±0.1 即前后左右各 10cm。
    angular_search_window = math.rad(20.),  -- 角度搜索范围（弧度），例：20 度。
    translation_delta_cost_weight = 1e-1,  -- 平移偏差在代价中的权重，越小越容忍平移。
    rotation_delta_cost_weight = 1e-1,      -- 旋转偏差在代价中的权重。
  },

  -- Ceres 扫描匹配：在初对齐基础上用优化进一步对齐，提高精度。
  ceres_scan_matcher = {
    occupied_space_weight = 1.,   -- 占用栅格与激光重合度的权重。
    translation_weight = 10.,    -- 平移正则权重，防止优化乱跳。
    rotation_weight = 40.,       -- 旋转正则权重，通常比平移大以稳定朝向。
    ceres_solver_options = {
      use_nonmonotonic_steps = false,  -- 是否允许目标函数偶尔变差（多用于困难场景）。
      max_num_iterations = 20,         -- 单次优化最大迭代次数，例：20 通常够用。
      num_threads = 1,                 -- Ceres 内部线程数。
    },
  },

  -- 运动过滤：只有位移/转角/时间超过阈值才插入新位姿，避免过于密集的节点。
  motion_filter = {
    max_time_seconds = 0.2,      -- 距上一帧超过 0.2 秒则允许插入。例：0.2 约 5Hz 最低更新。
    max_distance_meters = 0.2,   -- 移动超过 0.2 米才插入，例：减少静止时的冗余节点。
    max_angle_radians = 0.5,     -- 旋转超过约 28 度才插入。
  },

  -- 位姿外推器：在两次测量之间用匀速模型等估计位姿。C++ 端必填。
  pose_extrapolator = {
    use_imu_based = false,       -- 无 IMU 时用 constant_velocity。
    constant_velocity = {
      imu_gravity_time_constant = 10.,
      pose_queue_duration = 0.001,
    },
    imu_based = {
      pose_queue_duration = 5.,
      gravity_constant = 9.806,
      pose_translation_weight = 1.,
      pose_rotation_weight = 1.,
      imu_acceleration_weight = 1.,
      imu_rotation_weight = 1.,
      odometry_translation_weight = 1.,
      odometry_rotation_weight = 1.,
      solver_options = {
        use_nonmonotonic_steps = false,
        max_num_iterations = 10,
        num_threads = 1,
      },
    },
  },

  -- 注意：immutable_pose_min_observations、pose_observation_continuous_estimation_duration 等键在官方 core trajectory_builder_2d 中不存在，
  -- 当前 C++ 不读取会报 "Key was used the wrong number of times"，故不在此填写。

  -- 仅保留供 ROS 兼容；2D 无 IMU 时未使用。
  imu_gravity_time_constant = 10.,

  -- 子图配置：每个子图包含多少帧激光、栅格分辨率、占用插入参数。C++ 端必填。
  submaps = {
    num_range_data = 90,
    grid_options_2d = {
      grid_type = "PROBABILITY_GRID",
      resolution = 0.05,
    },
    range_data_inserter = {
      range_data_inserter_type = "PROBABILITY_GRID_INSERTER_2D",
      probability_grid_range_data_inserter = {
        insert_free_space = true,
        hit_probability = 0.55,
        miss_probability = 0.49,
      },
      -- 2D 使用 PROBABILITY_GRID 时由上面填充；C++ 端仍要求此键存在（可为占位）。
      tsdf_range_data_inserter = {
        truncation_distance = 0.3,
        maximum_weight = 10.,
        update_free_space = false,
        normal_estimation_options = {
          num_normal_samples = 4,
          sample_radius = 0.5,
        },
        project_sdf_distance_to_scan_normal = true,
        update_weight_range_exponent = 0,
        update_weight_angle_scan_normal_to_ray_kernel_bandwidth = 0.5,
        update_weight_distance_cell_to_hit_kernel_bandwidth = 0.5,
      },
    },
  },
}
