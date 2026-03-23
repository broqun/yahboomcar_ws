-- Cartographer 地图构建配置。主配置 cartographer_m3pro_2d.lua 会 include 本文件并设置 MAP_BUILDER.use_trajectory_builder_2d = true。
-- 结构对齐官方：https://github.com/cartographer-project/cartographer/blob/master/configuration_files/map_builder.lua

include "pose_graph.lua"

MAP_BUILDER = {
  use_trajectory_builder_2d = true,
  use_trajectory_builder_3d = false,
  num_background_threads = 4,
  pose_graph = POSE_GRAPH,
  collate_by_trajectory = false,
}
