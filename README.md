# Polished demos and UI patterns for replayt integrators with design-engineering handoff playbook

Replayt integrators land here for a reference showcase they can copy into real embeds. The repo packages replay UI examples, handoff docs, and a small Python demo surface for teams wiring replay into dashboards and product interfaces.

- **Audience:** Replayt integrators first; contributors and design-to-code handoff reviewers second. Scope and success criteria live in **[docs/MISSION.md](docs/MISSION.md)**.
- **What ships here:** **[Quick start](#quick-start)** for the local checks, copy-paste patterns in **[docs/examples/](docs/examples/)**, the handoff guide in **[docs/playbook/README.md](docs/playbook/README.md)**, design-kit rules in **[docs/design-kit/README.md](docs/design-kit/README.md)**, and the Python demo package in **[`src/replayt_ux_showcase/`](src/replayt_ux_showcase/)**.
- **Out of scope:** **replayt** core capture, storage, and replay APIs; a hosted product or standalone app surface; a published **npm** package or framework SDK. Upstream **replayt** docs stay canonical. Version coverage and upgrade notes live in **[docs/compat.md](docs/compat.md)**.
- **Read next:** **[docs/MISSION.md](docs/MISSION.md)** for repo boundaries, **[docs/compat.md](docs/compat.md)** for supported versions, **[docs/examples/PATTERNS.md](docs/examples/PATTERNS.md)** for shipped pattern inventory, and **[docs/playbook/README.md](docs/playbook/README.md)** for design-dev handoff.

## Overview

This project builds on **[replayt](https://pypi.org/project/replayt/)**. Read
**[docs/REPLAYT_ECOSYSTEM_IDEA.md](docs/REPLAYT_ECOSYSTEM_IDEA.md)** for positioning prompts, then
**[docs/MISSION.md](docs/MISSION.md)** for scope and goals.

## Design principles

**[docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md)** is the canonical contract for **replayt** and Python support matrices, extension points, deprecation policy, and **LLM** boundaries. For a short integrator digest (supported vs CI-tested, shims, upgrades), see **[docs/compat.md](docs/compat.md)**. For **replayt**’s **browser** bundle (**CDN** vs **npm**/**bundler**), optional **SRI**, and how that aligns with the same **`pyproject.toml`** semver story, see **[docs/FRONTEND_SUPPLY_CHAIN.md](docs/FRONTEND_SUPPLY_CHAIN.md)**.

## Continuous integration

[![CI](https://github.com/flogat/replayt-ux-showcase/actions/workflows/ci.yml/badge.svg)](https://github.com/flogat/replayt-ux-showcase/actions/workflows/ci.yml)

Workflow definition: [`.github/workflows/ci.yml`](.github/workflows/ci.yml). Normative requirements (tests with the **pytest-cov** gate, **ruff**, **replayt** install path, supply chain, badges) are in **[docs/DESIGN_PRINCIPLES.md — GitHub Actions CI workflow](docs/DESIGN_PRINCIPLES.md#github-actions-ci-workflow)**. Optional **Playwright** load smoke for **Shipped** vanilla **`docs/examples/*.html`** runs in the **`examples-playwright-smoke`** job (see **[Static HTML examples: browser smoke (Playwright)](docs/DESIGN_PRINCIPLES.md#static-html-examples-browser-smoke-playwright)** and [Optional Playwright smoke](#optional-playwright-smoke-static-html-examples) below).

**Playwright smoke (static `docs/examples/` demos):** Headless **Chromium** checks **`basic-player.html`** (**P-01**) over **HTTP** with root **`docs/examples/`** — see **`tests/docs_examples_playwright/`** and **[docs/DESIGN_PRINCIPLES.md — docs/examples static demos: Playwright smoke tests](docs/DESIGN_PRINCIPLES.md#docs-examples-static-demos-playwright-smoke-tests)**. **CI** job **`docs-examples-playwright`** runs after **`pip install -e ".[dev]"`** and **`python -m playwright install --with-deps chromium`**, then **`python -m pytest tests/docs_examples_playwright -q --no-cov --browser chromium`**. The main **`test`** job runs **`python -m pytest tests --ignore=tests/docs_examples_playwright`** so the **`demo.py`** **pytest-cov** gate is unchanged.

## Reference documentation

Optional **markdown** snapshots of **replayt** upstream docs live under **`docs/reference-documentation/`** (may be
empty except the spec). Normative workflow — **license**, **paths**, **refresh cadence**, **checklist**, optional
**[`scripts/refresh-reference-docs/copy_markdown_snapshots.py`](scripts/refresh-reference-docs/copy_markdown_snapshots.py)**
— is in **[`docs/reference-documentation/README.md`](docs/reference-documentation/README.md)**.
Upstream **PyPI** / project docs remain canonical; bundled files are contributor convenience only.

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

<<<<<<< HEAD
Run **`pytest`** from the **repository root** so **`[tool.pytest.ini_options]`** in **`pyproject.toml`** applies (coverage on **`replayt_ux_showcase.demo`**, fail-under **80**). Default collection skips **`@pytest.mark.playwright`** tests (**`-m "not playwright"`** in **`addopts`**) so the main suite stays fast and does not require browser binaries. The **dev** extra pulls in **pytest-cov**; an editable install **without** **`[dev]`** is not enough and **`pytest`** often exits **4** with an unrecognized **`--cov`** argument. Use **`python -m pytest`** from the repo root to match **CI** (same **`[tool.pytest.ini_options]`** as **`pytest`**).

**Design-to-code handoff (integrators):** After you can run the Python checks above, use **[`docs/playbook/README.md`](docs/playbook/README.md)** for **Tailwind-friendly** token tables, **timeline and overlay** component anatomy, and a **printable** checklist (accessibility, loading, error states). It links **[`docs/a11y/keyboard-model.md`](docs/a11y/keyboard-model.md)** and **[`docs/examples/PATTERNS.md`](docs/examples/PATTERNS.md)** for normative pattern rules. **Figma** library access, variable → **`rux-*`** mapping, interim **`design-tokens.json`**, shipped-example token wiring, and the component inventory live in **[`docs/design-kit/README.md`](docs/design-kit/README.md)** (**F1–F8**, **BC1–BC4**).
=======
Run the first **`pytest`** line from the **repository root** so **`[tool.pytest.ini_options]`** in **`pyproject.toml`** applies (coverage on **`replayt_ux_showcase.demo`**, fail-under **80**). **`--ignore=tests/docs_examples_playwright`** matches the main **CI** **`test`** job and keeps **Playwright** off the **cov** **addopts** path. The **dev** extra pulls in **pytest-cov**, **playwright**, and **pytest-playwright**; an editable install **without** **`[dev]`** is not enough and **`pytest`** often exits **4** with an unrecognized **`--cov`** argument. The second **`pytest`** line runs **P-01** smoke only; it needs **`playwright install chromium`** once per machine (**Linux** **CI** uses **`install --with-deps chromium`**). A bare **`pytest`** at the repo root still discovers **`tests/docs_examples_playwright`** and applies **cov** **addopts** to that session—use the two explicit commands above for a **CI**-aligned loop.
>>>>>>> origin/mc/backlog-ef4adea7

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
| `docs/README.md` | Documentation index — start here for navigation |
| `docs/REPLAYT_ECOSYSTEM_IDEA.md` | Positioning (core-gap / showcase / bridge / combinator prompts) |
| `docs/MISSION.md` | Mission and scope |
| `docs/DESIGN_PRINCIPLES.md` | Design and integration principles |
| `docs/FRONTEND_SUPPLY_CHAIN.md` | CDN vs bundled **replayt** (browser), optional **SRI**, **npm**/**Vite** notes; aligns with **`pyproject.toml`** pins |
| `docs/DEPENDENCY_AUDIT.md` | **`pip-audit`** (**Python** / **PyPI**): **CI** alignment, local reproduction, fix vs pin vs upstream, documented **`--ignore-vuln`** overrides |
| `docs/compat.md` | Compatibility matrix digest, CI coverage truth, shims, migration |
| `docs/demo.md` | Console demo contract (`python -m replayt_ux_showcase.demo`) |
<<<<<<< HEAD
| `docs/examples/` | Copy-paste static HTML/JS examples for integrators |
| `docs/examples/react/` | **P-06** React timeline player + README (**Shipped** — **[`docs/examples/PATTERNS.md`](docs/examples/PATTERNS.md#p-06--react-timeline-player-basic-player--scrubber-parity)**) |
| `docs/examples/vue/` | **P-07** Vue 3 minimal player + scrubber + README (**Shipped** — **[`docs/examples/PATTERNS.md`](docs/examples/PATTERNS.md#p-07--vue-3-timeline-player-basic-player--scrubber-parity)**) |
| `docs/examples/svelte/` | **P-08** Svelte 4 minimal player + scrubber + README (**Shipped** — **[`docs/examples/PATTERNS.md`](docs/examples/PATTERNS.md#p-08--svelte-4-timeline-player-basic-player--scrubber-parity)**) |
| `docs/examples/build.md` | Optional **npm** + **Vite** / **esbuild** local bundler spec (**private** **`package.json`**, **pytest-first** **CI**); not an implied public **npm** package |
| `package.json` | Private **npm** recipe (**Node** 18+): **`npm install`**, **`npm run build`**, **`npm run dev`** (watch), **`npm run preview`** (static server on **127.0.0.1**); **`replayt`** semver matches **`pyproject.toml`** |
| `scripts/replayt-bundler-preview/` | **esbuild** maintainer preview (**`entry.mjs`**, **`build.mjs`**, **`serve.mjs`**, **`index.html`**) |
| `docs/examples/fixture-replay.html` | **P-05** deterministic offline fixture for reviewers / **LLM** harnesses (**Shipped** — **`docs/examples/PATTERNS.md`**) |
| `docs/examples/event-overlay.html` | **P-09** event overlay lane (scrub-linked callouts, hover + keyboard) — **Shipped** (**[`docs/examples/PATTERNS.md`](docs/examples/PATTERNS.md#p-09--event-overlay-lane-scrub-hover-tooltips-keyboard)**) |
| `docs/examples/click-heatmap-canvas.html` | **P-10** click density heatmap on a viewport-sized canvas — **Shipped** (**[`docs/examples/PATTERNS.md`](docs/examples/PATTERNS.md#p-10--click-heatmap-on-static-canvas-session-click-coordinates)**) |
| `docs/examples/PATTERNS.md` | Canonical UI pattern inventory (mission **5+** tracking, per-pattern acceptance criteria) |
| `docs/playbook/README.md` | **Design-to-code handoff**: tokens (**[`tokens.md`](docs/playbook/tokens.md)**), anatomy (**[`component-anatomy.md`](docs/playbook/component-anatomy.md)**), printable checklist (**[`handoff-checklist.md`](docs/playbook/handoff-checklist.md)**) |
| `docs/design-kit/README.md` | **Figma** design kit spec: library access, **Figma** → **`rux-*`** mapping (**F3**), change requests, interim **`design-tokens.json`** (**F5**), shipped examples ↔ **`--rux-*`**, component inventory (**BC1–BC4**) — see **[`docs/DESIGN_PRINCIPLES.md`](docs/DESIGN_PRINCIPLES.md#design-kit-figma-and-token-export)** |
| `docs/a11y/keyboard-model.md` | Shared **keyboard / focus** checklist for player and timeline embeds (tab order, scrubber keys, **Escape**) |
=======
| `docs/examples/` | Copy-paste static HTML/JS examples for integrators (not npm packages—see **Examples** below) |
>>>>>>> origin/mc/backlog-b7eb5287
| `docs/reference-documentation/` | Optional markdown snapshot for contributors (when present) |
| `src/replayt_ux_showcase/` | Python package (import `replayt_ux_showcase`) |
| `tests/` | Packaging and design-principles contract tests; demo behavior and coverage gates; **`docs/examples/`** **replayt** pin contract; **`tests/docs_examples_playwright/`** — **Playwright** smoke for **`basic-player.html`** (**run with `--no-cov`**, see **Quick start**) |
| `pyproject.toml` | Package metadata, dependencies, **pytest**/**ruff** config |
<<<<<<< HEAD
| `.github/workflows/` | **GitHub Actions** (editable **dev** install, **pytest** with **pytest-cov**, **ruff**, **pip-audit**; optional **`examples-playwright-smoke`** — **Playwright** / **Chromium** on **Shipped** **`docs/examples/*.html`**) |
=======
| `.github/workflows/` | **GitHub Actions** (editable **dev** install, **pytest** with **pytest-cov** on **`tests/`** minus **`docs_examples_playwright`**, job **`docs-examples-playwright`**, **ruff**, **pip-audit**) |
>>>>>>> origin/mc/backlog-ef4adea7
| `CHANGELOG.md` | Release notes (Keep a Changelog); keep **Unreleased** updated |
| `CONTRIBUTING.md` | Contributor guide: **CHANGELOG** / semver, **DESIGN_PRINCIPLES** + pins same change set |
| `.gitignore` | Ignores `path/` (doc placeholders), `.orchestrator/`, `.cursor/skills/`, and `AGENTS.md` (local tooling) |

### Examples (`docs/examples/`)

- **[`docs/examples/basic-player.html`](docs/examples/basic-player.html)** — vanilla CSS minimal player layout; reference for the [basic player example contract](docs/DESIGN_PRINCIPLES.md#basic-player-example-contract-static-html).
- **[`docs/examples/tailwind-player.html`](docs/examples/tailwind-player.html)** — **Tailwind** utilities + CSS variables for the same [basic player example contract](docs/DESIGN_PRINCIPLES.md#basic-player-example-contract-static-html); details under [DESIGN_PRINCIPLES — Tailwind backlog traceability](docs/DESIGN_PRINCIPLES.md#backlog-traceability-tailwind-based-player-layout-example).

These files are **illustrative copy-paste** starters only. They are **not** published **npm** packages and do not extend the Python package surface—see [`docs/DESIGN_PRINCIPLES.md` — Module and directory boundaries](docs/DESIGN_PRINCIPLES.md#module-and-directory-boundaries).
