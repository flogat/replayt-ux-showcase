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

**Playwright smoke (static `docs/examples/` demos):** Headless **Chromium** checks **`basic-player.html`** (**P-01**) over **HTTP** with root **`docs/examples/`** — see **`tests/docs_examples_playwright/`** and **[docs/DESIGN_PRINCIPLES.md — docs/examples static demos: Playwright smoke tests](docs/DESIGN_PRINCIPLES.md#docs-examples-static-demos-playwright-smoke-tests)**. **CI** job **`docs-examples-playwright`** runs after **`pip install -e ".[dev]"`** and **`python -m playwright install --with-deps chromium`**, then **`python -m pytest tests/docs_examples_playwright -q --no-cov --browser chromium`**. The main **`test`** job runs **`python -m pytest tests --ignore=tests/docs_examples_playwright`** so the **`demo.py`** **pytest-cov** gate is unchanged.

## Reference documentation

No snapshot was copied into this checkout. Add markdown under `docs/reference-documentation/` if you want bundled
upstream context, or copy files from a local replayt documentation tree.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python -m playwright install chromium
python -m pytest tests --ignore=tests/docs_examples_playwright
python -m pytest tests/docs_examples_playwright --no-cov --browser chromium
```

Run the first **`pytest`** line from the **repository root** so **`[tool.pytest.ini_options]`** in **`pyproject.toml`** applies (coverage on **`replayt_ux_showcase.demo`**, fail-under **80**). **`--ignore=tests/docs_examples_playwright`** matches the main **CI** **`test`** job and keeps **Playwright** off the **cov** **addopts** path. The **dev** extra pulls in **pytest-cov**, **playwright**, and **pytest-playwright**; an editable install **without** **`[dev]`** is not enough and **`pytest`** often exits **4** with an unrecognized **`--cov`** argument. The second **`pytest`** line runs **P-01** smoke only; it needs **`playwright install chromium`** once per machine (**Linux** **CI** uses **`install --with-deps chromium`**). A bare **`pytest`** at the repo root still discovers **`tests/docs_examples_playwright`** and applies **cov** **addopts** to that session—use the two explicit commands above for a **CI**-aligned loop.

**Tests and coverage policy** (demo module, **replayt** boundaries, **dev** pins) live in
**[docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md)**; **[docs/demo.md](docs/demo.md)** defines the console demo contract.

## Optional agent workflows

This repo may include a [`.cursor/skills/`](.cursor/skills/) directory for Cursor-style agent skills. **`.gitignore`**
lists **`path/`** (so documentation-style placeholder paths are never committed), **`.cursor/skills/`**, and related
local tooling entries. Adapt or remove optional directories to match your team’s workflow.

## Reviewer and LLM harness fixture (vanilla)

**[P-05](docs/examples/PATTERNS.md#p-05-offline-deterministic-fixture-page-for-llm-and-reviewer-workflows)** — **`docs/examples/fixture-replay.html`** is a **deterministic**, **inlined** synthetic **`sessionData`** page with **no** runtime session fetch, **no** secrets, and **no** live model calls (see **[LLM boundaries](docs/DESIGN_PRINCIPLES.md#llm-boundaries)**).

**How to open locally:** From the repo, run a static server rooted at **`docs/examples/`** (for example `cd docs/examples && python -m http.server`) and open **`http://127.0.0.1:8000/fixture-replay.html`** (port as shown in the server log). Using **`file://`** may block the pinned **replayt** **CDN** script in some browsers; the local server avoids that. Normative detail: **[P-05 replayt pin and open instructions](docs/examples/PATTERNS.md#p-05-replayt-pin-and-open-instructions-normative)**.

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
| `docs/examples/build.md` | Optional **npm** + **Vite** / **esbuild** local bundler spec (**private** **`package.json`**, **pytest-first** **CI**); not an implied public **npm** package |
| `package.json` | Private **npm** recipe (**Node** 18+): **`npm install`**, **`npm run build`**, **`npm run dev`** (watch), **`npm run preview`** (static server on **127.0.0.1**); **`replayt`** semver matches **`pyproject.toml`** |
| `scripts/replayt-bundler-preview/` | **esbuild** maintainer preview (**`entry.mjs`**, **`build.mjs`**, **`serve.mjs`**, **`index.html`**) |
| `docs/examples/fixture-replay.html` | **P-05** deterministic offline fixture for reviewers / **LLM** harnesses (**Shipped** — **`docs/examples/PATTERNS.md`**) |
| `docs/examples/PATTERNS.md` | Canonical UI pattern inventory (mission **5+** tracking, per-pattern acceptance criteria) |
| `docs/a11y/keyboard-model.md` | Shared **keyboard / focus** checklist for player and timeline embeds (tab order, scrubber keys, **Escape**) |
| `docs/reference-documentation/` | Optional markdown snapshot for contributors (when present) |
| `src/replayt_ux_showcase/` | Python package (import `replayt_ux_showcase`) |
| `tests/` | Packaging and design-principles contract tests; demo behavior and coverage gates; **`docs/examples/`** **replayt** pin contract; **`tests/docs_examples_playwright/`** — **Playwright** smoke for **`basic-player.html`** (**run with `--no-cov`**, see **Quick start**) |
| `pyproject.toml` | Package metadata, dependencies, **pytest**/**ruff** config |
| `.github/workflows/` | **GitHub Actions** (editable **dev** install, **pytest** with **pytest-cov** on **`tests/`** minus **`docs_examples_playwright`**, job **`docs-examples-playwright`**, **ruff**, **pip-audit**) |
| `CHANGELOG.md` | Release notes (Keep a Changelog); keep **Unreleased** updated |
| `.gitignore` | Ignores `path/` (doc placeholders), `.orchestrator/`, `.cursor/skills/`, and `AGENTS.md` (local tooling) |
