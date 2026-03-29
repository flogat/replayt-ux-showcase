# Design principles

Revise as the project matures. This document is the **canonical contract** for integration boundaries, versioning,
and how demos and tooling may evolve. Prefer updating **one** source of truth here and linking from README or
mission docs rather than duplicating rules.

## Acceptance criteria (traceability)

The following backlog outcomes are satisfied **by this spec** (implementation of CI matrix rows, new examples, etc.
is tracked separately in code and CHANGELOG):

| Criterion | Where addressed |
| --------- | ----------------- |
| Version matrix table | [Replayt and Python matrix](#replayt-and-python-matrix), [Showcase stack matrix](#showcase-stack-matrix), [Compatibility matrix and upgrade paths](#compatibility-matrix-and-upgrade-paths), [Compatibility digest (integrators)](compat.md) |
| Compatibility matrix, CI coverage truth, shims, upgrade paths | [Compatibility matrix and upgrade paths](#compatibility-matrix-and-upgrade-paths), [Compatibility digest (integrators)](compat.md) |
| **replayt** / dev-tool pins and “no loose deps” | [Dependency pins and dev toolchain](#dependency-pins-and-dev-toolchain) |
| Demo **pytest** coverage and **replayt** boundary tests | [Demo module testing and replayt integration boundaries](#demo-module-testing-and-replayt-integration-boundaries) |
| **docs/examples** replayt pins vs **`pyproject.toml`** | [Vanilla examples: integrator-facing replayt pins](#vanilla-examples-integrator-facing-replayt-pins) |
| **Front-end** CDN vs bundled **replayt**, optional **SRI**, **npm**/**Vite** notes | [Frontend supply chain (JavaScript / CDN)](#frontend-supply-chain-javascript--cdn), [`docs/FRONTEND_SUPPLY_CHAIN.md`](FRONTEND_SUPPLY_CHAIN.md) |
| Optional **npm** workspace / **Vite** or **esbuild** local preview (**not** a published package) | [`docs/examples/build.md`](examples/build.md), [Module and directory boundaries](#module-and-directory-boundaries), [Showcase stack matrix](#showcase-stack-matrix) |
| **GitHub Actions** CI (tests, **ruff**, **replayt** install path, supply chain, badges) | [GitHub Actions CI workflow](#github-actions-ci-workflow) |
| Extension points documented | [Extension points](#extension-points) |
| Audience needs extended | [Audience](#audience) |
| Distinct vanilla UI patterns (mission: **5+**), per-pattern acceptance | [Vanilla UI pattern catalog](#vanilla-ui-pattern-catalog), [examples/PATTERNS.md](examples/PATTERNS.md), [MISSION.md](MISSION.md#pattern-coverage-tracking) |
| Timeline / player **keyboard** and **focus** (handoff checklist) | [`docs/a11y/keyboard-model.md`](a11y/keyboard-model.md), [Vanilla UI pattern catalog](#vanilla-ui-pattern-catalog) (shared contract), [examples/PATTERNS.md](examples/PATTERNS.md) (per-pattern rules) |
| Offline deterministic **fixture** page for **LLM** / reviewer harnesses | [Offline deterministic fixture page](#offline-deterministic-fixture-page-for-llm-and-reviewer-workflows), [LLM boundaries](#llm-boundaries), **[P-05](examples/PATTERNS.md#p-05-offline-deterministic-fixture-page-for-llm-and-reviewer-workflows)** |

### Traceability to automated checks

These alignments are **enforced in CI** today (the principles doc is broader):

| Check | Enforced by |
| ----- | ----------- |
| `requires-python` matches the Python row in [Replayt and Python matrix](#replayt-and-python-matrix) | `tests/test_design_principles_contract.py` |
| **`replayt`** dependency specifier matches that matrix (`>=0.1.0` and compatible `<0.5` cap, per `tests/test_design_principles_contract.py`) | Same |
| CI **Python** version(s) in the **test** job matrix in `.github/workflows/ci.yml` match that matrix | Same |
| Section headings for the two matrices, extension points, and audience | Same |
| Subsection **replayt Python API boundary** under [Module and directory boundaries](#module-and-directory-boundaries) | Same |
| Extension points row for packaged **`replayt_ux_showcase`** surface | Same |
| Audience rows for **Release / tag consumers** and **Automation agents (LLM tooling)** | Same |
| Each line in **`[project].dependencies`** and **`[project.optional-dependencies].dev`** carries a PEP 508 version constraint | Same |
| **`[project.optional-dependencies].dev`** package names match [Dev optional dependency set (baseline)](#dev-optional-dependency-set-baseline) | Same |
| **`[build-system].requires`** entries carry a PEP 508 version constraint | Same |
| **`replayt` is importable** after install (integration smoke) | Same |
| **`[project].version`** matches **`replayt_ux_showcase.__version__`** | Same (`test_package_version_matches_pyproject`) |
| CI installs with **`pip install -e ".[dev]"`** (quoted extras) per contributor entrypoint | Same |
| **pytest** in CI honors **`[tool.pytest.ini_options]`** (coverage on **`demo.py`**, fail-under) | [GitHub Actions CI workflow](#github-actions-ci-workflow) — job command MUST NOT drop the **cov** gate (requires **dev** install with **pytest-cov**) |
| **`ruff check`** (and **`ruff format --check`** when enforced) run in CI after **dev** install | [GitHub Actions CI workflow](#github-actions-ci-workflow); `tests/test_design_principles_contract.py` (`test_ci_runs_ruff_lint_and_format_check`) |
| explicit **replayt** version pins in **`docs/examples/`** match the **`replayt`** PEP 508 range in **`pyproject.toml`** | `tests/test_docs_examples_replayt_pins.py` (see [Vanilla examples: integrator-facing replayt pins](#vanilla-examples-integrator-facing-replayt-pins)); includes **`docs/examples/build.md`** when present |
| **`docs/FRONTEND_SUPPLY_CHAIN.md`** section anchors, keywords, cross-links, and **CHANGELOG** **Unreleased** mention (**A1–A5** in that doc) | `tests/test_frontend_supply_chain_doc.py` |
| Root **`package.json`** (optional **npm** bundler recipe) | **Not** asserted in **CI** today; when shipped, MUST follow [`docs/examples/build.md`](examples/build.md) (**`private`**, pytest-first **CI**); **npm** **`replayt`** semver MUST stay inside the **`pyproject.toml`** band (manual review; **`tests/test_docs_examples_replayt_pins.py`** covers **`docs/examples/build.md`**) |
| Optional **`integrity`** (**SRI**) on CDN **`<script>`** tags in examples | **Not** enforced in **CI** today; if present, must match the pinned URL’s bytes — see [`docs/FRONTEND_SUPPLY_CHAIN.md`](FRONTEND_SUPPLY_CHAIN.md) |

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
   pattern ships; avoid parallel unofficial copies at repo root. An **optional** repository-root **`package.json`**
   (**`"private": true`**) may exist **only** as a **maintainer** bundler recipe for **local preview**, documented in
   **[`docs/examples/build.md`](examples/build.md)** — not as a second canonical snippet tree or an implied **npm**
   publication (see [Module and directory boundaries](#module-and-directory-boundaries)).
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
| **`package.json`** (repo root, optional) | **Private** **npm** metadata + scripts for **Vite** / **esbuild** local bundling per **[`docs/examples/build.md`](examples/build.md)** | Imply a **published** **npm** product for this repository, or omit **`"private": true`**, without an explicit maintainer decision and **CHANGELOG** entry |
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

### Vanilla examples: integrator-facing replayt pins

Normative spec for copy-paste **HTML** and **Markdown** under **`docs/examples/`**: any **explicit** **replayt** version
pin shown to integrators MUST stay inside the supported consumer range declared on the **`replayt`** line in
**`[project].dependencies`** (same PEP 508 story as [Replayt and Python matrix](#replayt-and-python-matrix) and
[Dependency pins and dev toolchain](#dependency-pins-and-dev-toolchain)). **Enforcement:** **`tests/test_docs_examples_replayt_pins.py`**
via default **`pytest`** discovery (**CI** included). When detection rules or pins change, update **CHANGELOG** **Unreleased** in the same change set.

#### Scope (files)

- **Include:** every **`*.html`** and **`*.md`** file under **`docs/examples/`**, recursively (future
  **`docs/examples/react/`**-style trees included automatically).
- **Ignore:** other paths (e.g. **`docs/demo.md`**, **`README.md`**) unless a later backlog expands the contract.

#### What counts as a “pin” (detection)

A **pin** is a machine-extractable **replayt** version or requirement that an integrator might copy verbatim.

| Kind | Intent (Builder) | Notes |
| ---- | ------------------ | ----- |
| **npm / CDN URL** | `replayt@<version>` in a URL path (e.g. **jsDelivr**, **unpkg**, similar CDNs that encode the package version in the path) | Extract **`<version>`** as a PEP 440 version if possible; pre-release segments allowed when present in the snippet. |
| **Markdown / prose requirement lines** | A line (including inside fenced code blocks) that names the **`replayt`** distribution with a PEP 508-style constraint (`replayt==…`, `replayt>=…`, `replayt~=…`, comma-separated specifiers, or **`"replayt"`** / **`'replayt'`** entries in **`requirements*.txt`**-style or **`pyproject.toml`**-style examples) | The **declared constraint** MUST be **compatible with** the showcase’s **`[project].dependencies`** **replayt** specifier (i.e. every version allowed by the snippet’s constraint lies inside the range allowed by **`pyproject.toml`**, unless [Opt-out](#opt-out-documented-exceptions) applies). |
| **`latest` / unpinned** | URLs or prose that load **`replayt`** without a path or label version | **Out of scope** for this contract unless/until maintainers adopt a stricter policy; the goal is to catch **drift ahead** of the supported range (e.g. **`@0.6.0`** while the repo still caps **`<0.5`**). |

False positives (mentions of the word “replayt” without a version contract) SHOULD NOT fail CI; prefer narrow patterns
and clear test failure messages listing **file**, **line**, and **extracted token**.

#### Acceptance (assertion)

- Read the **`replayt`** requirement from **`pyproject.toml`** at test time (same pattern as
  **`tests/test_design_principles_contract.py`**: **`packaging.requirements.Requirement`** or equivalent).
- For each **pin** found in scope:
  - If it is a **single concrete version** (typical CDN case), assert that version **satisfies** the **`pyproject.toml`**
    specifier set.
  - If it is a **requirement string / specifier set** (typical Markdown example), assert that the **intersection** of
    “versions integrators could resolve from the snippet” is **non-empty** and **fully contained** in the versions
    allowed by **`pyproject.toml`** (equivalently: the snippet must not permit a version outside the declared showcase
    range). When this is awkward to compute, it is acceptable to require the snippet’s specifier to be **stricter or
    equal** to the showcase line (document the chosen rule in the test module docstring).
- When **`[project].dependencies`** **`replayt`** line or matrix policy changes, update **examples**, this section if
  the detection rules change, **`tests/`**, and **CHANGELOG** in one change set.

#### Opt-out (documented exceptions)

When an example **intentionally** shows an unsupported or transitional pin (e.g. migration narrative), the line **immediately
before** the exempt URL or fenced block MUST contain an HTML comment:

`<!-- replayt-examples:pin-exempt -->`

Optional text: `<!-- replayt-examples:pin-exempt reason="migration demo" -->`. The comment applies only to the **next**
non-empty line that would otherwise be scanned (single `<script src=…>`, single URL line, or single fenced code block).
Maintainers MUST keep **`reason=`** meaningful for reviewers. Human-readable explanation in prose above the snippet is
encouraged but **does not** replace the comment for CI.

**CDN delivery, optional SRI, bundlers:** See [`docs/FRONTEND_SUPPLY_CHAIN.md`](FRONTEND_SUPPLY_CHAIN.md) and
[Frontend supply chain (JavaScript / CDN)](#frontend-supply-chain-javascript--cdn) for **jsDelivr**-style URLs,
**Subresource Integrity**, and **npm**/**Vite** alternatives aligned with this pin contract.

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
| **docs/examples** replayt pins | Integrator snippets do not advertise **replayt** versions outside the declared PEP 508 range | **`tests/test_docs_examples_replayt_pins.py`** (or equivalent) scans **`docs/examples/**/*.{html,md}`** per [Vanilla examples: integrator-facing replayt pins](#vanilla-examples-integrator-facing-replayt-pins) |

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
| **docs/examples** **replayt** pins vs **`pyproject.toml`** | **`tests/test_docs_examples_replayt_pins.py`** |

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

### Backlog traceability: Contract test — examples reference replayt in supported semver range

**Normalized user story:** As maintainer, I want **pytest** to scan **`docs/examples/**/*.{html,md}`** for **replayt**
CDN or package pins and fail when any pin falls outside the PEP 508 range declared in **`pyproject.toml`**, so
integrator-facing snippets stay aligned with [DESIGN_PRINCIPLES](#design-principles) and **`docs/compat.md`**.

| Backlog acceptance criterion | Where specified | How verified |
| ---------------------------- | --------------- | ------------------------ |
| **Scan scope** | [Scope (files)](#scope-files) | **`tests/test_docs_examples_replayt_pins.py`** enumerates **`docs/examples/**/*.html`** and **`docs/examples/**/*.md`**. |
| **Detection rules** | [What counts as a “pin” (detection)](#what-counts-as-a-pin-detection) | Implementation matches the table; probe-grid simplifications are documented in the test module docstring. |
| **Assertion vs `pyproject.toml`** | [Acceptance (assertion)](#acceptance-assertion) | Each detected pin satisfies or is subsumed by the **`replayt`** specifier from **`[project].dependencies`**. |
| **Documented exceptions** | [Opt-out (documented exceptions)](#opt-out-documented-exceptions) | Snippets with **`<!-- replayt-examples:pin-exempt -->`** (and optional **`reason=`**) are skipped per rules above. |
| **Range changes** | [Acceptance (assertion)](#acceptance-assertion) | Same change set: **`pyproject.toml`**, matrices, affected examples, tests, **CHANGELOG** **Unreleased**. |

**Maintainer checklist:**

1. When extending detection rules or **`docs/examples/`** pins, update **`tests/test_docs_examples_replayt_pins.py`** (patterns, probe grid, or **`_EXTRA_PROBE_VERSIONS`**) and this section if the normative table changes, in one change set with **CHANGELOG** **Unreleased**.
2. Renaming the test module requires updating [Traceability to automated checks](#traceability-to-automated-checks) and **`docs/compat.md`** in the same change set.

---

## Frontend supply chain (JavaScript / CDN)

Normative detail for loading **replayt**’s **npm**-published browser bundle via **CDN** (e.g. **jsDelivr**, as in
**`docs/examples/basic-player.html`**), optional **Subresource Integrity** (**SRI**), and **bundlers** (**Vite**,
**webpack**, and similar) is in **[`docs/FRONTEND_SUPPLY_CHAIN.md`](FRONTEND_SUPPLY_CHAIN.md)**.

**Single compatibility story:** **`[project].dependencies`** **`replayt`** (PEP 508) remains the **authoritative**
supported range for **both** Python and **front-end** pins. When support moves, update **`pyproject.toml`**, matrices
in **this document**, **`docs/compat.md`**, **`docs/examples/`** CDN segments (and any example **SRI** hashes), **tests**
if pin rules change, and **CHANGELOG** **Unreleased** **together** (see [One way to do it](#one-way-to-do-it-canonical-patterns)).

**Python vs JS tooling:** **`pip-audit`** covers the **editable** **Python** install only; it does **not** replace
**CDN** trust decisions or **`npm audit`** in integrator pipelines — see **`docs/FRONTEND_SUPPLY_CHAIN.md`** and
**[`docs/DEPENDENCY_AUDIT.md`](DEPENDENCY_AUDIT.md)**.

### Backlog traceability: Document CDN vs bundled replayt with SRI and supply-chain notes

**Normalized user story:** As integrator or maintainer, I want a short, canonical doc that explains **when** to pin
**CDN** URLs for **replayt**’s browser bundle, **optional SRI**, and **npm**/**bundler** delivery as an alternative,
aligned with the **README** / **`pyproject.toml`** compatibility story and distinct from **Python** **`pip-audit`**.

| Backlog acceptance criterion | Where specified | How verified |
| ---------------------------- | --------------- | ------------ |
| **CDN pinning guidance** | [`docs/FRONTEND_SUPPLY_CHAIN.md` — CDN delivery](FRONTEND_SUPPLY_CHAIN.md#cdn-delivery-eg-jsdelivr) | **Spec gate** / review |
| **Optional SRI** | [Subresource Integrity (SRI)](FRONTEND_SUPPLY_CHAIN.md#subresource-integrity-sri) | Same |
| **Bundling alternative** | [Bundling alternative](FRONTEND_SUPPLY_CHAIN.md#bundling-alternative-npm--vite-webpack-etc) | Same |
| **Align with single compatibility story** | [Single change set when replayt minors move](FRONTEND_SUPPLY_CHAIN.md#single-change-set-when-replayt-minors-move); [Vanilla examples: integrator-facing replayt pins](#vanilla-examples-integrator-facing-replayt-pins) | **`tests/test_docs_examples_replayt_pins.py`** for in-range **CDN** pins; manual review for **SRI** / prose |
| **Python supply chain called out separately** | [`docs/FRONTEND_SUPPLY_CHAIN.md`](FRONTEND_SUPPLY_CHAIN.md) (opening sections + **[DEPENDENCY_AUDIT.md](DEPENDENCY_AUDIT.md)**) | Same |

**Builder checklist:** Link **README** / **design principles** (phase **2** spec); **`tests/test_frontend_supply_chain_doc.py`**
(phase **3**) locks **A1–A5** structure and links. Optional follow-up backlogs may add **SRI** byte checks or **npm** CI — **not** required here.

### Backlog traceability: Optional npm workspace or build recipe without publishing a package

**Normalized user story:** As maintainer, I want a **documented optional path** (root **`package.json`** marked **`private`**
plus **Vite** or **esbuild**) to bundle **replayt** from **npm** for **local preview** only, while **CI** stays
**pytest-first** and the repo does **not** claim a **supported npm package** unless explicitly published.

| Backlog acceptance criterion | Where specified | How verified |
| ---------------------------- | --------------- | ------------ |
| **Spec + acceptance criteria** | [`docs/examples/build.md`](examples/build.md) (**C1**–**C4**, **B1**–**B8**) | **Spec gate** / review |
| **Boundary: not a published npm surface** | [Module and directory boundaries](#module-and-directory-boundaries); **build.md** [Explicit non-goals](#explicit-non-goals-module-boundary) | **Spec gate**; **Builder** + **CHANGELOG** if publication intent ever changes |
| **CI pytest-first** | **build.md** deliverable **B7**; [GitHub Actions CI workflow](#github-actions-ci-workflow) | **Spec gate** today; **workflow** diff only if a **future** backlog adds optional **npm** jobs |
| **Pin alignment** | **build.md** [Single compatibility story](#single-compatibility-story-pins); [Vanilla examples: integrator-facing replayt pins](#vanilla-examples-integrator-facing-replayt-pins) | **`tests/test_docs_examples_replayt_pins.py`** on **`docs/examples/build.md`**; **`package.json`** semver reviewed when shipped |

**Builder checklist (phase 3):** Add **`package.json`** + minimal bundler config per **B1**–**B8**; link from **README**; **CHANGELOG** **Unreleased**; keep **`.github/workflows/ci.yml`** on **Python** **pytest** + **ruff** + **pip-audit** unless a separate backlog adds **npm** automation.

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
3. After any pin or dev-set change, run **`pip install -e ".[dev]"`** and **`pytest`** on at least one **test** job
   **Python** from the matrix (for example **3.12**);
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
| **Install** | **`pip install -e ".[dev]"`** (quoted extras) on each **test** job **Python** version from [Replayt and Python matrix](#replayt-and-python-matrix) | `test_ci_installs_editable_with_dev_extras`; green CI logs |
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
| **Python** | `>=3.11` per `requires-python` | **3.11** and **3.12** on `ubuntu-latest` via **`strategy.matrix`** in the **test** job (`.github/workflows/ci.yml`) | Add or drop matrix rows with `requires-python`, **compat.md**, and contract tests in one change set |

---

## Compatibility matrix and upgrade paths

Normative spec for the backlog item **Document compatibility matrix and upgrade paths**: what “table of supported
versions”, “CI matrix covers”, **replayt** versions **tested** vs **supported**, **shims**, and **migration** mean for
maintainers and integrators. **[docs/compat.md](compat.md)** is the readable digest; this section is authoritative when
the two differ.

### Supported vs tested (replayt and Python)

- **Supported (policy)** — Declared in **`pyproject.toml`** and summarized in [Replayt and Python matrix](#replayt-and-python-matrix)
  and [Showcase stack matrix](#showcase-stack-matrix). Integrators may rely on this range unless **CHANGELOG** narrows it.
- **Verified in CI today** — Whatever the default **GitHub Actions** workflow actually installs and runs tests against.
  Today the **test** job uses **two** **Python** rows (**3.11** and **3.12**); each row resolves **one** **replayt**
  version (**latest** satisfying the PEP 508 range at install time). That is **not** the same as “every **replayt**
  minor in the range is regression-tested” until optional jobs pin additional **replayt** cells.
- **No false claims** — Documentation (including **README**, this file, and **compat.md**) MUST NOT imply CI exercises
  matrix cells that are not implemented in **`.github/workflows/ci.yml`** (or documented follow-up jobs). When new rows
  ship, update the **Verified in CI today** columns here and in **compat.md** in the same change set as the workflow.

### Compatibility shims (consumer-side)

- **Goal** — Avoid stranding integrators when **replayt**’s public surface evolves within the supported range (or across a
  planned range change): adapt in **this repo** via thin wrappers or re-exports; **do not** fork or patch **replayt**
  internals ([Upstream boundary](#one-way-to-do-it-canonical-patterns)).
- **Placement** — Shims and adapter modules live only under **`src/replayt_ux_showcase/`**; they are part of the packaged
  surface and follow [Deprecation and removal](#deprecation-and-removal) when retired.
- **Documentation** — Every shim MUST ship with **CHANGELOG** notes (and user-facing pointers in **compat.md** or **`docs/demo.md`**
  when integrators copy affected examples). Upstream release notes remain the source of truth for **replayt** API semantics.

### Backlog traceability: Document compatibility matrix and upgrade paths

**Normalized user story:** As integrator, I want a clear **compatibility matrix**, honest **CI coverage** statements,
**shim** guidance, and **migration** notes so I can upgrade **replayt** and this showcase without surprise breakages.

| Backlog acceptance criterion | Where specified | How verified (target) |
| ---------------------------- | --------------- | ------------------------ |
| **Table of supported versions** | [Replayt and Python matrix](#replayt-and-python-matrix), [Showcase stack matrix](#showcase-stack-matrix), **[docs/compat.md](compat.md) quick reference** | **Spec gate** — tables present, consistent with **`pyproject.toml`** / `requires-python`; **Builder** keeps contract tests aligned when pins change |
| **CI matrix covers** | [Supported vs tested](#supported-vs-tested-replayt-and-python), **compat.md** [CI matrix coverage](compat.md#ci-matrix-coverage), [GitHub Actions CI workflow](#github-actions-ci-workflow) | **Spec gate** — no doc claims uncovered cells; **Builder** adds **`strategy.matrix`** (or equivalent jobs) when policy requires multiple **replayt** or **Python** rows and updates **Verified in CI today** cells |
| **Deprecation policy** | [Deprecation and removal](#deprecation-and-removal), **compat.md** summary | **Spec gate** — policy cross-linked from digest; releases honor **CHANGELOG** and semver rules |

**Builder checklist (follow-up):**

1. If **pytest** exits with code **4** / “unrecognized **--cov**”, ensure **`pip install -e ".[dev]"`** runs before **pytest** so **pytest-cov** matches **[tool.pytest.ini_options]** (see phase **1c** baseline notes).
2. When adding **replayt** or **Python** matrix rows, update **`.github/workflows/ci.yml`**, this matrix, **compat.md**, and **`tests/test_design_principles_contract.py`** (if CI assertions encode the matrix) in one change set.
3. Record user-visible compatibility or CI matrix changes under **CHANGELOG** **Unreleased**.

---

## Showcase stack matrix

Front-end stacks are **documented** here before (or as) examples land. “Supported” means we intend integrators to
copy the pattern; “CI” means automated verification exists.

| Stack | Supported (intent) | CI | Notes |
| ----- | ------------------- | --- | ----- |
| Vanilla HTML/JS | Yes (`docs/examples/`) | **`docs/examples`** **replayt** pin contract (**`tests/test_docs_examples_replayt_pins.py`**) plus any future file/smoke tests | Default integration path for smallest surface; pin contract keeps CDN/requirement snippets inside the PEP 508 range in **`pyproject.toml`** |
| Optional **npm** bundler preview | Yes (documented) — **[`docs/examples/build.md`](examples/build.md)** | Not required in default **CI** (pytest-first) | Root **`package.json`** with **`"private": true`**; **Vite** *or* **esbuild**; **not** an implied public **npm** package for this repo |
| React | ^18 when a React example exists | Not required until a React demo ships | Copy-paste snippets per the mission |
| Vue | ^3 when a Vue example exists | Not required until a Vue demo ships | Same as React |
| Svelte | ^4 when a Svelte example exists | Not required until a Svelte demo ships | Same as React |

### Vanilla UI pattern catalog

**Canonical inventory:** **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)** — distinct copy-paste vanilla patterns
(**P-01**, **P-02**, **P-03**, **P-04**, **P-05**, …), shipped vs spec-only status, and normative acceptance criteria for each pattern. The mission
target (**5+** patterns) is **tracked** in **[`docs/MISSION.md`](MISSION.md#pattern-coverage-tracking)** and the digest
**[`docs/compat.md` — Vanilla UI pattern catalog](compat.md#vanilla-ui-pattern-catalog)**.

New patterns **must** be registered in **`docs/examples/PATTERNS.md`** before or in the same change set as the new
**`docs/examples/*.html`** file (see [Single home for copy-paste demos](#one-way-to-do-it-canonical-patterns)).

**Shared accessibility contract:** Vanilla patterns that embed a player, metadata chrome, scrubbers, or future
focus-managed event lists **should** follow **[`docs/a11y/keyboard-model.md`](a11y/keyboard-model.md)** — tab order,
roving `tabindex` when composites apply, scrubber keys, and **Escape** for dismissible layers. Per-pattern normative
text remains in **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)**; the a11y doc is the single cross-pattern
checklist for design–engineering handoff.

#### Backlog traceability: Keyboard and focus model for timeline/player controls

**Normalized user story:** As a designer or integrator, I want a **single** documented **keyboard and focus** contract
for timeline/player embeds (tab order, list roving when applicable, scrubber and **Escape** behavior) so handoffs reuse
one checklist instead of re-negotiating accessibility per file.

| Backlog acceptance criterion | Where specified | How verified (target — Builder / gate) |
| ---------------------------- | --------------- | --------------------------------------- |
| Canonical a11y doc exists | **[`docs/a11y/keyboard-model.md`](a11y/keyboard-model.md)** | File present; sections cover tab order, roving tabindex, scrubber keys, **Escape**, focus visibility, Builder checklist |
| Linked from **P-01** instructions | **[`docs/examples/basic-player.html`](examples/basic-player.html)** | Instructions link to **`../a11y/keyboard-model.md`** |
| Linked from pattern catalog / shipped examples | **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)**, **P-02** / **P-03** / **P-04** comment blocks | Cross-links or “see keyboard model” references; **Tab order (handoff)** comments retained |
| Traceability from design principles | [Acceptance criteria (traceability)](#acceptance-criteria-traceability) row *Timeline / player keyboard and focus* | **Spec gate** / **Design gate** |
| Mission playbook alignment | **[`docs/MISSION.md`](MISSION.md)** (handoff under one dev-day) | Reviewer checklist includes this doc when touching player UX |

#### Offline deterministic fixture page for LLM and reviewer workflows

**Normalized user story:** As a **reviewer** or **automation agent**, I want a **registered vanilla example** (primary filename **`docs/examples/fixture-replay.html`**, or an alias recorded in **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)**) that initializes the replay player from **only** inlined, synthetic **`sessionData`**—with **no runtime network retrieval of session payloads**, **no secrets**, and **no live / non-reproducible model calls**—plus short prose in **[`README.md`](../README.md)** and **[`docs/REPLAYT_ECOSYSTEM_IDEA.md`](REPLAYT_ECOSYSTEM_IDEA.md)** on how to open it locally for harness and human review.

| Backlog acceptance criterion | Where specified | How verified (target — Builder) |
| ---------------------------- | --------------- | ------------------------------- |
| Artifact path + pattern registration | **[P-05](examples/PATTERNS.md#p-05-offline-deterministic-fixture-page-for-llm-and-reviewer-workflows)** — inventory row | **`docs/examples/fixture-replay.html`** (or approved alias) on disk; **P-05** → **Shipped** in **`docs/examples/PATTERNS.md`** |
| Inlined synthetic **`sessionData`** only | **P-05** [sessionData and offline boundary](examples/PATTERNS.md#p-05-sessiondata-and-offline-boundary-normative) | Code review: literal / constant in-page; no `fetch` / **XHR** / **WebSocket** / **EventSource** (or equivalent) for session payloads |
| **No secrets**; **no** non-reproducible model calls in this path | **P-05** [Forbidden behaviors](examples/PATTERNS.md#p-05-forbidden-behaviors-normative); [LLM boundaries](#llm-boundaries) | Code review; no API keys, tokens, or env-specific endpoints in source |
| **Deterministic** fixture data | **P-05** [Determinism](examples/PATTERNS.md#p-05-determinism-normative) | No `Date.now()` / `new Date()` / `Math.random()` (or equivalent) in **`sessionData`** or other harness-scraped copy unless documented test-only and stable |
| **replayt** JS pin in supported range | **P-05** [replayt pin and open instructions](examples/PATTERNS.md#p-05-replayt-pin-and-open-instructions-normative) | **`tests/test_docs_examples_replayt_pins.py`** |
| Reviewer / agent **open** instructions | **`README.md`**, **`docs/REPLAYT_ECOSYSTEM_IDEA.md`** | Linked sections describe local open path (see **P-05**); **CHANGELOG** **Unreleased** when **Shipped** |
| Mission pattern count | **[`docs/MISSION.md`](MISSION.md#pattern-coverage-tracking)** | Table lists **5** shipped vanilla patterns (**P-01**–**P-05**) |

**Shipped (phase 3):** **`docs/examples/fixture-replay.html`**, **P-05** marked **Shipped** in **`docs/examples/PATTERNS.md`**, **[`docs/MISSION.md`](MISSION.md#pattern-coverage-tracking)** and **[`docs/compat.md`](compat.md#vanilla-ui-pattern-catalog)** updated, **`tests/test_examples.py`** contract markers, **CHANGELOG** **Unreleased** **Added** entry, **replayt** CDN pin checked by **`tests/test_docs_examples_replayt_pins.py`**. Normative criteria remain under **[P-05](examples/PATTERNS.md#p-05-offline-deterministic-fixture-page-for-llm-and-reviewer-workflows)**.

#### Backlog traceability: Ship session metadata chrome pattern (viewport, duration, session id)

**Normalized user story:** As integrator, I want a **second vanilla HTML** example that adds a **compact metadata bar**
above the player (session id, viewport, duration) using the **same `sessionData` root shape** as **`basic-player.html`**,
with explicit **loading**, **error**, and **keyboard focus** behavior.

| Backlog acceptance criterion | Where specified | How verified (target) |
| ---------------------------- | --------------- | ------------------------ |
| Second vanilla snippet, bar above player | **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)** — **P-02** | **`docs/examples/player-session-metadata-bar.html`** shipped; **`tests/test_examples.py`** file presence + marker checks |
| Same `sessionData` shape as P-01 (additive `metadata`) | **P-02** [`sessionData` contract](examples/PATTERNS.md#sessiondata-contract-compatibility-with-p-01) | Code review + **`tests/test_examples.py`** markers (`sessionId`, `durationMs`, `viewport`) |
| Loading placeholder | **P-02** [Loading state](examples/PATTERNS.md#loading-state-normative) | **`tests/test_examples.py`** asserts loading copy; manual spot-check in browser optional |
| Error when required metadata missing | **P-02** [Error state](examples/PATTERNS.md#error-state-normative) | **`tests/test_examples.py`** asserts validation/error strings; **`Simulate invalid metadata`** control in the snippet |
| Keyboard focus order (bar before player) | **P-02** [Keyboard focus and accessibility](examples/PATTERNS.md#keyboard-focus-and-accessibility-normative) | **`tests/test_examples.py`** asserts tab-order comment block; manual tab order in browser optional |
| **CHANGELOG** + mission pattern count | **[`docs/MISSION.md`](MISSION.md#pattern-coverage-tracking)**, [P-02 Builder checklist](examples/PATTERNS.md#builder-acceptance-checklist-implementation) | **CHANGELOG** **Unreleased**; **MISSION** table |

**Shipped for this backlog (phase 3):** **`docs/examples/player-session-metadata-bar.html`**, **P-02** marked **Shipped** in **`docs/examples/PATTERNS.md`**, **[`docs/MISSION.md`](MISSION.md#pattern-coverage-tracking)** counts updated, **CHANGELOG** **Unreleased** **Added** entries, **replayt** CDN pin checked by **`tests/test_docs_examples_replayt_pins.py`**. Further edits to **P-02** should keep **PATTERNS.md**, **MISSION**, **CHANGELOG**, and pin contract tests in the same change set when contracts or filenames change.

#### Backlog traceability: Timeline scrubber strip example (replayt public events API)

**Normalized user story:** As integrator, I want a **vanilla** timeline **scrubber** that uses **`sessionData.events`**
and **replayt’s published JS API** for seek/scrub, with **documented** event-order assumptions, **throttling**, and a
**limitations** callout when CDN builds omit APIs.

| Backlog acceptance criterion | Where specified | How verified (target) |
| ---------------------------- | --------------- | ------------------------ |
| **`timeline-scrubber.html`** or clearly separated section | **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)** — **P-03** [Delivery shape](examples/PATTERNS.md#delivery-shape-normative) | File on disk + **CHANGELOG** when **Shipped**; optional **`tests/test_examples.py`** markers (Builder) |
| Seek/scrub UX + published JS only | **P-03** [Scrub / seek interactions](examples/PATTERNS.md#scrub--seek-interactions-normative) | Code review; symbols listed in-snippet |
| Event ordering assumptions | **P-03** [`sessionData` and events](examples/PATTERNS.md#sessiondata-and-events-normative) | Comment block present per spec |
| Throttling / final seek on commit | **P-03** [Throttling and coalescing](examples/PATTERNS.md#throttling-and-coalescing-normative) | Code review + optional contract strings in **`tests/test_examples.py`** |
| Limitations / upgrade note for CDN | **P-03** [Limitations and CDN builds](examples/PATTERNS.md#limitations-and-cdn-builds-normative) | Visible copy or view-source comment |
| **replayt** CDN pin in PEP 508 range | **P-03** [replayt pin and file placement](examples/PATTERNS.md#replayt-pin-and-file-placement) | **`tests/test_docs_examples_replayt_pins.py`** once HTML exists |
| Pattern inventory + mission table | **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)**, **[`docs/MISSION.md`](MISSION.md#pattern-coverage-tracking)** | **P-03** → **Shipped** with HTML; counts updated |

**Shipped (phase 3):** **`docs/examples/timeline-scrubber.html`**, **P-03** marked **Shipped** in **`docs/examples/PATTERNS.md`**,
**[`docs/MISSION.md`](MISSION.md#pattern-coverage-tracking)** counts updated, **`tests/test_examples.py`** contract markers,
**CHANGELOG** **Unreleased** **Added** entry, **replayt** CDN pin checked by **`tests/test_docs_examples_replayt_pins.py`**.
Further edits to **P-03** should keep **PATTERNS.md**, **MISSION**, **CHANGELOG**, and pin contract tests aligned when contracts change.

#### Backlog traceability: Empty, loading, and failure states for the embed container

**Normalized user story:** As **operator** or **integrator**, I want the **player embed container** to show **skeleton**
UI while `sessionData` loads, **visible errors** and **retry** when fetch/init fails, and **`aria-live` / `role="status"`**
announcements consistent with **[Audience](#audience)** (including **automation agents**), using only **published**
replayt JS— with the same vocabulary documented in **[`docs/demo.md`](demo.md#cross-surface-operator-story-console-demo-and-web-embed)**.

| Backlog acceptance criterion | Where specified | How verified (target) |
| ---------------------------- | --------------- | ------------------------ |
| Pattern registration + criteria | **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)** — **P-04** | **`docs/examples/embed-container-states.html`** on disk; **`tests/test_docs_examples_replayt_pins.py`** + **`tests/test_examples.py`** markers |
| Skeleton loading, failure, retry, live region | **P-04** sections (embed skeleton, failure, retry, status region) | Code review + **`tests/test_examples.py`** contract strings |
| No private replayt APIs | **P-04** [async sessionData](examples/PATTERNS.md#p-04-async-sessiondata-acquisition-normative) + [pin / placement](examples/PATTERNS.md#p-04-replayt-pin-and-file-placement) | Code review; symbols documented in-snippet |
| Console vs web story | **[`docs/demo.md` — Cross-surface operator story](demo.md#cross-surface-operator-story-console-demo-and-web-embed)** | Table + **Builder alignment** note kept in sync with shipped **P-04** |
| **CHANGELOG** / **MISSION** when shipped | **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)** Builder checklist | **P-04** → **Shipped** in phase **3** with **MISSION** count **4** |

**Shipped (phase 3):** **`docs/examples/embed-container-states.html`**, **P-04** marked **Shipped** in **`docs/examples/PATTERNS.md`**, **[`docs/MISSION.md`](MISSION.md#pattern-coverage-tracking)** counts updated, **`tests/test_examples.py`** contract markers, **CHANGELOG** **Unreleased** entries, **replayt** CDN pin checked by **`tests/test_docs_examples_replayt_pins.py`**, **[`docs/demo.md`](demo.md)** **Builder alignment** note updated. **Spec lead (phase 2)** registered **P-04** and the cross-surface table before HTML landed.

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
| **New vanilla UI pattern** | Add **`docs/examples/*.html`**, register in **`docs/examples/PATTERNS.md`**, update **CHANGELOG** **Unreleased** and **`docs/MISSION.md`** pattern table ([Vanilla UI pattern catalog](#vanilla-ui-pattern-catalog)) |
| **Integrator upgrading** | Compare their pinned **replayt** to this repo’s supported range; follow **CHANGELOG** for the showcase version they target |
| **Dev toolchain or replayt pin change** | Update **`pyproject.toml`**, [Dependency pins and dev toolchain](#dependency-pins-and-dev-toolchain) / matrix cells, contract tests, and **CHANGELOG** in one change set |

---

## LLM boundaries

This repo’s **default** posture is **static demos and documentation**—no hosted model calls, no API keys, no usage
metering in CI.

| Rule | Detail |
| ---- | ------ |
| **Secrets** | Never commit API keys, tokens, or `.env` with real credentials. Examples use placeholders only. |
| **Offline fixture page** | **[P-05](examples/PATTERNS.md#p-05-offline-deterministic-fixture-page-for-llm-and-reviewer-workflows)** (`docs/examples/fixture-replay.html` or registered alias) is the **canonical** vanilla surface for **deterministic**, **no-session-fetch** review and **LLM** harnesses: inlined synthetic **`sessionData`**, **no** runtime network retrieval of session payloads, **no** secrets, **no** live or stochastic model calls **in that file’s code path**. See **P-05** for the **replayt** script pin, local open instructions, and how this differs from **P-01**–**P-04** (which may demonstrate `fetch` or other network stories). |
| **replayt LLM helpers** | If an example uses **replayt**’s mock or workflow LLM utilities (e.g. `MockLLMClient`, `run_with_mock`), keep it **offline/deterministic** in CI and document that in the demo’s spec or header comment. **P-05** MUST NOT depend on such helpers unless the **P-05** spec is explicitly revised to allow a documented mock path that remains **deterministic** and **secret-free**. |
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
| **Automation agents (LLM tooling)** | Respect [LLM boundaries](#llm-boundaries); treat this file and `tests/` as normative for boundaries—do not invent alternate package layouts or secret-handling rules; for **vanilla** replay **fixtures** (no fetched session payloads), prefer **[P-05](examples/PATTERNS.md#p-05-offline-deterministic-fixture-page-for-llm-and-reviewer-workflows)** (**[`fixture-replay.html`](examples/fixture-replay.html)**); for **loading / failure / status** scraping in other patterns, use **only** documented visible copy, **`aria-live` / `role="status"`** text, or optional hooks (e.g. `data-demo-state`) **where a pattern spec says so**—see **[P-04](examples/PATTERNS.md#p-04-status-live-region-normative)** |
