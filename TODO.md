# TODO

## In Progress
- [ ] add landmass TOML for Scotese PALEOMAP model [data]
- [ ] derive kinematic landmasses from Merdith 2021 model (tested in test_package.py) [data]

## Next

## Backlog

### Data
- [ ] add landmass TOML for Scotese PALEOMAP model [data]
- [ ] collect shallow-marine platform polygons for tetrapod case study [data]

### Analysis & Code
- [ ] implement result.plot() with matplotlib [code]
- [ ] implement result.plotly() for interactive exploration [code]
- [ ] support comparing results across multiple tectonic models [code]
- [ ] implement stepping-stone shortest path between landmasses [code]
- [ ] add --quiet / --progress flags to CLI [code]

### Documentation
- [ ] write API reference docs with autodoc [documentation]
- [ ] write quickstart tutorial for docs site [documentation]
- [ ] add lycopsid case study notebook to docs [documentation]
- [ ] write paper.md and paper.bib for JOSS [documentation]

### CI & Release
- [ ] fix CI/CD workflows to green on GitHub Actions [code]
- [ ] tag v0.1.0 and publish to PyPI [code]

## Blocked
- [ ] JOSS submission (repo must be public and active 6+ months)

## Ideas & Future Work
- [ ] add sub-command paleoconnect compare for multi-model output
- [ ] web frontend with interactive globe (plotly + dash)
- [ ] conda-forge package

## Done (log)
- [X] 2026-08-05 initialize repo from scientific-python/cookie template [code]
- [X] 2026-08-05 implement ConnectivityModel, ConnectivityResult, CLI [code]
- [X] 2026-08-05 add unit tests for ConnectivityResult [code]
- [X] 2026-08-05 add AGENTS.md, README, .gitignore for data/ [documentation]
- [X] 2026-08-05 push to GitHub (public, starts JOSS clock) [code]
- [X] 2026-08-05 refactor ConnectivityModel: derive landmasses from ReconstructionTree, run_path API [code]
