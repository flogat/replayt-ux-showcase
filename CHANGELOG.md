# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Documentation

- `docs/examples/PATTERNS.md`: canonical **vanilla UI pattern** catalog (**P-01** / **P-02**), normative **P-02** spec (session metadata bar above player, `sessionData` compatibility with `basic-player.html`, loading / error / focus rules), and Builder checklist (backlog phase **2** spec lead, *Ship session metadata chrome pattern (viewport, duration, session id)*).
- `docs/MISSION.md`, `docs/compat.md`, `docs/DESIGN_PRINCIPLES.md`: pattern coverage tracking toward **5+** examples, digest link, design-principles traceability and backlog mapping for **P-02** (same backlog, phase **2**).

### Added

- `docs/examples/player-session-metadata-bar.html`: **P-02** vanilla example — metadata bar above the player, same **`sessionData`** shape as **`basic-player.html`**, loading placeholder, user-visible errors when **`sessionId`** / **`durationMs`** / **`viewport`** are missing or invalid after load, and bar focusable controls before the player in DOM order (backlog phase **3**, *Ship session metadata chrome pattern (viewport, duration, session id)*).
- `tests/test_examples.py`: asserts **`player-session-metadata-bar.html`** exists and keeps minimal **P-02** contract markers (loading copy, validation strings, tab-order comment, **replayt** script pin) aligned with **`docs/examples/PATTERNS.md`** (same backlog, phase **3**).
- `tests/test_docs_examples_replayt_pins.py`: **pytest** contract for **`docs/examples/**/*.{html,md}`** — **replayt** CDN (`replayt@…`) and PEP 508-style pins checked against the **`replayt`** line in **`pyproject.toml`**, with **`<!-- replayt-examples:pin-exempt -->`** skipping the next script line, URL line, or fenced block (backlog phase 3, Contract test: examples reference replayt in supported semver range).

### Documentation

- `docs/DESIGN_PRINCIPLES.md`, `docs/compat.md`: normative spec and traceability for **contract tests** that scan **`docs/examples/**/*.{html,md}`** so **replayt** CDN and requirement pins stay inside the PEP 508 range from **`pyproject.toml`**, including **`<!-- replayt-examples:pin-exempt -->`** for deliberate exceptions (backlog phase 2, Contract test: examples reference replayt in supported semver range).
- `docs/DESIGN_PRINCIPLES.md`, `docs/compat.md`: traceability updated now that **`tests/test_docs_examples_replayt_pins.py`** runs in default **CI** **pytest** (same backlog, phase 3).

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
