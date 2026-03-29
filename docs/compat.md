# Compatibility and upgrade paths

This page is the **readable digest** for integrators and release consumers. The **normative contract** is
[Design principles — Compatibility matrix and upgrade paths](DESIGN_PRINCIPLES.md#compatibility-matrix-and-upgrade-paths)
in `docs/DESIGN_PRINCIPLES.md`. If anything here disagrees with that document, **design principles win**.

## Quick reference: supported versions

| Dimension | Supported (policy) | Verified in CI today | Notes |
| --------- | ------------------ | -------------------- | ----- |
| **replayt** (PyPI) | `replayt>=0.1.0,<0.5.0` (PEP 508 in `pyproject.toml`) | **One** resolved version per default CI job: the **latest** package on PyPI that satisfies that range at install time | Not every patch release is pinned in CI; the range is the support promise. To claim specific minors are regression-tested, add explicit matrix jobs (see [CI matrix coverage](#ci-matrix-coverage)). |
| **Python** | `requires-python` (currently **≥ 3.11**) | **3.11** and **3.12** in the **test** job **`strategy.matrix`** (`.github/workflows/ci.yml`; see design principles matrix) | Extra interpreters need new matrix rows and doc updates in the same change set. |
| **Vanilla examples** (`docs/examples/`) | Intended copy-paste surface per [Showcase stack matrix](DESIGN_PRINCIPLES.md#showcase-stack-matrix); **replayt** pins must sit inside the same PEP 508 range as `pyproject.toml` | Contract test **`tests/test_docs_examples_replayt_pins.py`** (per [Vanilla examples: integrator-facing replayt pins](DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins)); optional extra file/smoke tests later | Keeps CDN and requirement snippets from drifting ahead of the supported consumer story; intentional out-of-range demos use `<!-- replayt-examples:pin-exempt -->` per design principles. **CDN** delivery, optional **SRI**, and **bundler** alternatives: [`docs/FRONTEND_SUPPLY_CHAIN.md`](FRONTEND_SUPPLY_CHAIN.md). Optional maintainer **npm** + **Vite** / **esbuild** preview recipe: [`docs/examples/build.md`](examples/build.md). |

Authoritative tables and policy notes: [Replayt and Python matrix](DESIGN_PRINCIPLES.md#replayt-and-python-matrix), [Showcase stack matrix](DESIGN_PRINCIPLES.md#showcase-stack-matrix).

## Vanilla UI pattern catalog

**Mission:** ≥ **5** distinct vanilla patterns under **`docs/examples/`** (see [MISSION.md — Pattern coverage tracking](MISSION.md#pattern-coverage-tracking)).

**Canonical inventory:** [`docs/examples/PATTERNS.md`](examples/PATTERNS.md) lists pattern IDs, filenames, shipped vs spec-only status, and **Builder** acceptance checklists. **P-03** (*timeline scrubber strip*, [`timeline-scrubber.html`](examples/timeline-scrubber.html)) is **Shipped**—see [P-03 — Timeline scrubber strip](examples/PATTERNS.md#p-03--timeline-scrubber-strip-events-driven-seek). **P-04** (*embed container states*, [`embed-container-states.html`](examples/embed-container-states.html)) is **Shipped**—see [P-04 embed container states](examples/PATTERNS.md#p-04-embed-container-states-empty-loading-failure-recovery). **P-05** (*offline deterministic fixture for reviewers / LLM harnesses*, [`fixture-replay.html`](examples/fixture-replay.html)) is **Shipped**—see [P-05 offline deterministic fixture page](examples/PATTERNS.md#p-05-offline-deterministic-fixture-page-for-llm-and-reviewer-workflows). **P-06** (*React* timeline player under [`docs/examples/react/`](examples/react/) — **Shipped**) mirrors **P-01**/**P-03** contracts; see [P-06 — React timeline player](examples/PATTERNS.md#p-06--react-timeline-player-basic-player--scrubber-parity). Shared **keyboard and focus** expectations for player/timeline embeds: [`docs/a11y/keyboard-model.md`](a11y/keyboard-model.md). **Design-to-code handoff** (tokens, timeline/overlay anatomy, printable a11y / loading / error checklist): [`docs/playbook/README.md`](playbook/README.md). When compatibility or pinning rules for examples change, follow [Vanilla examples: integrator-facing replayt pins](DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins) and update **CHANGELOG** **Unreleased** together with **`docs/examples/PATTERNS.md`** if the pattern list or contracts change.

## CI matrix coverage

**Rule:** CI must not claim coverage it does not run ([Replayt and Python matrix](DESIGN_PRINCIPLES.md#replayt-and-python-matrix)).

| Concern | What default CI is expected to exercise | What integrators should assume |
| ------- | ---------------------------------------- | ------------------------------ |
| **Install + tests** | Editable install with **`pip install -e ".[dev]"`**, then **`python -m pytest`** so `[tool.pytest.ini_options]` (including **pytest-cov** options) applies | Same commands reproduce the gate locally on a **supported** **Python** (see **`requires-python`** and the **test** job matrix). |
| **replayt resolution** | Whatever **pip** resolves for `replayt` under the declared PEP 508 range | Behavior is validated for **that** resolved version on that run; older minors inside the range are supported **by policy** until the range or matrices change. |
| **Lint / supply chain** | **ruff** and **pip-audit** (or equivalent) per [GitHub Actions CI workflow](DESIGN_PRINCIPLES.md#github-actions-ci-workflow) | Failures block merge when those steps are required. |

**Future matrix rows:** When maintainers need to **prove** compatibility with specific **replayt** minors (e.g. `0.4.x` and `0.3.x`), add parallel **CI** jobs or extra **`strategy.matrix`** dimensions that pin or constrain the resolver per row, and update the **Verified in CI today** cells in `docs/DESIGN_PRINCIPLES.md` and this file in the **same** change set.

## Deprecation policy (summary)

Full rules: [Deprecation and removal](DESIGN_PRINCIPLES.md#deprecation-and-removal).

- **Announce** deprecations in **CHANGELOG** (**Unreleased** first), with what replaces the old path and which release still supports the old surface.
- **Horizon:** keep deprecated demo paths or module aliases for **at least one** published **minor** release when external users could depend on them, unless security requires immediate removal.
- **Remove** in a later release with **Removed** notes and a short migration bullet.
- **SemVer:** removals of documented examples or CLI behavior ship as at least **minor** unless marked experimental.

## Compatibility shims

**Purpose:** When **replayt**’s public API shifts within a supported range (or across a planned range change), keep integrators **unstranded** with small adapters in **this repo**—not by patching **replayt** core.

**Where shims live:** Only under **`src/replayt_ux_showcase/`** (see [Module and directory boundaries](DESIGN_PRINCIPLES.md#module-and-directory-boundaries)). Prefer a dedicated module or thin wrapper re-exporting a stable surface for demos and tests; document the shim in **CHANGELOG** and, when user-visible, in this file or **`docs/demo.md`**.

**Today:** The console demo (`replayt_ux_showcase.demo`) is **stdlib-only**; there is no **replayt** import shim until the demo or examples import **replayt**. When they do, imported names must stay within **replayt**’s published public surface ([replayt Python API boundary](DESIGN_PRINCIPLES.md#replayt-python-api-boundary)).

## Migration and upgrades

1. **Compare pins:** Match your app’s **replayt** constraint to the **Supported (policy)** column in [Replayt and Python matrix](DESIGN_PRINCIPLES.md#replayt-and-python-matrix) and to `pyproject.toml`.
2. **Read release notes:** **CHANGELOG** for **replayt-ux-showcase** and **replayt** upstream (PyPI / upstream docs) for breaking changes and deprecations.
3. **Follow the playbook:** [Migration paths (replayt and repo)](DESIGN_PRINCIPLES.md#migration-paths-replayt-and-repo) lists maintainer triggers; integrators mirror the same steps for their copies of examples.
4. **API usage:** Rely only on **replayt**’s documented public API; private or underscore-prefixed symbols are not part of the compatibility promise.

## Tracking upstream

- Watch **replayt** on PyPI and upstream release notes for semver and API changes.
- When widening the supported **replayt** range (e.g. raising the `<0.5` cap), update **`pyproject.toml`**, design principles matrices, **`docs/examples/`** pins (and the examples contract test if detection rules change), **CHANGELOG**, and any contract tests **together**, per [Dependency pins and dev toolchain](DESIGN_PRINCIPLES.md#dependency-pins-and-dev-toolchain) and [Vanilla examples: integrator-facing replayt pins](DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins).
