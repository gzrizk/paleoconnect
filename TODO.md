# TODO

## In Progress
- [ ] implement run_dispersal() API — auto-derive FAD/LAD, order, time range from occurrences [code]

## Next
- [ ] prepare MVP fossil dataset (stage/age/plate_id) for target lineage [data]
- [ ] integrate GTS2020 stage→age lookup [data]
- [ ] integrate paleocoordinate script to resolve plate_id from modern coordinates [code]

## Backlog

### Data
- [ ] add Scotese PALEOMAP model support [data]
- [ ] collect shallow-marine platform polygons for tetrapod case study [data]

### Analysis & Code
- [ ] implement result.plot() with matplotlib [code]
- [ ] implement result.plotly() for interactive exploration [code]
- [ ] support comparing results across multiple tectonic models [code]
- [ ] implement stepping-stone shortest path between landmasses [code]
- [ ] add --quiet / --progress flags to CLI [code]

### Documentation
- [ ] write API reference docs with autodoc [documentation]
- [ ] write quickstart tutorial for docs site (new run_path / run_dispersal API) [documentation]
- [ ] add lycopsid/fern case study notebook to docs [documentation]
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
- [X] 2026-08-05 refactor ConnectivityModel: drop LandmassDefinitions, add run_path() + _find_component() [code]
- [X] 2026-08-05 download Merdith 2021 plate model to data/plate_models/ [data]
- [X] 2026-08-05 rename data/models/ → data/plate_models/ [data]
