# Compatibility and upgrade paths

This page is the **readable digest** for integrators and release consumers. The **normative contract** is
[Design principles — Compatibility matrix and upgrade paths](DESIGN_PRINCIPLES.md#compatibility-matrix-and-upgrade-paths)
in `docs/DESIGN_PRINCIPLES.md`. If anything here disagrees with that document, **design principles win**.

## Quick reference: supported versions

| Dimension | Supported (policy) | Verified in CI today | Notes |
| --------- | ------------------ | -------------------- | ----- |
| **replayt** (PyPI) | `replayt>=0.1.0,<0.5.0` (PEP 508 in `pyproject.toml`) | **One explicit `replayt-version` matrix coordinate per listed pin**, on **each** **Python** row — see [CI exercise row inventory](#ci-exercise-row-inventory) (**EX-311-RT-0-1-0**, …) | **Policy** still allows any version in the PEP 508 range; **CI** proves **0.1.0**, **0.2.0**, and **0.4.25** on **3.11** and **3.12** via **`pip install -e ".[dev]" -c`** (constraint file). Other releases in-range are **policy-only** until added to the matrix and inventory in the same change set. |
| **Python** | `requires-python` (currently **≥ 3.11**) | **One explicit matrix row per** **Python** × **replayt** combination — inventory IDs **EX-311-*** and **EX-312-*** in [CI exercise row inventory](#ci-exercise-row-inventory) | Extra interpreters need new **`strategy.matrix`** entries, inventory rows, design principles / contract tests, and **CHANGELOG** in the same change set. |
| **Vanilla examples** (`docs/examples/`) | Intended copy-paste surface per [Showcase stack matrix](DESIGN_PRINCIPLES.md#showcase-stack-matrix); **replayt** pins must sit inside the same PEP 508 range as `pyproject.toml` | **Bundled** — **`tests/test_docs_examples_replayt_pins.py`** runs inside every **test** matrix cell ([CI exercise rows](DESIGN_PRINCIPLES.md#ci-exercise-rows-matrix-jobs-and-best-effort)); see **EX-EXAMPLES-PINS** in [CI exercise row inventory](#ci-exercise-row-inventory) | Not a standalone workflow job; optional per-pattern browser jobs remain future work. Intentional out-of-range demos use `<!-- replayt-examples:pin-exempt -->` per design principles. **CDN** / **SRI** / bundlers: [`docs/FRONTEND_SUPPLY_CHAIN.md`](FRONTEND_SUPPLY_CHAIN.md). Optional **npm** preview: [`docs/examples/build.md`](examples/build.md). |

Authoritative tables and policy notes: [Replayt and Python matrix](DESIGN_PRINCIPLES.md#replayt-and-python-matrix), [Showcase stack matrix](DESIGN_PRINCIPLES.md#showcase-stack-matrix).

## CI exercise row inventory

Enumerates **default** **`.github/workflows/ci.yml`** automation for this repo. Each **ID** is stable copy for **CHANGELOG**
and contract tests; add rows **only** when the workflow gains a new **job** or **matrix** combination (or when demoting
a claim to best-effort — then **remove** or relabel the row).

| ID | Workflow | Matrix / coordinates | What runs |
| -- | -------- | -------------------- | --------- |
| **EX-311-RT-0-1-0** | `jobs.test` | `python-version: "3.11"`, `replayt-version: "0.1.0"` | Editable **`pip install -e ".[dev]"`** with **`-c`** pinning **`replayt==0.1.0`**; **`ruff check`**, **`ruff format --check`**, **`python -m pytest tests`** (honors **`[tool.pytest.ini_options]`** — demo coverage gate + **`tests/test_docs_examples_replayt_pins.py`** + other contract tests); asserts **`replayt.__version__`** matches the matrix pin |
| **EX-311-RT-0-2-0** | `jobs.test` | `python-version: "3.11"`, `replayt-version: "0.2.0"` | Same as **EX-311-RT-0-1-0** with **`replayt==0.2.0`** |
| **EX-311-RT-0-4-25** | `jobs.test` | `python-version: "3.11"`, `replayt-version: "0.4.25"` | Same as **EX-311-RT-0-1-0** with **`replayt==0.4.25`** |
| **EX-312-RT-0-1-0** | `jobs.test` | `python-version: "3.12"`, `replayt-version: "0.1.0"` | Same as **EX-311-RT-0-1-0** on **3.12** |
| **EX-312-RT-0-2-0** | `jobs.test` | `python-version: "3.12"`, `replayt-version: "0.2.0"` | Same as **EX-311-RT-0-2-0** on **3.12** |
| **EX-312-RT-0-4-25** | `jobs.test` | `python-version: "3.12"`, `replayt-version: "0.4.25"` | Same as **EX-311-RT-0-4-25** on **3.12** |
| **EX-EXAMPLES-PINS** | (bundled) | Runs inside every **`jobs.test`** matrix cell via **pytest** | **`tests/test_docs_examples_replayt_pins.py`** |
| **EX-SUPPLY-CHAIN** | `jobs.supply-chain` | `ubuntu-latest`, **Python 3.12** (setup-python) | Editable dev install (**replayt** resolves to latest in-range, not matrix-pinned) + **`pip-audit`** per **`docs/DEPENDENCY_AUDIT.md`** |

**Not listed as exercise rows:** optional **npm** `dev`/`build` for **Vue** / **Svelte** subtrees under **`docs/examples/`**
(pytest does not run those scripts); **replayt** pins in those trees are still checked by **EX-EXAMPLES-PINS** via
**`tests/test_docs_examples_replayt_pins.py`**. Optional repository-root bundler preview per **`docs/examples/build.md`**
remains **local** unless a future backlog adds workflow jobs.

## Vanilla UI pattern catalog

**Mission:** ≥ **5** distinct vanilla patterns under **`docs/examples/`** (see [MISSION.md — Pattern coverage tracking](MISSION.md#pattern-coverage-tracking)).

**Canonical inventory:** [`docs/examples/PATTERNS.md`](examples/PATTERNS.md) lists pattern IDs, filenames, shipped vs spec-only status, and **Builder** acceptance checklists. **P-03** (*timeline scrubber strip*, [`timeline-scrubber.html`](examples/timeline-scrubber.html)) is **Shipped**—see [P-03 — Timeline scrubber strip](examples/PATTERNS.md#p-03--timeline-scrubber-strip-events-driven-seek). **P-04** (*embed container states*, [`embed-container-states.html`](examples/embed-container-states.html)) is **Shipped**—see [P-04 embed container states](examples/PATTERNS.md#p-04-embed-container-states-empty-loading-failure-recovery). **P-05** (*offline deterministic fixture for reviewers / LLM harnesses*, [`fixture-replay.html`](examples/fixture-replay.html)) is **Shipped**—see [P-05 offline deterministic fixture page](examples/PATTERNS.md#p-05-offline-deterministic-fixture-page-for-llm-and-reviewer-workflows). **P-06** (*React* timeline player under [`docs/examples/react/`](examples/react/) — **Shipped**) mirrors **P-01**/**P-03** contracts; see [P-06 — React timeline player](examples/PATTERNS.md#p-06--react-timeline-player-basic-player--scrubber-parity). **P-07** (*Vue 3*, [`docs/examples/vue/`](examples/vue/) — **Shipped**) and **P-08** (*Svelte 4*, [`docs/examples/svelte/`](examples/svelte/) — **Shipped**) match **P-06** scrubber and init intent; see [P-07](examples/PATTERNS.md#p-07--vue-3-timeline-player-basic-player--scrubber-parity) and [P-08](examples/PATTERNS.md#p-08--svelte-4-timeline-player-basic-player--scrubber-parity). Shared **keyboard and focus** expectations for player/timeline embeds: [`docs/a11y/keyboard-model.md`](a11y/keyboard-model.md). **Design-to-code handoff** (tokens, timeline/overlay anatomy, printable a11y / loading / error checklist): [`docs/playbook/README.md`](playbook/README.md). Doc structure for **`docs/playbook/*.md`** is checked by **`tests/test_playbook_docs.py`**. When compatibility or pinning rules for examples change, follow [Vanilla examples: integrator-facing replayt pins](DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins) and update **CHANGELOG** **Unreleased** together with **`docs/examples/PATTERNS.md`** if the pattern list or contracts change.

## CI matrix coverage

**Rule:** CI must not claim coverage it does not run ([Replayt and Python matrix](DESIGN_PRINCIPLES.md#replayt-and-python-matrix),
[CI exercise rows](DESIGN_PRINCIPLES.md#ci-exercise-rows-matrix-jobs-and-best-effort)).

| Concern | What default CI is expected to exercise | What integrators should assume |
| ------- | ---------------------------------------- | ------------------------------ |
| **Install + tests** | One full gate per **Python** × **replayt** matrix cell (**EX-311-RT-*** … **EX-312-RT-***): editable **`".[dev]"`** install with **`-c`** **replayt** pin, **ruff**, **`python -m pytest tests`** with **`[tool.pytest.ini_options]`** | Reproduce locally with the same **`replayt==…`** constraint file or **`pip install "replayt==…"`** before **`pip install -e ".[dev]"`**, on a **supported** **Python**. |
| **replayt resolution** | Explicit **`replayt-version`** per cell (**0.1.0**, **0.2.0**, **0.4.25**) | Other releases in-range are **policy** until new inventory rows + matrix pins prove them. |
| **Example pins** | **EX-EXAMPLES-PINS** — bundled in **pytest** on every **test** cell | Snippet pins are checked on each **Python** × **replayt** matrix cell; not separate jobs per pattern file. |
| **Lint / supply chain** | **ruff** inside each **test** row; **`pip-audit`** in **EX-SUPPLY-CHAIN** | Failures block merge when those steps are required. |

**Future matrix rows:** When maintainers add or change **replayt** pins in **`ci.yml`**, update this inventory, **Verified in CI today** in **`docs/DESIGN_PRINCIPLES.md`**, and **`tests/test_design_principles_contract.py`** in the **same** change set.

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
