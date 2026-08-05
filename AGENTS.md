# AGENTS.md — paleoconnect

## What this is
Python package for palaeogeographic connectivity analysis. Quantifies
minimum oceanic gaps between landmasses (or any geographic entities)
through geological time using pyGPlates plate tectonic models.

## Project layout
```
paleoconnect/
├── pyproject.toml            # PEP 621, hatchling backend, VCS versioning
├── src/paleoconnect/         # Package source (src layout)
│   ├── __init__.py           # Public API
│   ├── model.py              # ConnectivityModel
│   ├── landmasses.py         # LandmassDefinitions
│   ├── result.py             # ConnectivityResult
│   └── cli.py                # CLI entry point
├── tests/                    # Pytest suite
├── docs/                     # Sphinx + MyST documentation
└── data/                     # Not tracked — model files (.rot, .gpml)
```

## Toolchain
- **uv** for dependency management: `uv sync` installs everything
- **ruff** for linting/formatting: `uv run ruff check .`
- **mypy** for static typing: `uv run mypy`
- **pytest** for tests: `uv run pytest`
- **nox** for task runner: `nox -l` lists sessions
- **pre-commit** for git hooks: configured via `.pre-commit-config.yaml`

## Development workflow
```bash
uv sync --group dev      # install deps + dev tools
uv run ruff check .      # lint
uv run mypy              # type check
uv run pytest            # run tests
uv run pre-commit run -a # run all hooks
```

## Data conventions
- Tectonic model files (.rot, .gpml) live in `data/models/` (gitignored)
- Landmass-to-plate-ID mappings: TOML format, see `docs/` for examples
- Users source model files independently (licensing)

## Publication strategy
- Package: PyPI (trusted publisher via GitHub Actions)
- Docs: ReadTheDocs
- Paper: JOSS (Journal of Open Source Software)
- Case studies: separate repos/notebooks
