# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Phase **3** (*Figma design kit stub: tokens export + link from docs*): **`docs/design-kit/design-tokens.json`** — interim export (**`schemaVersion`**, **`exportDate`**, **`tokens[]`**) aligned with **[`docs/playbook/tokens.md`](docs/playbook/tokens.md)**; **`tests/test_design_kit_docs.py`** — **CI** contract for **F1–F8** headings, **F3** semantics coverage, JSON shape, cross-links, **CHANGELOG** **Unreleased** mention; **`docs/DESIGN_PRINCIPLES.md`** — **`docs/design-kit/`** row now references **`test_design_kit_docs.py`**; **`docs/design-kit/README.md`** operator sections **F1–F8** and **F3** mapping table; **`docs/playbook/README.md`** **CI** note; **`README.md`** **Quick start** wording for the design kit.

### Documentation

- Phase **2** spec (*Figma design kit stub: tokens export + link from docs*): **`docs/design-kit/README.md`** — acceptance **F1–F8** (library access, duplication, **Figma** → **`rux-*`** mapping vs **[`docs/playbook/tokens.md`](docs/playbook/tokens.md)**, change requests, interim **`design-tokens.json`** schema and versioning); **`docs/DESIGN_PRINCIPLES.md`** — traceability row, **`docs/`** module boundary, [Design kit (Figma) and token export](docs/DESIGN_PRINCIPLES.md#design-kit-figma-and-token-export) + backlog traceability table; cross-links from **`docs/playbook/README.md`**, **`docs/playbook/tokens.md`**, **`README.md`** (**Quick start** + layout), **`docs/MISSION.md`**, **`docs/compat.md`**.
- Phase **5** architecture review (*Figma design kit stub: tokens export + link from docs*): **`docs/compat.md`** — vanilla catalog blurb now matches default **CI**: **`tests/test_design_kit_docs.py`** runs with **`pytest`** (replaces stale “**CI** optional” wording for the design kit).

### Changed

- Phase **3** (*Expand compatibility matrix with explicit CI matrix job per row*): **`.github/workflows/ci.yml`** — **`test`** job **`python-version`** × **`replayt-version`** matrix (**0.1.0**, **0.2.0**, **0.4.25**) with **`pip install -e ".[dev]" -c`** constraint file and **`replayt.__version__`** check; **`docs/compat.md`** — inventory IDs **EX-311-RT-*** / **EX-312-RT-*** plus bundled **EX-EXAMPLES-PINS**; **`docs/DESIGN_PRINCIPLES.md`** — matrix / CI exercise row / traceability updates; **`tests/test_design_principles_contract.py`** — `test_ci_test_job_matrix_matches_design_principles_matrix`, `test_compat_ci_exercise_inventory_ids_match_ci_matrix`.

### Documentation

- Phase **5** architecture review (*Add Vue and Svelte minimal player examples alongside React*): **`docs/DESIGN_PRINCIPLES.md`** — **Fails on boundary breaks** pin-scan row and contract-test user story glob updated to **`docs/examples/**/*.{html,md,vue,svelte}`** (matches **`tests/test_docs_examples_replayt_pins.py`** and [Scope (files)](docs/DESIGN_PRINCIPLES.md#scope-files)); **`CHANGELOG.md`** **Unreleased** **Added** bullet for that test updated for the same glob.
- Phase **2** spec (*Add Vue and Svelte minimal player examples alongside React*): **`docs/examples/PATTERNS.md`** — **P-07** (**Vue 3**) and **P-08** (**Svelte 4**) registered as **Spec only** (same **`sessionData`** / **`replayt.player.init`** contract as **P-01**, scrubber intent aligned with **P-03**/**P-06**, **Vite**, **`private`** subtree **`package.json`**, documented **`npm run build`**, README non-goal / directory-boundary language); **`docs/MISSION.md`** framework metrics table; **`docs/DESIGN_PRINCIPLES.md`** — **Showcase stack matrix** **Vue**/**Svelte** rows, **Vanilla UI pattern catalog** blurb, **backlog traceability** subsection; **`docs/compat.md`** digest; **`README.md`** project layout rows for planned **`vue/`** and **`svelte/`** paths.
- Phase **5** architecture review (*Expand compatibility matrix with explicit CI matrix job per row*): **`docs/compat.md`** — **CI matrix coverage** table: example-pin contract tests run per **Python** × **replayt** cell, not per **Python** version alone.
- Phase **2** spec (*Author design-to-code handoff playbook (checklist + tokens)*): **`docs/playbook/`** — **[`README.md`](docs/playbook/README.md)** (index), **[`tokens.md`](docs/playbook/tokens.md)** (spacing / typography / color → **`--rux-*`** CSS variables + **Tailwind `theme.extend`** names), **[`component-anatomy.md`](docs/playbook/component-anatomy.md)** (timeline/scrubber + overlay regions, **P-03** / **P-06** / **P-04** ties), **[`handoff-checklist.md`](docs/playbook/handoff-checklist.md)** (printable accessibility, loading, error sections); **`README.md`** **Quick start** integrator link; **`docs/DESIGN_PRINCIPLES.md`** traceability row, module-boundary note, **Vanilla UI pattern catalog** cross-link, and **backlog traceability** table; **`docs/MISSION.md`**, **`docs/compat.md`**, **`docs/examples/PATTERNS.md`** cross-links.

### Added

- Phase **3** (*Add Vue and Svelte minimal player examples alongside React*): **`docs/examples/vue/`** (**P-07**) and **`docs/examples/svelte/`** (**P-08**) — **Vue 3** and **Svelte 4** + **Vite** timeline players with the same **`sessionData`** / **`replayt.player.init`** contract as **`basic-player.html`**, **P-03**-style **`requestAnimationFrame`** scrub throttling, **Limitations** copy, **`private`** subtree **`package.json`**, pinned **replayt** CDN in **`index.html`**, **`README.md`** runbooks; **`tests/test_examples.py`** file-presence and contract markers; **`tests/test_docs_examples_replayt_pins.py`** scans **`*.vue`** and **`*.svelte`**; **`docs/examples/PATTERNS.md`**, **`docs/MISSION.md`**, **`README.md`**, **`docs/compat.md`**, **`docs/DESIGN_PRINCIPLES.md`** updated for **Shipped** rows.
- Phase **3** (*Author design-to-code handoff playbook (checklist + tokens)*): **`tests/test_playbook_docs.py`** — contract tests for **`docs/playbook/`** (sections and acceptance markers **T1–T3** / **A1–A3** / **H1–H3**, **README** index links, **README.md** quick start, **DESIGN_PRINCIPLES** traceability); **`docs/playbook/README.md`** **CI** note; **`docs/DESIGN_PRINCIPLES.md`** and **`docs/compat.md`** traceability for the new test module.
- **`docs/examples/basic-player.html`** (**P-01**): layout and chrome use **`--rux-*`** semantic variables from **[`docs/playbook/tokens.md`](docs/playbook/tokens.md)** with **`--replayt-primary: var(--rux-color-primary)`** for player theming (phase **3**, same backlog).
- **`docs/examples/react/`** — **P-06** **Shipped**: **React 18** + **Vite** timeline scrubber + **`replayt.player.init`** (pinned **replayt** CDN in **`index.html`**), fixed **`sessionData`** literals, **P-03**-style **requestAnimationFrame** throttling and seek hooks, **Limitations** copy, **`README.md`** (copy-paste, pins, runbook, non-goal); **`tests/test_examples.py`** file-presence + contract markers; **`docs/examples/PATTERNS.md`**, **`docs/MISSION.md`**, **`README.md`**, **`docs/compat.md`**, **`docs/demo.md`**, **`docs/DESIGN_PRINCIPLES.md`** updated for **Shipped** (phase **3**, *Ship React timeline player snippet under docs/examples/react/*).
- Optional **npm** bundler recipe (phase **3**, *Optional npm workspace or build recipe without publishing a package*): repository-root **`package.json`** (**`"private": true`**, **`name`**: **`ux-showcase-examples-bundler`**), direct **`replayt`** **`>=0.1.0 <0.5.0`**, **`esbuild`** devDependency, scripts **`build`** / **`dev`** / **`preview`**; **`scripts/replayt-bundler-preview/`** (**`entry.mjs`**, **`build.mjs`**, **`serve.mjs`**, **`index.html`**) bundles **`replayt/dist/player.min.js`** into **`dist/bundler-preview/`**; **`.gitignore`** **`node_modules/`**; **`tests/test_optional_npm_bundler_recipe.py`** contract tests; **`docs/examples/build.md`** contributor path and automated-checks note; **`docs/DESIGN_PRINCIPLES.md`** traceability row; **`README.md`** layout rows.
- `tests/test_examples.py`: contract asserts **`docs/a11y/keyboard-model.md`** exists with core section headings and that **P-01**–**P-05** **`docs/examples/*.html`** plus **`docs/examples/PATTERNS.md`** reference **`keyboard-model.md`** (phase **3**, *Keyboard and focus model for timeline/player controls*).
- `docs/examples/fixture-replay.html`: **P-05** vanilla example — **deterministic** header comment, **inlined** synthetic **`sessionData`** (fixed timestamps and ids), **no** `fetch(` / **`Date.now`** / **`Math.random`** in source, **`replayt.player.init`** only; pinned **replayt** on **jsDelivr** (phase **3**, *Offline deterministic fixture page for LLM and reviewer workflows*).
- `tests/test_examples.py`: asserts **`fixture-replay.html`** exists and keeps minimal **P-05** contract markers aligned with **`docs/examples/PATTERNS.md`** (same backlog, phase **3**).
- `tests/test_frontend_supply_chain_doc.py`: contract tests for **`docs/FRONTEND_SUPPLY_CHAIN.md`** (section anchors, **pip-audit** vs **JS** keywords, **README** / **DESIGN_PRINCIPLES** / **compat** links, **CHANGELOG** **Unreleased** mention per doc **A1–A5**; phase **3**, *Document CDN vs bundled replayt with SRI and supply-chain notes*).
- `docs/examples/embed-container-states.html`: **P-04** vanilla example — async `sessionData` (simulated delay), skeleton UI with **Loading replay…**, user-visible **network** vs **invalid payload** errors, focusable **Retry**, **`role="status"`** / **`aria-live="polite"`** announcement contract, optional **`data-demo-state`** on **`#embed-shell`**; **`replayt.player.init`** only (backlog phase **3**, *Empty, loading, and failure states for the embed container*).
- `tests/test_examples.py`: asserts **`embed-container-states.html`** exists and keeps minimal **P-04** contract markers aligned with **`docs/examples/PATTERNS.md`** (same backlog, phase **3**).
- `docs/examples/timeline-scrubber.html`: **P-03** vanilla example — `sessionData.events` + `metadata` time range, defensive sort-by-timestamp comment, `requestAnimationFrame`-throttled scrub seeks with final commit on `change` / `pointerup`, optional `seekToMs` / `goto` seek hooks, visible **Limitations** note for CDN builds (backlog phase **3**, *Timeline scrubber strip example using replayt public events API*).
- `tests/test_examples.py`: asserts **`timeline-scrubber.html`** exists and keeps minimal **P-03** contract markers aligned with **`docs/examples/PATTERNS.md`** (same backlog, phase **3**).
- `docs/examples/player-session-metadata-bar.html`: **P-02** vanilla example — metadata bar above the player, same **`sessionData`** shape as **`basic-player.html`**, loading placeholder, user-visible errors when **`sessionId`** / **`durationMs`** / **`viewport`** are missing or invalid after load, and bar focusable controls before the player in DOM order (backlog phase **3**, *Ship session metadata chrome pattern (viewport, duration, session id)*).
- `tests/test_examples.py`: asserts **`player-session-metadata-bar.html`** exists and keeps minimal **P-02** contract markers (loading copy, validation strings, tab-order comment, **replayt** script pin) aligned with **`docs/examples/PATTERNS.md`** (same backlog, phase **3**).
- `tests/test_docs_examples_replayt_pins.py`: **pytest** contract for **`docs/examples/**/*.{html,md,vue,svelte}`** — **replayt** CDN (`replayt@…`) and PEP 508-style pins checked against the **`replayt`** line in **`pyproject.toml`**, with **`<!-- replayt-examples:pin-exempt -->`** skipping the next script line, URL line, or fenced block (backlog phase 3, Contract test: examples reference replayt in supported semver range).

### Documentation

- Phase **2** spec (*Optional npm workspace or build recipe without publishing a package*): **`docs/examples/build.md`** — optional root **`package.json`** (**`private`**) + **Vite** or **esbuild** local preview, **pytest-first** **CI**, **npm** semver alignment with **`pyproject.toml`**, deliverables **B1**–**B8** / acceptance **C1**–**C4**; cross-links and traceability in **`docs/DESIGN_PRINCIPLES.md`** (module boundaries, **Showcase stack matrix**, **Frontend supply chain** backlog table), **`docs/FRONTEND_SUPPLY_CHAIN.md`**, **`README.md`**, **`docs/compat.md`**, **`docs/examples/PATTERNS.md`**.
- Phase **2** spec (*Keyboard and focus model for timeline/player controls*): **`docs/a11y/keyboard-model.md`** — tab order, roving **`tabindex`** for future event-list composites, scrubber (**Arrow** / **Home** / **End** / **Page Up / Page Down**) and **Escape** behavior, focus visibility, cross-pattern Builder checklist; linked from **`docs/examples/basic-player.html`**, **`fixture-replay.html`**, **P-02** / **P-03** / **P-04** comment blocks, **`docs/examples/PATTERNS.md`**, **`docs/DESIGN_PRINCIPLES.md`** (traceability row + **Vanilla UI pattern catalog** + backlog traceability table), **`docs/MISSION.md`**, **`docs/compat.md`**, **`README.md`** project layout table.
- Phase **2**–**3** (*Offline deterministic fixture page for LLM and reviewer workflows*): **`docs/examples/PATTERNS.md`** — **P-05** normative contract and **Shipped** **`fixture-replay.html`** (inlined synthetic **`sessionData`**, no session payload I/O, no secrets, no live/stochastic model calls, pinned **replayt** script + local static-server instructions in **`README.md`** and **`docs/REPLAYT_ECOSYSTEM_IDEA.md`**); **`docs/DESIGN_PRINCIPLES.md`** traceability, **[LLM boundaries](docs/DESIGN_PRINCIPLES.md#llm-boundaries)**, **Audience**; **`docs/MISSION.md`** / **`docs/compat.md`** pattern counts. Phase **2** registered the spec; phase **3** shipped the **HTML** and **`tests/test_examples.py`** markers.
- Phase **2** spec (*Document CDN vs bundled replayt with SRI and supply-chain notes*): **`docs/FRONTEND_SUPPLY_CHAIN.md`** — **CDN** (**jsDelivr**-style) pinning, optional **Subresource Integrity**, **npm**/**bundler** alternative, **`pip-audit`** vs **JS** surface; linked from **`README.md`**, **`docs/DESIGN_PRINCIPLES.md`** (**Frontend supply chain** + traceability), and **`docs/compat.md`**.
- **`docs/DESIGN_PRINCIPLES.md`**: **Traceability to automated checks** — **`tests/test_frontend_supply_chain_doc.py`** row lists **A1–A5** (including **CHANGELOG** **Unreleased** checks described in **`docs/FRONTEND_SUPPLY_CHAIN.md`**).
- **P-04** (*Empty, loading, and failure states for the embed container*): **`docs/examples/PATTERNS.md`** (spec then **Shipped**), **`docs/MISSION.md`** pattern count (**4** shipped), **`docs/compat.md`** digest, **`docs/DESIGN_PRINCIPLES.md`** catalog / **Audience** / backlog traceability, **`docs/demo.md`** cross-surface operator story and **Builder alignment** with **`embed-container-states.html`** (phases **2**–**3**).
- `docs/examples/PATTERNS.md`: **P-03** marked **Shipped**; **`docs/MISSION.md`** pattern table (**3** shipped with **P-03**); **`docs/compat.md`**, **`docs/DESIGN_PRINCIPLES.md`** catalog and **P-03** traceability (phase **3**).
- `docs/examples/PATTERNS.md`: **P-02** catalog and normative spec; **`docs/MISSION.md`**, **`docs/compat.md`**, **`docs/DESIGN_PRINCIPLES.md`** pattern coverage and traceability (phase **2**).
- `docs/DESIGN_PRINCIPLES.md`, `docs/compat.md`: normative spec for **`tests/test_docs_examples_replayt_pins.py`** (pin scan scope, **`pin-exempt`** comments); traceability for default **CI** **pytest** (phases **2**–**3**).
- **CHANGELOG** **Unreleased** (phase **5** architect): one **`Added`** group and consolidated **P-04** / **P-03** documentation bullets (no duplicate **`### Added`** headings).
- Phase **6** security review (*Empty, loading, and failure states for the embed container*): **`docs/examples/embed-container-states.html`** updates the live region and visible errors with **`textContent`** only (no **`innerHTML`** for dynamic strings); **replayt** script pin remains **`replayt@0.1.0`** on **jsDelivr**, within **`pyproject.toml`**. Init failures log via **`console.error`** for developer tooling only—not copied into **`#embed-status`**.

### Fixed

- `tests/test_examples.py`: **ruff format** so **`ruff format --check`** passes in CI (phase **8**, *Offline deterministic fixture page for LLM and reviewer workflows*).

## [0.2.0] - 2026-03-28

### Changed

- **0.2.0** release: **`[project].version`** and **`replayt_ux_showcase.__version__`** set to **0.2.0**; **`test_package_version_matches_pyproject`** keeps them aligned; prior **Unreleased** notes consolidated here (Prepare CHANGELOG.md for 0.2.0 release).
- `.github/workflows/ci.yml`: **test** job uses **`strategy.matrix`** for **Python 3.11** and **3.12**, **`pip install --upgrade pip`** before **`pip install -e ".[dev]"`**, and **`${{ matrix.python-version }}`** so **pytest-cov** gates run on each row (phase 3, Document compatibility matrix and upgrade paths).
- `docs/DESIGN_PRINCIPLES.md`: **Traceability to automated checks** includes **`test_package_version_matches_pyproject`** (Prepare CHANGELOG.md for 0.2.0 release).
- `docs/DESIGN_PRINCIPLES.md`, `docs/compat.md`: **Verified in CI today** for **Python** matches the matrix; supported-vs-tested wording updated for two interpreter rows (same backlog).
- `tests/test_design_principles_contract.py`: contract asserts the **test** job **Python** matrix lists **3.11** and **3.12** (same backlog).
- `.github/workflows/ci.yml`: run **`ruff check`** and **`ruff format --check`** after **`pip install -e ".[dev]"`** and before **pytest** (phase 3, Set up GitHub Actions CI for tests and linting).
- `README.md`: CI workflow badge points at **`flogat/replayt-ux-showcase`** on GitHub (same backlog).
- `tests/test_design_principles_contract.py`: assert **ruff** steps in CI and a real **README** badge URL (same backlog).
- `src/replayt_ux_showcase/demo.py`, `tests/test_examples.py`: **ruff format** so **`ruff format --check`** passes in CI (same backlog).
- `docs/DESIGN_PRINCIPLES.md`: traceability rows for **ruff**/**README** badge checks match **`tests/test_design_principles_contract.py`** (same backlog).
- `pyproject.toml`: **`pytest-cov`** in **`[dev]`**; **`[tool.pytest.ini_options]`** enforces **≥ 80%** line coverage on **`replayt_ux_showcase.demo`** (phase 3, Add unit/integration tests for demo).
- `docs/DESIGN_PRINCIPLES.md`: **dev** baseline table includes **pytest-cov**; demo testing traceability updated for the coverage gate and import-boundary test (same backlog).
- `tests/test_design_principles_contract.py`: **`[dev]`** optional dependencies must be **pytest**, **pytest-cov**, **ruff**, **pip-audit** (same backlog).
- `src/replayt_ux_showcase/demo.py`: **`main()`** entrypoint for tests and **`python -m replayt_ux_showcase.demo`** (same backlog).
- `tests/test_demo.py`: in-process timeline and **`main()`** tests, unknown-event branch, stdlib-only import guard on **`demo.py`** (same backlog).
- `docs/DESIGN_PRINCIPLES.md`: traceability rows for those contract checks (same backlog).
- `pyproject.toml`: **replayt** bounded to `>=0.1.0,<0.5.0` (PEP 508); `tests/test_design_principles_contract.py` enforces version constraints on **`[project].dependencies`**, **`[project.optional-dependencies].dev`**, and **`[build-system].requires`**, plus **replayt** import smoke (phase 3, Pin replayt dependency and dev tools in pyproject.toml).
- `docs/DESIGN_PRINCIPLES.md`: **Replayt and Python matrix** and traceability table aligned with the declared **replayt** range and new contract checks (same backlog).
- `docs/demo.md`: implementation and integration notes reference the same **replayt** PEP 508 range as `pyproject.toml` (same backlog).
- `tests/test_design_principles_contract.py`: asserts replayt API boundary subsection, packaged **`replayt_ux_showcase`** extension row, and release/automation audience rows; traceability table in `docs/DESIGN_PRINCIPLES.md` lists these checks (phase 3, Expand DESIGN_PRINCIPLES.md with canonical patterns).
- `docs/DESIGN_PRINCIPLES.md`: traceability to `tests/test_design_principles_contract.py`, explicit **replayt** Python API boundary, extension point for packaged **`replayt_ux_showcase`** surface, and audience rows for release consumers and LLM/automation tooling (phase 2, Expand DESIGN_PRINCIPLES.md with canonical patterns).

### Documentation

- `README.md`: quick start documents **`source .venv/bin/activate`**, why **dev** extras matter for **pytest-cov** (exit code **4** without them), **`python -m pytest`** for **CI** parity; layout table adds **`tests/`**, **`.github/workflows/`**, **`docs/demo.md`**, **`docs/examples/`** (phase 3, Update README quickstart and layout docs).
- `docs/DESIGN_PRINCIPLES.md`, `docs/compat.md`: **GitHub Actions** **Install** / local-repro wording matches the **test** job **Python** matrix (phase 3, Document compatibility matrix and upgrade paths).
- `CHANGELOG.md`: **Unreleased** entries for this cycle moved under **`[0.2.0]`** (Prepare CHANGELOG.md for 0.2.0 release).
- `docs/DESIGN_PRINCIPLES.md`: normative [GitHub Actions CI workflow](docs/DESIGN_PRINCIPLES.md#github-actions-ci-workflow) — triggers, observable logs, **pytest**/**ruff**/**pip-audit** jobs, **README** badge rules, backlog traceability (phase 2 spec, Set up GitHub Actions CI for tests and linting).
- `README.md`: CI badge section for **`ci.yml`**; phase 3 replaces **`OWNER/REPO`** with **`flogat/replayt-ux-showcase`** (same backlog).
- `docs/DESIGN_PRINCIPLES.md`: normative [Demo module testing and replayt integration boundaries](docs/DESIGN_PRINCIPLES.md#demo-module-testing-and-replayt-integration-boundaries) — 80% line coverage on `demo.py`, boundary-break semantics, **pytest-cov** in **dev** (phase 2 spec; phase 3 implements gate and contract alignment).
- `docs/demo.md`: automated test plan aligned with design principles; coverage gate documents **`pyproject.toml`** **`[tool.pytest.ini_options]`** (phase 3, Add unit/integration tests for demo).
- `docs/DESIGN_PRINCIPLES.md`: dependency pins and dev toolchain (PEP 508 vs caret wording, no loose direct deps, dev optional set table); traceability to `tests/test_design_principles_contract.py` including **replayt** specifier (`>=0.1.0` and `<0.5` cap); backlog-to-spec mapping, **`pip install -e ".[dev]"`** quoting note, and phase-3 builder checklist for “Pin replayt dependency and dev tools in pyproject.toml” (phase 2 spec lead).

### Added

- Pytest contract checks: `pyproject.toml` replayt pin and `requires-python`, CI **test** job **Python** matrix, and required headings in `docs/DESIGN_PRINCIPLES.md` stay consistent with the documented matrices (phase 3 backlog).
- Expanded `docs/DESIGN_PRINCIPLES.md` with canonical “one way” patterns, module boundaries, replayt/showcase version matrices, extension points, deprecation and migration policy, LLM boundaries, and extended audience table (spec-only refinement, phase 2 backlog).
- Defined project mission (users, Replayt role, scope, success metrics with CI tests) in MISSION.md.
- Initial polished demo: basic-player.html (vanilla JS replay player).
- Explicit contracts in DESIGN_PRINCIPLES.md: supported replayt/frameworks versions.
- `demo.py`: console timeline renderer (`python -m replayt_ux_showcase.demo`) with sample session data (12 events, 30s).
- Refined `docs/demo.md` spec: added replayt primitives usage notes, expanded test plan with 5 test cases, integration notes.

## [0.1.0] - 2026-03-25

### Added

- Initial scaffold and package layout.
