from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

import pandas as pd


@dataclass
class ConnectivityResult:
    records: list[dict[str, Any]] = field(default_factory=list)

    def add(
        self,
        time: float,
        landmass_a: str,
        landmass_b: str,
        distance_km: float,
    ) -> None:
        self.records.append(
            {
                "time_ma": time,
                "landmass_a": landmass_a,
                "landmass_b": landmass_b,
                "distance_km": distance_km,
            }
        )

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.records)

    def to_csv(self, path: str | Path) -> None:
        self.to_dataframe().to_csv(path, index=False)

    def summary(self) -> pd.DataFrame:
        df = self.to_dataframe()
        if df.empty:
            return df
        pair_cols = ["landmass_a", "landmass_b"]
        return (
            df.groupby(pair_cols)
            .agg(
                min_km=("distance_km", "min"),
                mean_km=("distance_km", "mean"),
                max_km=("distance_km", "max"),
                time_span=("time_ma", lambda x: f"{x.min():.0f}-{x.max():.0f} Ma"),
            )
            .reset_index()
        )

    def __len__(self) -> int:
        return len(self.records)

    def __bool__(self) -> bool:
        return bool(self.records)
