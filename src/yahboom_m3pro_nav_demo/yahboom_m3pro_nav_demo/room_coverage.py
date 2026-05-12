"""Boustrophedon (zigzag / lawn-mower) coverage path generator.

Pure geometry — no ROS dependency.  Given a closed polygon, stripe width,
sweep angle and safety margin, returns an ordered list of ``(x, y, yaw)``
poses that a differential-drive robot can follow via Nav2 ``goToPose``.
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

Pose2D = Tuple[float, float, float]

_EPS = 1e-6  # keep endpoints strictly inside the polygon boundary


def _rotate(x: float, y: float, cos_a: float, sin_a: float) -> Tuple[float, float]:
    return x * cos_a - y * sin_a, x * sin_a + y * cos_a


def _sweep_intersections(
    y_sweep: float, poly: List[Tuple[float, float]]
) -> List[float]:
    """X-coords where a horizontal line at *y_sweep* crosses *poly* edges.

    Uses a half-open interval ``(lo, hi]`` per edge to avoid double-counting
    shared vertices.
    """
    xs: List[float] = []
    n = len(poly) - 1
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[i + 1]
        if y1 == y2:
            continue
        lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
        if not (lo < y_sweep <= hi):
            continue
        t = (y_sweep - y1) / (y2 - y1)
        xs.append(x1 + t * (x2 - x1))
    xs.sort()
    return xs


def _norm_angle(a: float) -> float:
    return math.atan2(math.sin(a), math.cos(a))


def generate_coverage_poses(
    polygon: List[List[float]],
    stripe_width: float,
    stripe_angle_deg: float = 0.0,
    sweep_margin: float = 0.0,
    entry_pose: Optional[Pose2D] = None,
) -> List[Pose2D]:
    """Generate an ordered boustrophedon coverage path inside *polygon*.

    Parameters
    ----------
    polygon
        ``[[x, y], ...]`` closed polygon vertices in the map frame.
    stripe_width
        Spacing between adjacent parallel sweeps (metres).
    stripe_angle_deg
        Direction of the sweep lines in degrees.  ``0`` means sweeps run
        parallel to the map X-axis; ``90`` means parallel to Y-axis.
    sweep_margin
        Safety inset from the polygon boundary (metres).
    entry_pose
        ``(x, y, yaw)`` of the door / entry point.  The first stripe starts
        from whichever side of the polygon is closest to this pose.

    Returns
    -------
    list of ``(x, y, yaw)``
        Poses in the map frame, alternating direction stripe-by-stripe.
    """
    if len(polygon) < 3 or stripe_width <= 0:
        return []

    angle = math.radians(stripe_angle_deg)
    ca_fwd, sa_fwd = math.cos(-angle), math.sin(-angle)

    rotated = [_rotate(p[0], p[1], ca_fwd, sa_fwd) for p in polygon]
    if rotated[0] != rotated[-1]:
        rotated.append(rotated[0])

    ys = [p[1] for p in rotated]
    y_lo = min(ys) + sweep_margin + _EPS
    y_hi = max(ys) - sweep_margin - _EPS
    if y_lo >= y_hi:
        return []

    span = y_hi - y_lo
    n_stripes = max(1, int(span / stripe_width))
    remainder = span - n_stripes * stripe_width
    y_start = y_lo + remainder / 2.0 + stripe_width / 2.0
    sweep_ys = [y_start + i * stripe_width for i in range(n_stripes)]
    if not sweep_ys:
        return []

    vertex_ys = {p[1] for p in rotated}
    _NUDGE = 4 * _EPS
    sweep_ys = [
        y + _NUDGE if any(abs(y - vy) < _NUDGE for vy in vertex_ys) else y
        for y in sweep_ys
    ]

    left_first = True
    if entry_pose is not None:
        ex, _ = _rotate(entry_pose[0], entry_pose[1], ca_fwd, sa_fwd)
        first_xs = _sweep_intersections(sweep_ys[0], rotated)
        if len(first_xs) >= 2:
            mid = (first_xs[0] + first_xs[-1]) / 2.0
            left_first = ex < mid

    ca_back, sa_back = math.cos(angle), math.sin(angle)
    fwd_yaw = _norm_angle(angle)
    rev_yaw = _norm_angle(angle + math.pi)

    poses: List[Pose2D] = []
    going_right = left_first

    for y_s in sweep_ys:
        xs = _sweep_intersections(y_s, rotated)
        if len(xs) < 2:
            continue
        x_left = xs[0] + sweep_margin + _EPS
        x_right = xs[-1] - sweep_margin - _EPS
        if x_left >= x_right:
            continue

        if going_right:
            p0, p1, yaw = (x_left, y_s), (x_right, y_s), fwd_yaw
        else:
            p0, p1, yaw = (x_right, y_s), (x_left, y_s), rev_yaw

        sx, sy = _rotate(p0[0], p0[1], ca_back, sa_back)
        ex, ey = _rotate(p1[0], p1[1], ca_back, sa_back)
        poses.append((sx, sy, yaw))
        poses.append((ex, ey, yaw))

        going_right = not going_right

    return poses
