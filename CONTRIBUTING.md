# Contributing

This repository’s integration contracts live in **[`docs/DESIGN_PRINCIPLES.md`](docs/DESIGN_PRINCIPLES.md)**. Read that
file before changing dependencies, CI, or normative docs.

## Local setup

See **[`README.md`](README.md#quick-start)** — Python **3.11+**, editable install with **dev** extras, and **`pytest`**
from the repo root (so **`[tool.pytest.ini_options]`** applies).

## Changelog

[`CHANGELOG.md`](CHANGELOG.md) follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and aligns with
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) for the **`replayt-ux-showcase`** package.

- Add bullets under **`[Unreleased]`** for user-visible work in the **same** PR as the change.
- For **Shipped** UI patterns (**P-xx**), include **`CHANGELOG`** notes in the **same change set** as
  **`docs/examples/PATTERNS.md`**, **`docs/MISSION.md`** (pattern table), and **`docs/compat.md`** (vanilla catalog)
  when applicable — see [Unreleased: pattern coverage and mission tracking](docs/DESIGN_PRINCIPLES.md#unreleased-pattern-coverage-and-mission-tracking).

**Semver when tagging** (MINOR vs PATCH for the package vs copy-paste examples): [Changelog, semver, and release notes](docs/DESIGN_PRINCIPLES.md#changelog-semver-and-release-notes).

## When to edit `docs/DESIGN_PRINCIPLES.md` in the same change set as pins

Update **`docs/DESIGN_PRINCIPLES.md`** together with metadata or automation edits when you touch any of the following,
so the **canonical spec** stays aligned with **`pyproject.toml`**, **CI**, and contract tests:

| Change | Also update in `docs/DESIGN_PRINCIPLES.md` |
| ------ | ------------------------------------------ |
| **`[project].dependencies`** — **`replayt`** PEP 508 line | [Replayt and Python matrix](docs/DESIGN_PRINCIPLES.md#replayt-and-python-matrix), [Dependency pins and dev toolchain](docs/DESIGN_PRINCIPLES.md#dependency-pins-and-dev-toolchain), and any prose that states the supported **replayt** band |
| **`requires-python`** | [Replayt and Python matrix](docs/DESIGN_PRINCIPLES.md#replayt-and-python-matrix) and related matrix wording |
| **`[project.optional-dependencies].dev`** package set or pins | [Dev optional dependency set (baseline)](docs/DESIGN_PRINCIPLES.md#dev-optional-dependency-set-baseline), [Dependency pins and dev toolchain](docs/DESIGN_PRINCIPLES.md#dependency-pins-and-dev-toolchain) |
| **`[build-system].requires`** | [Dependency pins and dev toolchain](docs/DESIGN_PRINCIPLES.md#dependency-pins-and-dev-toolchain) |
| **`.github/workflows/ci.yml`** — **test** job **Python** or **`replayt-version`** matrix, install command, or lint/test steps asserted by contract tests | [GitHub Actions CI workflow](docs/DESIGN_PRINCIPLES.md#github-actions-ci-workflow), [Replayt and Python matrix](docs/DESIGN_PRINCIPLES.md#replayt-and-python-matrix), [Showcase stack matrix](docs/DESIGN_PRINCIPLES.md#showcase-stack-matrix) if scope changes |
| **`docs/compat.md`** **CI exercise row inventory** or quick-reference tables driven by the same pins | Cross-check [Compatibility matrix and upgrade paths](docs/DESIGN_PRINCIPLES.md#compatibility-matrix-and-upgrade-paths) and matrix tables for **drift** |
| New **normative** subsection or **§** title **referenced by `tests/test_design_principles_contract.py`** | Matching heading text and [Traceability to automated checks](docs/DESIGN_PRINCIPLES.md#traceability-to-automated-checks) rows |

**CHANGELOG:** Add **`[Unreleased]`** notes in that same change set per [One way to do it — single compatibility story](docs/DESIGN_PRINCIPLES.md#one-way-to-do-it-canonical-patterns).

**Tests:** **`tests/test_changelog_release_policy_docs.py`** guards **`CONTRIBUTING.md`**, the [Changelog, semver, and release notes](docs/DESIGN_PRINCIPLES.md#changelog-semver-and-release-notes) section, and **CHANGELOG** **Unreleased** mentions of that module. When pins or normative headings change, update **`tests/test_design_principles_contract.py`** and related contract tests in the **same** PR — see [Traceability to automated checks](docs/DESIGN_PRINCIPLES.md#traceability-to-automated-checks).
