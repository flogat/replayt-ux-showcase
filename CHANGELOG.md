# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- `tests/test_design_principles_contract.py`: **`[dev]`** optional dependencies must be exactly **pytest**, **ruff**, **pip-audit**; CI must keep **`pip install -e ".[dev]"`** (phase 3, Pin replayt dependency and dev tools in pyproject.toml).
- `docs/DESIGN_PRINCIPLES.md`: traceability rows for those contract checks (same backlog).
- `pyproject.toml`: **replayt** bounded to `>=0.1.0,<0.5.0` (PEP 508); `tests/test_design_principles_contract.py` enforces version constraints on **`[project].dependencies`**, **`[project.optional-dependencies].dev`**, and **`[build-system].requires`**, plus **replayt** import smoke (phase 3, Pin replayt dependency and dev tools in pyproject.toml).
- `docs/DESIGN_PRINCIPLES.md`: **Replayt and Python matrix** and traceability table aligned with the declared **replayt** range and new contract checks (same backlog).
- `docs/demo.md`: implementation and integration notes reference the same **replayt** PEP 508 range as `pyproject.toml` (same backlog).
- `tests/test_design_principles_contract.py`: asserts replayt API boundary subsection, packaged **`replayt_ux_showcase`** extension row, and release/automation audience rows; traceability table in `docs/DESIGN_PRINCIPLES.md` lists these checks (phase 3, Expand DESIGN_PRINCIPLES.md with canonical patterns).
- `docs/DESIGN_PRINCIPLES.md`: traceability to `tests/test_design_principles_contract.py`, explicit **replayt** Python API boundary, extension point for packaged **`replayt_ux_showcase`** surface, and audience rows for release consumers and LLM/automation tooling (phase 2, Expand DESIGN_PRINCIPLES.md with canonical patterns).

### Documentation

- `docs/DESIGN_PRINCIPLES.md`: normative [Demo module testing and replayt integration boundaries](docs/DESIGN_PRINCIPLES.md#demo-module-testing-and-replayt-integration-boundaries) — 80% line coverage on `demo.py`, boundary-break semantics, **pytest-cov** as planned **dev** dependency with builder checklist; traceability row for this backlog (phase 2, Add unit/integration tests for demo).
- `docs/demo.md`: automated test plan aligned with design principles; coverage gate called out with link to spec.
- `README.md`: quick start runs **`pytest`**; pointer to design principles for test/coverage policy (same backlog).
- `docs/DESIGN_PRINCIPLES.md`: dependency pins and dev toolchain (PEP 508 vs caret wording, no loose direct deps, dev optional set table); traceability to `tests/test_design_principles_contract.py` including **replayt** specifier (`>=0.1.0` and `<0.5` cap); backlog-to-spec mapping, **`pip install -e ".[dev]"`** quoting note, and phase-3 builder checklist for “Pin replayt dependency and dev tools in pyproject.toml” (phase 2 spec lead).

### Added

- Pytest contract checks: `pyproject.toml` replayt pin and `requires-python`, CI Python version, and required headings in `docs/DESIGN_PRINCIPLES.md` stay consistent with the documented matrices (phase 3 backlog).
- Expanded `docs/DESIGN_PRINCIPLES.md` with canonical “one way” patterns, module boundaries, replayt/showcase version matrices, extension points, deprecation and migration policy, LLM boundaries, and extended audience table (spec-only refinement, phase 2 backlog).
- Defined project mission (users, Replayt role, scope, success metrics with CI tests) in MISSION.md.
- Initial polished demo: basic-player.html (vanilla JS replay player).
- Explicit contracts in DESIGN_PRINCIPLES.md: supported replayt/frameworks versions.
- `demo.py`: console timeline renderer (`python -m replayt_ux_showcase.demo`) with sample session data (12 events, 30s).
- Refined `docs/demo.md` spec: added replayt primitives usage notes, expanded test plan with 5 test cases, integration notes.

## [0.1.0] - 2026-03-25

### Added

- Initial scaffold and package layout.
