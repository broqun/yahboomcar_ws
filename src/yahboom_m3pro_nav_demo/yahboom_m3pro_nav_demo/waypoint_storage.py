"""Shared helpers for recording and loading named map-frame waypoints (YAML)."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Tuple

import yaml

DEFAULT_REL_SUBPATH = Path('yahboom_m3pro_nav_demo') / 'recorded_waypoints.yaml'


def default_record_path() -> Path:
    """User-writable path under $ROS_HOME (default ~/.ros), works after install."""
    ros_home = Path(os.environ.get('ROS_HOME', str(Path.home() / '.ros')))
    return ros_home / DEFAULT_REL_SUBPATH


def load_waypoints_file(path: Path) -> Tuple[str, Dict[str, Dict[str, float]]]:
    if not path.is_file():
        return 'map', {}
    with path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        return 'map', {}
    frame_id = data.get('frame_id') or 'map'
    raw = data.get('waypoints') or {}
    if not isinstance(raw, dict):
        return str(frame_id), {}
    waypoints: Dict[str, Dict[str, float]] = {}
    for name, entry in raw.items():
        if not isinstance(entry, dict):
            continue
        try:
            waypoints[str(name)] = {
                'x': float(entry['x']),
                'y': float(entry['y']),
                'yaw': float(entry['yaw']),
            }
        except (KeyError, TypeError, ValueError):
            continue
    return str(frame_id), waypoints


def save_waypoints_atomic(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(
        prefix='waypoints_', suffix='.yaml', dir=str(path.parent), text=True
    )
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            yaml.safe_dump(
                data,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def merge_waypoint(
    path: Path, name: str, x: float, y: float, yaw: float, frame_id: str = 'map'
) -> None:
    """Load existing file (if any), upsert one waypoint, write atomically."""
    existing_frame, wps = load_waypoints_file(path)
    frame = frame_id or existing_frame
    wps[name] = {'x': float(x), 'y': float(y), 'yaw': float(yaw)}
    save_waypoints_atomic(
        path,
        {
            'frame_id': frame,
            'waypoints': wps,
        },
    )
