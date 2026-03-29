# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `docs/examples/fixture-replay.html`: **P-05** vanilla example — **deterministic** header comment, **inlined** synthetic **`sessionData`** (fixed timestamps and ids), **no** `fetch(` / **`Date.now`** / **`Math.random`** in source, **`replayt.player.init`** only; pinned **replayt** on **jsDelivr** (phase **3**, *Offline deterministic fixture page for LLM and reviewer workflows*).
- `tests/test_examples.py`: asserts **`fixture-replay.html`** exists and keeps minimal **P-05** contract markers aligned with **`docs/examples/PATTERNS.md`** (same backlog, phase **3**).
- `tests/test_frontend_supply_chain_doc.py`: contract tests for **`docs/FRONTEND_SUPPLY_CHAIN.md`** (section anchors, **pip-audit** vs **JS** keywords, **README** / **DESIGN_PRINCIPLES** / **compat** links, **CHANGELOG** **Unreleased** mention per doc **A1–A5**; phase **3**, *Document CDN vs bundled replayt with SRI and supply-chain notes*).
- `docs/examples/embed-container-states.html`: **P-04** vanilla example — async `sessionData` (simulated delay), skeleton UI with **Loading replay…**, user-visible **network** vs **invalid payload** errors, focusable **Retry**, **`role="status"`** / **`aria-live="polite"`** announcement contract, optional **`data-demo-state`** on **`#embed-shell`**; **`replayt.player.init`** only (backlog phase **3**, *Empty, loading, and failure states for the embed container*).
- `tests/test_examples.py`: asserts **`embed-container-states.html`** exists and keeps minimal **P-04** contract markers aligned with **`docs/examples/PATTERNS.md`** (same backlog, phase **3**).
- `docs/examples/timeline-scrubber.html`: **P-03** vanilla example — `sessionData.events` + `metadata` time range, defensive sort-by-timestamp comment, `requestAnimationFrame`-throttled scrub seeks with final commit on `change` / `pointerup`, optional `seekToMs` / `goto` seek hooks, visible **Limitations** note for CDN builds (backlog phase **3**, *Timeline scrubber strip example using replayt public events API*).
- `tests/test_examples.py`: asserts **`timeline-scrubber.html`** exists and keeps minimal **P-03** contract markers aligned with **`docs/examples/PATTERNS.md`** (same backlog, phase **3**).
- `docs/examples/player-session-metadata-bar.html`: **P-02** vanilla example — metadata bar above the player, same **`sessionData`** shape as **`basic-player.html`**, loading placeholder, user-visible errors when **`sessionId`** / **`durationMs`** / **`viewport`** are missing or invalid after load, and bar focusable controls before the player in DOM order (backlog phase **3**, *Ship session metadata chrome pattern (viewport, duration, session id)*).
- `tests/test_examples.py`: asserts **`player-session-metadata-bar.html`** exists and keeps minimal **P-02** contract markers (loading copy, validation strings, tab-order comment, **replayt** script pin) aligned with **`docs/examples/PATTERNS.md`** (same backlog, phase **3**).
- `tests/test_docs_examples_replayt_pins.py`: **pytest** contract for **`docs/examples/**/*.{html,md}`** — **replayt** CDN (`replayt@…`) and PEP 508-style pins checked against the **`replayt`** line in **`pyproject.toml`**, with **`<!-- replayt-examples:pin-exempt -->`** skipping the next script line, URL line, or fenced block (backlog phase 3, Contract test: examples reference replayt in supported semver range).

### Documentation

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
