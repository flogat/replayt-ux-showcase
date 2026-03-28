# Design principles

Revise as the project matures. This document is the **canonical contract** for integration boundaries, versioning,
and how demos and tooling may evolve. Prefer updating **one** source of truth here and linking from README or
mission docs rather than duplicating rules.

## Acceptance criteria (traceability)

The following backlog outcomes are satisfied **by this spec** (implementation of CI matrix rows, new examples, etc.
is tracked separately in code and CHANGELOG):

| Criterion | Where addressed |
| --------- | ----------------- |
| Version matrix table | [Replayt and Python matrix](#replayt-and-python-matrix), [Showcase stack matrix](#showcase-stack-matrix) |
| **replayt** / dev-tool pins and “no loose deps” | [Dependency pins and dev toolchain](#dependency-pins-and-dev-toolchain) |
| Demo **pytest** coverage and **replayt** boundary tests | [Demo module testing and replayt integration boundaries](#demo-module-testing-and-replayt-integration-boundaries) |
| **GitHub Actions** CI (tests, **ruff**, **replayt** install path, supply chain, badges) | [GitHub Actions CI workflow](#github-actions-ci-workflow) |
| Extension points documented | [Extension points](#extension-points) |
| Audience needs extended | [Audience](#audience) |

### Traceability to automated checks

These alignments are **enforced in CI** today (the principles doc is broader):

| Check | Enforced by |
| ----- | ----------- |
| `requires-python` matches the Python row in [Replayt and Python matrix](#replayt-and-python-matrix) | `tests/test_design_principles_contract.py` |
| **`replayt`** dependency specifier matches that matrix (`>=0.1.0` and compatible `<0.5` cap, per `tests/test_design_principles_contract.py`) | Same |
| CI **Python** version in `.github/workflows/ci.yml` matches that matrix | Same |
| Section headings for the two matrices, extension points, and audience | Same |
| Subsection **replayt Python API boundary** under [Module and directory boundaries](#module-and-directory-boundaries) | Same |
| Extension points row for packaged **`replayt_ux_showcase`** surface | Same |
| Audience rows for **Release / tag consumers** and **Automation agents (LLM tooling)** | Same |
| Each line in **`[project].dependencies`** and **`[project.optional-dependencies].dev`** carries a PEP 508 version constraint | Same |
| **`[project.optional-dependencies].dev`** package names match [Dev optional dependency set (baseline)](#dev-optional-dependency-set-baseline) | Same |
| **`[build-system].requires`** entries carry a PEP 508 version constraint | Same |
| **`replayt` is importable** after install (integration smoke) | Same |
| CI installs with **`pip install -e ".[dev]"`** (quoted extras) per contributor entrypoint | Same |
| **pytest** in CI honors **`[tool.pytest.ini_options]`** (coverage on **`demo.py`**, fail-under) | [GitHub Actions CI workflow](#github-actions-ci-workflow) — job command MUST NOT drop the **cov** gate (requires **dev** install with **pytest-cov**) |
| **`ruff check`** (and **`ruff format --check`** when enforced) run in CI after **dev** install | [GitHub Actions CI workflow](#github-actions-ci-workflow); `tests/test_design_principles_contract.py` (`test_ci_runs_ruff_lint_and_format_check`) |

When pins, workflow images, or section titles change, update **this document** and **tests** together in one change set
unless the test is being retired on purpose.

---

## One way to do it (canonical patterns)

1. **Single compatibility story** — Supported ranges for **replayt**, **Python**, and **dev** tooling are defined in
   **`pyproject.toml`** (runtime deps, **`[project.optional-dependencies].dev`**, **`[build-system].requires`**) and
   summarized in the matrices and [Dependency pins and dev toolchain](#dependency-pins-and-dev-toolchain). When
   support changes, update **both** spec and metadata and add a **CHANGELOG** entry under **Unreleased** in the same
   change set as the pin or CI update.
2. **Single home for copy-paste demos** — New static examples live under **`docs/examples/`** with clear filenames
   (e.g. `basic-player.html`). Framework-specific trees (e.g. `docs/examples/react/`) are introduced only when a
   pattern ships; avoid parallel unofficial copies at repo root.
3. **Single automation surface for Python** — Importable code and CLIs live under **`src/replayt_ux_showcase/`** only.
   Do not add a second package name or duplicate entrypoints without a deprecation path.
4. **Upstream boundary** — Integrate **replayt** via its **published public API** (see PyPI release notes / upstream
   docs). This repo does not fork or patch **replayt** internals to ship demos.

---

## Module and directory boundaries

| Area | Owns | Must not |
| ---- | ---- | -------- |
| **`src/replayt_ux_showcase/`** | Python package surface (`import replayt_ux_showcase`), console demos, test helpers that exercise replayt through supported APIs | Become a second “core” for capture/replay; depend on unreleased or git-pinned replayt without an explicit maintainer decision recorded in CHANGELOG |
| **`docs/`** | Mission, principles, demo specs, copy-paste examples, playbook-oriented markdown | Hold secrets, credentials, or environment-specific endpoints checked into git |
| **`docs/examples/`** | Static HTML/JS (and future framework snippets) that integrators copy | Imply they are supported npm packages unless explicitly published as such |
| **`tests/`** | Repo invariants: packaging, file presence, smoke behavior against installed **replayt** | Replace upstream **replayt** unit tests or depend on private APIs |
| **`.github/workflows/`** | CI that installs with **`pip install -e ".[dev]"`**, runs **pytest** (with **`[tool.pytest.ini_options]`** coverage gate), **ruff**, and **pip-audit** (see [GitHub Actions CI workflow](#github-actions-ci-workflow)); future matrix jobs as needed | Store long-lived tokens (read-only `contents` is the default contract) |

**Dependency direction:** showcase code and tests **→** **replayt** (PyPI). Demos may document how integrators pull
**replayt** in their own apps; this repo does not re-export **replayt** as a different product.

### replayt Python API boundary

- Depend on **replayt** only through its **published** PyPI package and **documented** public surface (release notes,
  upstream reference docs). Do not rely on private modules, underscore-prefixed internals, or undocumented symbols.
- Workflow or mock-LLM helpers from **replayt** are allowed only when they stay **offline** and **deterministic** in
  default CI, per [LLM boundaries](#llm-boundaries).

---

## Demo module testing and replayt integration boundaries

Normative spec for the backlog item **Add unit/integration tests for demo**: what “coverage on demo”, “fails on
boundary breaks”, and “dev dependencies” mean in **`pyproject.toml`**. **Implementation** (**pytest-cov** pin,
**`[tool.pytest.ini_options]`**, contract tests, and **CI** running **`pytest`**) is in tree; extend tests when new
boundary rows appear here.

### Scope of “the demo” for coverage

- **Primary:** `src/replayt_ux_showcase/demo.py` — the console timeline module described in **`docs/demo.md`**.
- **Out of scope for the 80% gate:** static files under **`docs/examples/`** (see [Showcase stack matrix](#showcase-stack-matrix));
  future browser automation or framework tests are tracked separately when those examples ship CI.

### Line coverage (acceptance: 80%+ on demo)

- **Metric:** CPython **line** coverage for **`src/replayt_ux_showcase/demo.py`** only (not the whole package tree),
  measured in default contributor and **CI** flows after **`pip install -e ".[dev]"`**.
- **Threshold:** **≥ 80%** lines covered. **CI** MUST fail if coverage falls below the threshold (non-zero exit).
- **Tooling:** **`pytest-cov`** (or equivalent that honors the same threshold semantics) with an **explicit PEP 508**
  version constraint on its own line under **`[project.optional-dependencies].dev`**.

### “Fails on boundary breaks” (acceptance)

Tests MUST cause **CI** to fail when integration boundaries or the demo contract regress. At minimum this includes:

| Boundary / contract | Intent | Examples of what to enforce (Builder) |
| ------------------- | ------ | ------------------------------------- |
| **Design principles metadata** | Pins, matrices, and headings stay aligned with **`pyproject.toml`** and **CI** | Existing `tests/test_design_principles_contract.py` (extend when new normative rows are added here) |
| **Demo behavioral spec** | Observable behavior matches **`docs/demo.md`** | Subprocess **`python -m replayt_ux_showcase.demo`**, exports, log prefixes, sample data shape (see **`docs/demo.md`** test plan) |
| **replayt Python API boundary** | Showcase code does not depend on private or undocumented **replayt** symbols | Lint/review plus tests: if **`demo.py`** (or other showcase modules under test) import **replayt**, imports MUST be restricted to **published** **`__all__`** / documented public surface; removing or renaming those symbols in a supported **replayt** release is an upstream semver concern—this repo adjusts pins and tests per [Migration paths](#migration-paths) |
| Declared **replayt** range | Supported consumer range in **`pyproject.toml`** matches [Replayt and Python matrix](#replayt-and-python-matrix) | Contract tests on the **replayt** dependency line; optional smoke that **`import replayt`** succeeds after install (already part of contract tests today) |

“Integration” here means **tests run against the installed environment** (editable install + resolved **replayt**),
not mocked **replayt** internals.

### Dev dependencies (acceptance: in pyproject.toml)

- **`pytest`** is the test runner; **`pytest-cov`** is a direct **dev** dependency with a PEP 508 constraint (see
  [Dev optional dependency set (baseline)](#dev-optional-dependency-set-baseline)).
- **`[tool.pytest.ini_options]`** in **`pyproject.toml`** passes **`--cov=replayt_ux_showcase.demo`** and
  **`--cov-fail-under=80`** so local **`pytest`** and **CI** (`python -m pytest tests`) share the same gate.

### Traceability (implementation)

**CI** and contributor **`pytest`** runs enforce at least:

| Check | Enforced by |
| ----- | ----------- |
| Line coverage **≥ 80%** on **`src/replayt_ux_showcase/demo.py`** | **`pytest`** + **`pytest-cov`** via **`[tool.pytest.ini_options]`** (`--cov-fail-under=80`) |
| Demo subprocess and data-shape checks | **`tests/`** per **`docs/demo.md`** (including in-process calls so **pytest-cov** traces **`demo.py`**) |
| **replayt** pin, **dev** pins, and design-principles structure | **`tests/test_design_principles_contract.py`** (extend if new spec rows require it) |
| **replayt** import surface in **`demo.py`** | **`tests/test_demo.py`** asserts the module source does not import the **`replayt`** package (stdlib-only demo) |

### Backlog traceability: Add unit/integration tests for demo

**Normalized user story:** As maintainer, I want a **pytest** suite that covers **demo** behavior, enforces **replayt**
integration boundaries, and runs in **CI** with coverage and explicit **dev** tooling pins.

| Backlog acceptance criterion | Where specified | How it is verified (target) |
| ---------------------------- | --------------- | --------------------------- |
| **80%+ coverage on demo** | [Line coverage](#line-coverage-acceptance-80-on-demo) | **`pytest-cov`** on **`demo.py`** with fail-under **80** in **CI** |
| **Fails on boundary breaks** | [Fails on boundary breaks](#fails-on-boundary-breaks-acceptance) | Failing tests / non-zero **pytest** when spec, pins, or public **replayt** usage regress |
| **In pyproject.toml dev deps** | [Dev dependencies](#dev-dependencies-acceptance-in-pyprojecttoml), [Dev optional dependency set (baseline)](#dev-optional-dependency-set-baseline) | **`pytest`** and **`pytest-cov`** under **`[project.optional-dependencies].dev`** with PEP 508 constraints; **`test_dev_optional_dependencies_match_baseline_package_set`** matches the baseline table |

**Maintainer checklist (follow-up):**

1. When raising or adding coverage gates, update **`[tool.pytest.ini_options]`**, **CHANGELOG**, and this section together.
2. When **`demo.py`** begins importing **replayt**, replace or extend the stdlib-only import test with an assertion that
   imported names are a subset of the published **`replayt`** public surface (per [Fails on boundary breaks](#fails-on-boundary-breaks-acceptance)).

---

## Dependency pins and dev toolchain

Normative spec for pinning **replayt** and contributor **dev** dependencies in **`pyproject.toml`** (consumer-side
constraints; integration boundaries). **`pyproject.toml`** and `tests/test_design_principles_contract.py` implement
this section; it is what “done” means.

### Goals

- **`pip install -e ".[dev]"`** is the supported local/CI entrypoint and must remain reliable.
- Declared dependencies are **explicit** enough for review, security tooling (e.g. **pip-audit** in **dev**), and
  integrators reading the repo—not ambiguous “latest” direct requirements.

### PEP 508 vs caret-style wording

- Python uses **PEP 508** requirement specifiers in **`pyproject.toml`**, not npm’s **`^` / `~`** syntax.
- When the backlog or integrator docs refer to a **caret**-style pin (e.g. “^0.4”), interpret that as a **bounded
  compatible range** on the **replayt** line (for example `>=0.4.0,<0.5.0`, or **`~=0.4.0`** if the intent is “0.4.x
  only” per PEP 440). The **Maintainers** choose numeric bounds that match supported policy, what CI exercises, and
  **CHANGELOG** notes when crossing lines.

### Acceptance criteria (implementation)

1. **`pip install -e ".[dev]"`** completes successfully on Python versions this repo claims under **`requires-python`**
   and in CI (see [Replayt and Python matrix](#replayt-and-python-matrix)).
2. **`replayt` is importable** after that install (e.g. `python -c "import replayt"` or via existing package/tests that
   import **replayt** through its public API).
3. **No loose direct requirements** — every line in **`[project].dependencies`** and in
   **`[project.optional-dependencies].dev`** MUST include at least one explicit version constraint (lower bound, and
   for **replayt** preferably a **compatible upper bound** unless maintainers document a deliberate “open ceiling”
   policy in the matrix notes).
4. **`[build-system].requires`** entries remain constrained (e.g. **`setuptools>=61`**), not bare unpinned names.
5. **Single change set for truth** — when the **replayt** specifier or supported-range story changes, update
   **`pyproject.toml`**, the [Replayt and Python matrix](#replayt-and-python-matrix) **Supported (policy)** cell,
   **`tests/test_design_principles_contract.py`** (as needed), and **CHANGELOG** **Unreleased** together, per
   [Traceability to automated checks](#traceability-to-automated-checks).

### Dev optional dependency set (baseline)

These are the **direct** **dev** tools expected under **`[project.optional-dependencies].dev`** today; each keeps
explicit version constraints on its line:

| Package | Role |
| ------- | ---- |
| **pytest** | Test runner |
| **pytest-cov** | Line coverage and **`--cov-fail-under`** for **`src/replayt_ux_showcase/demo.py`** (via **`[tool.pytest.ini_options]`**) |
| **ruff** | Lint/format (as adopted by the repo) |
| **pip-audit** | Supply-chain / vulnerability checks in contributor workflows |

Adding, renaming, or dropping a **dev** tool updates this table, **CHANGELOG**, and (when applicable) CI or docs that
mention the workflow.

### Out of scope for “pins” here

- Committing a **lock file** or **`pip freeze`** output is **not** required by this spec unless maintainers adopt that
  separately. **Pins** mean **declared constraints in `pyproject.toml`** for **direct** dependencies; transitive versions
  follow the resolver unless a stricter policy is adopted later.

### Backlog traceability: Pin replayt dependency and dev tools in pyproject.toml

This subsection maps the staff-engineering backlog item to this document so **Spec gate** and **Builder** (phase 3)
can confirm intent without re-deriving it. **Implementation and contract-test edits** belong to the Builder phase
unless a change here explicitly requires synchronized updates to **`pyproject.toml`**, **`tests/test_design_principles_contract.py`**, and **CHANGELOG**.

**Normalized user story:** Maintainers and integrators want **replayt** and direct **dev** dependencies declared in
**`pyproject.toml`** with explicit PEP 508 constraints so editable installs are reproducible, reviewable, and
covered by the dependency contract tests.

| Backlog acceptance criterion | Where specified | How it is verified (today) |
| ---------------------------- | --------------- | -------------------------- |
| **`pip install -e .[dev]`** works | [Goals](#goals) and [Acceptance criteria (implementation)](#acceptance-criteria-implementation) item 1 | Contributor **README** quick start and CI use **`pip install -e ".[dev]"`** (quoted extras are reliable in **POSIX** shells; unquoted **`.[dev]`** matches backlog wording but may need quotes under **zsh** / some setups); `test_ci_installs_editable_with_dev_extras` asserts the workflow keeps that command |
| **replayt** importable | [Acceptance criteria (implementation)](#acceptance-criteria-implementation) item 2 | `tests/test_design_principles_contract.py` (`test_replayt_importable`) after install |
| No loose direct deps | [Acceptance criteria (implementation)](#acceptance-criteria-implementation) items 3–4 and [Dev optional dependency set (baseline)](#dev-optional-dependency-set-baseline) | Same test module: every line in **`[project].dependencies`**, **`[project.optional-dependencies].dev`**, and **`[build-system].requires`** carries a non-empty PEP 508 specifier; **replayt** line must match [Replayt and Python matrix](#replayt-and-python-matrix); **`test_dev_optional_dependencies_match_baseline_package_set`** keeps **dev** to **pytest**, **pytest-cov**, **ruff**, **pip-audit** |

**Caret-style backlog wording (e.g. “^0.1” for **replayt**):** Express in **`pyproject.toml`** using PEP 508 only—see
[PEP 508 vs caret-style wording](#pep-508-vs-caret-style-wording). The numeric range in **`pyproject.toml`** and the
matrix is authoritative, not npm **`^` / `~`**.

**Builder checklist (phase 3):**

1. Keep a **single** **`replayt`** entry in **`[project].dependencies`** whose specifier matches the matrix and
   **`test_replayt_dependency_matches_design_principles_matrix`** (lower bound and **`<0.5`**-style cap unless the
   matrix and tests are intentionally revised together).
2. Keep **`[project.optional-dependencies].dev`** aligned with [Dev optional dependency set (baseline)](#dev-optional-dependency-set-baseline)
   (**pytest**, **pytest-cov**, **ruff**, **pip-audit**). Adding, renaming, or dropping a tool requires updating this table,
   **CHANGELOG**, and any workflow docs that mention the tool, in the same change set as **`pyproject.toml`**.
3. After any pin or dev-set change, run **`pip install -e ".[dev]"`** and **`pytest`** on the CI Python version;
   update **CHANGELOG** **Unreleased** per [Single change set for truth](#acceptance-criteria-implementation).

---

## GitHub Actions CI workflow

Normative spec for the backlog item **Set up GitHub Actions CI for tests and linting**: what “runs on push/PR”, “fails on
dirty tests”, **ruff**, **replayt** compatibility, observable logs, and **README** badges mean. **Implementation**
(workflow YAML, badge URLs with the real **GitHub** `owner/repo`, and any new contract assertions) is **Builder**
work unless a change here explicitly requires synchronized updates to **`.github/workflows/ci.yml`**, **README**, and
**`tests/test_design_principles_contract.py`**.

### Canonical workflow file

- **Path:** **`.github/workflows/ci.yml`** — single primary workflow for PR/push automation on this repo (name aligns with
  contract tests that read this file).

### Triggers (acceptance)

- **Pull requests:** MUST run on **`pull_request`** for the branch(es) this project integrates to (for example
  **`master`** and optional **`mc/**`** when Mission Control backlog branches are in use). Adjust the **`branches:`**
  filter here and in **README** badge examples if the default branch is renamed.
- **Push:** MUST run on **`push`** to the same branch set (or document a deliberate narrower policy in this section if
  maintainers intentionally skip some push events).
- **Optional:** **`workflow_dispatch`** for manual runs is allowed.

### Observable automation (acceptance)

- Use **clear step names** (install, tests, lint, supply chain) so logs identify what failed.
- Steps MUST **propagate failure** (**non-zero** exit) for **pytest**, **ruff**, and **pip-audit**; do not mask failures
  with `|| true` unless a step is explicitly non-blocking and documented as such.

### Jobs and commands (normative target)

| Job / concern | Requirement | Verified by (target) |
| ------------- | ----------- | -------------------- |
| **Install** | **`pip install -e ".[dev]"`** (quoted extras) on the **CI Python** version from [Replayt and Python matrix](#replayt-and-python-matrix) | `test_ci_installs_editable_with_dev_extras`; green CI logs |
| **Tests** | Run **`python -m pytest`** from the repo root so **`[tool.pytest.ini_options]`** applies ( **`--cov=replayt_ux_showcase.demo`**, **`--cov-fail-under=80`**, etc.). Extra CLI flags (e.g. **`-q`**, **`--tb=short`**) are fine if they do **not** remove coverage options. **CI** MUST install **dev** extras so **pytest-cov** is available — a plain editable install **without** **`[dev]`** is **not** sufficient for the coverage gate. | [Demo module testing and replayt integration boundaries](#demo-module-testing-and-replayt-integration-boundaries); green **`test`** job |
| **Lint** | Run **`ruff check`** at the repository root (use **`pyproject.toml`** **`[tool.ruff]`** when present). If the repo adopts enforced formatting in CI, add **`ruff format --check`** in the same or a dedicated step. | Non-zero on violations; **Spec gate** treats missing **ruff** in CI as incomplete for this backlog |
| **replayt** compatibility | **replayt** is resolved by the runtime install per **`[project].dependencies`**; contract tests and the **pytest** suite exercise pins, import smoke, and integration boundaries ([Demo module testing](#demo-module-testing-and-replayt-integration-boundaries), [Dependency pins](#dependency-pins-and-dev-toolchain)) | **`test_replayt_importable`**, **`test_replayt_dependency_matches_design_principles_matrix`**, and full **`pytest`** run in CI |
| **Supply chain** | Keep **`pip-audit`** aligned with **`docs/DEPENDENCY_AUDIT.md`** (including documented **`--ignore-vuln`** entries that match the workflow). | Existing **`supply-chain`** (or equivalent) job |

### README badges (acceptance)

- **README.md** MUST include at least one **GitHub Actions** workflow status badge for **`ci.yml`**, linking to the
  workflow or **Actions** tab. Substitute the real **`OWNER/REPO`** (for example
  **`https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg`** with a matching **`href`** to the same repo’s
  workflow). **shields.io** equivalents are acceptable if they reference the same workflow and default branch policy.
- Badges are **documentation surface**: when the default branch or workflow file is renamed, update **README** and this
  section in the same change set.

### Backlog traceability: Set up GitHub Actions CI for tests and linting

**Normalized user story:** As platform engineer, I want **`.github/workflows/ci.yml`** enforcing **pytest** (with the
same coverage gate as local **dev** installs), **ruff**, and **replayt** compatibility on PRs and pushes, with
observable logs and **README** badges.

| Backlog acceptance criterion | Where specified | How verified (target) |
| ---------------------------- | --------------- | ---------------------- |
| Runs on push/PR | [Triggers](#triggers-acceptance) | **`on:`** in **`ci.yml`** |
| Fails on dirty tests | [Jobs and commands](#jobs-and-commands-normative-target) (**Tests** row) | **pytest** non-zero on failures / coverage below threshold |
| Badges in **README** | [README badges](#readme-badges-acceptance) | **README.md** workflow badge URL; `tests/test_design_principles_contract.py` (`test_readme_ci_badge_uses_repository_slug`) |
| **ruff** | [Jobs and commands](#jobs-and-commands-normative-target) (**Lint** row) | **`ruff check`** and **`ruff format --check`** in CI; `test_ci_runs_ruff_lint_and_format_check` |
| **replayt** compat | [Jobs and commands](#jobs-and-commands-normative-target) (**replayt** row) | Editable **dev** install + **pytest** + contract tests |

**Builder checklist (phase 3):**

1. Ensure the **test** job installs **`".[dev]"`** and runs **pytest** in a way that keeps the **pytest-cov** gate (see
   phase **1c** logs: **exit code 4** / “unrecognized **--cov**” indicates **pytest-cov** not installed or **addopts**
   stripped).
2. Add **`ruff check`** (and **`ruff format --check`** if required) to **`ci.yml`**; keep **pip-audit** policy in sync
   with **`docs/DEPENDENCY_AUDIT.md`**.
3. Add **README** workflow badge(s) with the actual **GitHub** coordinates; extend **`tests/test_design_principles_contract.py`**
   if maintainers want CI to assert **ruff** (and/or badge presence) mechanically.
4. Record user-visible CI changes under **CHANGELOG** **Unreleased**.

---

## Replayt and Python matrix

Policy vs what CI currently exercises may differ; **CI must not claim coverage it does not run**. Expand matrix jobs
when additional cells become required.

| Dimension | Supported (policy) | Verified in CI today | Migration / notes |
| --------- | ------------------- | -------------------- | ------------------ |
| **replayt** (PyPI) | `replayt>=0.1.0,<0.5.0` in `[project].dependencies` (PEP 508); MUST match [Dependency pins and dev toolchain](#dependency-pins-and-dev-toolchain) | Latest **replayt** allowed by that range on `pip install -e ".[dev]"` (see lock-free installs in CI logs) | The `<0.5` cap excludes 0.5+ until maintainers widen the range after compatibility checks; any change to bounds updates this cell, contract tests, and **CHANGELOG** together; on breaking **replayt** majors, add migration notes and adjust examples or shims **in this repo**; propose upstream fixes through normal channels |
| **Python** | `>=3.11` per `requires-python` | **3.12** on `ubuntu-latest` (`.github/workflows/ci.yml`) | Adding 3.11 to the matrix is optional; document if parity is required for integrators |

---

## Showcase stack matrix

Front-end stacks are **documented** here before (or as) examples land. “Supported” means we intend integrators to
copy the pattern; “CI” means automated verification exists.

| Stack | Supported (intent) | CI | Notes |
| ----- | ------------------- | --- | ----- |
| Vanilla HTML/JS | Yes (`docs/examples/`) | File/smoke tests as implemented under `tests/` | Default integration path for smallest surface |
| React | ^18 when a React example exists | Not required until a React demo ships | Copy-paste snippets per the mission |
| Vue | ^3 when a Vue example exists | Not required until a Vue demo ships | Same as React |
| Svelte | ^4 when a Svelte example exists | Not required until a Svelte demo ships | Same as React |

---

## Extension points

What integrators and maintainers may rely on or extend:

| Audience | Extension point | Stability expectation |
| -------- | ----------------- | ---------------------- |
| **Integrators** | Static files under **`docs/examples/`** as copy-paste starting points | Examples may gain features; breaking filename or contract changes follow [Deprecation and removal](#deprecation-and-removal) |
| **Integrators** | **replayt** APIs used in examples (imports, session/event shapes) | Governed by **replayt** semver and this repo’s stated supported range |
| **Integrators** | **`replayt_ux_showcase`** entrypoints and helpers described in README or package docs as stable | SemVer for behavior; breaking CLI or import paths follow [Deprecation and removal](#deprecation-and-removal) |
| **Maintainers** | New pytest coverage and optional CI matrix dimensions | Internal to repo; must keep logs and exit codes obvious ([Observable automation](#principles)) |
| **Maintainers** | Optional **`docs/reference-documentation/`** snapshots | Contributor convenience only; not a substitute for upstream docs |

**Non–extension points:** Undocumented imports from **replayt**, private modules, or scraping this repo’s CI logs as
an API.

---

## Deprecation and removal

1. **Announce** in **CHANGELOG** under **Unreleased** with a **Deprecated** subsection (or clear **Changed** note)
   stating what replaces the old path and the last version where the old path works.
2. **Minimum horizon** — Keep deprecated demo paths or module aliases for **at least one** published **minor**
   release when external users could have linked to them, unless a security issue forces immediate removal.
3. **Remove** in a subsequent release with **Removed** in CHANGELOG and a short migration bullet (e.g. “replace
   `old-demo.html` with `new-demo.html`”).
4. **Semver** — This package follows SemVer for **Python package** behavior (`pyproject.toml` version). Purely
   documentary moves can ship in patch releases; **removal** of a documented example or CLI behavior is at least
   **minor** unless explicitly marked experimental.

---

## Migration paths (replayt and repo)

| Trigger | Maintainer actions |
| ------- | ------------------ |
| **replayt** minor/major with API changes | Update examples and tests; refresh matrices; **CHANGELOG** with “how to update your copy” bullets |
| **New Python floor** | Update `requires-python`, CI images, and the [Replayt and Python matrix](#replayt-and-python-matrix) |
| **New framework example** | Add under **`docs/examples/`** (or scoped subdir), link from README/demo spec, add showcase row above |
| **Integrator upgrading** | Compare their pinned **replayt** to this repo’s supported range; follow **CHANGELOG** for the showcase version they target |
| **Dev toolchain or replayt pin change** | Update **`pyproject.toml`**, [Dependency pins and dev toolchain](#dependency-pins-and-dev-toolchain) / matrix cells, contract tests, and **CHANGELOG** in one change set |

---

## LLM boundaries

This repo’s **default** posture is **static demos and documentation**—no hosted model calls, no API keys, no usage
metering in CI.

| Rule | Detail |
| ---- | ------ |
| **Secrets** | Never commit API keys, tokens, or `.env` with real credentials. Examples use placeholders only. |
| **replayt LLM helpers** | If an example uses **replayt**’s mock or workflow LLM utilities (e.g. `MockLLMClient`, `run_with_mock`), keep it **offline/deterministic** in CI and document that in the demo’s spec or header comment. |
| **Future “live” demos** | Require an explicit maintainer decision, opt-in env vars documented in **README** or **docs/demo.md**, and must not run by default in CI. |
| **Costs** | CI and default contributor workflows must not incur model spend. |

---

## Principles

1. **Explicit contracts** — Document supported **replayt** (and third-party framework) versions; test integration
   boundaries as the matrix and CI jobs are expanded.
2. **Small public surfaces** — Prefer narrow Python APIs and documented extension points (see above).
3. **Observable automation** — Local scripts and CI produce clear logs and non-zero exit codes on failure.
4. **Consumer-side maintenance** — Compatibility shims and pins live **here**; upstream changes are tracked with tests
   and changelog notes.
5. **Not a lever on core** — This repo does not exist to steer **replayt** core; propose upstream changes through normal
   channels.

---

## Audience

| Audience | Needs |
| -------- | ----- |
| **Maintainers** | Mission, scripts, pinned versions, release notes, CI matrix truth vs policy, deprecation policy |
| **Integrators** | Stable adapter surface, compatibility matrix, copy-paste examples, migration notes in CHANGELOG |
| **Contributors** | README, tests, coding expectations, directory boundaries, “one way to do it” for new examples |
| **Design / DX** | Tokens and handoff checklist alignment (playbook docs); clarity on what is example-only vs maintained API |
| **Security / compliance** | No secrets in repo; LLM and third-party boundaries; supply-chain audit expectations in CI |
| **Release / tag consumers** | SemVer and CHANGELOG for removals; matrix “policy vs CI” truth at the version they pin |
| **Automation agents (LLM tooling)** | Respect [LLM boundaries](#llm-boundaries); treat this file and `tests/` as normative for boundaries—do not invent alternate package layouts or secret-handling rules |
