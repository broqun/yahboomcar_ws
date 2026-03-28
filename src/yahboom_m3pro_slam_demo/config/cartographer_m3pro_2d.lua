
include "map_builder.lua"
include "trajectory_builder_2d.lua"
include "trajectory_builder_3d.lua"

options = {
  map_frame = "map",
  tracking_frame = "imu_link",
  published_frame = "odom",
  odom_frame = "odom",
  provide_odom_frame = false,
  use_odometry = true,
  use_nav_sat = false,
  use_landmarks = false,
  num_laser_scans = 2,
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
TRAJECTORY_BUILDER_2D.min_range = 0.1
TRAJECTORY_BUILDER_2D.max_range = 10.0

options.map_builder = MAP_BUILDER
options.trajectory_builder = {
  trajectory_builder_2d = TRAJECTORY_BUILDER_2D,
  trajectory_builder_3d = TRAJECTORY_BUILDER_3D,
  collate_fixed_frame = true,
  collate_landmarks = false,
}

return options
