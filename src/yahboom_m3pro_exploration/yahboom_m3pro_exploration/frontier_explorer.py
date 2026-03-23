import math
from collections import deque
from typing import Deque, List, Optional, Sequence, Tuple

from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped, Quaternion
from nav2_msgs.action import BackUp, ComputePathToPose, NavigateToPose, Spin
from nav_msgs.msg import OccupancyGrid
import rclpy
from rclpy.action import ActionClient
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import Buffer, TransformException, TransformListener


GridPoint = Tuple[int, int]
WorldPoint = Tuple[float, float]


class FrontierExplorer(Node):
    """Explore the unknown map by repeatedly sending Nav2 frontier goals."""

    def __init__(self) -> None:
        super().__init__('frontier_explorer')

        # 下面这些参数则完全由 frontier_explorer 自己定义和消费。
        # 它们先覆盖“最小可用探索”场景：地图来自 slam_toolbox，
        # 控制由 Nav2 完成，frontier 节点只负责挑选目标点。
        self.declare_parameter('map_topic', '/map')
        self.declare_parameter('global_frame', 'map')
        self.declare_parameter('base_frame', 'base_footprint')
        self.declare_parameter('planning_period_sec', 3.0)
        self.declare_parameter('goal_timeout_sec', 90.0)
        self.declare_parameter('min_frontier_size', 8)
        self.declare_parameter('occupied_threshold', 50)
        self.declare_parameter('frontier_size_weight', 0.06)
        self.declare_parameter('blacklist_radius', 0.75)
        self.declare_parameter('goal_reached_radius', 0.60)
        self.declare_parameter('startup_min_frontier_size', 3)
        self.declare_parameter('goal_backoff_distance', 0.35)
        self.declare_parameter('no_frontier_cycles_before_spin', 3)
        self.declare_parameter('spin_recovery_angle', 1.57)
        self.declare_parameter('spin_time_allowance_sec', 20.0)
        self.declare_parameter('backup_recovery_distance', 0.35)
        self.declare_parameter('backup_recovery_speed', 0.08)
        self.declare_parameter('backup_time_allowance_sec', 12.0)
        self.declare_parameter('candidate_goal_limit', 8)
        self.declare_parameter('candidate_clearance_radius', 0.35)
        self.declare_parameter('goal_known_free_radius', 0.20)
        self.declare_parameter('goal_backoff_step', 0.10)
        self.declare_parameter('startup_known_free_radius', 0.10)
        self.declare_parameter('startup_goal_min_distance', 0.80)
        self.declare_parameter('startup_goal_reuse_radius', 0.35)
        self.declare_parameter('startup_goal_success_limit', 4)
        self.declare_parameter('path_validation_min_poses', 2)

        self.map_topic = self.get_parameter('map_topic').value
        self.global_frame = self.get_parameter('global_frame').value
        self.base_frame = self.get_parameter('base_frame').value
        self.planning_period_sec = float(self.get_parameter('planning_period_sec').value)
        self.goal_timeout_sec = float(self.get_parameter('goal_timeout_sec').value)
        self.min_frontier_size = int(self.get_parameter('min_frontier_size').value)
        self.occupied_threshold = int(self.get_parameter('occupied_threshold').value)
        self.frontier_size_weight = float(self.get_parameter('frontier_size_weight').value)
        self.blacklist_radius = float(self.get_parameter('blacklist_radius').value)
        self.goal_reached_radius = float(self.get_parameter('goal_reached_radius').value)
        self.startup_min_frontier_size = int(self.get_parameter('startup_min_frontier_size').value)
        self.goal_backoff_distance = float(self.get_parameter('goal_backoff_distance').value)
        self.no_frontier_cycles_before_spin = int(
            self.get_parameter('no_frontier_cycles_before_spin').value
        )
        self.spin_recovery_angle = float(self.get_parameter('spin_recovery_angle').value)
        self.spin_time_allowance_sec = float(
            self.get_parameter('spin_time_allowance_sec').value
        )
        self.backup_recovery_distance = float(
            self.get_parameter('backup_recovery_distance').value
        )
        self.backup_recovery_speed = float(
            self.get_parameter('backup_recovery_speed').value
        )
        self.backup_time_allowance_sec = float(
            self.get_parameter('backup_time_allowance_sec').value
        )
        self.candidate_goal_limit = int(self.get_parameter('candidate_goal_limit').value)
        self.candidate_clearance_radius = float(
            self.get_parameter('candidate_clearance_radius').value
        )
        self.goal_known_free_radius = float(
            self.get_parameter('goal_known_free_radius').value
        )
        self.goal_backoff_step = float(self.get_parameter('goal_backoff_step').value)
        self.startup_known_free_radius = float(
            self.get_parameter('startup_known_free_radius').value
        )
        self.startup_goal_min_distance = float(
            self.get_parameter('startup_goal_min_distance').value
        )
        self.startup_goal_reuse_radius = float(
            self.get_parameter('startup_goal_reuse_radius').value
        )
        self.startup_goal_success_limit = int(
            self.get_parameter('startup_goal_success_limit').value
        )
        self.path_validation_min_poses = int(
            self.get_parameter('path_validation_min_poses').value
        )

        self.latest_map: Optional[OccupancyGrid] = None
        self.goal_active = False
        self.goal_pending = False
        self.path_check_pending = False
        self.goal_handle = None
        self.goal_sent_time = None
        self.current_goal_xy: Optional[WorldPoint] = None
        self.current_goal_mode: Optional[str] = None
        self.candidate_goal_mode: Optional[str] = None
        self.blacklisted_goals: List[WorldPoint] = []
        self._map_received_once = False
        self._server_wait_logged = False
        self._no_frontier_logged = False
        self._no_frontier_cycles = 0
        self._successful_goals = 0
        self.spin_active = False
        self.spin_pending = False
        self.backup_active = False
        self.backup_pending = False
        self.candidate_goals: List[Tuple[WorldPoint, float]] = []
        self._path_validation_goal_xy: Optional[WorldPoint] = None
        self._path_validation_robot_pose: Optional[Tuple[float, float, float]] = None
        self._startup_goal_successes = 0
        self._last_recovery_mode: Optional[str] = None

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.navigate_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        # 在真正把目标交给 NavigateToPose 之前，先调用 planner 做一次路径预检查，
        # 避免“前方近障碍、目标点看起来不错但实际上根本规划不过去”的情况。
        self.compute_path_client = ActionClient(self, ComputePathToPose, 'compute_path_to_pose')
        # 当启动早期地图太小、frontier 还没成型时，使用 Nav2 的 Spin 行为
        # 主动扩大可见区域，避免“不动 -> 地图不长 -> 没 frontier -> 一直不动”。
        self.spin_client = ActionClient(self, Spin, 'spin')
        # 当 planner 连一个短距离启动目标都做不出来时，单纯 spin 往往不够；
        # 这里增加 Nav2 的 BackUp 恢复，让机器人先强制后退一小段，脱离原地僵局。
        self.backup_client = ActionClient(self, BackUp, 'backup')

        self.map_sub = self.create_subscription(
            OccupancyGrid,
            self.map_topic,
            self._map_callback,
            10,
        )
        self.plan_timer = self.create_timer(self.planning_period_sec, self._planning_timer_cb)

        self.get_logger().info(
            'frontier_explorer is running. It will read /map, pick frontier goals, '
            'and send them to Nav2 via NavigateToPose.'
        )

    def _map_callback(self, msg: OccupancyGrid) -> None:
        self.latest_map = msg
        if not self._map_received_once:
            self._map_received_once = True
            self.get_logger().info(f'Received first map on {self.map_topic}.')

    def _planning_timer_cb(self) -> None:
        if self.latest_map is None:
            return

        if not self.navigate_client.server_is_ready():
            if not self._server_wait_logged:
                self._server_wait_logged = True
                self.get_logger().info('Waiting for Nav2 action server: navigate_to_pose')
            return

        if not self.compute_path_client.server_is_ready():
            if not self._server_wait_logged:
                self._server_wait_logged = True
                self.get_logger().info('Waiting for Nav2 action server: compute_path_to_pose')
            return

        self._server_wait_logged = False

        if self.goal_pending or self.spin_pending or self.backup_pending or self.path_check_pending:
            return

        if self.goal_active or self.spin_active or self.backup_active:
            self._check_goal_timeout()
            return

        robot_pose = self._lookup_robot_pose()
        if robot_pose is None:
            return

        if self.candidate_goals:
            self._start_next_path_validation(robot_pose)
            return

        candidate_goals = self._rank_frontier_candidates(robot_pose)
        if not candidate_goals and self._startup_goal_successes < self.startup_goal_success_limit:
            candidate_goals = self._rank_startup_candidates(robot_pose)
            self.candidate_goal_mode = 'startup' if candidate_goals else None
        else:
            self.candidate_goal_mode = 'frontier' if candidate_goals else None

        if not candidate_goals:
            self._no_frontier_cycles += 1
            if not self._no_frontier_logged:
                self._no_frontier_logged = True
                self.get_logger().info(
                    'No valid frontier found yet; waiting for map growth or spin recovery.'
                )
            if self._no_frontier_cycles >= self.no_frontier_cycles_before_spin:
                self._trigger_recovery_behavior()
            return

        self._no_frontier_logged = False
        self._no_frontier_cycles = 0
        self.candidate_goals = candidate_goals
        self._start_next_path_validation(robot_pose)

    def _lookup_robot_pose(self) -> Optional[Tuple[float, float, float]]:
        try:
            transform = self.tf_buffer.lookup_transform(
                self.global_frame,
                self.base_frame,
                Time(),
                timeout=Duration(seconds=0.2),
            )
        except TransformException:
            return None

        tx = transform.transform.translation.x
        ty = transform.transform.translation.y
        q = transform.transform.rotation
        yaw = self._yaw_from_quaternion(q.x, q.y, q.z, q.w)
        return (tx, ty, yaw)

    def _rank_frontier_candidates(
        self,
        robot_pose: Tuple[float, float, float],
    ) -> List[Tuple[WorldPoint, float]]:
        assert self.latest_map is not None

        frontier_cells = self._find_frontier_cells(self.latest_map)
        if not frontier_cells:
            return []

        frontier_clusters = self._cluster_frontiers(frontier_cells)
        ranked_goals: List[Tuple[WorldPoint, float]] = []
        # 首个探索目标通常最难出现，因此在“还没有任何成功导航”之前，
        # 放宽 frontier 最小规模阈值，优先打破启动僵局。
        effective_min_frontier_size = (
            self.min_frontier_size
            if self._successful_goals > 0
            else min(self.min_frontier_size, self.startup_min_frontier_size)
        )

        for cluster in frontier_clusters:
            if len(cluster) < effective_min_frontier_size:
                continue

            candidate = self._frontier_cluster_to_world_goal(cluster, self.latest_map, robot_pose)
            if candidate is None:
                continue

            if self._is_blacklisted(candidate):
                continue

            # 候选目标除了“点本身是 free”，还要求周围不要明显贴着已知障碍物。
            # 注意这里不能把“靠近未知区域”也当成失败条件，否则启动阶段那一小圈
            # frontier 会被全部过滤掉，机器人就只会反复 spin 而不出发。
            if not self._has_local_clearance(candidate, self.latest_map):
                continue

            distance = math.hypot(candidate[0] - robot_pose[0], candidate[1] - robot_pose[1])
            # 太靠近机器人本体的 frontier 没有导航意义，直接跳过。
            if distance < self.goal_reached_radius:
                continue
            # 分数越低越优先：离机器人更近、同时 frontier 规模更大。
            score = distance - len(cluster) * self.frontier_size_weight
            ranked_goals.append((candidate, score))

        ranked_goals.sort(key=lambda item: item[1])
        return ranked_goals[:self.candidate_goal_limit]

    def _rank_startup_candidates(
        self,
        robot_pose: Tuple[float, float, float],
    ) -> List[Tuple[WorldPoint, float]]:
        assert self.latest_map is not None

        ranked_goals: List[Tuple[WorldPoint, float]] = []
        # 如果启动阶段 frontier 还太“薄”，先尝试机器人周围几个短距离已知自由点，
        # 让底盘先挪出初始位置，把地图扩起来，再进入正常 frontier 探索。
        direction_offsets = (
            (0.0, 0.0),
            (math.pi / 4.0, 0.15),
            (-math.pi / 4.0, 0.15),
            (math.pi / 2.0, 0.25),
            (-math.pi / 2.0, 0.25),
            (math.pi, 0.45),
        )
        distances = (0.40, 0.60, 0.80)

        for distance in distances:
            for yaw_offset, penalty in direction_offsets:
                heading = robot_pose[2] + yaw_offset
                candidate = (
                    robot_pose[0] + math.cos(heading) * distance,
                    robot_pose[1] + math.sin(heading) * distance,
                )
                if distance < self.startup_goal_min_distance:
                    continue
                if self._is_blacklisted(candidate):
                    continue
                if self._is_near_recent_startup_goal(candidate):
                    continue
                if not self._is_known_free_patch(
                    candidate,
                    self.latest_map,
                    required_radius=self.startup_known_free_radius,
                ):
                    continue
                if not self._has_local_clearance(candidate, self.latest_map):
                    continue

                ranked_goals.append((candidate, distance + penalty))

        if ranked_goals:
            self.get_logger().info(
                f'Using {len(ranked_goals)} short-range startup candidates before frontier expansion.'
            )

        ranked_goals.sort(key=lambda item: item[1])
        return ranked_goals[:self.candidate_goal_limit]

    def _find_frontier_cells(self, occupancy_grid: OccupancyGrid) -> List[GridPoint]:
        width = occupancy_grid.info.width
        height = occupancy_grid.info.height
        data = occupancy_grid.data
        frontier_cells: List[GridPoint] = []

        # frontier 的定义采用“自由单元格，且四邻域至少有一个未知单元格”。
        # 这样 Nav2 拿到的目标点仍落在自由区，更容易规划和到达。
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                idx = y * width + x
                value = data[idx]
                if not self._is_free(value):
                    continue

                neighbors = (
                    data[idx - 1],
                    data[idx + 1],
                    data[idx - width],
                    data[idx + width],
                )
                if any(n == -1 for n in neighbors):
                    frontier_cells.append((x, y))

        return frontier_cells

    def _cluster_frontiers(
        self,
        frontier_cells: Sequence[GridPoint],
    ) -> List[List[GridPoint]]:
        frontier_set = set(frontier_cells)
        visited = set()
        clusters: List[List[GridPoint]] = []

        # 通过 8 邻域 BFS 聚类，把零散 frontier 点合并成“可探索边界段”。
        for cell in frontier_cells:
            if cell in visited:
                continue

            queue: Deque[GridPoint] = deque([cell])
            visited.add(cell)
            cluster: List[GridPoint] = []

            while queue:
                current = queue.popleft()
                cluster.append(current)
                cx, cy = current
                for nx, ny in self._neighbors8(cx, cy):
                    if nx < 0 or ny < 0:
                        continue
                    if (nx, ny) not in frontier_set or (nx, ny) in visited:
                        continue
                    visited.add((nx, ny))
                    queue.append((nx, ny))

            if cluster:
                clusters.append(cluster)

        return clusters

    def _frontier_cluster_to_world_goal(
        self,
        cluster: Sequence[GridPoint],
        occupancy_grid: OccupancyGrid,
        robot_pose: Tuple[float, float, float],
    ) -> Optional[WorldPoint]:
        # 直接把 frontier 边界点交给 Nav2，容易遇到“目标还贴在未知边界上，
        # 对 planner 来说根本没有一块稳定可落脚的自由区域”的情况。
        # 这里不再只回退一次，而是沿着 frontier -> robot 的方向逐步往回试，
        # 直到找到真正位于已知自由区内部的候选点。
        centroid_x = sum(cell[0] for cell in cluster) / len(cluster)
        centroid_y = sum(cell[1] for cell in cluster) / len(cluster)
        best_cell = min(
            cluster,
            key=lambda cell: (cell[0] - centroid_x) ** 2 + (cell[1] - centroid_y) ** 2,
        )

        frontier_world = self._grid_to_world(best_cell[0], best_cell[1], occupancy_grid)
        dx = robot_pose[0] - frontier_world[0]
        dy = robot_pose[1] - frontier_world[1]
        distance = math.hypot(dx, dy)
        if distance < 1e-6:
            return frontier_world

        max_backoff = min(distance - 0.05, max(self.goal_backoff_distance, self.goal_known_free_radius))
        if max_backoff <= 0.0:
            return None

        backoff = max_backoff
        while backoff >= 0.0:
            candidate_world = (
                frontier_world[0] + dx / distance * backoff,
                frontier_world[1] + dy / distance * backoff,
            )
            if self._is_known_free_patch(candidate_world, occupancy_grid):
                return candidate_world
            backoff -= self.goal_backoff_step

        return None

    def _start_next_path_validation(self, robot_pose: Tuple[float, float, float]) -> None:
        if not self.candidate_goals:
            return

        candidate_world, score = self.candidate_goals.pop(0)
        self._path_validation_goal_xy = candidate_world
        self._path_validation_robot_pose = robot_pose
        self.path_check_pending = True
        self.current_goal_mode = self.candidate_goal_mode

        goal = ComputePathToPose.Goal()
        goal.goal = PoseStamped()
        goal.goal.header.frame_id = self.global_frame
        goal.goal.header.stamp = self.get_clock().now().to_msg()
        goal.goal.pose.position.x = candidate_world[0]
        goal.goal.pose.position.y = candidate_world[1]

        goal.start = PoseStamped()
        goal.start.header.frame_id = self.global_frame
        goal.start.header.stamp = goal.goal.header.stamp
        goal.start.pose.position.x = robot_pose[0]
        goal.start.pose.position.y = robot_pose[1]
        goal.start.pose.orientation = self._quaternion_from_yaw(robot_pose[2])

        goal_yaw = math.atan2(candidate_world[1] - robot_pose[1], candidate_world[0] - robot_pose[0])
        goal.goal.pose.orientation = self._quaternion_from_yaw(goal_yaw)
        goal.planner_id = 'GridBased'
        goal.use_start = True

        # 在真正导航前先让规划器对候选点“过一遍筛子”，能有效减少
        # 机器人在坏目标上长时间卡住做 recovery 的情况。
        self.get_logger().info(
            f'Validating frontier candidate ({candidate_world[0]:.2f}, {candidate_world[1]:.2f}) '
            f'with score {score:.2f}.'
        )

        future = self.compute_path_client.send_goal_async(goal)
        future.add_done_callback(self._path_validation_response_callback)

    def _path_validation_response_callback(self, future) -> None:
        goal_handle = future.result()
        if goal_handle is None or not goal_handle.accepted:
            self.path_check_pending = False
            self.get_logger().warn('Planner rejected frontier path validation request.')
            self._continue_candidate_validation()
            return

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._path_validation_result_callback)

    def _path_validation_result_callback(self, future) -> None:
        self.path_check_pending = False
        action_result = future.result()
        status = action_result.status
        result = action_result.result
        candidate = self._path_validation_goal_xy
        robot_pose = self._path_validation_robot_pose
        self._path_validation_goal_xy = None
        self._path_validation_robot_pose = None

        if candidate is None or robot_pose is None:
            self._continue_candidate_validation()
            return

        if status == GoalStatus.STATUS_SUCCEEDED and len(result.path.poses) >= self.path_validation_min_poses:
            goal_x, goal_y = candidate
            goal_yaw = math.atan2(goal_y - robot_pose[1], goal_x - robot_pose[0])
            self.get_logger().info(
                f'Frontier candidate ({goal_x:.2f}, {goal_y:.2f}) passed path validation.'
            )
            self.candidate_goals = []
            self.candidate_goal_mode = None
            self._send_navigation_goal(goal_x, goal_y, goal_yaw)
            return

        self.blacklisted_goals.append(candidate)
        self.get_logger().warn(
            f'Frontier candidate ({candidate[0]:.2f}, {candidate[1]:.2f}) '
            f'failed path validation with status {status}; trying next candidate.'
        )
        self._continue_candidate_validation()

    def _continue_candidate_validation(self) -> None:
        robot_pose = self._lookup_robot_pose()
        if robot_pose is None:
            self.candidate_goals = []
            return

        if self.candidate_goals:
            self._start_next_path_validation(robot_pose)
            return

        self.candidate_goal_mode = None
        self._no_frontier_logged = False
        self._no_frontier_cycles += 1
        self.get_logger().info('All current frontier candidates failed path validation.')
        if self._no_frontier_cycles >= self.no_frontier_cycles_before_spin:
            self._trigger_recovery_behavior()

    def _send_navigation_goal(self, goal_x: float, goal_y: float, goal_yaw: float) -> None:
        goal = NavigateToPose.Goal()
        goal.pose = PoseStamped()
        goal.pose.header.frame_id = self.global_frame
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x = goal_x
        goal.pose.pose.position.y = goal_y
        goal.pose.pose.orientation = self._quaternion_from_yaw(goal_yaw)

        self.goal_pending = True
        self.current_goal_xy = (goal_x, goal_y)
        self.get_logger().info(f'Sending exploration goal to ({goal_x:.2f}, {goal_y:.2f}).')

        future = self.navigate_client.send_goal_async(goal)
        future.add_done_callback(self._goal_response_callback)

    def _goal_response_callback(self, future) -> None:
        self.goal_pending = False
        goal_handle = future.result()
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().warn('Nav2 rejected the exploration goal.')
            self._blacklist_current_goal()
            self.current_goal_mode = None
            return

        self.goal_handle = goal_handle
        self.goal_active = True
        self.goal_sent_time = self.get_clock().now()

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._goal_result_callback)

    def _goal_result_callback(self, future) -> None:
        status = future.result().status
        goal_xy = self.current_goal_xy

        self.goal_active = False
        self.goal_handle = None
        self.goal_sent_time = None
        self.current_goal_xy = None

        if status == GoalStatus.STATUS_SUCCEEDED:
            if goal_xy is not None:
                if self.current_goal_mode == 'startup':
                    self._startup_goal_successes += 1
                    # 启动引导点只用一次，避免反复在同一个近点上“秒成功”。
                    self.blacklisted_goals.append(goal_xy)
                else:
                    self._successful_goals += 1
                self.get_logger().info(
                    f'Exploration goal reached at ({goal_xy[0]:.2f}, {goal_xy[1]:.2f}).'
                )
            self.current_goal_mode = None
            return

        if goal_xy is not None:
            self.blacklisted_goals.append(goal_xy)
            self.get_logger().warn(
                f'Exploration goal failed with status {status}; blacklisting that area.'
            )
        self.current_goal_mode = None

    def _trigger_spin_recovery(self) -> None:
        if not self.spin_client.server_is_ready():
            self.get_logger().info('Spin recovery requested, but Nav2 spin server is not ready yet.')
            return

        self._no_frontier_cycles = 0
        self.spin_pending = True
        self.get_logger().info(
            f'No frontier for {self.no_frontier_cycles_before_spin} cycles; '
            f'triggering spin recovery ({self.spin_recovery_angle:.2f} rad).'
        )

        goal = Spin.Goal()
        goal.target_yaw = self.spin_recovery_angle
        goal.time_allowance = Duration(seconds=self.spin_time_allowance_sec).to_msg()

        future = self.spin_client.send_goal_async(goal)
        future.add_done_callback(self._spin_response_callback)

    def _trigger_backup_recovery(self) -> None:
        if not self.backup_client.server_is_ready():
            self.get_logger().info('Backup recovery requested, but Nav2 backup server is not ready yet.')
            return

        self._no_frontier_cycles = 0
        self.backup_pending = True
        self.get_logger().info(
            f'Planner still cannot produce a movable goal; '
            f'triggering backup recovery ({self.backup_recovery_distance:.2f} m).'
        )

        goal = BackUp.Goal()
        goal.target.x = -abs(self.backup_recovery_distance)
        goal.target.y = 0.0
        goal.speed = self.backup_recovery_speed
        goal.time_allowance = Duration(seconds=self.backup_time_allowance_sec).to_msg()

        future = self.backup_client.send_goal_async(goal)
        future.add_done_callback(self._backup_response_callback)

    def _trigger_recovery_behavior(self) -> None:
        # 优先尝试 backup，让机器人产生实际平移；若刚做过 backup，
        # 再交给 spin 扩展视野，避免永远重复同一种恢复动作。
        if self._last_recovery_mode != 'backup':
            self._trigger_backup_recovery()
            return
        self._trigger_spin_recovery()

    def _backup_response_callback(self, future) -> None:
        self.backup_pending = False
        goal_handle = future.result()
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().warn('Backup recovery goal was rejected by Nav2.')
            self._last_recovery_mode = 'backup_rejected'
            return

        self.backup_active = True
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._backup_result_callback)

    def _backup_result_callback(self, future) -> None:
        self.backup_active = False
        status = future.result().status
        self._last_recovery_mode = 'backup'
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Backup recovery completed; frontier search will resume.')
            return

        self.get_logger().warn(
            f'Backup recovery finished with status {status}; falling back to spin if needed.'
        )

    def _spin_response_callback(self, future) -> None:
        self.spin_pending = False
        goal_handle = future.result()
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().warn('Spin recovery goal was rejected by Nav2.')
            return

        self.spin_active = True
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._spin_result_callback)

    def _spin_result_callback(self, future) -> None:
        self.spin_active = False
        status = future.result().status
        self._last_recovery_mode = 'spin'
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Spin recovery completed; frontier search will resume.')
            return

        self.get_logger().warn(
            f'Spin recovery finished with status {status}; frontier search will continue anyway.'
        )

    def _check_goal_timeout(self) -> None:
        if self.goal_sent_time is None or self.goal_handle is None:
            return

        elapsed = (self.get_clock().now() - self.goal_sent_time).nanoseconds / 1e9
        if elapsed < self.goal_timeout_sec:
            return

        self.get_logger().warn('Exploration goal timed out; canceling and blacklisting it.')
        self.goal_handle.cancel_goal_async()
        self._blacklist_current_goal()
        self.goal_active = False
        self.goal_handle = None
        self.goal_sent_time = None
        self.current_goal_xy = None
        self.current_goal_mode = None

    def _blacklist_current_goal(self) -> None:
        if self.current_goal_xy is not None:
            self.blacklisted_goals.append(self.current_goal_xy)

    def _is_blacklisted(self, point: WorldPoint) -> bool:
        return any(
            math.hypot(point[0] - bad[0], point[1] - bad[1]) < self.blacklist_radius
            for bad in self.blacklisted_goals
        )

    def _is_near_recent_startup_goal(self, point: WorldPoint) -> bool:
        return any(
            math.hypot(point[0] - used[0], point[1] - used[1]) < self.startup_goal_reuse_radius
            for used in self.blacklisted_goals
        )

    def _is_free(self, occupancy_value: int) -> bool:
        return 0 <= occupancy_value < self.occupied_threshold

    def _has_local_clearance(
        self,
        candidate_world: WorldPoint,
        occupancy_grid: OccupancyGrid,
    ) -> bool:
        center = self._world_to_grid(candidate_world[0], candidate_world[1], occupancy_grid)
        if center is None:
            return False

        radius_cells = max(1, int(self.candidate_clearance_radius / occupancy_grid.info.resolution))
        width = occupancy_grid.info.width
        height = occupancy_grid.info.height
        cx, cy = center

        # 目标点附近如果明显贴着已知障碍物，很容易出现“规划勉强通过，
        # 但 controller 贴障碍发呆或不断触发 recovery”的现象。
        # 这里故意只把“已知占用栅格”视为失败，不把 unknown 视为失败：
        # frontier 本来就天然贴着未知边界，若把 unknown 也拦掉，启动后只会原地转圈。
        for dy in range(-radius_cells, radius_cells + 1):
            for dx in range(-radius_cells, radius_cells + 1):
                if dx * dx + dy * dy > radius_cells * radius_cells:
                    continue
                gx = cx + dx
                gy = cy + dy
                if not (0 <= gx < width and 0 <= gy < height):
                    continue
                idx = gy * width + gx
                cell_value = occupancy_grid.data[idx]
                if cell_value >= self.occupied_threshold:
                    return False

        return True

    def _is_known_free_patch(
        self,
        candidate_world: WorldPoint,
        occupancy_grid: OccupancyGrid,
        required_radius: Optional[float] = None,
    ) -> bool:
        center = self._world_to_grid(candidate_world[0], candidate_world[1], occupancy_grid)
        if center is None:
            return False

        patch_radius = self.goal_known_free_radius if required_radius is None else required_radius
        radius_cells = max(1, int(patch_radius / occupancy_grid.info.resolution))
        width = occupancy_grid.info.width
        height = occupancy_grid.info.height
        cx, cy = center

        # 这里比 _has_local_clearance 更严格：不仅不能撞已知障碍，
        # 还要求目标点周围有一小块“确定已知的 free 区域”，
        # 避免把 Nav2 目标落在 frontier 边缘那条窄窄的未知边界上。
        for dy in range(-radius_cells, radius_cells + 1):
            for dx in range(-radius_cells, radius_cells + 1):
                if dx * dx + dy * dy > radius_cells * radius_cells:
                    continue
                gx = cx + dx
                gy = cy + dy
                if not (0 <= gx < width and 0 <= gy < height):
                    return False
                idx = gy * width + gx
                if not self._is_free(occupancy_grid.data[idx]):
                    return False

        return self._has_local_clearance(candidate_world, occupancy_grid)

    def _grid_to_world(
        self,
        grid_x: int,
        grid_y: int,
        occupancy_grid: OccupancyGrid,
    ) -> WorldPoint:
        origin = occupancy_grid.info.origin.position
        resolution = occupancy_grid.info.resolution
        world_x = origin.x + (grid_x + 0.5) * resolution
        world_y = origin.y + (grid_y + 0.5) * resolution
        return (world_x, world_y)

    def _world_to_grid(
        self,
        world_x: float,
        world_y: float,
        occupancy_grid: OccupancyGrid,
    ) -> Optional[GridPoint]:
        origin = occupancy_grid.info.origin.position
        resolution = occupancy_grid.info.resolution
        grid_x = int((world_x - origin.x) / resolution)
        grid_y = int((world_y - origin.y) / resolution)
        if not (0 <= grid_x < occupancy_grid.info.width and 0 <= grid_y < occupancy_grid.info.height):
            return None
        return (grid_x, grid_y)

    def _neighbors8(self, x: int, y: int) -> Sequence[GridPoint]:
        return (
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y),                 (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
        )

    def _quaternion_from_yaw(self, yaw: float) -> Quaternion:
        q = Quaternion()
        q.z = math.sin(yaw / 2.0)
        q.w = math.cos(yaw / 2.0)
        return q

    def _yaw_from_quaternion(self, x: float, y: float, z: float, w: float) -> float:
        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
        return math.atan2(siny_cosp, cosy_cosp)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = FrontierExplorer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        # launch 在收到 SIGINT 时可能已经帮我们关闭了 context；
        # 这里先判断，再避免重复 shutdown 导致异常栈输出。
        if rclpy.ok():
            rclpy.shutdown()
