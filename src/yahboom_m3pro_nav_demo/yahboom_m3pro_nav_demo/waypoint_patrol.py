#!/usr/bin/env python3
"""Visit named waypoints from YAML using Nav2 NavigateToPose (no waypoint_follower required).

Waypoint YAML entries may set ``patrol_order`` (or ``order``) per point; when the ROS
parameter ``waypoint_order`` is empty, patrol uses ascending ``patrol_order``, then
name as tie-breaker. Waypoints without ``patrol_order`` sort after those that have it.
If no waypoint defines ``patrol_order``, order is alphabetical by name (legacy).
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy

from yahboom_m3pro_nav_demo.waypoint_storage import default_record_path, load_waypoints_file


def yaw_to_orientation_zw(yaw: float) -> Tuple[float, float]:
    return math.sin(yaw * 0.5), math.cos(yaw * 0.5)


def make_pose_stamped(
    navigator: BasicNavigator, frame_id: str, x: float, y: float, yaw: float
) -> PoseStamped:
    msg = PoseStamped()
    msg.header.frame_id = frame_id
    msg.header.stamp = navigator.get_clock().now().to_msg()
    msg.pose.position.x = x
    msg.pose.position.y = y
    msg.pose.position.z = 0.0
    msg.pose.orientation.x = 0.0
    msg.pose.orientation.y = 0.0
    z, w = yaw_to_orientation_zw(yaw)
    msg.pose.orientation.z = z
    msg.pose.orientation.w = w
    return msg


def resolve_waypoints_path(explicit: str) -> Path:
    if explicit.strip():
        return Path(explicit).expanduser()
    user_path = default_record_path()
    if user_path.is_file():
        return user_path
    share = Path(get_package_share_directory('yahboom_m3pro_nav_demo'))
    packaged = share / 'config' / 'recorded_waypoints.yaml'
    return packaged if packaged.is_file() else user_path


def _patrol_sort_key(name: str, waypoints: Dict[str, Dict[str, Any]]) -> Tuple[float, str]:
    v = waypoints[name]
    po = v.get('patrol_order')
    if po is None:
        return (float('inf'), name)
    try:
        return (float(po), name)
    except (TypeError, ValueError):
        return (float('inf'), name)


def ordered_names(
    waypoints: Dict[str, Dict[str, Any]], order_csv: str
) -> Tuple[List[str], List[str], str]:
    """Return (names, missing_from_csv, order_source) where order_source is 'param', 'patrol_order', or 'name'."""
    if order_csv.strip():
        requested = [s.strip() for s in order_csv.split(',') if s.strip()]
        out: List[str] = []
        missing: List[str] = []
        for n in requested:
            if n in waypoints:
                out.append(n)
            else:
                missing.append(n)
        return out, missing, 'param'
    if any('patrol_order' in v for v in waypoints.values()):
        names = sorted(waypoints.keys(), key=lambda n: _patrol_sort_key(n, waypoints))
        return names, [], 'patrol_order'
    return sorted(waypoints.keys()), [], 'name'


def main(args=None) -> None:
    rclpy.init(args=args)
    navigator = BasicNavigator('waypoint_patrol_navigator')
    navigator.declare_parameter('waypoints_file', '')
    navigator.declare_parameter('patrol_loop', False)
    navigator.declare_parameter('waypoint_order', '')

    path = resolve_waypoints_path(
        navigator.get_parameter('waypoints_file').get_parameter_value().string_value
    )
    do_loop = navigator.get_parameter('patrol_loop').get_parameter_value().bool_value
    order_csv = navigator.get_parameter('waypoint_order').get_parameter_value().string_value

    frame_id, waypoints = load_waypoints_file(path)
    if not waypoints:
        navigator.get_logger().error(
            f'No waypoints in {path}. Record with '
            f'`ros2 run yahboom_m3pro_nav_demo waypoint_recorder`, or edit '
            f'config/recorded_waypoints.yaml.'
        )
        navigator.destroy_node()
        rclpy.shutdown()
        sys.exit(1)

    names, missing, order_src = ordered_names(waypoints, order_csv)
    for m in missing:
        navigator.get_logger().warn(f'Skipping unknown waypoint name in waypoint_order: {m}')

    if not names:
        navigator.get_logger().error('Waypoint order resolved to an empty list.')
        navigator.destroy_node()
        rclpy.shutdown()
        sys.exit(1)

    navigator.get_logger().info(
        f'Loaded {len(waypoints)} waypoint(s) from {path} (frame_id={frame_id!r}, '
        f'order_source={order_src!r}, patrol order: {names}, loop={do_loop})'
    )

    navigator.waitUntilNav2Active()

    cycle = 0
    try:
        while rclpy.ok():
            cycle += 1
            navigator.get_logger().info(f'--- Patrol cycle {cycle} ---')
            aborted = False
            for name in names:
                entry = waypoints[name]
                pose = make_pose_stamped(
                    navigator, frame_id, entry['x'], entry['y'], entry['yaw']
                )
                navigator.get_logger().info(f'Going to {name!r} ...')
                if not navigator.goToPose(pose):
                    navigator.get_logger().error(f'Goal to {name!r} was rejected.')
                    aborted = True
                    break
                while not navigator.isTaskComplete():
                    pass
                result = navigator.getResult()
                if result == TaskResult.SUCCEEDED:
                    navigator.get_logger().info(f'Reached {name!r}.')
                elif result == TaskResult.CANCELED:
                    navigator.get_logger().warn(f'Goal {name!r} canceled.')
                    aborted = True
                    break
                else:
                    navigator.get_logger().error(f'Goal {name!r} failed.')
                    aborted = True
                    break
            if aborted or not do_loop:
                break
    except KeyboardInterrupt:
        navigator.get_logger().info('Patrol interrupted by user.')
        navigator.cancelTask()

    navigator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
