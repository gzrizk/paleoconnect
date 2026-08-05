# paleoconnect

[![Actions Status][actions-badge]][actions]
[![PyPI version][pypi-badge]][pypi]
[![Documentation Status][rtd-badge]][rtd]

**Palaeogeographic connectivity analysis for biogeographic dispersal studies.**

Quantify the minimum oceanic gap between geographic entities
(continents, shallow marine platforms, island arcs) through geological time
using pyGPlates plate tectonic reconstructions.

## Installation

```bash
pip install paleoconnect
```

For plotting support:

```bash
pip install "paleoconnect[plot]"
```

## Quickstart

```python
from paleoconnect import ConnectivityModel, LandmassDefinitions

defs = LandmassDefinitions.from_dict({
    "euramerica": [101, 102],
    "south_china": [311, 312],
})

model = ConnectivityModel(
    rotation_files=["model.rot"],
    topology_files=["model.gpml"],
    landmasses=defs,
)

result = model.run(start_time=359, end_time=252, time_step=1)
result.to_csv("gaps.csv")
print(result.summary())
```

## Documentation

Full documentation at [paleoconnect.readthedocs.io][rtd].

## License

BSD-3-Clause. See [LICENSE](LICENSE).

[actions-badge]: https://github.com/gzrizk/paleoconnect/workflows/CI/badge.svg
[actions]: https://github.com/gzrizk/paleoconnect/actions
[pypi-badge]: https://img.shields.io/pypi/v/paleoconnect.svg
[pypi]: https://pypi.org/project/paleoconnect/
[rtd-badge]: https://readthedocs.org/projects/paleoconnect/badge/
[rtd]: https://paleoconnect.readthedocs.io/
