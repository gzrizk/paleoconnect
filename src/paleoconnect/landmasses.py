from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import tomllib

if TYPE_CHECKING:
    from collections.abc import Iterator


@dataclass(frozen=True)
class LandmassDefinitions:
    landmasses: dict[str, list[int]] = field(default_factory=dict)

    @classmethod
    def from_toml(cls, path: str | Path) -> LandmassDefinitions:
        data = tomllib.loads(Path(path).read_text())
        return cls(landmasses=data["landmasses"])

    @classmethod
    def from_dict(cls, data: dict[str, list[int]]) -> LandmassDefinitions:
        return cls(landmasses=data)

    @property
    def names(self) -> list[str]:
        return list(self.landmasses.keys())

    @property
    def pairs(self) -> list[tuple[str, str]]:
        return list(itertools.combinations(sorted(self.landmasses), 2))

    def plate_ids(self, name: str) -> list[int]:
        return self.landmasses[name]

    def iter_plate_ids(self) -> Iterator[int]:
        yield from self.landmasses.values()

    def __len__(self) -> int:
        return len(self.landmasses)

    def __contains__(self, name: str) -> bool:
        return name in self.landmasses
