# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Documentation

- `docs/DESIGN_PRINCIPLES.md`: dependency pin and dev-toolchain acceptance criteria (PEP 508 vs caret wording, no loose direct deps, dev optional set table, traceability for future contract tests) for backlog “Pin replayt dependency and dev tools in pyproject.toml” (phase 2 spec).

### Changed

- `tests/test_design_principles_contract.py`: asserts replayt API boundary subsection, packaged **`replayt_ux_showcase`** extension row, and release/automation audience rows; traceability table in `docs/DESIGN_PRINCIPLES.md` lists these checks (phase 3, Expand DESIGN_PRINCIPLES.md with canonical patterns).
- `docs/DESIGN_PRINCIPLES.md`: traceability to `tests/test_design_principles_contract.py`, explicit **replayt** Python API boundary, extension point for packaged **`replayt_ux_showcase`** surface, and audience rows for release consumers and LLM/automation tooling (phase 2, Expand DESIGN_PRINCIPLES.md with canonical patterns).
- `docs/REPLAYT_ECOSYSTEM_IDEA.md` pitch: compatibility and CI wording matches **DESIGN_PRINCIPLES.md** (supported ranges vs verified-in-CI, pytest contract) (phase 5, architect review, Expand DESIGN_PRINCIPLES.md with canonical patterns).
- `docs/demo.md`: integration notes label matches principle names in **DESIGN_PRINCIPLES.md** (phase 5, same backlog).
- `README.md`: **MISSION.md** is no longer described as stub content (phase 5, same backlog).

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
