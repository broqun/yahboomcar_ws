#!/usr/bin/env python3
"""Visit named waypoints from YAML using Nav2 NavigateToPose.

Supports two per-waypoint *behavior* types (set in the YAML):

* ``goto`` (default) — single NavigateToPose to ``(x, y, yaw)``.
* ``room_coverage``  — drive to ``(x, y, yaw)`` (door/entry), then execute
  boustrophedon (zigzag) coverage inside the ``coverage.polygon``.

Waypoint ordering follows ``patrol_order`` / ``order`` fields, falling back to
alphabetical name sort.  ``goto`` and ``room_coverage`` entries can be freely
interleaved.
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

from yahboom_m3pro_nav_demo.room_coverage import generate_coverage_poses
from yahboom_m3pro_nav_demo.waypoint_storage import default_record_path, load_waypoints_file


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _yaw_to_quat_zw(yaw: float) -> Tuple[float, float]:
    return math.sin(yaw * 0.5), math.cos(yaw * 0.5)


def _make_pose(
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
    z, w = _yaw_to_quat_zw(yaw)
    msg.pose.orientation.z = z
    msg.pose.orientation.w = w
    return msg


def _resolve_waypoints_path(explicit: str) -> Path:
    if explicit.strip():
        return Path(explicit).expanduser()
    user_path = default_record_path()
    if user_path.is_file():
        return user_path
    share = Path(get_package_share_directory('yahboom_m3pro_nav_demo'))
    packaged = share / 'config' / 'recorded_waypoints.yaml'
    return packaged if packaged.is_file() else user_path


def _patrol_sort_key(
    name: str, waypoints: Dict[str, Dict[str, Any]]
) -> Tuple[float, str]:
    v = waypoints[name]
    po = v.get('patrol_order')
    if po is None:
        return (float('inf'), name)
    try:
        return (float(po), name)
    except (TypeError, ValueError):
        return (float('inf'), name)


def _ordered_names(
    waypoints: Dict[str, Dict[str, Any]], order_csv: str
) -> Tuple[List[str], List[str], str]:
    if order_csv.strip():
        requested = [s.strip() for s in order_csv.split(',') if s.strip()]
        out: List[str] = []
        missing: List[str] = []
        for n in requested:
            (out if n in waypoints else missing).append(n)
        return out, missing, 'param'
    if any('patrol_order' in v for v in waypoints.values()):
        names = sorted(
            waypoints.keys(), key=lambda n: _patrol_sort_key(n, waypoints)
        )
        return names, [], 'patrol_order'
    return sorted(waypoints.keys()), [], 'name'


# ---------------------------------------------------------------------------
# Nav2 single-goal execution
# ---------------------------------------------------------------------------

def _go_and_wait(
    navigator: BasicNavigator,
    frame_id: str,
    x: float,
    y: float,
    yaw: float,
    label: str,
) -> TaskResult:
    """Send *goToPose* and block until the action finishes."""
    pose = _make_pose(navigator, frame_id, x, y, yaw)
    navigator.get_logger().info(f'Navigating to {label} …')
    if not navigator.goToPose(pose):
        navigator.get_logger().error(f'Goal {label} rejected by Nav2.')
        return TaskResult.FAILED
    while not navigator.isTaskComplete():
        pass
    return navigator.getResult()


# ---------------------------------------------------------------------------
# Behavior executors
# ---------------------------------------------------------------------------

def _exec_goto(
    navigator: BasicNavigator,
    frame_id: str,
    name: str,
    entry: Dict[str, Any],
) -> bool:
    """Classic point-to-point navigation.  Returns *True* on success."""
    result = _go_and_wait(
        navigator, frame_id, entry['x'], entry['y'], entry['yaw'], repr(name)
    )
    if result == TaskResult.SUCCEEDED:
        navigator.get_logger().info(f'Reached {name!r}.')
        return True
    level = 'warn' if result == TaskResult.CANCELED else 'error'
    getattr(navigator.get_logger(), level)(
        f'Goal {name!r} ended with {result.name}.'
    )
    return False


def _exec_coverage(
    navigator: BasicNavigator,
    frame_id: str,
    name: str,
    entry: Dict[str, Any],
    on_child_failure: str,
) -> bool:
    """Drive to entry pose, then execute boustrophedon coverage.

    Returns *True* when the patrol loop should **continue** to the next
    waypoint (even if coverage was only partially completed under
    ``abort_segment`` policy).
    """
    # --- reach the door / entry pose first ---
    res = _go_and_wait(
        navigator,
        frame_id,
        entry['x'],
        entry['y'],
        entry['yaw'],
        f'{name!r} (entry)',
    )
    if res != TaskResult.SUCCEEDED:
        navigator.get_logger().error(
            f'Cannot reach entry for coverage {name!r} ({res.name}); '
            f'skipping segment.'
        )
        return on_child_failure != 'abort_patrol'

    # --- generate sub-goals ---
    cfg = entry.get('coverage') or {}
    polygon = cfg.get('polygon', [])
    if not polygon or len(polygon) < 3:
        navigator.get_logger().error(
            f'Coverage {name!r}: polygon missing or < 3 vertices.'
        )
        return True

    poses = generate_coverage_poses(
        polygon=polygon,
        stripe_width=float(cfg.get('stripe_width', 0.5)),
        stripe_angle_deg=float(cfg.get('stripe_angle_deg', 0.0)),
        sweep_margin=float(cfg.get('sweep_margin', 0.0)),
        entry_pose=(entry['x'], entry['y'], entry['yaw']),
    )
    total = len(poses)
    navigator.get_logger().info(
        f'Coverage {name!r}: generated {total} sub-goals '
        f'(stripe_width={cfg.get("stripe_width")}, '
        f'angle={cfg.get("stripe_angle_deg", 0)}°).'
    )
    if total == 0:
        navigator.get_logger().warn(f'Coverage {name!r}: empty pose list.')
        return True

    # --- execute sub-goals sequentially ---
    for idx, (sx, sy, syaw) in enumerate(poses, 1):
        label = f'{name!r} [{idx}/{total}]'
        res = _go_and_wait(navigator, frame_id, sx, sy, syaw, label)
        if res == TaskResult.SUCCEEDED:
            continue
        if res == TaskResult.CANCELED:
            navigator.get_logger().warn(f'Coverage {name!r} canceled at [{idx}/{total}].')
            return False
        navigator.get_logger().warn(
            f'Coverage {name!r} sub-goal [{idx}/{total}] failed ({res.name}).'
        )
        if on_child_failure == 'abort_patrol':
            return False
        navigator.get_logger().info(
            f'Policy=abort_segment → skipping rest of {name!r}, '
            f'continuing patrol.'
        )
        navigator.cancelTask()
        return True

    navigator.get_logger().info(
        f'Coverage {name!r} complete ({total} sub-goals).'
    )
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(args=None) -> None:
    rclpy.init(args=args)
    navigator = BasicNavigator('waypoint_patrol_navigator')

    navigator.declare_parameter('waypoints_file', '')
    navigator.declare_parameter('patrol_loop', False)
    navigator.declare_parameter('waypoint_order', '')
    navigator.declare_parameter('coverage_on_child_failure', 'abort_segment')

    path = _resolve_waypoints_path(
        navigator.get_parameter('waypoints_file')
        .get_parameter_value()
        .string_value
    )
    do_loop = (
        navigator.get_parameter('patrol_loop')
        .get_parameter_value()
        .bool_value
    )
    order_csv = (
        navigator.get_parameter('waypoint_order')
        .get_parameter_value()
        .string_value
    )
    on_child_failure = (
        navigator.get_parameter('coverage_on_child_failure')
        .get_parameter_value()
        .string_value
    )

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

    names, missing, order_src = _ordered_names(waypoints, order_csv)
    for m in missing:
        navigator.get_logger().warn(
            f'Skipping unknown waypoint name in waypoint_order: {m}'
        )

    if not names:
        navigator.get_logger().error('Waypoint order resolved to an empty list.')
        navigator.destroy_node()
        rclpy.shutdown()
        sys.exit(1)

    behaviors = {
        n: waypoints[n].get('behavior', 'goto') for n in names
    }
    navigator.get_logger().info(
        f'Loaded {len(waypoints)} waypoint(s) from {path} '
        f'(frame_id={frame_id!r}, order_source={order_src!r}, '
        f'patrol order: {names}, loop={do_loop})\n'
        f'  behaviors: {behaviors}'
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
                behavior = entry.get('behavior', 'goto')

                if behavior == 'room_coverage':
                    ok = _exec_coverage(
                        navigator, frame_id, name, entry, on_child_failure
                    )
                    if not ok:
                        aborted = True
                        break
                else:
                    if not _exec_goto(navigator, frame_id, name, entry):
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
