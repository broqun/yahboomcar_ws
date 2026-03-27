import math
from collections import deque
from typing import Deque, Dict, List, Optional, Sequence, Tuple

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
import numpy as np
import cv2
from skimage.morphology import skeletonize


GridPoint = Tuple[int, int]
WorldPoint = Tuple[float, float]
RegionKey = Tuple[int, int]
PoseSample = Tuple[float, float, float]
CandidateGoal = Tuple[WorldPoint, float, RegionKey]


class FrontierExplorer(Node):
    """Explore the unknown map by repeatedly sending Nav2 frontier goals."""

    def __init__(self) -> None:
        super().__init__('frontier_explorer')

        # 下面这些参数则完全由 frontier_explorer 自己定义和消费。
        # 它们先覆盖“最小可用探索”场景：地图来自 slam_toolbox，
        # 控制由 Nav2 完成，frontier 节点只负责挑选目标点。
        self.declare_parameter('map_topic', '/map')  # 订阅地图话题（通常由 slam_toolbox 发布）。
        self.declare_parameter('global_frame', 'map')  # 全局参考坐标系；需与 Nav2 全局帧一致。
        self.declare_parameter('base_frame', 'base_footprint')  # 机器人本体坐标系；TF 查询位姿用。
        self.declare_parameter('planning_period_sec', 2.0)  # 主循环周期；越小重规划越快但 CPU 更高。
        self.declare_parameter('goal_timeout_sec', 90.0)  # 单个导航目标总超时；超过后触发逃逸恢复。
        self.declare_parameter('min_frontier_size', 8)  # 常态下 frontier 最小簇大小阈值（当前骨架算法弱化使用）。
        self.declare_parameter('occupied_threshold', 50)  # 占用阈值：>=该值视为障碍；影响 free/occupied 判定。
        self.declare_parameter('frontier_size_weight', 0.00)  # frontier 规模评分权重（当前评分逻辑已基本停用）。
        self.declare_parameter('frontier_size_score_cap', 30)  # frontier 规模奖励上限（与上项配套，当前弱化）。
        self.declare_parameter('blacklist_radius', 1.10)  # 黑名单半径：失败点附近该半径内目标会被跳过。
        self.declare_parameter('goal_reached_radius', 0.60)  # 候选点若离机器人过近（<该值）视为无意义目标。
        self.declare_parameter('startup_min_frontier_size', 3)  # 启动期最小 frontier 阈值；与 min_frontier_size 联动。
        self.declare_parameter('goal_backoff_distance', 0.35)  # 从 frontier 边界向机器人方向回退的最大尝试距离。
        self.declare_parameter('no_frontier_cycles_before_spin', 3)  # 连续无候选循环次数阈值，达到后触发恢复。
        self.declare_parameter('spin_recovery_angle', 1.57)  # 常规 spin 恢复旋转角（rad）。
        self.declare_parameter('spin_time_allowance_sec', 20.0)  # spin 行为最大允许执行时长。
        self.declare_parameter('backup_recovery_distance', 0.60)  # 常规 backup 恢复后退距离（m）。
        self.declare_parameter('backup_recovery_speed', 0.14)  # 常规 backup 后退速度（m/s）。
        self.declare_parameter('backup_time_allowance_sec', 8.0)  # backup 行为最大允许执行时长。
        self.declare_parameter('escape_backup_distance', 0.90)  # 卡住时更激进的逃逸后退距离。
        self.declare_parameter('escape_backup_speed', 0.15)  # 卡住时逃逸后退速度。
        self.declare_parameter('escape_spin_angle', 1.05)  # 逃逸 backup 后追加短 spin 的角度。
        self.declare_parameter('candidate_goal_limit', 20)  # 每轮保留的候选目标上限（排序后截断）。
        self.declare_parameter('candidate_clearance_radius', 0.26)  # 候选点局部净空半径（仅对已知障碍做碰撞过滤）。
        self.declare_parameter('path_pose_clearance_radius', 0.20)  # 路径质量检查时，路径采样点净空检查半径。
        self.declare_parameter('path_quality_check_distance', 1.4)  # 仅检查路径前段这么长的距离，关注“起步是否顺畅”。
        self.declare_parameter('path_min_clearance_pass_ratio', 0.50)  # 前段路径净空通过率下限；低于则拒绝该目标。
        self.declare_parameter('path_max_length_ratio', 4.2)  # 路径长度/直线距离上限；过绕路视为不优。
        self.declare_parameter('goal_known_free_radius', 0.20)  # 目标点“已知自由补丁”半径，要求比纯净空更严格。
        self.declare_parameter('goal_backoff_step', 0.10)  # frontier 回退搜索步长；越小越细致但计算更慢。
        self.declare_parameter('startup_known_free_radius', 0.10)  # 启动过渡点所需已知自由半径（通常小于常规目标）。
        self.declare_parameter('startup_goal_min_distance', 0.80)  # 启动过渡点最小距离；避免挑到脚边点。
        self.declare_parameter('startup_goal_reuse_radius', 0.35)  # 启动阶段避免重复使用近邻目标的去重半径。
        self.declare_parameter('startup_goal_success_limit', 12)  # 启动成功计数上限（当前主要用于统计/状态追踪）。
        self.declare_parameter('goal_progress_radius', 0.12)  # 判定“有位移进展”的最小位移阈值。
        self.declare_parameter('goal_stall_timeout_sec', 7.0)  # 超过该时长无位移进展则判定卡住。
        self.declare_parameter('goal_approach_improvement_radius', 0.35)  # 判定“更接近目标”的最小改善量。
        self.declare_parameter('goal_approach_timeout_sec', 12.0)  # 长时间不更接近目标则触发逃逸恢复。
        self.declare_parameter('path_validation_min_poses', 2)  # 预检路径最少姿态点数量；太短视为无效验证。
        self.declare_parameter('path_validation_rejection_limit', 8)  # 连续预检被拒阈值；达到后暂时绕过预检。
        self.declare_parameter('path_validation_disable_sec', 45.0)  # 预检临时禁用时长（防止一直卡在 compute_path）。
        self.declare_parameter('region_cell_size', 1.5)  # 区域划分网格边长（m）；用于区域级失败记忆与冷却。
        self.declare_parameter('region_fail_limit', 2)  # 单区域连续失败阈值；达到后该区域进入 cooldown。
        self.declare_parameter('region_fail_penalty', 3.0)  # 区域失败惩罚分（加到候选 score）。
        self.declare_parameter('region_novelty_bonus', 2.0)  # 长时间未访问区域奖励（从 score 中减去）。    
        self.declare_parameter('region_recent_visit_penalty', 3.0)  # 近期访问区域惩罚（抑制反复原地徘徊）。
        self.declare_parameter('region_recent_visit_window_sec', 180.0)  # 判定“近期访问”的时间窗。
        self.declare_parameter('region_cooldown_sec', 30.0)  # 区域冷却时长；冷却中区域不再选目标。
        self.declare_parameter('wander_detect_window_sec', 60.0)  # 漫游检测窗口时长（看是否长期困在小范围）。
        self.declare_parameter('wander_radius', 3.5)  # 漫游半径阈值；窗口内轨迹都在此半径内则判定徘徊。
        self.declare_parameter('wander_region_cooldown_sec', 180.0)  # 触发漫游干预后，对附近区域施加冷却时长。
        self.declare_parameter('wander_trigger_cooldown_sec', 45.0)  # 两次漫游干预的最小间隔，避免频繁触发。
        # 距离惩罚权重降低，让机器人更愿意去远处的走廊。
        self.declare_parameter('frontier_distance_pivot_m', 2.0)  # 距离奖励起算点；超过该距离才给“远距离探索奖励”。
        self.declare_parameter('frontier_distance_bonus_per_m', 0.5)  # 每超出 1m 给多少分奖励（从 score 中扣减）。
        self.declare_parameter('frontier_distance_bonus_cap', 15.0)  # 距离奖励上限，避免远点长期垄断候选榜。
        # 方位扇区轮换：近期已选方向会加惩罚分，促使目标在水平面上散开。
        self.declare_parameter('explore_sector_count', 8)  # 方位扇区数量；把平面方向离散成 N 个区间。
        self.declare_parameter('explore_sector_repeat_penalty', 2.2)  # 最近选过同扇区时附加惩罚，促进方向分散。
        self.declare_parameter('explore_sector_memory_sec', 100.0)  # 扇区“已访问”记忆窗口。
        # 单段导航最远距离：大图里一次跳到十几米外，在 SLAM 图上经常与当前位置不连通，
        # Navfn 反复失败；裁成多段短跳更接近扫地机式“小步探索”。
        self.declare_parameter('max_navigation_goal_distance_m', 7.0)  # 单次目标最远距离；把长跳切成更稳定的短跳。
        self.declare_parameter('goal_ray_refine_iterations', 14)  # 沿射线二分细化迭代次数；影响可行点定位精度。

        # 关键参数联动说明：
        # 1) goal_known_free_radius / candidate_clearance_radius / occupied_threshold：
        #    三者共同决定“候选点是否可落脚且不贴障碍”，阈值越保守成功率高但可选点更少。
        # 2) goal_progress_radius + goal_stall_timeout_sec + goal_approach_timeout_sec：
        #    共同定义“卡住”判据，过严会频繁误触发逃逸，过松会长时间原地耗时。
        # 3) region_fail_limit / region_fail_penalty / region_cooldown_sec：
        #    共同实现区域级避坑记忆，抑制在坏区域反复尝试。
        # 4) frontier_distance_* + explore_sector_*：
        #    前者鼓励去更远处，后者鼓励方向分散，二者平衡“覆盖速度”和“空间均匀性”。
        # 5) max_navigation_goal_distance_m + goal_ray_refine_iterations + goal_reached_radius：
        #    共同影响“短跳策略”稳定性；距离上限过小会产生过多碎步，过大则回到远跳失败风险。

        self.map_topic = self.get_parameter('map_topic').value
        self.global_frame = self.get_parameter('global_frame').value
        self.base_frame = self.get_parameter('base_frame').value
        self.planning_period_sec = float(
            self.get_parameter('planning_period_sec').value)
        self.goal_timeout_sec = float(
            self.get_parameter('goal_timeout_sec').value)
        self.min_frontier_size = int(
            self.get_parameter('min_frontier_size').value)
        self.occupied_threshold = int(
            self.get_parameter('occupied_threshold').value)
        self.frontier_size_weight = float(
            self.get_parameter('frontier_size_weight').value)
        self.frontier_size_score_cap = int(
            self.get_parameter('frontier_size_score_cap').value
        )
        self.blacklist_radius = float(
            self.get_parameter('blacklist_radius').value)
        self.goal_reached_radius = float(
            self.get_parameter('goal_reached_radius').value)
        self.startup_min_frontier_size = int(
            self.get_parameter('startup_min_frontier_size').value)
        self.goal_backoff_distance = float(
            self.get_parameter('goal_backoff_distance').value)
        self.no_frontier_cycles_before_spin = int(
            self.get_parameter('no_frontier_cycles_before_spin').value
        )
        self.spin_recovery_angle = float(
            self.get_parameter('spin_recovery_angle').value)
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
        self.escape_backup_distance = float(
            self.get_parameter('escape_backup_distance').value
        )
        self.escape_backup_speed = float(
            self.get_parameter('escape_backup_speed').value
        )
        self.escape_spin_angle = float(
            self.get_parameter('escape_spin_angle').value)
        self.candidate_goal_limit = int(
            self.get_parameter('candidate_goal_limit').value)
        self.candidate_clearance_radius = float(
            self.get_parameter('candidate_clearance_radius').value
        )
        self.path_pose_clearance_radius = float(
            self.get_parameter('path_pose_clearance_radius').value
        )
        self.path_quality_check_distance = float(
            self.get_parameter('path_quality_check_distance').value
        )
        self.path_min_clearance_pass_ratio = float(
            self.get_parameter('path_min_clearance_pass_ratio').value
        )
        self.path_max_length_ratio = float(
            self.get_parameter('path_max_length_ratio').value
        )
        self.goal_known_free_radius = float(
            self.get_parameter('goal_known_free_radius').value
        )
        self.goal_backoff_step = float(
            self.get_parameter('goal_backoff_step').value)
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
        self.goal_progress_radius = float(
            self.get_parameter('goal_progress_radius').value)
        self.goal_stall_timeout_sec = float(
            self.get_parameter('goal_stall_timeout_sec').value
        )
        self.goal_approach_improvement_radius = float(
            self.get_parameter('goal_approach_improvement_radius').value
        )
        self.goal_approach_timeout_sec = float(
            self.get_parameter('goal_approach_timeout_sec').value
        )
        self.path_validation_min_poses = int(
            self.get_parameter('path_validation_min_poses').value
        )
        self.path_validation_rejection_limit = int(
            self.get_parameter('path_validation_rejection_limit').value
        )
        self.path_validation_disable_sec = float(
            self.get_parameter('path_validation_disable_sec').value
        )
        self.region_cell_size = float(
            self.get_parameter('region_cell_size').value)
        self.region_fail_limit = int(
            self.get_parameter('region_fail_limit').value)
        self.region_fail_penalty = float(
            self.get_parameter('region_fail_penalty').value)
        self.region_novelty_bonus = float(
            self.get_parameter('region_novelty_bonus').value)
        self.region_recent_visit_penalty = float(
            self.get_parameter('region_recent_visit_penalty').value
        )
        self.region_recent_visit_window_sec = float(
            self.get_parameter('region_recent_visit_window_sec').value
        )
        self.region_cooldown_sec = float(
            self.get_parameter('region_cooldown_sec').value)
        self.wander_detect_window_sec = float(
            self.get_parameter('wander_detect_window_sec').value
        )
        self.wander_radius = float(self.get_parameter('wander_radius').value)
        self.wander_region_cooldown_sec = float(
            self.get_parameter('wander_region_cooldown_sec').value
        )
        self.wander_trigger_cooldown_sec = float(
            self.get_parameter('wander_trigger_cooldown_sec').value
        )
        self.frontier_distance_pivot_m = float(
            self.get_parameter('frontier_distance_pivot_m').value
        )
        self.frontier_distance_bonus_per_m = float(
            self.get_parameter('frontier_distance_bonus_per_m').value
        )
        self.frontier_distance_bonus_cap = float(
            self.get_parameter('frontier_distance_bonus_cap').value
        )
        self.explore_sector_count = int(
            self.get_parameter('explore_sector_count').value)
        self.explore_sector_repeat_penalty = float(
            self.get_parameter('explore_sector_repeat_penalty').value
        )
        self.explore_sector_memory_sec = float(
            self.get_parameter('explore_sector_memory_sec').value
        )
        self.max_navigation_goal_distance_m = float(
            self.get_parameter('max_navigation_goal_distance_m').value
        )
        self.goal_ray_refine_iterations = int(
            self.get_parameter('goal_ray_refine_iterations').value
        )

        self.latest_map: Optional[OccupancyGrid] = None
        self.goal_active = False
        self.goal_pending = False
        self.path_check_pending = False
        self.goal_handle = None
        self.goal_sent_time = None
        self.current_goal_xy: Optional[WorldPoint] = None
        self.current_goal_region: Optional[RegionKey] = None
        self.current_goal_mode: Optional[str] = None
        self.candidate_goal_mode: Optional[str] = None
        self.goal_last_progress_time = None
        self.goal_last_progress_xy: Optional[WorldPoint] = None
        self.goal_best_distance_to_target: Optional[float] = None
        self.goal_last_target_progress_time = None
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
        self._backup_distance_override: Optional[float] = None
        self._backup_speed_override: Optional[float] = None
        self._backup_log_message: Optional[str] = None
        self._spin_angle_override: Optional[float] = None
        self._spin_log_message: Optional[str] = None
        self._escape_spin_after_backup = False
        self.candidate_goals: List[CandidateGoal] = []
        self._path_validation_goal_xy: Optional[WorldPoint] = None
        self._path_validation_goal_region: Optional[RegionKey] = None
        self._path_validation_robot_pose: Optional[Tuple[float,
                                                         float, float]] = None
        self._consecutive_path_validation_rejections = 0
        self._path_validation_disabled_until = 0.0
        self._startup_goal_successes = 0
        self._last_recovery_mode: Optional[str] = None
        self._pose_history: Deque[PoseSample] = deque(maxlen=240)
        self._region_fail_counts: Dict[RegionKey, int] = {}
        self._region_cooldown_until: Dict[RegionKey, float] = {}
        self._region_last_selected_at: Dict[RegionKey, float] = {}
        self._region_last_reached_at: Dict[RegionKey, float] = {}
        self._last_wander_intervention_at = -1e9
        self._explore_sector_history: Deque[Tuple[float, int]] = deque(
            maxlen=64)
        self._goal_token_counter = 0
        self._active_goal_token: Optional[int] = None
        self._pending_goal_token: Optional[int] = None

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.navigate_client = ActionClient(
            self, NavigateToPose, 'navigate_to_pose')
        # 在真正把目标交给 NavigateToPose 之前，先调用 planner 做一次路径预检查，
        # 避免“前方近障碍、目标点看起来不错但实际上根本规划不过去”的情况。
        self.compute_path_client = ActionClient(
            self, ComputePathToPose, 'compute_path_to_pose')
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
        self.plan_timer = self.create_timer(
            self.planning_period_sec, self._planning_timer_cb)

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

        if not self._is_path_validation_temporarily_disabled() and not self.compute_path_client.server_is_ready():
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
        self._record_robot_pose(robot_pose)

        if self._should_trigger_wander_escape():
            self._apply_wander_cooldown(robot_pose)

        if self.candidate_goals:
            self._start_next_path_validation(robot_pose)
            return

        candidate_goals = self._rank_frontier_candidates(robot_pose)
        if not candidate_goals:
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
    ) -> List[CandidateGoal]:
        assert self.latest_map is not None

        frontier_cells = self._find_frontier_cells(self.latest_map)
        if not frontier_cells:
            return []

        frontier_clusters = self._cluster_frontiers(frontier_cells)
        ranked_by_region: Dict[RegionKey, CandidateGoal] = {}
        self._purge_explore_sector_history()
        # 首个探索目标通常最难出现，因此在“还没有任何成功导航”之前，
        # 放宽 frontier 最小规模阈值，优先打破启动僵局。
        effective_min_frontier_size = (
            self.min_frontier_size
            if self._successful_goals > 0
            else min(self.min_frontier_size, self.startup_min_frontier_size)
        )

        for cluster in frontier_clusters:
            # == 架构师的终极一刀：拔除旧时代体积安检门 ==
            # Voronoi 找出的端点永远只有 1 个像素，绝对不能用 8 像素去卡它！
            # if len(cluster) < effective_min_frontier_size:
            #     continue
            # ==========================================

            candidate = self._frontier_cluster_to_world_goal(
                cluster, self.latest_map, robot_pose)
            if candidate is None:
                continue

            if self._is_blacklisted(candidate):
                continue

            # 候选目标除了“点本身是 free”，还要求周围不要明显贴着已知障碍物。
            # 注意这里不能把“靠近未知区域”也当成失败条件，否则启动阶段那一小圈
            # frontier 会被全部过滤掉，机器人就只会反复 spin 而不出发。
            if not self._has_local_clearance(candidate, self.latest_map):
                continue

            distance = math.hypot(
                candidate[0] - robot_pose[0], candidate[1] - robot_pose[1])
            # 太靠近机器人本体的 frontier 没有导航意义，直接跳过。
            if distance < self.goal_reached_radius:
                continue
            region_key = self._point_to_region_key(candidate)
            if self._is_region_on_cooldown(region_key):
                continue
            # 分数越低越优先：离机器人更近、同时 frontier 规模更大。
            # cluster 奖励要设上限，否则超大 frontier 会把分数压成离谱负值，
            # 导致远处但并不“好走”的目标长期霸榜。

            # ================ 架构师植入：方向惯性 ================
            angle_to_candidate = math.atan2(candidate[1] - robot_pose[1], candidate[0] - robot_pose[0])
            angle_diff = abs(angle_to_candidate - robot_pose[2])
            if angle_diff > math.pi:
                angle_diff = 2.0 * math.pi - angle_diff
            
            heading_penalty = angle_diff * 2.5 
            # ======================================================

            # 直接计算总分：只看距离和方向转角惩罚！
            # 删掉所有关于 cluster_score 和 frontier_size_weight 的计算！
            score = distance + heading_penalty
            
            score -= self._frontier_distance_score_bonus(distance)
            score += self._explore_sector_repeat_penalty(robot_pose, candidate)
            score = self._apply_region_score_adjustments(score, region_key)

            existing = ranked_by_region.get(region_key)
            candidate_entry = (candidate, score, region_key)
            if existing is None or score < existing[1]:
                ranked_by_region[region_key] = candidate_entry

        ranked_goals = list(ranked_by_region.values())
        ranked_goals.sort(key=lambda item: item[1])
        return ranked_goals[:self.candidate_goal_limit]

    def _rank_startup_candidates(
        self,
        robot_pose: Tuple[float, float, float],
    ) -> List[CandidateGoal]:
        assert self.latest_map is not None

        ranked_by_region: Dict[RegionKey, CandidateGoal] = {}
        # 当 frontier 候选为空/不可执行时，先走一跳“过渡点”离开局部死角，
        # 特别是门口、房间角落等易反复触发 recovery 的区域。
        direction_offsets = (
            (0.0, 0.0),
            (math.pi / 6.0, 0.08),
            (-math.pi / 6.0, 0.08),
            (math.pi / 3.0, 0.16),
            (-math.pi / 3.0, 0.16),
            (math.pi / 2.0, 0.28),
            (-math.pi / 2.0, 0.28),
            (math.pi, 0.45),
        )
        distances = (0.80, 1.20, 1.80, 2.40)

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
                if not self._has_local_clearance(
                    candidate,
                    self.latest_map,
                    required_radius=max(
                        0.16, self.candidate_clearance_radius - 0.05),
                ):
                    continue
                region_key = self._point_to_region_key(candidate)
                if self._is_region_on_cooldown(region_key):
                    continue
                score = self._apply_region_score_adjustments(
                    distance + penalty, region_key)
                existing = ranked_by_region.get(region_key)
                candidate_entry = (candidate, score, region_key)
                if existing is None or score < existing[1]:
                    ranked_by_region[region_key] = candidate_entry

        ranked_goals = list(ranked_by_region.values())
        if ranked_goals:
            self.get_logger().info(
                f'Using {len(ranked_goals)} startup/escape transit candidates before frontier expansion.'
            )

        ranked_goals.sort(key=lambda item: item[1])
        return ranked_goals[:self.candidate_goal_limit]

    # def _find_frontier_cells(self, occupancy_grid: OccupancyGrid) -> List[GridPoint]:
    #     # width = occupancy_grid.info.width
    #     # height = occupancy_grid.info.height
    #     # data = occupancy_grid.data
    #     # frontier_cells: List[GridPoint] = []

    #     # # frontier 的定义采用“自由单元格，且四邻域至少有一个未知单元格”。
    #     # # 这样 Nav2 拿到的目标点仍落在自由区，更容易规划和到达。
    #     # for y in range(1, height - 1):
    #     #     for x in range(1, width - 1):
    #     #         idx = y * width + x
    #     #         value = data[idx]
    #     #         if not self._is_free(value):
    #     #             continue

    #     #         neighbors = (
    #     #             data[idx - 1],
    #     #             data[idx + 1],
    #     #             data[idx - width],
    #     #             data[idx + width],
    #     #         )
    #     #         if any(n == -1 for n in neighbors):
    #     #             frontier_cells.append((x, y))

    #     # return frontier_cells

    #     width = occupancy_grid.info.width
    #     height = occupancy_grid.info.height
        
    #     data = np.array(occupancy_grid.data, dtype=np.int8).reshape((height, width))

    #     free_space = ((data >= 0) & (data < self.occupied_threshold)).astype(np.uint8)

    #     kernel = np.ones((3, 3), np.uint8)
    #     eroded_free = cv2.erode(free_space, kernel, iterations=1)

    #     skeleton = skeletonize(eroded_free).astype(np.uint8)
    #     frontier_cells: List[GridPoint] = []

    #     skel_y, skel_x = np.where(skeleton == 1)

    #     for y, x in zip(skel_y, skel_x):
    #         if x <= 2 or x >= width - 3 or y <= 2 or y <= height - 3:
    #             continue

    #         neighbors_sum = np.sum(skeleton[y-1:y+2, x-1:x+2])

    #         if neighbors_sum == 2:
    #             local_patch = data[y-4:y+5, x-4:x+5]
    #             if np.any(local_patch == -1):
    #                 frontier_cells.append((int(x), int(y)))

    #     return frontier_cells

    def _find_frontier_cells(self, occupancy_grid: OccupancyGrid) -> List[GridPoint]:
        width = occupancy_grid.info.width
        height = occupancy_grid.info.height
        data = np.array(occupancy_grid.data, dtype=np.int8).reshape((height, width))

        # 1. 提取 Free Space
        free_space = ((data >= 0) & (data < self.occupied_threshold)).astype(np.uint8)

        # 2. 架构师核武器：重型形态学滤波 (依赖 i9 超强单核)
        # 闭运算：无视大厅里的椅子腿和微小障碍物（填补内部黑洞）
        # 开运算：削掉墙壁边缘的锯齿和毛刺，防止骨架分叉
        morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        smoothed_free = cv2.morphologyEx(free_space, cv2.MORPH_CLOSE, morph_kernel)
        smoothed_free = cv2.morphologyEx(smoothed_free, cv2.MORPH_OPEN, morph_kernel)

        # 3. 腐蚀边界，让小车保持在走廊中心
        erode_kernel = np.ones((3, 3), np.uint8)
        eroded_free = cv2.erode(smoothed_free, erode_kernel, iterations=1)

        skeleton = skeletonize(eroded_free).astype(np.uint8)
        frontier_cells: List[GridPoint] = []

        skel_y, skel_x = np.where(skeleton == 1)

        for y, x in zip(skel_y, skel_x):
            if x <= 5 or x >= width - 6 or y <= 5 or y >= height - 6:
                continue

            neighbors_sum = np.sum(skeleton[y-1:y+2, x-1:x+2])

            # 找到骨架端点
            if neighbors_sum == 2:
                # 4. 真假走廊过滤器：扩大视野到 11x11 (约 0.55m x 0.55m)
                local_patch = data[y-5:y+6, x-5:x+6]
                unknown_count = np.sum(local_patch == -1)
                
                # 只有发现“大片连续的未知区域(>15个像素)”才承认它是真前沿！
                # 彻底无视椅子背后的那两三个像素的阴影！
                if unknown_count > 45:
                    frontier_cells.append((int(x), int(y)))

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
            key=lambda cell: (cell[0] - centroid_x) ** 2 +
            (cell[1] - centroid_y) ** 2,
        )

        frontier_world = self._grid_to_world(
            best_cell[0], best_cell[1], occupancy_grid)
        dx = robot_pose[0] - frontier_world[0]
        dy = robot_pose[1] - frontier_world[1]
        distance = math.hypot(dx, dy)
        if distance < 1e-6:
            return frontier_world

        max_backoff = min(
            distance - 0.05, max(self.goal_backoff_distance, self.goal_known_free_radius))
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

    def _refine_goal_along_ray(
        self,
        robot_pose: Tuple[float, float, float],
        goal_xy: WorldPoint,
        occupancy_grid: OccupancyGrid,
    ) -> Optional[WorldPoint]:
        """沿机器人指向原目标的方向，裁短距离并尽量落在已知自由格上（多段短跳）。"""
        rx, ry, _ = robot_pose
        gx, gy = goal_xy
        dx, dy = gx - rx, gy - ry
        dist = math.hypot(dx, dy)
        if dist < 1e-6:
            return None

        if self.max_navigation_goal_distance_m > 0.0:
            t_cap = min(1.0, self.max_navigation_goal_distance_m / dist)
        else:
            t_cap = 1.0

        n_iter = max(4, self.goal_ray_refine_iterations)
        lo, hi = 0.0, t_cap
        best: Optional[WorldPoint] = None
        for _ in range(n_iter):
            mid = 0.5 * (lo + hi)
            wx = rx + dx * mid
            wy = ry + dy * mid
            if self._is_known_free_patch((wx, wy), occupancy_grid):
                best = (wx, wy)
                lo = mid
            else:
                hi = mid

        if best is None:
            for k in range(1, 10):
                mid = t_cap * (k / 10.0)
                wx = rx + dx * mid
                wy = ry + dy * mid
                if self._is_known_free_patch((wx, wy), occupancy_grid):
                    best = (wx, wy)
                    break

        if best is None:
            return None

        if math.hypot(best[0] - rx, best[1] - ry) < self.goal_reached_radius:
            return None

        return best

    def _start_next_path_validation(self, robot_pose: Tuple[float, float, float]) -> None:
        if not self.candidate_goals:
            return

        raw_candidate, score, region_key = self.candidate_goals.pop(0)
        assert self.latest_map is not None
        candidate_world = self._refine_goal_along_ray(
            robot_pose, raw_candidate, self.latest_map
        )
        if candidate_world is None:
            self.get_logger().warn(
                f'Could not place a known-free goal along ray toward '
                f'({raw_candidate[0]:.2f}, {raw_candidate[1]:.2f}); skipping candidate.'
            )
            self.blacklisted_goals.append(raw_candidate)
            if region_key is not None:
                self._record_region_failure(region_key)
            self._continue_candidate_validation()
            return

        if (
            math.hypot(candidate_world[0] - raw_candidate[0],
                       candidate_world[1] - raw_candidate[1])
            > 0.35
        ):
            self.get_logger().info(
                f'Refined goal ({raw_candidate[0]:.2f}, {raw_candidate[1]:.2f}) -> '
                f'({candidate_world[0]:.2f}, {candidate_world[1]:.2f}) '
                f'(max segment {self.max_navigation_goal_distance_m:.1f} m).'
            )

        self._path_validation_goal_xy = candidate_world
        self._path_validation_goal_region = region_key
        self._path_validation_robot_pose = robot_pose
        self.current_goal_mode = self.candidate_goal_mode

        if self._is_path_validation_temporarily_disabled():
            goal_yaw = math.atan2(
                candidate_world[1] - robot_pose[1], candidate_world[0] - robot_pose[0])
            self.get_logger().warn(
                'Path validation is temporarily disabled; '
                f'sending candidate directly to NavigateToPose ({candidate_world[0]:.2f}, {candidate_world[1]:.2f}).'
            )
            self._path_validation_goal_xy = None
            self._path_validation_goal_region = None
            self._path_validation_robot_pose = None
            self.candidate_goals = []
            self.candidate_goal_mode = None
            self._send_navigation_goal(
                candidate_world[0],
                candidate_world[1],
                goal_yaw,
                region_key=region_key,
            )
            return

        self.path_check_pending = True

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

        goal_yaw = math.atan2(
            candidate_world[1] - robot_pose[1], candidate_world[0] - robot_pose[0])
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
            self._consecutive_path_validation_rejections += 1
            candidate = self._path_validation_goal_xy
            region_key = self._path_validation_goal_region
            robot_pose = self._path_validation_robot_pose
            self.get_logger().warn(
                'Planner rejected frontier path validation request '
                f'({self._consecutive_path_validation_rejections}/'
                f'{self.path_validation_rejection_limit}).'
            )
            if (
                candidate is not None
                and robot_pose is not None
                and self._consecutive_path_validation_rejections >= self.path_validation_rejection_limit
            ):
                self._path_validation_disabled_until = self._now_sec() + \
                    self.path_validation_disable_sec
                goal_x, goal_y = candidate
                goal_yaw = math.atan2(
                    goal_y - robot_pose[1], goal_x - robot_pose[0])
                self.get_logger().warn(
                    'Path validation appears unavailable; bypassing pre-check and '
                    f'sending candidate directly to NavigateToPose ({goal_x:.2f}, {goal_y:.2f}).'
                )
                self._path_validation_goal_xy = None
                self._path_validation_goal_region = None
                self._path_validation_robot_pose = None
                self.candidate_goals = []
                self.candidate_goal_mode = None
                self._send_navigation_goal(
                    goal_x, goal_y, goal_yaw, region_key=region_key)
                return
            self._continue_candidate_validation()
            return

        self._consecutive_path_validation_rejections = 0
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._path_validation_result_callback)

    def _path_validation_result_callback(self, future) -> None:
        self.path_check_pending = False
        action_result = future.result()
        status = action_result.status
        result = action_result.result
        candidate = self._path_validation_goal_xy
        region_key = self._path_validation_goal_region
        robot_pose = self._path_validation_robot_pose
        self._path_validation_goal_xy = None
        self._path_validation_goal_region = None
        self._path_validation_robot_pose = None

        if candidate is None or robot_pose is None:
            self._continue_candidate_validation()
            return

        if status == GoalStatus.STATUS_SUCCEEDED and len(result.path.poses) >= self.path_validation_min_poses:
            assert self.latest_map is not None
            path_ok, rejection_reason = self._path_looks_navigable(
                result.path.poses,
                robot_pose,
                candidate,
                self.latest_map,
            )
            if not path_ok:
                self.blacklisted_goals.append(candidate)
                if region_key is not None:
                    self._record_region_failure(region_key)
                self.get_logger().warn(
                    f'Frontier candidate ({candidate[0]:.2f}, {candidate[1]:.2f}) '
                    f'was rejected after path validation: {rejection_reason}'
                )
                self._continue_candidate_validation()
                return

            goal_x, goal_y = candidate
            goal_yaw = math.atan2(
                goal_y - robot_pose[1], goal_x - robot_pose[0])
            self.get_logger().info(
                f'Frontier candidate ({goal_x:.2f}, {goal_y:.2f}) passed path validation.'
            )
            self.candidate_goals = []
            self.candidate_goal_mode = None
            self._send_navigation_goal(
                goal_x, goal_y, goal_yaw, region_key=region_key)
            return

        self.blacklisted_goals.append(candidate)
        if region_key is not None:
            self._record_region_failure(region_key)
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

    def _send_navigation_goal(
        self,
        goal_x: float,
        goal_y: float,
        goal_yaw: float,
        region_key: Optional[RegionKey] = None,
    ) -> None:
        goal = NavigateToPose.Goal()
        goal.pose = PoseStamped()
        goal.pose.header.frame_id = self.global_frame
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x = goal_x
        goal.pose.pose.position.y = goal_y
        goal.pose.pose.orientation = self._quaternion_from_yaw(goal_yaw)

        self.goal_pending = True
        self.current_goal_xy = (goal_x, goal_y)
        self.current_goal_region = region_key if region_key is not None else self._point_to_region_key(
            (goal_x, goal_y))
        self._region_last_selected_at[self.current_goal_region] = self._now_sec(
        )
        robot_pose = self._lookup_robot_pose()
        if robot_pose is None:
            self.goal_best_distance_to_target = None
            self.goal_last_target_progress_time = self.get_clock().now()
        else:
            self.goal_best_distance_to_target = math.hypot(
                goal_x - robot_pose[0], goal_y - robot_pose[1])
            self.goal_last_target_progress_time = self.get_clock().now()
            if self.current_goal_mode == 'frontier':
                self._record_explore_sector_for_goal(
                    robot_pose, (goal_x, goal_y))
        self.get_logger().info(
            f'Sending exploration goal to ({goal_x:.2f}, {goal_y:.2f}).')

        self._goal_token_counter += 1
        self._pending_goal_token = self._goal_token_counter
        future = self.navigate_client.send_goal_async(goal)
        future.add_done_callback(self._goal_response_callback)

    def _goal_response_callback(self, future) -> None:
        self.goal_pending = False
        goal_handle = future.result()
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().warn('Nav2 rejected the exploration goal.')
            self._blacklist_current_goal()
            if self.current_goal_region is not None:
                self._record_region_failure(self.current_goal_region)
            self.current_goal_mode = None
            self.current_goal_xy = None
            self.current_goal_region = None
            self.goal_best_distance_to_target = None
            self.goal_last_target_progress_time = None
            self._pending_goal_token = None
            return

        self.goal_handle = goal_handle
        self.goal_active = True
        self.goal_sent_time = self.get_clock().now()
        self._active_goal_token = self._pending_goal_token
        self._pending_goal_token = None
        self.goal_last_progress_time = self.goal_sent_time
        robot_pose = self._lookup_robot_pose()
        self.goal_last_progress_xy = None if robot_pose is None else (
            robot_pose[0], robot_pose[1])

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(
            lambda future_result, token=self._active_goal_token: self._goal_result_callback(
                future_result,
                token,
            )
        )

    def _goal_result_callback(self, future, token: Optional[int]) -> None:
        if token is None or token != self._active_goal_token:
            return

        status = future.result().status
        goal_xy = self.current_goal_xy
        goal_region = self.current_goal_region

        self.goal_active = False
        self.goal_handle = None
        self.goal_sent_time = None
        self.current_goal_xy = None
        self.current_goal_region = None
        self.goal_last_progress_time = None
        self.goal_last_progress_xy = None
        self.goal_best_distance_to_target = None
        self.goal_last_target_progress_time = None
        self._active_goal_token = None

        if status == GoalStatus.STATUS_SUCCEEDED:
            if goal_xy is not None:
                if self.current_goal_mode == 'startup':
                    self._startup_goal_successes += 1
                    # 启动引导点只用一次，避免反复在同一个近点上“秒成功”。
                    self.blacklisted_goals.append(goal_xy)
                else:
                    self._successful_goals += 1
                if goal_region is not None:
                    self._record_region_success(goal_region)
                self.get_logger().info(
                    f'Exploration goal reached at ({goal_xy[0]:.2f}, {goal_xy[1]:.2f}).'
                )
            self.current_goal_mode = None
            return

        if goal_xy is not None:
            self.blacklisted_goals.append(goal_xy)
            if goal_region is not None:
                self._record_region_failure(goal_region)
            self.get_logger().warn(
                f'Exploration goal failed with status {status}; blacklisting that area.'
            )
        self.current_goal_mode = None

    def _trigger_spin_recovery(self) -> None:
        if not self.spin_client.server_is_ready():
            self.get_logger().info('Spin recovery requested, but Nav2 spin server is not ready yet.')
            return

        spin_angle = self._spin_angle_override
        if spin_angle is None:
            spin_angle = self.spin_recovery_angle

        self._no_frontier_cycles = 0
        self.spin_pending = True
        log_message = self._spin_log_message
        if log_message is None:
            log_message = (
                f'No frontier for {self.no_frontier_cycles_before_spin} cycles; '
                f'triggering spin recovery ({spin_angle:.2f} rad).'
            )
        self.get_logger().info(log_message)

        goal = Spin.Goal()
        goal.target_yaw = spin_angle
        goal.time_allowance = Duration(
            seconds=self.spin_time_allowance_sec).to_msg()

        future = self.spin_client.send_goal_async(goal)
        future.add_done_callback(self._spin_response_callback)

    def _trigger_backup_recovery(self) -> None:
        if not self.backup_client.server_is_ready():
            self.get_logger().info(
                'Backup recovery requested, but Nav2 backup server is not ready yet.')
            return

        backup_distance = self._backup_distance_override
        if backup_distance is None:
            backup_distance = self.backup_recovery_distance
        backup_speed = self._backup_speed_override
        if backup_speed is None:
            backup_speed = self.backup_recovery_speed

        self._no_frontier_cycles = 0
        self.backup_pending = True
        log_message = self._backup_log_message
        if log_message is None:
            log_message = (
                'Planner still cannot produce a movable goal; '
                f'triggering backup recovery ({backup_distance:.2f} m).'
            )
        self.get_logger().info(log_message)

        goal = BackUp.Goal()
        goal.target.x = -abs(backup_distance)
        goal.target.y = 0.0
        goal.speed = backup_speed
        goal.time_allowance = Duration(
            seconds=self.backup_time_allowance_sec).to_msg()

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
        should_spin_after_backup = self._escape_spin_after_backup
        self._escape_spin_after_backup = False
        self._backup_distance_override = None
        self._backup_speed_override = None
        self._backup_log_message = None
        if status == GoalStatus.STATUS_SUCCEEDED:
            if should_spin_after_backup:
                self.get_logger().info(
                    'Escape backup completed; triggering a short spin before replanning.'
                )
                self._spin_angle_override = self.escape_spin_angle
                self._spin_log_message = (
                    f'Escape backup finished; triggering short spin recovery '
                    f'({self.escape_spin_angle:.2f} rad).'
                )
                self._trigger_spin_recovery()
                return
            self.get_logger().info('Backup recovery completed; frontier search will resume.')
            return

        self.get_logger().warn(
            f'Backup recovery finished with status {status}; falling back to spin if needed.'
        )
        if should_spin_after_backup:
            self._spin_angle_override = self.escape_spin_angle
            self._spin_log_message = (
                'Escape backup did not fully succeed; still attempting a short spin '
                'before replanning.'
            )
            self._trigger_spin_recovery()

    def _spin_response_callback(self, future) -> None:
        self.spin_pending = False
        goal_handle = future.result()
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().warn('Spin recovery goal was rejected by Nav2.')
            self._spin_angle_override = None
            self._spin_log_message = None
            return

        self.spin_active = True
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._spin_result_callback)

    def _spin_result_callback(self, future) -> None:
        self.spin_active = False
        status = future.result().status
        self._last_recovery_mode = 'spin'
        self._spin_angle_override = None
        self._spin_log_message = None
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Spin recovery completed; frontier search will resume.')
            return

        self.get_logger().warn(
            f'Spin recovery finished with status {status}; frontier search will continue anyway.'
        )

    def _check_goal_timeout(self) -> None:
        if self.goal_sent_time is None or self.goal_handle is None:
            return

        elapsed = (self.get_clock().now() -
                   self.goal_sent_time).nanoseconds / 1e9
        robot_pose = self._lookup_robot_pose()
        if robot_pose is not None:
            current_xy = (robot_pose[0], robot_pose[1])
            if (
                self.goal_last_progress_xy is None
                or math.hypot(
                    current_xy[0] - self.goal_last_progress_xy[0],
                    current_xy[1] - self.goal_last_progress_xy[1],
                ) >= self.goal_progress_radius
            ):
                self.goal_last_progress_xy = current_xy
                self.goal_last_progress_time = self.get_clock().now()

            if self.current_goal_xy is not None:
                distance_to_goal = math.hypot(
                    self.current_goal_xy[0] - current_xy[0],
                    self.current_goal_xy[1] - current_xy[1],
                )
                if (
                    self.goal_best_distance_to_target is None
                    or self.goal_best_distance_to_target - distance_to_goal
                    >= self.goal_approach_improvement_radius
                ):
                    self.goal_best_distance_to_target = distance_to_goal
                    self.goal_last_target_progress_time = self.get_clock().now()

        if self.goal_last_progress_time is not None:
            stalled_for = (self.get_clock().now() -
                           self.goal_last_progress_time).nanoseconds / 1e9
            if stalled_for >= self.goal_stall_timeout_sec:
                self._abort_goal_for_escape(
                    'Exploration goal appears stuck with no meaningful progress; '
                    'canceling it and triggering escape backup.'
                )
                return

        if self.goal_last_target_progress_time is not None:
            not_closer_for = (
                self.get_clock().now() - self.goal_last_target_progress_time
            ).nanoseconds / 1e9
            if not_closer_for >= self.goal_approach_timeout_sec:
                self._abort_goal_for_escape(
                    'Exploration goal is not getting meaningfully closer; '
                    'canceling it and triggering escape backup.'
                )
                return

        if elapsed < self.goal_timeout_sec:
            return

        self._abort_goal_for_escape(
            'Exploration goal timed out; canceling it and triggering escape backup.'
        )

    def _abort_goal_for_escape(self, log_message: str) -> None:
        if self.goal_handle is None:
            return

        self.get_logger().warn(log_message)
        self.goal_handle.cancel_goal_async()
        self._blacklist_current_goal()
        if self.current_goal_region is not None:
            self._record_region_failure(self.current_goal_region)
        self._clear_active_goal_state()
        self._backup_distance_override = self.escape_backup_distance
        self._backup_speed_override = self.escape_backup_speed
        self._backup_log_message = (
            'Goal cancellation indicates the robot is trapped in a tight space; '
            f'triggering escape backup ({self.escape_backup_distance:.2f} m).'
        )
        self._escape_spin_after_backup = True
        self._trigger_backup_recovery()

    def _clear_active_goal_state(self) -> None:
        self.goal_active = False
        self.goal_handle = None
        self.goal_sent_time = None
        self.current_goal_xy = None
        self.current_goal_region = None
        self.current_goal_mode = None
        self.goal_last_progress_time = None
        self.goal_last_progress_xy = None
        self.goal_best_distance_to_target = None
        self.goal_last_target_progress_time = None
        self._active_goal_token = None

    def _now_sec(self) -> float:
        return self.get_clock().now().nanoseconds / 1e9

    def _purge_explore_sector_history(self) -> None:
        now = self._now_sec()
        while (
            self._explore_sector_history
            and now - self._explore_sector_history[0][0] > self.explore_sector_memory_sec
        ):
            self._explore_sector_history.popleft()

    def _bearing_sector(self, robot_pose: Tuple[float, float, float], point: WorldPoint) -> int:
        n = self.explore_sector_count
        if n <= 1:
            return 0
        ang = math.atan2(point[1] - robot_pose[1], point[0] - robot_pose[0])
        u = (ang + math.pi) / (2.0 * math.pi) * n
        s = int(math.floor(u))
        if s < 0:
            s = 0
        if s >= n:
            s = n - 1
        return s

    def _frontier_distance_score_bonus(self, distance: float) -> float:
        """Amount to subtract from candidate score; farther goals become more attractive."""
        if self.frontier_distance_bonus_per_m <= 0.0:
            return 0.0
        excess = max(0.0, distance - self.frontier_distance_pivot_m)
        return min(excess * self.frontier_distance_bonus_per_m, self.frontier_distance_bonus_cap)

    def _explore_sector_repeat_penalty(
        self,
        robot_pose: Tuple[float, float, float],
        candidate: WorldPoint,
    ) -> float:
        if self.explore_sector_count <= 0 or self.explore_sector_repeat_penalty <= 0.0:
            return 0.0
        self._purge_explore_sector_history()
        sector = self._bearing_sector(robot_pose, candidate)
        now = self._now_sec()
        for t, s in self._explore_sector_history:
            if now - t <= self.explore_sector_memory_sec and s == sector:
                return self.explore_sector_repeat_penalty
        return 0.0

    def _record_explore_sector_for_goal(
        self,
        robot_pose: Tuple[float, float, float],
        goal_xy: WorldPoint,
    ) -> None:
        if self.explore_sector_count <= 0:
            return
        sec = self._bearing_sector(robot_pose, goal_xy)
        self._explore_sector_history.append((self._now_sec(), sec))

    def _point_to_region_key(self, point: WorldPoint) -> RegionKey:
        cell_size = max(0.5, self.region_cell_size)
        return (
            int(math.floor(point[0] / cell_size)),
            int(math.floor(point[1] / cell_size)),
        )

    def _is_region_on_cooldown(self, region_key: RegionKey) -> bool:
        return self._region_cooldown_until.get(region_key, 0.0) > self._now_sec()

    def _set_region_cooldown(self, region_key: RegionKey, cooldown_sec: float) -> None:
        self._region_cooldown_until[region_key] = self._now_sec(
        ) + cooldown_sec

    def _apply_region_score_adjustments(self, base_score: float, region_key: RegionKey) -> float:
        score = base_score
        fail_count = self._region_fail_counts.get(region_key, 0)
        score += fail_count * self.region_fail_penalty

        last_visit = max(
            self._region_last_selected_at.get(region_key, -1e18),
            self._region_last_reached_at.get(region_key, -1e18),
        )
        if self._now_sec() - last_visit < self.region_recent_visit_window_sec:
            score += self.region_recent_visit_penalty
        else:
            score -= self.region_novelty_bonus
        return score

    def _record_region_success(self, region_key: RegionKey) -> None:
        self._region_fail_counts[region_key] = 0
        self._region_last_reached_at[region_key] = self._now_sec()

    def _record_region_failure(self, region_key: RegionKey) -> None:
        new_fail_count = self._region_fail_counts.get(region_key, 0) + 1
        self._region_fail_counts[region_key] = new_fail_count
        if new_fail_count >= self.region_fail_limit:
            self._set_region_cooldown(region_key, self.region_cooldown_sec)
            self._region_fail_counts[region_key] = 0
            self.get_logger().warn(
                f'Region {region_key} entered cooldown for {self.region_cooldown_sec:.0f}s '
                'after repeated failures.'
            )

    def _record_robot_pose(self, robot_pose: Tuple[float, float, float]) -> None:
        now_sec = self._now_sec()
        if not self._pose_history:
            self._pose_history.append((now_sec, robot_pose[0], robot_pose[1]))
            return

        _, last_x, last_y = self._pose_history[-1]
        if (
            math.hypot(robot_pose[0] - last_x, robot_pose[1] - last_y) >= 0.15
            or now_sec - self._pose_history[-1][0] >= self.planning_period_sec
        ):
            self._pose_history.append((now_sec, robot_pose[0], robot_pose[1]))

        cutoff = now_sec - self.wander_detect_window_sec
        while self._pose_history and self._pose_history[0][0] < cutoff:
            self._pose_history.popleft()

    def _should_trigger_wander_escape(self) -> bool:
        if len(self._pose_history) < 6:
            return False
        if self._now_sec() - self._last_wander_intervention_at < self.wander_trigger_cooldown_sec:
            return False

        window = list(self._pose_history)
        duration = window[-1][0] - window[0][0]
        if duration < self.wander_detect_window_sec * 0.6:
            return False

        center_x = window[-1][1]
        center_y = window[-1][2]
        max_radius = max(
            math.hypot(sample[1] - center_x, sample[2] - center_y)
            for sample in window
        )
        return max_radius <= self.wander_radius

    def _apply_wander_cooldown(self, robot_pose: Tuple[float, float, float]) -> None:
        base_key = self._point_to_region_key((robot_pose[0], robot_pose[1]))
        radius_in_cells = max(
            1, int(math.ceil(self.wander_radius / max(0.5, self.region_cell_size))))
        for dy in range(-radius_in_cells, radius_in_cells + 1):
            for dx in range(-radius_in_cells, radius_in_cells + 1):
                region_key = (base_key[0] + dx, base_key[1] + dy)
                self._set_region_cooldown(
                    region_key, self.wander_region_cooldown_sec)
        self._last_wander_intervention_at = self._now_sec()
        self.get_logger().warn(
            'Detected repeated wandering in the same local area; '
            f'cooling down nearby regions for {self.wander_region_cooldown_sec:.0f}s.'
        )

    def _is_path_validation_temporarily_disabled(self) -> bool:
        return self._path_validation_disabled_until > self._now_sec()

    def _blacklist_current_goal(self) -> None:
        if self.current_goal_xy is not None:
            self.blacklisted_goals.append(self.current_goal_xy)

    def _is_blacklisted(self, point: WorldPoint) -> bool:
        return any(
            math.hypot(point[0] - bad[0], point[1] -
                       bad[1]) < self.blacklist_radius
            for bad in self.blacklisted_goals
        )

    def _is_near_recent_startup_goal(self, point: WorldPoint) -> bool:
        return any(
            math.hypot(point[0] - used[0], point[1] - used[1]
                       ) < self.startup_goal_reuse_radius
            for used in self.blacklisted_goals
        )

    def _is_free(self, occupancy_value: int) -> bool:
        return 0 <= occupancy_value < self.occupied_threshold

    def _path_looks_navigable(
        self,
        path_poses: Sequence[PoseStamped],
        robot_pose: Tuple[float, float, float],
        candidate_world: WorldPoint,
        occupancy_grid: OccupancyGrid,
    ) -> Tuple[bool, str]:
        straight_line = math.hypot(
            candidate_world[0] - robot_pose[0],
            candidate_world[1] - robot_pose[1],
        )
        if straight_line <= 1e-6:
            return False, 'goal is effectively colocated with the robot'

        path_length = self._path_length(path_poses)
        if (
            straight_line >= 1.0
            and path_length > straight_line * self.path_max_length_ratio
        ):
            return (
                False,
                f'path is too tortuous (length {path_length:.2f} m vs straight {straight_line:.2f} m)',
            )

        sampled_points = self._collect_path_points_for_quality_check(
            path_poses,
            max_distance=self.path_quality_check_distance,
        )
        if len(sampled_points) < 3:
            return True, ''

        clear_count = sum(
            1
            for point in sampled_points
            if self._has_local_clearance(
                point,
                occupancy_grid,
                required_radius=self.path_pose_clearance_radius,
            )
        )
        clear_ratio = clear_count / len(sampled_points)
        if clear_ratio < self.path_min_clearance_pass_ratio:
            return (
                False,
                f'early path segment is too constrained (clear ratio {clear_ratio:.2f})',
            )
        return True, ''

    def _collect_path_points_for_quality_check(
        self,
        path_poses: Sequence[PoseStamped],
        max_distance: float,
    ) -> List[WorldPoint]:
        if not path_poses:
            return []

        sampled_points: List[WorldPoint] = []
        traveled = 0.0
        previous_point: Optional[WorldPoint] = None
        for pose_stamped in path_poses:
            point = (
                pose_stamped.pose.position.x,
                pose_stamped.pose.position.y,
            )
            if previous_point is not None:
                traveled += math.hypot(
                    point[0] - previous_point[0],
                    point[1] - previous_point[1],
                )
                if traveled > max_distance:
                    break
            sampled_points.append(point)
            previous_point = point
        return sampled_points

    def _path_length(self, path_poses: Sequence[PoseStamped]) -> float:
        if len(path_poses) < 2:
            return 0.0

        length = 0.0
        previous = path_poses[0].pose.position
        for pose_stamped in path_poses[1:]:
            current = pose_stamped.pose.position
            length += math.hypot(current.x - previous.x,
                                 current.y - previous.y)
            previous = current
        return length

    def _has_local_clearance(
        self,
        candidate_world: WorldPoint,
        occupancy_grid: OccupancyGrid,
        required_radius: Optional[float] = None,
    ) -> bool:
        center = self._world_to_grid(
            candidate_world[0], candidate_world[1], occupancy_grid)
        if center is None:
            return False

        clearance_radius = (
            self.candidate_clearance_radius if required_radius is None else required_radius
        )
        radius_cells = max(
            1, int(clearance_radius / occupancy_grid.info.resolution))
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
        center = self._world_to_grid(
            candidate_world[0], candidate_world[1], occupancy_grid)
        if center is None:
            return False

        patch_radius = self.goal_known_free_radius if required_radius is None else required_radius
        radius_cells = max(
            1, int(patch_radius / occupancy_grid.info.resolution))
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
