-- Cartographer 2D SLAM for M3Pro with depth-to-laserscan.
-- Used with depth_cartographer_launch.py (same depth/scan setup as depth_slam_launch).
-- Frames: map -> odom -> base_footprint (compatible with hospital_m3pro_teleop_launch).

include "map_builder.lua"
include "trajectory_builder_2d.lua"
include "trajectory_builder_3d.lua"

-- options 需与 cartographer_ros NodeOptions 一致，缺键会报 HasKey(key) / used the wrong number of times
-- 参考：https://google-cartographer-ros.readthedocs.io/en/latest/configuration.html
options = {
  map_frame = "map",
  tracking_frame = "base_footprint",
  published_frame = "odom",
  odom_frame = "odom",
  provide_odom_frame = true,
  use_odometry = false,
  use_nav_sat = false,
  use_landmarks = false,
  num_laser_scans = 1,
  num_subdivisions_per_laser_scan = 1,
  num_multi_echo_laser_scans = 0,
  num_point_clouds = 0,
  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 0.03,
  publish_frame_projected_to_2d = true,
  rangefinder_sampling_ratio = 1.0,
  odometry_sampling_ratio = 1.0,
  imu_sampling_ratio = 1.0,
  fixed_frame_pose_sampling_ratio = 1.0,
  landmarks_sampling_ratio = 1.0,
}

MAP_BUILDER.use_trajectory_builder_2d = true
-- 不要在此覆盖 TRAJECTORY_BUILDER_2D.scan_period：此版本 C++ 不读取该键，会报 "Key 'scan_period' was used the wrong number of times"
TRAJECTORY_BUILDER_2D.min_range = 0.1
TRAJECTORY_BUILDER_2D.max_range = 10.0

-- C++ 端要求 options.trajectory_builder 同时包含 trajectory_builder_2d 与 trajectory_builder_3d（官方 trajectory_builder.lua 结构）
options.map_builder = MAP_BUILDER
options.trajectory_builder = {
  trajectory_builder_2d = TRAJECTORY_BUILDER_2D,
  trajectory_builder_3d = TRAJECTORY_BUILDER_3D,
  collate_fixed_frame = true,
  collate_landmarks = false,
}

-- Cartographer 要求主配置文件的“返回值”为 options 表
return options
