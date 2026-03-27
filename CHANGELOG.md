# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Expanded `docs/DESIGN_PRINCIPLES.md` with canonical “one way” patterns, module boundaries, replayt/showcase version matrices, extension points, deprecation and migration policy, LLM boundaries, and extended audience table (spec-only refinement, phase 2 backlog).
- Defined project mission (users, Replayt role, scope, success metrics with CI tests) in MISSION.md.
- Initial polished demo: basic-player.html (vanilla JS replay player).
- Explicit contracts in DESIGN_PRINCIPLES.md: supported replayt/frameworks versions.
- `demo.py`: console timeline renderer (`python -m replayt_ux_showcase.demo`) with sample session data (12 events, 30s).
- Refined `docs/demo.md` spec: added replayt primitives usage notes, expanded test plan with 5 test cases, integration notes.

## [0.1.0] - 2026-03-25

### Added

- Initial scaffold and package layout.
