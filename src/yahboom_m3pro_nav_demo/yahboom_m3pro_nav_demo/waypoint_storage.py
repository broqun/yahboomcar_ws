"""Shared helpers for recording and loading named map-frame waypoints (YAML).

Each waypoint may include optional ``patrol_order`` (float/int): lower values are
visited first by ``waypoint_patrol`` when the ``waypoint_order`` parameter is empty.
Alias key ``order`` is accepted when loading / merging and normalized to
``patrol_order`` on write.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import yaml

DEFAULT_REL_SUBPATH = Path('yahboom_m3pro_nav_demo') / 'recorded_waypoints.yaml'


def default_record_path() -> Path:
    """User-writable path under $ROS_HOME (default ~/.ros), works after install."""
    ros_home = Path(os.environ.get('ROS_HOME', str(Path.home() / '.ros')))
    return ros_home / DEFAULT_REL_SUBPATH


def _parse_patrol_order(entry: Dict[str, Any]) -> Optional[float]:
    for key in ('patrol_order', 'order'):
        if key not in entry:
            continue
        try:
            return float(entry[key])
        except (TypeError, ValueError):
            return None
    return None


def _parse_waypoint_entry(entry: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(entry, dict):
        return None
    try:
        out: Dict[str, Any] = {
            'x': float(entry['x']),
            'y': float(entry['y']),
            'yaw': float(entry['yaw']),
        }
    except (KeyError, TypeError, ValueError):
        return None
    po = _parse_patrol_order(entry)
    if po is not None:
        out['patrol_order'] = po
    if 'behavior' in entry:
        out['behavior'] = str(entry['behavior'])
    if 'coverage' in entry and isinstance(entry['coverage'], dict):
        out['coverage'] = entry['coverage']
    return out


def load_waypoints_file(path: Path) -> Tuple[str, Dict[str, Dict[str, Any]]]:
    """Return ``frame_id`` and waypoint dicts with ``x``, ``y``, ``yaw`` and optional ``patrol_order``."""
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
    waypoints: Dict[str, Dict[str, Any]] = {}
    for name, entry in raw.items():
        parsed = _parse_waypoint_entry(entry)
        if parsed is not None:
            waypoints[str(name)] = parsed
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
    """Load existing file (if any), upsert one waypoint, write atomically.

    Preserves ``patrol_order`` when updating an existing name. New names get
    ``max(patrol_order) + 1`` among existing waypoints (default 1 if none).
    """
    if path.is_file():
        with path.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            data = {}
    else:
        data = {}
    raw_wps = data.get('waypoints')
    if not isinstance(raw_wps, dict):
        raw_wps = {}
    frame = frame_id or data.get('frame_id') or 'map'

    old = raw_wps.get(name)
    new_entry: Dict[str, Any] = {'x': float(x), 'y': float(y), 'yaw': float(yaw)}

    if isinstance(old, dict):
        po = _parse_patrol_order(old)
        if po is not None:
            new_entry['patrol_order'] = po
    else:
        max_po = 0.0
        for e in raw_wps.values():
            if not isinstance(e, dict):
                continue
            po = _parse_patrol_order(e)
            if po is not None:
                max_po = max(max_po, po)
        new_entry['patrol_order'] = max_po + 1.0

    raw_wps[name] = new_entry
    save_waypoints_atomic(
        path,
        {
            'frame_id': frame,
            'waypoints': raw_wps,
        },
    )
