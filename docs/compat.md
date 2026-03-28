# Compatibility and upgrade paths

This page is the **readable digest** for integrators and release consumers. The **normative contract** is
[Design principles — Compatibility matrix and upgrade paths](DESIGN_PRINCIPLES.md#compatibility-matrix-and-upgrade-paths)
in `docs/DESIGN_PRINCIPLES.md`. If anything here disagrees with that document, **design principles win**.

## Quick reference: supported versions

| Dimension | Supported (policy) | Verified in CI today | Notes |
| --------- | ------------------ | -------------------- | ----- |
| **replayt** (PyPI) | `replayt>=0.1.0,<0.5.0` (PEP 508 in `pyproject.toml`) | **One** resolved version per default CI job: the **latest** package on PyPI that satisfies that range at install time | Not every patch release is pinned in CI; the range is the support promise. To claim specific minors are regression-tested, add explicit matrix jobs (see [CI matrix coverage](#ci-matrix-coverage)). |
| **Python** | `requires-python` (currently **≥ 3.11**) | The single **Python** version configured in `.github/workflows/ci.yml` (see design principles matrix) | Policy may allow 3.11+ while CI runs one interpreter; do not imply CI exercises every allowed minor without extra jobs. |
| **Vanilla examples** (`docs/examples/`) | Intended copy-paste surface per [Showcase stack matrix](DESIGN_PRINCIPLES.md#showcase-stack-matrix) | File or smoke checks under `tests/` **when implemented** | Front-end stacks (React/Vue/Svelte) are documented ahead of examples; CI follows when demos ship. |

Authoritative tables and policy notes: [Replayt and Python matrix](DESIGN_PRINCIPLES.md#replayt-and-python-matrix), [Showcase stack matrix](DESIGN_PRINCIPLES.md#showcase-stack-matrix).

## CI matrix coverage

**Rule:** CI must not claim coverage it does not run ([Replayt and Python matrix](DESIGN_PRINCIPLES.md#replayt-and-python-matrix)).

| Concern | What default CI is expected to exercise | What integrators should assume |
| ------- | ---------------------------------------- | ------------------------------ |
| **Install + tests** | Editable install with **`pip install -e ".[dev]"`**, then **`python -m pytest`** so `[tool.pytest.ini_options]` (including **pytest-cov** options) applies | Same commands reproduce the gate locally on the supported Python line. |
| **replayt resolution** | Whatever **pip** resolves for `replayt` under the declared PEP 508 range | Behavior is validated for **that** resolved version on that run; older minors inside the range are supported **by policy** until the range or matrices change. |
| **Lint / supply chain** | **ruff** and **pip-audit** (or equivalent) per [GitHub Actions CI workflow](DESIGN_PRINCIPLES.md#github-actions-ci-workflow) | Failures block merge when those steps are required. |

**Future matrix rows (Builder):** When maintainers need to **prove** compatibility with specific **replayt** minors (e.g. `0.4.x` and `0.3.x`) or multiple **Python** versions, add parallel **CI** jobs (or a `strategy.matrix`) that pin or constrain the resolver per row, and update the **Verified in CI today** cells in `docs/DESIGN_PRINCIPLES.md` and this file in the **same** change set.

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
2. **Read release notes:** **CHANGELOG** for this package (showcase) and **replayt** upstream (PyPI / upstream docs) for breaking changes and deprecations.
3. **Follow the playbook:** [Migration paths (replayt and repo)](DESIGN_PRINCIPLES.md#migration-paths-replayt-and-repo) lists maintainer triggers; integrators mirror the same steps for their copies of examples.
4. **API usage:** Rely only on **replayt**’s documented public API; private or underscore-prefixed symbols are not part of the compatibility promise.

## Tracking upstream

- Watch **replayt** on PyPI and upstream release notes for semver and API changes.
- When widening the supported **replayt** range (e.g. raising the `<0.5` cap), update **`pyproject.toml`**, design principles matrices, **CHANGELOG**, and any contract tests **together**, per [Dependency pins and dev toolchain](DESIGN_PRINCIPLES.md#dependency-pins-and-dev-toolchain).
