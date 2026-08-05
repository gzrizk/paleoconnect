from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

import numpy as np
import pygplates

from .result import ConnectivityResult


@dataclass
class ConnectivityModel:
    rotation_files: list[str | Path]
    topology_files: list[str | Path]

    _topo_model: Any = field(init=False, repr=False)
    _rotation_model: Any = field(init=False, repr=False)

    def __post_init__(self) -> None:
        rot_strs = [str(f) for f in self.rotation_files]
        topo_strs = [str(f) for f in self.topology_files]
        self._rotation_model = pygplates.RotationModel(rot_strs)
        self._topo_model = pygplates.TopologicalModel(topo_strs, rot_strs)

    def run_path(
        self,
        proxies: list[int],
        names: list[str],
        start_time: float,
        end_time: float,
        time_step: float = 1.0,
    ) -> ConnectivityResult:
        result = ConnectivityResult()
        t = start_time

        while t >= end_time - 1e-9:
            components = [self._find_component(t, pid) for pid in proxies]

            for i in range(len(proxies) - 1):
                if components[i] == components[i + 1]:
                    result.add(t, names[i], names[i + 1], 0.0)
                else:
                    gap = self._compute_gap(t, components[i], components[i + 1])
                    result.add(t, names[i], names[i + 1], gap)

            t -= time_step

        return result

    def _find_component(self, time: float, plate_id: int) -> frozenset[int]:
        tree = self._rotation_model.get_reconstruction_tree(
            time, anchor_plate_id=plate_id
        )
        component: set[int] = {plate_id}
        for edge in tree.get_edges():
            component.add(edge.get_moving_plate_id())
            component.add(edge.get_fixed_plate_id())
        return frozenset(component)

    def _compute_gap(
        self, time: float, plates_a: frozenset[int], plates_b: frozenset[int]
    ) -> float:
        snapshot = self._topo_model.topological_snapshot(time)
        polys_a: list[Any] = []
        polys_b: list[Any] = []

        for topo in snapshot.get_resolved_topologies():
            pid = topo.get_feature().get_reconstruction_plate_id()
            if pid in plates_a:
                polys_a.append(topo.get_resolved_boundary())
            elif pid in plates_b:
                polys_b.append(topo.get_resolved_boundary())

        if not polys_a or not polys_b:
            return float("nan")

        min_d = float("inf")
        for pa in polys_a:
            for pb in polys_b:
                d = pygplates.GeometryOnSphere.distance(
                    pa, pb, geometry1_is_solid=True, geometry2_is_solid=True
                )
                if d is not None and d < min_d:
                    min_d = d

        if np.isinf(min_d):
            return float("nan")
        return float(min_d * pygplates.Earth.mean_radius_in_kms)
