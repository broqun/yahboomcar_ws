import math
from collections import deque
from typing import Deque, List, Optional, Sequence, Tuple

from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped, Quaternion
from nav2_msgs.action import NavigateToPose
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

        # use_sim_time 由 launch 作为参数覆写直接传入，ROS 2 在某些情况下
        # 会提前声明它；这里不再重复 declare，避免节点启动时抛出
        # ParameterAlreadyDeclaredException。
        #
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

        self.latest_map: Optional[OccupancyGrid] = None
        self.goal_active = False
        self.goal_pending = False
        self.goal_handle = None
        self.goal_sent_time = None
        self.current_goal_xy: Optional[WorldPoint] = None
        self.blacklisted_goals: List[WorldPoint] = []
        self._map_received_once = False
        self._server_wait_logged = False
        self._no_frontier_logged = False

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.navigate_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

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

        self._server_wait_logged = False

        if self.goal_pending:
            return

        if self.goal_active:
            self._check_goal_timeout()
            return

        robot_pose = self._lookup_robot_pose()
        if robot_pose is None:
            return

        best_goal = self._select_best_frontier(robot_pose)
        if best_goal is None:
            if not self._no_frontier_logged:
                self._no_frontier_logged = True
                self.get_logger().info('No valid frontier found yet; waiting for map growth.')
            return

        self._no_frontier_logged = False
        goal_x, goal_y = best_goal
        goal_yaw = math.atan2(goal_y - robot_pose[1], goal_x - robot_pose[0])
        self._send_navigation_goal(goal_x, goal_y, goal_yaw)

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

    def _select_best_frontier(self, robot_pose: Tuple[float, float, float]) -> Optional[WorldPoint]:
        assert self.latest_map is not None

        frontier_cells = self._find_frontier_cells(self.latest_map)
        if not frontier_cells:
            return None

        frontier_clusters = self._cluster_frontiers(frontier_cells)
        best_goal = None
        best_score = float('inf')

        for cluster in frontier_clusters:
            if len(cluster) < self.min_frontier_size:
                continue

            candidate = self._frontier_cluster_to_world_goal(cluster, self.latest_map)
            if candidate is None:
                continue

            if self._is_blacklisted(candidate):
                continue

            distance = math.hypot(candidate[0] - robot_pose[0], candidate[1] - robot_pose[1])
            # 太靠近机器人本体的 frontier 没有导航意义，直接跳过。
            if distance < self.goal_reached_radius:
                continue
            # 分数越低越优先：离机器人更近、同时 frontier 规模更大。
            score = distance - len(cluster) * self.frontier_size_weight
            if score < best_score:
                best_score = score
                best_goal = candidate

        return best_goal

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
    ) -> Optional[WorldPoint]:
        # 用 cluster 质心近似代表这段 frontier，再选一个最接近质心的自由点作为导航目标。
        centroid_x = sum(cell[0] for cell in cluster) / len(cluster)
        centroid_y = sum(cell[1] for cell in cluster) / len(cluster)
        best_cell = min(
            cluster,
            key=lambda cell: (cell[0] - centroid_x) ** 2 + (cell[1] - centroid_y) ** 2,
        )
        return self._grid_to_world(best_cell[0], best_cell[1], occupancy_grid)

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
                self.get_logger().info(
                    f'Exploration goal reached at ({goal_xy[0]:.2f}, {goal_xy[1]:.2f}).'
                )
            return

        if goal_xy is not None:
            self.blacklisted_goals.append(goal_xy)
            self.get_logger().warn(
                f'Exploration goal failed with status {status}; blacklisting that area.'
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

    def _blacklist_current_goal(self) -> None:
        if self.current_goal_xy is not None:
            self.blacklisted_goals.append(self.current_goal_xy)

    def _is_blacklisted(self, point: WorldPoint) -> bool:
        return any(
            math.hypot(point[0] - bad[0], point[1] - bad[1]) < self.blacklist_radius
            for bad in self.blacklisted_goals
        )

    def _is_free(self, occupancy_value: int) -> bool:
        return 0 <= occupancy_value < self.occupied_threshold

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
        rclpy.shutdown()
