# Polished demos and UI patterns for replayt integrators with design-engineering handoff playbook

## Overview

This project builds on **[replayt](https://pypi.org/project/replayt/)**. Read
**[docs/REPLAYT_ECOSYSTEM_IDEA.md](docs/REPLAYT_ECOSYSTEM_IDEA.md)** for positioning prompts, then
**[docs/MISSION.md](docs/MISSION.md)** for scope and goals.

## Design principles

**[docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md)** is the canonical contract for **replayt** and Python support matrices, extension points, deprecation policy, and **LLM** boundaries. For a short integrator digest (supported vs CI-tested, shims, upgrades), see **[docs/compat.md](docs/compat.md)**. For **replayt**’s **browser** bundle (**CDN** vs **npm**/**bundler**), optional **SRI**, and how that aligns with the same **`pyproject.toml`** semver story, see **[docs/FRONTEND_SUPPLY_CHAIN.md](docs/FRONTEND_SUPPLY_CHAIN.md)**.

## Continuous integration

[![CI](https://github.com/flogat/replayt-ux-showcase/actions/workflows/ci.yml/badge.svg)](https://github.com/flogat/replayt-ux-showcase/actions/workflows/ci.yml)

Workflow definition: [`.github/workflows/ci.yml`](.github/workflows/ci.yml). Normative requirements (tests with the **pytest-cov** gate, **ruff**, **replayt** install path, supply chain, badges) are in **[docs/DESIGN_PRINCIPLES.md — GitHub Actions CI workflow](docs/DESIGN_PRINCIPLES.md#github-actions-ci-workflow)**.

## Reference documentation

No snapshot was copied into this checkout. Add markdown under `docs/reference-documentation/` if you want bundled
upstream context, or copy files from a local replayt documentation tree.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

Run **`pytest`** from the **repository root** so **`[tool.pytest.ini_options]`** in **`pyproject.toml`** applies (coverage on **`replayt_ux_showcase.demo`**, fail-under **80**). The **dev** extra pulls in **pytest-cov**; an editable install **without** **`[dev]`** is not enough and **`pytest`** often exits **4** with an unrecognized **`--cov`** argument. Use **`python -m pytest`** from the repo root to match **CI** (same **`[tool.pytest.ini_options]`** as **`pytest`**).

**Tests and coverage policy** (demo module, **replayt** boundaries, **dev** pins) live in
**[docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md)**; **[docs/demo.md](docs/demo.md)** defines the console demo contract.

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
| `docs/FRONTEND_SUPPLY_CHAIN.md` | CDN vs bundled **replayt** (browser), optional **SRI**, **npm**/**Vite** notes; aligns with **`pyproject.toml`** pins |
| `docs/compat.md` | Compatibility matrix digest, CI coverage truth, shims, migration |
| `docs/demo.md` | Console demo contract (`python -m replayt_ux_showcase.demo`) |
| `docs/examples/` | Copy-paste static HTML/JS examples for integrators |
| `docs/examples/PATTERNS.md` | Canonical UI pattern inventory (mission **5+** tracking, per-pattern acceptance criteria) |
| `docs/reference-documentation/` | Optional markdown snapshot for contributors (when present) |
| `src/replayt_ux_showcase/` | Python package (import `replayt_ux_showcase`) |
| `tests/` | Packaging and design-principles contract tests; demo behavior and coverage gates; **`docs/examples/`** **replayt** pin contract |
| `pyproject.toml` | Package metadata, dependencies, **pytest**/**ruff** config |
| `.github/workflows/` | **GitHub Actions** (editable **dev** install, **pytest** with **pytest-cov**, **ruff**, **pip-audit**) |
| `CHANGELOG.md` | Release notes (Keep a Changelog); keep **Unreleased** updated |
| `.gitignore` | Ignores `path/` (doc placeholders), `.orchestrator/`, `.cursor/skills/`, and `AGENTS.md` (local tooling) |
