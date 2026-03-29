# Polished demos and UI patterns for replayt integrators with design-engineering handoff playbook

## Overview

This project builds on **[replayt](https://pypi.org/project/replayt/)**. Read
**[docs/REPLAYT_ECOSYSTEM_IDEA.md](docs/REPLAYT_ECOSYSTEM_IDEA.md)** for positioning prompts, then
**[docs/MISSION.md](docs/MISSION.md)** for scope and goals.

## Design principles

**[docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md)** is the canonical contract for **replayt** and Python support matrices, extension points, deprecation policy, and **LLM** boundaries. For a short integrator digest (supported vs CI-tested, shims, upgrades), see **[docs/compat.md](docs/compat.md)**. For **replayt**’s **browser** bundle (**CDN** vs **npm**/**bundler**), optional **SRI**, and how that aligns with the same **`pyproject.toml`** semver story, see **[docs/FRONTEND_SUPPLY_CHAIN.md](docs/FRONTEND_SUPPLY_CHAIN.md)**.

## Continuous integration

[![CI](https://github.com/flogat/replayt-ux-showcase/actions/workflows/ci.yml/badge.svg)](https://github.com/flogat/replayt-ux-showcase/actions/workflows/ci.yml)

Workflow definition: [`.github/workflows/ci.yml`](.github/workflows/ci.yml). Normative requirements (tests with the **pytest-cov** gate, **ruff**, **replayt** install path, supply chain, badges) are in **[docs/DESIGN_PRINCIPLES.md — GitHub Actions CI workflow](docs/DESIGN_PRINCIPLES.md#github-actions-ci-workflow)**. Optional **Playwright** load smoke for **Shipped** vanilla **`docs/examples/*.html`** runs in the **`examples-playwright-smoke`** job (see **[Static HTML examples: browser smoke (Playwright)](docs/DESIGN_PRINCIPLES.md#static-html-examples-browser-smoke-playwright)** and [Optional Playwright smoke](#optional-playwright-smoke-static-html-examples) below).

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

Run **`pytest`** from the **repository root** so **`[tool.pytest.ini_options]`** in **`pyproject.toml`** applies (coverage on **`replayt_ux_showcase.demo`**, fail-under **80**). Default collection skips **`@pytest.mark.playwright`** tests (**`-m "not playwright"`** in **`addopts`**) so the main suite stays fast and does not require browser binaries. The **dev** extra pulls in **pytest-cov**; an editable install **without** **`[dev]`** is not enough and **`pytest`** often exits **4** with an unrecognized **`--cov`** argument. Use **`python -m pytest`** from the repo root to match **CI** (same **`[tool.pytest.ini_options]`** as **`pytest`**).

**Design-to-code handoff (integrators):** After you can run the Python checks above, use **[`docs/playbook/README.md`](docs/playbook/README.md)** for **Tailwind-friendly** token tables, **timeline and overlay** component anatomy, and a **printable** checklist (accessibility, loading, error states). It links **[`docs/a11y/keyboard-model.md`](docs/a11y/keyboard-model.md)** and **[`docs/examples/PATTERNS.md`](docs/examples/PATTERNS.md)** for normative pattern rules. **Figma** library access, variable → **`rux-*`** mapping, and interim **`design-tokens.json`** live in **[`docs/design-kit/README.md`](docs/design-kit/README.md)** (**F1–F8**).

**Tests and coverage policy** (demo module, **replayt** boundaries, **dev** pins) live in
**[docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md)**; **[docs/demo.md](docs/demo.md)** defines the console demo contract.

**Contributing** (changelog, semver expectations, when to update **DESIGN_PRINCIPLES** with **pins**): **[`CONTRIBUTING.md`](CONTRIBUTING.md)**.

### Optional Playwright smoke (static HTML examples)

Normative detail: **[`docs/DESIGN_PRINCIPLES.md` — Static HTML examples: browser smoke (Playwright)](docs/DESIGN_PRINCIPLES.md#static-html-examples-browser-smoke-playwright)**. Tests live in **`tests/playwright/test_static_html_examples_load.py`** (loopback **HTTP** root **`docs/examples/`**, **Chromium**, fail on **console** **`error`**, **`pageerror`**, and **console** **`warning`** unless allowlisted in that file).

**Local run** (after **`pip install -e ".[dev]"`**):

```bash
python -m playwright install chromium
python -m pytest tests/playwright -q --override-ini="addopts=" --no-cov --browser chromium
```

**CI:** **`jobs.examples-playwright-smoke`** uses **Python 3.12**, **`replayt==0.4.25`** with the same **`-c`** constraint pattern as **`jobs.test`**, then **`python -m playwright install chromium --with-deps`** and the **`pytest`** line above. **`docs/compat.md`** lists **EX-PLAYWRIGHT-SMOKE**.

## Troubleshooting

- **`supply-chain` / `pip-audit` fails in CI:** Reproduce locally with **`pip install -e ".[dev]"`** then the same
  **`pip-audit`** flags as **`.github/workflows/ci.yml`**. See **[`docs/DEPENDENCY_AUDIT.md`](docs/DEPENDENCY_AUDIT.md)**
  for triage (bump vs pin vs upstream issue vs documented **`--ignore-vuln`**). **JavaScript** / **npm** advisories are
  a separate concern — **[`docs/FRONTEND_SUPPLY_CHAIN.md`](docs/FRONTEND_SUPPLY_CHAIN.md)**.

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
| `docs/DEPENDENCY_AUDIT.md` | **`pip-audit`** (**Python** / **PyPI**): **CI** alignment, local reproduction, fix vs pin vs upstream, documented **`--ignore-vuln`** overrides |
| `docs/compat.md` | Compatibility matrix digest, CI coverage truth, shims, migration |
| `docs/demo.md` | Console demo contract (`python -m replayt_ux_showcase.demo`) |
| `docs/examples/` | Copy-paste static HTML/JS examples for integrators |
| `docs/examples/react/` | **P-06** React timeline player + README (**Shipped** — **[`docs/examples/PATTERNS.md`](docs/examples/PATTERNS.md#p-06--react-timeline-player-basic-player--scrubber-parity)**) |
| `docs/examples/vue/` | **P-07** Vue 3 minimal player + scrubber + README (**Shipped** — **[`docs/examples/PATTERNS.md`](docs/examples/PATTERNS.md#p-07--vue-3-timeline-player-basic-player--scrubber-parity)**) |
| `docs/examples/svelte/` | **P-08** Svelte 4 minimal player + scrubber + README (**Shipped** — **[`docs/examples/PATTERNS.md`](docs/examples/PATTERNS.md#p-08--svelte-4-timeline-player-basic-player--scrubber-parity)**) |
| `docs/examples/build.md` | Optional **npm** + **Vite** / **esbuild** local bundler spec (**private** **`package.json`**, **pytest-first** **CI**); not an implied public **npm** package |
| `package.json` | Private **npm** recipe (**Node** 18+): **`npm install`**, **`npm run build`**, **`npm run dev`** (watch), **`npm run preview`** (static server on **127.0.0.1**); **`replayt`** semver matches **`pyproject.toml`** |
| `scripts/replayt-bundler-preview/` | **esbuild** maintainer preview (**`entry.mjs`**, **`build.mjs`**, **`serve.mjs`**, **`index.html`**) |
| `docs/examples/fixture-replay.html` | **P-05** deterministic offline fixture for reviewers / **LLM** harnesses (**Shipped** — **`docs/examples/PATTERNS.md`**) |
| `docs/examples/event-overlay.html` | **P-09** event overlay lane (scrub-linked callouts, hover + keyboard) — **Shipped** (**[`docs/examples/PATTERNS.md`](docs/examples/PATTERNS.md#p-09--event-overlay-lane-scrub-hover-tooltips-keyboard)**) |
| `docs/examples/PATTERNS.md` | Canonical UI pattern inventory (mission **5+** tracking, per-pattern acceptance criteria) |
| `docs/playbook/README.md` | **Design-to-code handoff**: tokens (**[`tokens.md`](docs/playbook/tokens.md)**), anatomy (**[`component-anatomy.md`](docs/playbook/component-anatomy.md)**), printable checklist (**[`handoff-checklist.md`](docs/playbook/handoff-checklist.md)**) |
| `docs/design-kit/README.md` | **Figma** design kit spec: library access, **Figma** → **`rux-*`** mapping (**F3**), change requests, interim **`design-tokens.json`** (**F5**) — see **[`docs/DESIGN_PRINCIPLES.md`](docs/DESIGN_PRINCIPLES.md#design-kit-figma-and-token-export)** |
| `docs/a11y/keyboard-model.md` | Shared **keyboard / focus** checklist for player and timeline embeds (tab order, scrubber keys, **Escape**) |
| `docs/reference-documentation/` | Optional markdown snapshot for contributors (when present) |
| `src/replayt_ux_showcase/` | Python package (import `replayt_ux_showcase`) |
| `tests/` | Packaging and design-principles contract tests; demo behavior and coverage gates; **`docs/examples/`** **replayt** pin contract |
| `pyproject.toml` | Package metadata, dependencies, **pytest**/**ruff** config |
| `.github/workflows/` | **GitHub Actions** (editable **dev** install, **pytest** with **pytest-cov**, **ruff**, **pip-audit**; optional **`examples-playwright-smoke`** — **Playwright** / **Chromium** on **Shipped** **`docs/examples/*.html`**) |
| `CHANGELOG.md` | Release notes (Keep a Changelog); keep **Unreleased** updated |
| `CONTRIBUTING.md` | Contributor guide: **CHANGELOG** / semver, **DESIGN_PRINCIPLES** + pins same change set |
| `.gitignore` | Ignores `path/` (doc placeholders), `.orchestrator/`, `.cursor/skills/`, and `AGENTS.md` (local tooling) |
