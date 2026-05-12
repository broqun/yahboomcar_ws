"""Unit tests for the boustrophedon room_coverage generator."""

import math
from yahboom_m3pro_nav_demo.room_coverage import generate_coverage_poses


# ---- helpers ---------------------------------------------------------------

def _all_inside_polygon(poses, polygon, tol=1e-6):
    """Ray-casting point-in-polygon for every pose (x, y)."""
    from functools import reduce
    n = len(polygon)
    for x, y, _ in poses:
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = polygon[i]
            xj, yj = polygon[j]
            if ((yi > y) != (yj > y)) and (
                x < (xj - xi) * (y - yi) / (yj - yi + 1e-30) + xi
            ):
                inside = not inside
            j = i
        assert inside, f'Pose ({x:.4f}, {y:.4f}) outside polygon'


def _min_dist_to_edges(px, py, polygon):
    """Minimum distance from (px, py) to any polygon edge."""
    best = float('inf')
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        len_sq = dx * dx + dy * dy
        if len_sq < 1e-12:
            dist = math.hypot(px - x1, py - y1)
        else:
            t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / len_sq))
            proj_x = x1 + t * dx
            proj_y = y1 + t * dy
            dist = math.hypot(px - proj_x, py - proj_y)
        best = min(best, dist)
    return best


# ---- rectangle tests -------------------------------------------------------

class TestRectangle:
    RECT = [[0, 0], [4, 0], [4, 3], [0, 3]]

    def test_basic_output(self):
        poses = generate_coverage_poses(self.RECT, stripe_width=0.5)
        assert len(poses) >= 4, f'Expected >=4 poses, got {len(poses)}'
        assert len(poses) % 2 == 0, 'Poses should come in start/end pairs'

    def test_poses_inside_polygon(self):
        poses = generate_coverage_poses(self.RECT, stripe_width=0.5)
        _all_inside_polygon(poses, self.RECT)

    def test_margin_respected(self):
        margin = 0.3
        poses = generate_coverage_poses(
            self.RECT, stripe_width=0.5, sweep_margin=margin
        )
        assert len(poses) > 0
        for x, y, _ in poses:
            d = _min_dist_to_edges(x, y, self.RECT)
            assert d >= margin - 0.05, (
                f'Pose ({x:.3f},{y:.3f}) only {d:.3f}m from edge, '
                f'expected >={margin - 0.05:.3f}'
            )

    def test_zigzag_alternation(self):
        """Consecutive stripe endpoints should alternate X direction."""
        poses = generate_coverage_poses(self.RECT, stripe_width=0.5)
        for i in range(0, len(poses) - 2, 2):
            sx1, _, _ = poses[i]
            ex1, _, _ = poses[i + 1]
            sx2, _, _ = poses[i + 2]
            dir1 = ex1 - sx1
            dir2 = poses[i + 3][0] - sx2
            assert dir1 * dir2 < 0, (
                f'Stripes {i // 2} and {i // 2 + 1} should alternate direction'
            )

    def test_yaw_matches_direction(self):
        poses = generate_coverage_poses(self.RECT, stripe_width=0.5)
        for i in range(0, len(poses), 2):
            sx, sy, yaw = poses[i]
            ex, ey, _ = poses[i + 1]
            expected = math.atan2(ey - sy, ex - sx)
            diff = abs(math.atan2(math.sin(yaw - expected), math.cos(yaw - expected)))
            assert diff < 0.1, (
                f'Stripe {i // 2}: yaw={yaw:.3f} vs expected={expected:.3f}'
            )

    def test_entry_pose_determines_start_side(self):
        left_entry = (0.1, 1.5, 0.0)
        right_entry = (3.9, 1.5, 0.0)
        poses_l = generate_coverage_poses(
            self.RECT, stripe_width=0.5, entry_pose=left_entry
        )
        poses_r = generate_coverage_poses(
            self.RECT, stripe_width=0.5, entry_pose=right_entry
        )
        assert poses_l[0][0] < 2.0, 'Left entry → first pose on left side'
        assert poses_r[0][0] > 2.0, 'Right entry → first pose on right side'

    def test_stripe_angle(self):
        poses_0 = generate_coverage_poses(self.RECT, stripe_width=0.5, stripe_angle_deg=0)
        poses_90 = generate_coverage_poses(self.RECT, stripe_width=0.5, stripe_angle_deg=90)
        assert len(poses_0) > 0
        assert len(poses_90) > 0
        yaws_0 = {round(p[2], 2) for p in poses_0}
        yaws_90 = {round(p[2], 2) for p in poses_90}
        assert yaws_0 != yaws_90, 'Different angles should yield different yaws'


# ---- concave (L-shape) test ------------------------------------------------

class TestConcavePolygon:
    L_SHAPE = [[0, 0], [4, 0], [4, 2], [2, 2], [2, 4], [0, 4]]

    def test_poses_non_empty(self):
        poses = generate_coverage_poses(self.L_SHAPE, stripe_width=0.5)
        assert len(poses) >= 2

    def test_poses_inside(self):
        poses = generate_coverage_poses(self.L_SHAPE, stripe_width=0.5)
        _all_inside_polygon(poses, self.L_SHAPE)


# ---- edge cases ------------------------------------------------------------

class TestEdgeCases:
    def test_degenerate_polygon(self):
        assert generate_coverage_poses([[0, 0], [1, 0]], stripe_width=0.5) == []

    def test_zero_stripe_width(self):
        rect = [[0, 0], [4, 0], [4, 3], [0, 3]]
        assert generate_coverage_poses(rect, stripe_width=0) == []

    def test_margin_too_large(self):
        tiny = [[0, 0], [1, 0], [1, 0.3], [0, 0.3]]
        assert generate_coverage_poses(tiny, stripe_width=0.1, sweep_margin=0.2) == []
