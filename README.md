# Polished demos and UI patterns for replayt integrators with design-engineering handoff playbook

## Overview

This project builds on **[replayt](https://pypi.org/project/replayt/)**. Read
**[docs/REPLAYT_ECOSYSTEM_IDEA.md](docs/REPLAYT_ECOSYSTEM_IDEA.md)** for positioning prompts, then
**[docs/MISSION.md](docs/MISSION.md)** for scope and goals.

## Design principles

**[docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md)** is the canonical contract for **replayt** and Python support matrices, extension points, deprecation policy, and **LLM** boundaries.

## Continuous integration

[![CI](https://github.com/flogat/replayt-ux-showcase/actions/workflows/ci.yml/badge.svg)](https://github.com/flogat/replayt-ux-showcase/actions/workflows/ci.yml)

Workflow definition: [`.github/workflows/ci.yml`](.github/workflows/ci.yml). Normative requirements (tests with the **pytest-cov** gate, **ruff**, **replayt** install path, supply chain, badges) are in **[docs/DESIGN_PRINCIPLES.md — GitHub Actions CI workflow](docs/DESIGN_PRINCIPLES.md#github-actions-ci-workflow)**.

## Reference documentation

No snapshot was copied into this checkout. Add markdown under `docs/reference-documentation/` if you want bundled
upstream context, or copy files from a local replayt documentation tree.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
pytest
```

**Tests and coverage policy** (demo module, **replayt** boundaries, **dev** pins) live in
**[docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md)**; **`docs/demo.md`** defines the console demo contract.

## Optional agent workflows

This repo may include a [`.cursor/skills/`](.cursor/skills/) directory for Cursor-style agent skills. **`.gitignore`**
lists **`path/`** (so documentation-style placeholder paths are never committed), **`.cursor/skills/`**, and related
local tooling entries. Adapt or remove optional directories to match your team’s workflow.

## Project layout

| Path | Purpose |
| ---- | ------- |
| `docs/REPLAYT_ECOSYSTEM_IDEA.md` | Positioning (core-gap / showcase / bridge / combinator prompts) |
| `docs/MISSION.md` | Mission and scope |
| `docs/DESIGN_PRINCIPLES.md` | Design and integration principles |
| `docs/reference-documentation/` | Optional markdown snapshot for contributors (when present) |
| `src/replayt_ux_showcase/` | Python package (import `replayt_ux_showcase`) |
| `pyproject.toml` | Package metadata |
| `CHANGELOG.md` | Release notes (Keep a Changelog); keep **Unreleased** updated |
| `.gitignore` | Ignores `path/` (doc placeholders), `.orchestrator/`, `.cursor/skills/`, and `AGENTS.md` (local tooling) |
