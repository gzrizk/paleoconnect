from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

    from .landmasses import LandmassDefinitions

import numpy as np
import pygplates

from .result import ConnectivityResult


@dataclass
class ConnectivityModel:
    rotation_files: list[str | Path]
    topology_files: list[str | Path]
    landmasses: LandmassDefinitions
    anchor_plate_id: int = 0

    _topo_model: Any = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rotation_files = [str(f) for f in self.rotation_files]
        self._topology_files = [str(f) for f in self.topology_files]

        self._topo_model = pygplates.TopologicalModel(
            self._topology_files, self._rotation_files
        )

    def run(
        self,
        start_time: float,
        end_time: float,
        time_step: float = 1.0,
    ) -> ConnectivityResult:
        result = ConnectivityResult()
        plate_to_landmass: dict[int, str] = {}
        for name, ids in self.landmasses.landmasses.items():
            for pid in ids:
                plate_to_landmass[pid] = name

        time = start_time

        while time >= end_time - 1e-9:
            snapshot = self._topo_model.topological_snapshot(time)
            resolved = snapshot.get_resolved_topologies()

            polys_by_landmass: dict[str, list[Any]] = {
                name: [] for name in self.landmasses.names
            }

            for topo in resolved:
                fid = topo.get_feature()
                pid = fid.get_reconstruction_plate_id()
                name = plate_to_landmass.get(pid)
                if name is not None:
                    polys_by_landmass[name].append(
                        topo.get_resolved_boundary()
                    )

            for a, b in self.landmasses.pairs:
                polys_a = polys_by_landmass[a]
                polys_b = polys_by_landmass[b]

                if not polys_a or not polys_b:
                    result.add(time, a, b, np.nan)
                    continue

                min_dist = float("inf")
                for pa in polys_a:
                    for pb in polys_b:
                        d = pygplates.GeometryOnSphere.distance(
                            pa,
                            pb,
                            geometry1_is_solid=True,
                            geometry2_is_solid=True,
                        )
                        if d is not None and d < min_dist:
                            min_dist = d

                if np.isinf(min_dist):
                    result.add(time, a, b, np.nan)
                else:
                    result.add(
                        time,
                        a,
                        b,
                        float(min_dist * pygplates.Earth.mean_radius_in_kms),
                    )

            time -= time_step

        return result
