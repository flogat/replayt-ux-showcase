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
| **Static HTML** load smoke (**Playwright**): no console errors on open, fast **CI** matrix, local run docs | [Static HTML examples: browser smoke (Playwright)](#static-html-examples-browser-smoke-playwright), [GitHub Actions CI workflow](#github-actions-ci-workflow), [README.md](../README.md#optional-playwright-smoke-static-html-examples) |
| **pip-audit** failures, local reproduction, overrides vs pins | [Dependency vulnerability audit (pip-audit)](#dependency-vulnerability-audit-pip-audit), [`docs/DEPENDENCY_AUDIT.md`](DEPENDENCY_AUDIT.md) |
| Extension points documented | [Extension points](#extension-points) |
| Audience needs extended | [Audience](#audience) |
| Distinct vanilla UI patterns (mission: **5+**), per-pattern acceptance | [Vanilla UI pattern catalog](#vanilla-ui-pattern-catalog), [examples/PATTERNS.md](examples/PATTERNS.md), [MISSION.md](MISSION.md#pattern-coverage-tracking) |
| Timeline / player **keyboard** and **focus** (handoff checklist) | [`docs/a11y/keyboard-model.md`](a11y/keyboard-model.md), [Vanilla UI pattern catalog](#vanilla-ui-pattern-catalog) (shared contract), [examples/PATTERNS.md](examples/PATTERNS.md) (per-pattern rules) |
| **Design-to-code handoff** (tokens, anatomy, printable checklist) | [`docs/playbook/README.md`](playbook/README.md), [`tokens.md`](playbook/tokens.md), [`component-anatomy.md`](playbook/component-anatomy.md), [`handoff-checklist.md`](playbook/handoff-checklist.md), [README.md](../README.md#quick-start) (integrator quick start link) |
| **Figma design kit** (library access, variable → **`rux-*`** mapping, change process, interim **JSON** export) | [Design kit (Figma) and token export](#design-kit-figma-and-token-export), [`docs/design-kit/README.md`](design-kit/README.md) |
| Offline deterministic **fixture** page for **LLM** / reviewer harnesses | [Offline deterministic fixture page](#offline-deterministic-fixture-page-for-llm-and-reviewer-workflows), [LLM boundaries](#llm-boundaries), **[P-05](examples/PATTERNS.md#p-05-offline-deterministic-fixture-page-for-llm-and-reviewer-workflows)** |
| **Event overlay** vanilla teaching example (scrub-linked callouts, hover + keyboard, offline **`sessionData`**) | **[P-09](examples/PATTERNS.md#p-09--event-overlay-lane-scrub-hover-tooltips-keyboard)** (**[`event-overlay.html`](examples/event-overlay.html)**), [`component-anatomy.md` §2 overlays](playbook/component-anatomy.md#2-overlays-dialogs-popovers-event-callouts), [`keyboard-model.md`](a11y/keyboard-model.md), **[`docs/demo.md`](demo.md#cross-surface-operator-story-console-demo-and-web-embed)** cross-surface row + **`demo.py`** overlay teaching line |
| **replayt** public Python API guard on showcase modules | [replayt Python API boundary](#replayt-python-api-boundary), [Compatibility digest — API table](compat.md#replayt-python-public-api-showcase-digest) |
| **Session fixture** (`SAMPLE_SESSION_DATA` ↔ **`docs/examples`**) | [`docs/examples/SESSION_SCHEMA.md`](examples/SESSION_SCHEMA.md), [examples/PATTERNS.md — Canonical session fixture](examples/PATTERNS.md#canonical-session-fixture-cross-surface), [`docs/demo.md`](demo.md) |
| **CHANGELOG**, semver bumps, and **Unreleased** pattern milestones | [Changelog, semver, and release notes](#changelog-semver-and-release-notes), [`CONTRIBUTING.md`](../CONTRIBUTING.md) |

### Traceability to automated checks

These alignments are **enforced in CI** today (the principles doc is broader):

| Check | Enforced by |
| ----- | ----------- |
| `requires-python` matches the Python row in [Replayt and Python matrix](#replayt-and-python-matrix) | `tests/test_design_principles_contract.py` |
| **`replayt`** dependency specifier matches that matrix (`>=0.1.0` and compatible `<0.5` cap, per `tests/test_design_principles_contract.py`) | Same |
| CI **Python** version(s) and **`replayt-version`** pins in the **test** job matrix in `.github/workflows/ci.yml` match [Replayt and Python matrix](#replayt-and-python-matrix) and **`docs/compat.md`** inventory IDs | Same (`test_ci_test_job_matrix_matches_design_principles_matrix`, `test_compat_ci_exercise_inventory_ids_match_ci_matrix`) |
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
| **`basic-player.html`** (and scoped peers) stay aligned with **`SAMPLE_SESSION_DATA`** for canonical keys | **`tests/test_session_schema_examples.py`** — JSON fixture block in **`docs/examples/basic-player.html`** vs **`SAMPLE_SESSION_DATA`** per [`docs/examples/SESSION_SCHEMA.md`](examples/SESSION_SCHEMA.md) §5; see [Backlog traceability: Normalize session schema examples](#backlog-traceability-normalize-session-schema-examples-python-demo-and-basic-playerhtml) |
| **`docs/FRONTEND_SUPPLY_CHAIN.md`** section anchors, keywords, cross-links, and **CHANGELOG** **Unreleased** mention (**A1–A5** in that doc) | `tests/test_frontend_supply_chain_doc.py` |
| **`docs/playbook/`** — **tokens** / **component anatomy** / **printable checklist** sections, index links, **README** quick start, **CHANGELOG** **Unreleased** mention (**T1–T5**, **A1–A5**, **H1–H5**) | `tests/test_playbook_docs.py` |
| **`CONTRIBUTING.md`**, [Changelog, semver, and release notes](#changelog-semver-and-release-notes) headings and semver tables, pins ↔ **DESIGN_PRINCIPLES** table, **CHANGELOG** **Unreleased** mention | `tests/test_changelog_release_policy_docs.py` |
| **`docs/design-kit/`** — **F1–F8** acceptance, **`design-tokens.json`** schema when interim export applies | `tests/test_design_kit_docs.py` (sections **F1–F8**, **F3** ↔ **`tokens.md`** semantics, JSON top-level keys + **`tokens[]`** shape); see [Design kit (Figma) and token export](#design-kit-figma-and-token-export) |
| Root **`package.json`** (optional **npm** bundler recipe) | **`tests/test_optional_npm_bundler_recipe.py`** (**`private`**, scripts, **`replayt`** semver string, no **npm** in **`.github/workflows/ci.yml`**); **`npm run build`** not run in **CI**; MUST follow [`docs/examples/build.md`](examples/build.md); **`tests/test_docs_examples_replayt_pins.py`** covers **`docs/examples/build.md`** prose pins |
| Optional **`integrity`** (**SRI**) on CDN **`<script>`** tags in examples | **Not** enforced in **CI** today; if present, must match the pinned URL’s bytes — see [`docs/FRONTEND_SUPPLY_CHAIN.md`](FRONTEND_SUPPLY_CHAIN.md) |
| Static **HTML** examples: **Playwright** load smoke (no **console** errors on initial load; **Chromium**-first matrix) | **Not** enforced in **CI** today; target workflow + **`tests/`** module named in [Static HTML examples: browser smoke (Playwright)](#static-html-examples-browser-smoke-playwright) and **`docs/compat.md`** [CI exercise row inventory](compat.md#ci-exercise-row-inventory) when **Builder** lands the job |
| Showcase code: **replayt** imports use only published top-level symbols (**`replayt.__all__`**) and no underscore-private **`replayt` submodules** | **`tests/test_replayt_public_api_boundary.py`** — default **`pytest`** in every **CI** **test** matrix cell; see [Backlog traceability: Harden replayt public-API boundary](#backlog-traceability-harden-replayt-public-api-boundary-lint-or-import-guard) |
| **`docs/DEPENDENCY_AUDIT.md`** — **D1–D10** playbook (local **`pip-audit`**, fix vs override policy, **README** troubleshooting link) | **`tests/test_dependency_audit_doc.py`** (see [Dependency vulnerability audit (pip-audit)](#dependency-vulnerability-audit-pip-audit)) |

The **`docs/compat.md`** [CI exercise row inventory](compat.md#ci-exercise-row-inventory) MUST stay aligned with
**`.github/workflows/ci.yml`** per [CI exercise rows](#ci-exercise-rows-matrix-jobs-and-best-effort). Drift fails **CI** via
**`test_compat_ci_exercise_inventory_ids_match_ci_matrix`** (same change set as workflow or inventory edits — see
[Backlog traceability: Expand compatibility matrix with explicit CI matrix job per row](#backlog-traceability-expand-compatibility-matrix-with-explicit-ci-matrix-job-per-row)).

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
| **`docs/`** | Mission, principles, demo specs, copy-paste examples, **[`docs/playbook/`](playbook/README.md)** (design-to-code handoff: tokens, anatomy, printable checklist), **[`docs/design-kit/`](design-kit/README.md)** (**Figma** library spec, variable → **`rux-*`** mapping rules, interim **`design-tokens.json`**), playbook-oriented markdown | Hold secrets, credentials, or environment-specific endpoints checked into git |
| **`docs/examples/`** | Static HTML/JS (and future framework snippets) that integrators copy | Imply they are supported npm packages unless explicitly published as such |
| **`package.json`** (repo root, optional) | **Private** **npm** metadata + scripts for **Vite** / **esbuild** local bundling per **[`docs/examples/build.md`](examples/build.md)** | Imply a **published** **npm** product for this repository, or omit **`"private": true`**, without an explicit maintainer decision and **CHANGELOG** entry |
| **`tests/`** | Repo invariants: packaging, file presence, smoke behavior against installed **replayt** | Replace upstream **replayt** unit tests or depend on private APIs |
| **`.github/workflows/`** | CI that installs with **`pip install -e ".[dev]"`**, runs **pytest** (with **`[tool.pytest.ini_options]`** coverage gate), **ruff**, and **pip-audit** (see [GitHub Actions CI workflow](#github-actions-ci-workflow)); optional **Playwright** smoke job when implemented (see [Static HTML examples: browser smoke (Playwright)](#static-html-examples-browser-smoke-playwright)) | Store long-lived tokens (read-only `contents` is the default contract) |

**Dependency direction:** showcase code and tests **→** **replayt** (PyPI). Demos may document how integrators pull
**replayt** in their own apps; this repo does not re-export **replayt** as a different product.

### replayt Python API boundary

- Depend on **replayt** only through its **published** PyPI package and **documented** public surface (release notes,
  upstream reference docs). Do not rely on private modules, underscore-prefixed internals, or undocumented symbols.
- Workflow or mock-LLM helpers from **replayt** are allowed only when they stay **offline** and **deterministic** in
  default CI, per [LLM boundaries](#llm-boundaries).

#### Normative import rules (showcase Python)

These rules apply to **all** `*.py` files under **`src/replayt_ux_showcase/`** (including **`demo.py`** and
**`__init__.py`**). They do **not** apply to **`tests/`** (tests may introspect **replayt** for contract purposes).

1. **No private submodule paths:** Any **static** import MUST NOT load a **replayt** submodule whose **first dotted
   segment after `replayt.`** starts with an underscore (e.g. `import replayt._foo`, `from replayt._bar import …`).
   Imports of **non-underscore** submodules (e.g. `import replayt.something`) are **out of scope** for this backlog
   unless/until upstream documents them as public; default posture is **top-level package only** (see rule 2).
2. **Top-level symbols ⊆ `__all__`:** For `from replayt import a, b, …`, every imported **name** MUST appear in
   **`replayt.__all__`** in the **replayt** version installed when **`pytest`** runs (same environment as **CI** matrix
   cells). **Bare** `import replayt` (optionally `as` aliased) is always allowed; if code uses attribute access
   (`replayt.Workflow`, `rt.Workflow` after `import replayt as rt`), those attribute names SHOULD satisfy the same
   **allowlist** as rule 2 — **Builder** SHOULD implement the strictest practical static check (imports **and** obvious
   `load_attr` / alias patterns) and MAY document residual risk (dynamic **`getattr`**, string **`importlib`**) as
   **code-review** / follow-up backlog.
3. **Underscore-prefixed bind names:** Importing a **replayt** symbol whose **exported public name** starts with
   **`_`** is forbidden **unless** that name is explicitly listed in **`replayt.__all__`** (today **`__version_tuple__`**
   is the only such case in the reference pin — see [`docs/compat.md` digest](compat.md#replayt-python-public-api-showcase-digest)).

**Allowlist digest:** [`docs/compat.md` — replayt Python public API](compat.md#replayt-python-public-api-showcase-digest)
mirrors the **`__all__`** set for the reference **CI** pin (**0.4.25**); when **`__all__`** changes in a supported
**replayt** release, update the digest and **CHANGELOG** **Unreleased** in the same change set as pin/matrix updates.

**Enforcement (implementation):** **`tests/test_replayt_public_api_boundary.py`** (**`pytest`** + **AST**) fails **CI** when
rules 1–3 are violated on **`src/replayt_ux_showcase/**/*.py`**. **`demo.py`** may import **`replayt`** when it stays on
the published surface; the console demo remains **stdlib-only** for runtime today, but that is no longer enforced by a
separate **`test_demo.py`** guard.

---

## Demo module testing and replayt integration boundaries

Normative spec for the backlog item **Add unit/integration tests for demo**: what “coverage on demo”, “fails on
boundary breaks”, and “dev dependencies” mean in **`pyproject.toml`**. **Implementation** (**pytest-cov** pin,
**`[tool.pytest.ini_options]`**, contract tests, and **CI** running **`pytest`**) is in tree; extend tests when new
boundary rows appear here.

### Scope of “the demo” for coverage

- **Primary:** `src/replayt_ux_showcase/demo.py` — the console timeline module described in **`docs/demo.md`**.
- **Out of scope for the 80% gate:** static files under **`docs/examples/`** (see [Showcase stack matrix](#showcase-stack-matrix));
  optional **Playwright** load smoke for those pages is specified in [Static HTML examples: browser smoke (Playwright)](#static-html-examples-browser-smoke-playwright) and does **not** change the **`demo.py`** coverage metric.

### Vanilla examples: integrator-facing replayt pins

Normative spec for copy-paste **HTML** and **Markdown** under **`docs/examples/`**: any **explicit** **replayt** version
pin shown to integrators MUST stay inside the supported consumer range declared on the **`replayt`** line in
**`[project].dependencies`** (same PEP 508 story as [Replayt and Python matrix](#replayt-and-python-matrix) and
[Dependency pins and dev toolchain](#dependency-pins-and-dev-toolchain)). **Enforcement:** **`tests/test_docs_examples_replayt_pins.py`**
via default **`pytest`** discovery (**CI** included). When detection rules or pins change, update **CHANGELOG** **Unreleased** in the same change set.

#### Scope (files)

- **Include:** every **`*.html`**, **`*.md`**, **`*.vue`**, and **`*.svelte`** file under **`docs/examples/`**, recursively
  (framework subtrees such as **`docs/examples/react/`**, **`vue/`**, **`svelte/`** are included automatically).
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
| **replayt Python API boundary** | Showcase code does not depend on private or undocumented **replayt** symbols | **`tests/test_replayt_public_api_boundary.py`** on **`src/replayt_ux_showcase/**/*.py`** per [Normative import rules](#normative-import-rules-showcase-python): no **`replayt._*`** first-segment submodule imports; **`from replayt import …`** names ⊆ **`replayt.__all__`** at the installed version. Upstream **semver** still governs renames/removals in **`__all__`** — adjust pins, **`docs/compat.md`** digest, and tests per [Migration paths](#migration-paths) |
| Declared **replayt** range | Supported consumer range in **`pyproject.toml`** matches [Replayt and Python matrix](#replayt-and-python-matrix) | Contract tests on the **replayt** dependency line; optional smoke that **`import replayt`** succeeds after install (already part of contract tests today) |
| **docs/examples** replayt pins | Integrator snippets do not advertise **replayt** versions outside the declared PEP 508 range | **`tests/test_docs_examples_replayt_pins.py`** (or equivalent) scans **`docs/examples/**/*.{html,md,vue,svelte}`** per [Vanilla examples: integrator-facing replayt pins](#vanilla-examples-integrator-facing-replayt-pins) |

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
| **replayt** import surface in **`demo.py`** | Same as **replayt** public API row — **`tests/test_replayt_public_api_boundary.py`** includes **`demo.py`**; **`demo.py`** remains **stdlib-only** at runtime today but is not special-cased in **`tests/test_demo.py`** |
| **replayt** public API on all showcase modules | **`tests/test_replayt_public_api_boundary.py`** per [Backlog traceability: Harden replayt public-API boundary](#backlog-traceability-harden-replayt-public-api-boundary-lint-or-import-guard) |
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
2. When **`demo.py`** (or any **`src/replayt_ux_showcase/*.py`**) imports **replayt**, keep names inside **`replayt.__all__`**
   and off private submodule paths — enforced by **`tests/test_replayt_public_api_boundary.py`** ([Normative import rules](#normative-import-rules-showcase-python)).

### Backlog traceability: Contract test — examples reference replayt in supported semver range

**Normalized user story:** As maintainer, I want **pytest** to scan **`docs/examples/**/*.{html,md,vue,svelte}`** for **replayt**
CDN or package pins and fail when any pin falls outside the PEP 508 range declared in **`pyproject.toml`**, so
integrator-facing snippets stay aligned with [DESIGN_PRINCIPLES](#design-principles) and **`docs/compat.md`**.

| Backlog acceptance criterion | Where specified | How verified |
| ---------------------------- | --------------- | ------------------------ |
| **Scan scope** | [Scope (files)](#scope-files) | **`tests/test_docs_examples_replayt_pins.py`** enumerates **`docs/examples/**/*.{html,md,vue,svelte}`**. |
| **Detection rules** | [What counts as a “pin” (detection)](#what-counts-as-a-pin-detection) | Implementation matches the table; probe-grid simplifications are documented in the test module docstring. |
| **Assertion vs `pyproject.toml`** | [Acceptance (assertion)](#acceptance-assertion) | Each detected pin satisfies or is subsumed by the **`replayt`** specifier from **`[project].dependencies`**. |
| **Documented exceptions** | [Opt-out (documented exceptions)](#opt-out-documented-exceptions) | Snippets with **`<!-- replayt-examples:pin-exempt -->`** (and optional **`reason=`**) are skipped per rules above. |
| **Range changes** | [Acceptance (assertion)](#acceptance-assertion) | Same change set: **`pyproject.toml`**, matrices, affected examples, tests, **CHANGELOG** **Unreleased**. |

**Maintainer checklist:**

1. When extending detection rules or **`docs/examples/`** pins, update **`tests/test_docs_examples_replayt_pins.py`** (patterns, probe grid, or **`_EXTRA_PROBE_VERSIONS`**) and this section if the normative table changes, in one change set with **CHANGELOG** **Unreleased**.
2. Renaming the test module requires updating [Traceability to automated checks](#traceability-to-automated-checks) and **`docs/compat.md`** in the same change set.

### Backlog traceability: Harden replayt public-API boundary lint or import guard

**Normalized user story:** As a maintainer, I want **CI** to fail when **`demo.py`** or any packaged showcase module
under **`src/replayt_ux_showcase/`** imports **replayt** through underscore-private subpaths or pulls top-level names
outside **`replayt.__all__`**, so the repo cannot accidentally couple demos to unpublished internals.

| Backlog acceptance criterion | Where specified | How verified (target) |
| ---------------------------- | --------------- | ----------------------- |
| **Scope of scanned files** | [Normative import rules](#normative-import-rules-showcase-python) | Every **`*.py`** under **`src/replayt_ux_showcase/`**; **`tests/`** excluded |
| **Forbidden: private submodule paths** | Same — rule 1 | **`tests/test_replayt_public_api_boundary.py`** flags static **`import`** / **`from`** where the **first** dotted segment after **`replayt.`** starts with **`_`** |
| **Forbidden: non-public top-level names** | Same — rules 2–3 | For `from replayt import …`, each name ∈ **`replayt.__all__`** at test runtime; **`import replayt`** allowed |
| **Human-readable allowlist** | [`docs/compat.md` — digest table](compat.md#replayt-python-public-api-showcase-digest) | Stays aligned with **`__all__`** for the reference **CI** **replayt** pin; updated when matrix pins or upstream exports change |
| **Runs in default CI** | [Traceability to automated checks](#traceability-to-automated-checks); [GitHub Actions CI workflow](#github-actions-ci-workflow) | **`python -m pytest tests`** after **`pip install -e ".[dev]"`** in each **Python** × **replayt-version** cell — same as other contract tests |
| **Implementation shape** | (Builder choice) | **Acceptable:** **`pytest`** module + **AST** walk and/or **`importlib`** introspection; **ruff** plugin or **`ruff check`** integration if maintainers prefer lint-time failure. Clear failure messages (**file**, **line**, offending import). |

**Builder checklist (phase 3):** Shipped — **`tests/test_replayt_public_api_boundary.py`**, **`docs/compat.md`** **EX-REPLAYT-PY-API**,
[Traceability to automated checks](#traceability-to-automated-checks) row, **CHANGELOG** **Unreleased**.

---

## Static HTML examples: browser smoke (Playwright)

Normative spec for the backlog item **CI smoke: load static HTML examples with Playwright**: what an **optional**
**Playwright**-based check, “no console errors”, a **small browser matrix**, and **README** local run instructions
mean. **Implementation** (workflow YAML, **`pytest-playwright`** or equivalent, **`[project.optional-dependencies].dev`**
pins, and any contract tests) is **Builder** work.

### Goal

- **Shipped** vanilla **`*.html`** examples under **`docs/examples/`** (integrator copy-paste surface — see
  [Showcase stack matrix](#showcase-stack-matrix)) **load in a real browser** with the pinned **replayt** **CDN** script
  behavior, without **JavaScript** errors that would show up in the **browser console** on initial load.

### How pages are opened (acceptance)

- **MUST** serve files over **HTTP** with document root **`docs/examples/`** (same rationale as
  **[P-05 replayt pin and open instructions](examples/PATTERNS.md#p-05-replayt-pin-and-open-instructions-normative)**:
  **`file://`** often blocks cross-origin **CDN** `<script>` loads).
- **MAY** use **stdlib** **`http.server`**, a small **pytest** fixture (background thread), or tooling recommended by
  **`pytest-playwright`** — **Builder** picks one approach and documents it in **[`README.md`](../README.md)**.
- **URL shape:** tests open **`http://127.0.0.1:<port>/<filename>.html`** (or equivalent **loopback** binding documented
  in **README**).

### Assertions (acceptance)

- After navigation settles (**`load`** / **`domcontentloaded`**, or **`networkidle`** only if maintainers document
  why), treat these as **failures**:
  - **Console** messages at **`error`** severity.
  - **`pageerror`** (uncaught exceptions in the page).
- **Console** **`warning`** — **SHOULD** fail by default; **MAY** be ignored only via an **explicit** allowlist in the
  **`tests/`** module (**file**, **message substring or stable id**, **rationale** comment) kept as small as possible.
- **Failed network requests** are **out of scope** for the default gate (focus on **console** + **pageerror**) unless a
  follow-on backlog tightens this.

### CI shape (acceptance)

- **Automation style:** **Optional** separate **`jobs.*`** workflow job **or** a **`pytest`** module run with
  **`pytest -m …`** / path selection so the default **`jobs.test`** command stays
  **`python -m pytest tests`** with **`[tool.pytest.ini_options]`** (**`--cov`**, fail-under) unchanged.
- **Browser matrix:** **Chromium** only for the **default** spec (fast **CI**); **Firefox** / **WebKit** require an
  explicit maintainer decision, workflow matrix expansion, and **CHANGELOG** **Unreleased** in the same change set.
- **Python × replayt:** **Default** cost control is **one** coordinate (for example **Python 3.12** + **`replayt==0.4.25`**
  via the same **`-c`** constraint file pattern as **`jobs.test`**). Expanding to every **Python** × **replayt** cell
  is allowed but **MUST** update **`docs/compat.md`** [CI exercise row inventory](compat.md#ci-exercise-row-inventory),
  **`tests/test_design_principles_contract.py`** when workflow structure is contract-tested, and **CHANGELOG** together.
- **Dependencies:** **`pytest-playwright`** (or equivalent) **SHOULD** live under **`[project.optional-dependencies].dev`**
  with a **PEP 508** pin; **CI** runs **`playwright install chromium`** (or the documented **Playwright** CLI equivalent)
  before smoke tests. Adding the package **MUST** update [Dev optional dependency set (baseline)](#dev-optional-dependency-set-baseline)
  and satisfy **`test_dev_optional_dependencies_match_baseline_package_set`**.

### Pages in scope (acceptance)

- **Include:** every **Shipped** vanilla **`docs/examples/*.html`** file registered in **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)**
  (today **P-01**–**P-05**, **P-09**). **Builder** MAY discover files by glob + allowlist or maintain an explicit list in
  **`tests/`** — either way, **Shipped** set changes in **PATTERNS.md** **SHOULD** trigger the same change set as test
  updates when filenames are added or removed.
- **Exclude (this backlog):** framework dev **`index.html`** trees under **`docs/examples/react/`**, **`vue/`**,
  **`svelte/`** — they require **Vite** (or similar); cover them in a separate backlog unless maintainers explicitly
  extend this spec.

### Local run (README) (acceptance)

- **[`README.md`](../README.md#optional-playwright-smoke-static-html-examples)** **MUST** describe: supported **Python**,
  **`pip install -e ".[dev]"`**, installing **Playwright** browser binaries, the exact command to run the smoke tests
  (path, **`-m`**, or **marker**), and that the server root is **`docs/examples/`**.

### Backlog traceability: CI smoke — load static HTML examples with Playwright

**Normalized user story:** As maintainer, I want an **optional** **CI** step that serves **`docs/examples/`** over **HTTP**,
opens each **Shipped** vanilla **`*.html`** page in **Playwright** (**Chromium** first), and fails on **console** errors
or uncaught **page** exceptions — with **README** instructions for local runs — so static demos stay loadable as **replayt**
and browsers evolve.

| Backlog acceptance criterion | Where specified | How verified (target — Builder / gate) |
| ---------------------------- | --------------- | --------------------------------------- |
| Optional **CI** gate | [CI shape](#ci-shape-acceptance) | New **`ci.yml`** job or scoped **`pytest`** invocation; non-zero exit on regression |
| **HTTP** root **`docs/examples/`** | [How pages are opened](#how-pages-are-opened-acceptance) | Logs / code review; failure if **`file://`** is the default |
| No **error**-level **console** or **`pageerror`** on load | [Assertions](#assertions-acceptance) | Automated assertion in **`tests/`** or job script |
| **Chromium**-first matrix | [CI shape](#ci-shape-acceptance) | **`playwright install chromium`** (or documented equivalent) only, unless expanded |
| **`replayt`** install matches policy | [CI shape](#ci-shape-acceptance) | **`pip install -e ".[dev]" -c`** with pinned **replayt** for chosen cell(s) |
| **README** local run | [Local run (README)](#local-run-readme-acceptance) | Section present; **CONTRIBUTING** / **Quick start** cross-link optional but encouraged |
| Inventory + contract tests | [Traceability to automated checks](#traceability-to-automated-checks); **`docs/compat.md`** | **EX-PLAYWRIGHT-SMOKE** (or successor ID) when the job ships; update **`test_design_principles_contract.py`** if **CI** structure is asserted |

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

## Design kit (Figma) and token export

Normative spec for the backlog item **Figma design kit stub: tokens export + link from docs**. **Figma** variable names and export tooling are **not** duplicated inside [`tokens.md`](playbook/tokens.md); that file stays the **CSS / Tailwind** contract. **[`docs/design-kit/README.md`](design-kit/README.md)** owns **library access**, **duplication**, **Figma → `rux-*` mapping**, **change requests**, and the interim **`design-tokens.json`** shape.

**Single semantic story:** [`tokens.md`](playbook/tokens.md) semantic names (**`rux-*`**) are authoritative. **Figma** variables MUST map **to** those names (see **F3** in the design-kit README). If playbook tokens are renamed, update **`tokens.md`**, the **Figma** mapping (or **JSON** export), and **CHANGELOG** in one change set.

### Backlog traceability: Figma design kit stub (tokens export + link from docs)

**Normalized user story:** As a designer or integrator, I want a documented path to the **Figma** library (or a duplicate), a clear map from **Figma** variables to playbook **`rux-*`** tokens, instructions to request token changes, and—when no public **Figma** URL exists—a checked-in **JSON** export as the interim source of truth.

| Backlog acceptance criterion | Where specified | How verified (target) |
| ---------------------------- | --------------- | --------------------- |
| **Obtain / duplicate library** | [`docs/design-kit/README.md`](design-kit/README.md) — **F1**, **F2** | `tests/test_design_kit_docs.py` |
| **Variables map to playbook tokens** | Same — **F3**; canonical rows in [`tokens.md`](playbook/tokens.md) | Same |
| **Request changes** | Same — **F4** | Same |
| **Interim JSON when no public URL** | Same — **F5**, [JSON export schema](design-kit/README.md#json-export-schema-interim-source-of-truth) | Same; **file** **`docs/design-kit/design-tokens.json`** present when maintainers declare no public link |
| **Discoverable from repo home / playbook** | Same — **F7**, **F8**; [`docs/playbook/README.md`](playbook/README.md) cross-link | Same |

**Shipped (phase 3):** **F1–F8** prose in **`docs/design-kit/README.md`**, **`design-tokens.json`** as interim export (**F5**), root **[`README.md`](../README.md)** / playbook index links, **`tests/test_design_kit_docs.py`**, **CHANGELOG** **Unreleased**.

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
| **replayt** compatibility | **replayt** is pinned per **test** matrix cell (**`-c`** constraint) while staying inside **`[project].dependencies`**; contract tests and the **pytest** suite exercise pins, import smoke, and integration boundaries ([Demo module testing](#demo-module-testing-and-replayt-integration-boundaries), [Dependency pins](#dependency-pins-and-dev-toolchain)) | **`test_replayt_importable`**, **`test_replayt_dependency_matches_design_principles_matrix`**, **`test_ci_test_job_matrix_matches_design_principles_matrix`**, **`test_compat_ci_exercise_inventory_ids_match_ci_matrix`**, and full **`pytest`** run in CI |
| **Supply chain** | Keep **`pip-audit`** aligned with **`docs/DEPENDENCY_AUDIT.md`** (including documented **`--ignore-vuln`** entries that match the workflow). | Existing **`supply-chain`** (or equivalent) job |
| **Static HTML smoke (optional)** | When implemented: **Playwright** loads **Shipped** **`docs/examples/*.html`** over **HTTP** per [Static HTML examples: browser smoke (Playwright)](#static-html-examples-browser-smoke-playwright); **Chromium**-first; does **not** replace **`jobs.test`** **pytest** **cov** gate | New job or scoped **`pytest`**; **`docs/compat.md`** inventory row; **CHANGELOG** **Unreleased** |

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
| **replayt** compat | [Jobs and commands](#jobs-and-commands-normative-target) (**replayt** row) | Editable **dev** install with per-cell **replayt** pin (**`-c`**) + **pytest** + contract tests |

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

## Dependency vulnerability audit (pip-audit)

Normative spec for the backlog item **Document pip-audit failures and dependency override playbook**: what contributors
should run locally when the **`supply-chain`** job fails, how **`pip-audit`** output maps to **fix vs pin vs upstream**
work, and when **`--ignore-vuln`** is allowed without weakening the supply-chain gate.

**Canonical contributor doc:** **[`docs/DEPENDENCY_AUDIT.md`](DEPENDENCY_AUDIT.md)** — operational commands, override
governance, and numbered acceptance **D1–D10**.

### Policy (summary)

- **Single gate:** Default **CI** MUST run **`pip-audit`** on the **`pip install -e ".[dev]"`** graph and treat **non-zero**
  exits as failures ([GitHub Actions CI workflow](#github-actions-ci-workflow) — **Supply chain** row).
- **Doc ↔ workflow parity:** Any **`--ignore-vuln`** in **`.github/workflows/ci.yml`** MUST appear in
  **`docs/DEPENDENCY_AUDIT.md`** with **CVE ID**, **rationale**, and **removal / revisit** criteria; same change set as
  **CHANGELOG** **Unreleased** when the ignore list changes.
- **Not a substitute for semver hygiene:** Prefer **PEP 508** bumps and documented transitive pins over growing the
  ignore list ([Dependency pins and dev toolchain](#dependency-pins-and-dev-toolchain)).
- **JavaScript / npm** tooling is **out of scope** for **`pip-audit`** — cross-link
  **[`docs/FRONTEND_SUPPLY_CHAIN.md`](FRONTEND_SUPPLY_CHAIN.md)** (**A3**).

### Backlog traceability: Document pip-audit failures and dependency override playbook

**Normalized user story:** As a contributor, when **`supply-chain`** / **`pip-audit`** fails in **CI**, I want a short
playbook (local reproduction, triage, upstream vs pin, documented overrides) linked from **README** so I can fix or
escalate without bypassing the gate.

| Backlog acceptance criterion | Where specified | How verified (target) |
| ---------------------------- | --------------- | ------------------------ |
| **Playbook doc** | **[`docs/DEPENDENCY_AUDIT.md`](DEPENDENCY_AUDIT.md)** — **D1–D10** | **`tests/test_dependency_audit_doc.py`** |
| **CI alignment** | **D2**, **D7**; [GitHub Actions CI workflow](#github-actions-ci-workflow) **Supply chain** row | **`tests/test_dependency_audit_doc.py`** (`pip-audit` line parity + documented **CVE** IDs) |
| **README discoverability** | **D9** | **`README.md`** troubleshooting link; asserted by **`tests/test_dependency_audit_doc.py`** |
| **CHANGELOG** on material changes | **D10**; [Changelog, semver, and release notes](#changelog-semver-and-release-notes) | **CHANGELOG** **Unreleased** mention asserted by **`tests/test_dependency_audit_doc.py`** |

**Builder / Tester checklist (follow-up):**

1. When **`docs/DEPENDENCY_AUDIT.md`** acceptance rows (**D1–D10**) or required cross-links change, update
   **`tests/test_dependency_audit_doc.py`** in the same change set.
2. When adding **`--ignore-vuln`**, update **`docs/DEPENDENCY_AUDIT.md`**, **`.github/workflows/ci.yml`**, and
   **CHANGELOG** **Unreleased** in one PR.

---

## Replayt and Python matrix

Policy vs what CI currently exercises may differ; **CI must not claim coverage it does not run**. Expand matrix jobs
when additional cells become required.

| Dimension | Supported (policy) | Verified in CI today | Migration / notes |
| --------- | ------------------- | -------------------- | ------------------ |
| **replayt** (PyPI) | `replayt>=0.1.0,<0.5.0` in `[project].dependencies` (PEP 508); MUST match [Dependency pins and dev toolchain](#dependency-pins-and-dev-toolchain) | **0.1.0**, **0.2.0**, and **0.4.25** pinned per **`strategy.matrix.replayt-version`** on `pip install -e ".[dev]" -c …` in the **test** job (`.github/workflows/ci.yml`); see [CI exercise row inventory](compat.md#ci-exercise-row-inventory) | The `<0.5` cap excludes 0.5+ until maintainers widen the range after compatibility checks; any change to bounds updates this cell, contract tests, pins, matrix, inventory, and **CHANGELOG** together; other in-range releases remain **policy-only** until added to the matrix; on breaking **replayt** majors, add migration notes and adjust examples or shims **in this repo**; propose upstream fixes through normal channels |
| **Python** | `>=3.11` per `requires-python` | **3.11** and **3.12** on `ubuntu-latest` via **`strategy.matrix.python-version`** in the **test** job, combined with **`replayt-version`** as in **compat.md** | Add or drop matrix rows with `requires-python`, **compat.md**, and contract tests in one change set |

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
  The **test** job uses a **`python-version`** × **`replayt-version`** matrix (**3.11** / **3.12** × **0.1.0** / **0.2.0** /
  **0.4.25**), each cell pinning **replayt** via **pip** **`-c`**. That is **not** the same as “every **replayt** release
  in the PEP 508 range is regression-tested” until more pins are added to the matrix and inventory.
- **No false claims** — Documentation (including **README**, this file, and **compat.md**) MUST NOT imply CI exercises
  matrix cells that are not implemented in **`.github/workflows/ci.yml`** (or documented follow-up jobs). When new rows
  ship, update the **Verified in CI today** columns here and in **compat.md** in the same change set as the workflow.

### CI exercise rows (matrix jobs and best-effort)

Normative spec for **honest CI coverage**: every dimension the project describes as **verified in CI** must either map to
a **concrete** workflow job (or **`strategy.matrix`** combination) or be explicitly labeled **best-effort** /
**policy-only** / **bundled** so integrators are not misled.

- **CI exercise row** — A single, enumerable unit of automation listed in **`docs/compat.md`**
  [CI exercise row inventory](compat.md#ci-exercise-row-inventory). Rows are **not** the same as “every cell in every
  prose table”; they are the **minimal** set of workflow coordinates that explain what actually runs on **GitHub Actions**.

- **Explicit job rule** — A row that claims **CI** runs a gate MUST trace to at least one of:
  1. **`test` job matrix** — Each **`strategy.matrix`** combination (today: **`python-version`** × **`replayt-version`**)
     is its own exercise row for the **full** contributor gate (**editable dev install** with **replayt** pinned per cell,
     **ruff**, **pytest** with **`[tool.pytest.ini_options]`** including coverage, and any tests bundled in that **pytest**
     invocation).
  2. **Separate named job** — A top-level **`jobs.<name>`** block that runs a distinct gate (today: **`supply-chain`**
     for **`pip-audit`** on a pinned **Python** image). That job is its own exercise row even when it does not re-run
     **pytest**.
  3. **Bundled inside another row** — Verification that does **not** get its own job or matrix dimension but runs as
     part of a row above (today: **`docs/examples`** **replayt** pin scanning via **`tests/test_docs_examples_replayt_pins.py`**
     runs inside every **`test`** matrix cell).
  4. **Best-effort / policy-only** — Supported ranges or stacks **without** a dedicated automation row MUST use wording
     like *supported by policy*, *not regression-tested per minor*, or *not required in default CI* (see [Showcase stack matrix](#showcase-stack-matrix)
     for stacks marked **Not required**).

- **Adding or removing rows** — Update **`.github/workflows/ci.yml`**, the [Replayt and Python matrix](#replayt-and-python-matrix),
  **`docs/compat.md`** (quick reference + inventory), **`CHANGELOG`**, and **`tests/test_design_principles_contract.py`**
  (when the contract encodes matrix coordinates or inventory rules) **in one change set**.

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
| Vanilla HTML/JS | Yes (`docs/examples/`) | **`docs/examples`** **replayt** pin contract (**`tests/test_docs_examples_replayt_pins.py`**) today; optional **Playwright** load smoke per [Static HTML examples: browser smoke (Playwright)](#static-html-examples-browser-smoke-playwright) when **Builder** ships it | Default integration path for smallest surface; pin contract keeps CDN/requirement snippets inside the PEP 508 range in **`pyproject.toml`** |
| Optional **npm** bundler preview | Yes (documented) — **[`docs/examples/build.md`](examples/build.md)** | Not required in default **CI** (pytest-first) | Root **`package.json`** with **`"private": true`**; **Vite** *or* **esbuild**; **not** an implied public **npm** package for this repo |
| React | **^18**; **[P-06](examples/PATTERNS.md#p-06--react-timeline-player-basic-player--scrubber-parity)** under **`docs/examples/react/`** (**Shipped**) | Optional browser automation later; **pytest** pin contract covers **`docs/examples/react/*.{html,md}`** today | Copy-paste subtree + **README** per **P-06**; **not** a published npm package from this repo |
| Vue | **^3**; **[P-07](examples/PATTERNS.md#p-07--vue-3-timeline-player-basic-player--scrubber-parity)** under **`docs/examples/vue/`** (**Shipped**) | **`tests/test_docs_examples_replayt_pins.py`** covers **`docs/examples/vue/*.{html,md,vue}`** | Same boundary as **P-06**: **Vite** + **`@vitejs/plugin-vue`**, **`private`** subtree **`package.json`**, **not** a published npm product |
| Svelte | **^4**; **[P-08](examples/PATTERNS.md#p-08--svelte-4-timeline-player-basic-player--scrubber-parity)** under **`docs/examples/svelte/`** (**Shipped**) | Pin contract covers **`docs/examples/svelte/*.{html,md,svelte}`** | **Vite** + **`@sveltejs/vite-plugin-svelte`**; same **npm** / directory-boundary rules as **P-06** |

### Vanilla UI pattern catalog

**Canonical inventory:** **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)** — distinct copy-paste vanilla patterns
(**P-01**–**P-05** and **P-09** **Shipped**; **P-09** is **`event-overlay.html`**), plus **framework** subtrees
(**P-06** **React**, **P-07** **Vue**, **P-08** **Svelte** — all **Shipped**),
each with normative acceptance criteria in **`docs/examples/PATTERNS.md`**. The mission
target (**5+** patterns) is **tracked** in **[`docs/MISSION.md`](MISSION.md#pattern-coverage-tracking)** and the digest
**[`docs/compat.md` — Vanilla UI pattern catalog](compat.md#vanilla-ui-pattern-catalog)**.

New patterns **must** be registered in **`docs/examples/PATTERNS.md`** before or in the same change set as the new
**`docs/examples/*.html`** file (see [Single home for copy-paste demos](#one-way-to-do-it-canonical-patterns)).

**Shared accessibility contract:** Vanilla patterns that embed a player, metadata chrome, scrubbers, or future
focus-managed event lists **should** follow **[`docs/a11y/keyboard-model.md`](a11y/keyboard-model.md)** — tab order,
roving `tabindex` when composites apply, scrubber keys, and **Escape** for dismissible layers. Per-pattern normative
text remains in **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)**; the a11y doc is the single cross-pattern
checklist for keyboard and focus. **Broader handoff** (tokens, component anatomy, printable a11y / loading / error checklist) lives under **[`docs/playbook/`](playbook/README.md)**.

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

#### Backlog traceability: Design-to-code handoff playbook (checklist + tokens)

**Normalized user story:** As a designer or integrator, I want a **single** **`docs/playbook/`** home for **spacing / type / color** tokens mapped to **Tailwind-friendly** names, **viewport / session-frame** semantics, **CSS variable naming** aligned with **P-01** **`basic-player.html`**, **timeline / scrubber** anatomy **including interaction states**, **overlay** anatomy **including hover vs keyboard focus** for event callouts (**P-09**), and a **printable** **accessibility / loading / error** checklist — plus a short **how to verify** story (**pytest** today, visual smoke later) — linked from the **README** **Quick start** — so handovers reuse one contract and stay under **one dev-day**.

| Backlog acceptance criterion | Where specified | How verified (target — Builder / gate) |
| ---------------------------- | --------------- | --------------------------------------- |
| Playbook index | **[`docs/playbook/README.md`](playbook/README.md)** | Lists **`tokens.md`**, **`component-anatomy.md`**, **`handoff-checklist.md`**; links **keyboard-model**, **PATTERNS**, **P-04**, supply chain; **How to verify** table (**pytest** + future visual smoke) |
| Token table (spacing, typography, color) | **[`docs/playbook/tokens.md`](playbook/tokens.md)** | Each category has semantic name, **CSS variable** (`--rux-*`), and **Tailwind `theme.extend`** mapping; acceptance **T1**–**T5** in-file (viewport + canonical **P-01** wiring rows **T4**–**T5**) |
| Viewport + **P-01** canonical **`--rux-*`** wiring | **[`docs/playbook/tokens.md`](playbook/tokens.md)** — *Viewport and session frame*, *Canonical `--rux-*` usage* | Spec / **Spec gate**: session **`metadata.viewport`** vs host layout documented; **P-01** cited as minimal reference implementation |
| Timeline + overlay anatomy | **[`docs/playbook/component-anatomy.md`](playbook/component-anatomy.md)** | Named regions; **scrubber interaction states**; **P-03** / **P-06**–**P-08**; overlay modal vs popover; **hover + focus parity** for **P-09** callouts; acceptance **A1**–**A5** in-file |
| Printable checklist | **[`docs/playbook/handoff-checklist.md`](playbook/handoff-checklist.md)** | Sections **Accessibility**, **Viewport**, **Timeline scrubber**, **Loading**, **Error**; print instructions; acceptance **H1**–**H5** in-file |
| README integrator link | **[`README.md`](../README.md#quick-start)** **Quick start** | Explicit link to **`docs/playbook/README.md`** |
| Traceability | [Acceptance criteria (traceability)](#acceptance-criteria-traceability) row *Design-to-code handoff* | **`tests/test_playbook_docs.py`** (sections, acceptance markers **T1–T5** / **A1–A5** / **H1–H5**, index links, **README** quick start, **DESIGN_PRINCIPLES** self-reference, **CHANGELOG** **Unreleased**); **Spec gate** / **Design gate** for prose quality |

**Maintainer note:** Vanilla examples are **not** required to adopt **`--rux-*`** in lockstep with the playbook; **P-01** **`basic-player.html`** demonstrates variables + **`--replayt-primary`** bridge. Further token adoption should ship with **CHANGELOG** + pattern ID.

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

#### Backlog traceability: Ship React timeline player snippet

**Scope:** **`docs/examples/react/`** — see **[P-06](examples/PATTERNS.md#p-06--react-timeline-player-basic-player--scrubber-parity)** in **`docs/examples/PATTERNS.md`**.

**Normalized user story:** As a **React** integrator, I want a **self-contained** **`docs/examples/react/`** tree with a **timeline scrubber** and player embed that mirrors **[`basic-player.html`](examples/basic-player.html)** (`sessionData`, **`replayt.player.init`**) and **P-03** timeline intent, plus a **README** with **Vite** (preferred) or **esbuild** notes and **replayt** / **React** pin guidance, without treating the folder as a **published** npm product.

| Backlog acceptance criterion | Where specified | How verified (target — Builder / gate) |
| ---------------------------- | --------------- | --------------------------------------- |
| **P-06** registration + normative contract | **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)** — **P-06** | **Shipped**: **`docs/examples/react/`** + **README** per **P-06** checklist |
| **`sessionData`** + **`replayt.player.init`** parity with **P-01** | **P-06** [Relationship to P-01 and P-03](examples/PATTERNS.md#relationship-to-p-01-and-p-03) | Code review; **`tests/test_examples.py`** markers |
| Timeline scrub UX aligned with **P-03** | **P-06** sections (tooling, limitations, a11y) | Code review |
| **Published** replayt JS only | **P-06** [replayt JavaScript surface](examples/PATTERNS.md#replayt-javascript-surface-normative) | Code review; symbols listed in-snippet |
| **README**: copy-paste, pins, runbook, non-goal | **P-06** [README and folder layout](examples/PATTERNS.md#p-06-readme-and-folder-layout-normative) | **Spec gate** / review |
| **replayt** pins in **`docs/examples/react/*.{html,md}`** | [Vanilla examples: integrator-facing replayt pins](#vanilla-examples-integrator-facing-replayt-pins) | **`tests/test_docs_examples_replayt_pins.py`** |
| **MISSION** / **README** layout | **[`docs/MISSION.md`](MISSION.md#pattern-coverage-tracking)**, **[`README.md`](../README.md)** | **P-06** **Shipped**; framework row + layout table updated |

#### Backlog traceability: Vue and Svelte minimal player examples

**Scope:** **`docs/examples/vue/`** (**[P-07](examples/PATTERNS.md#p-07--vue-3-timeline-player-basic-player--scrubber-parity)**) and **`docs/examples/svelte/`** (**[P-08](examples/PATTERNS.md#p-08--svelte-4-timeline-player-basic-player--scrubber-parity)**) — see **`docs/examples/PATTERNS.md`**.

**Normalized user story:** As a **Vue** or **Svelte** integrator, I want **minimal runnable** examples under the respective **`docs/examples/`** subtrees that use the **same replayt-facing data contract** as **[`basic-player.html`](examples/basic-player.html)** (**P-01**), include **timeline scrubber** behavior consistent with **P-03** / shipped **P-06**, support **static production builds** (**`npm run build`**), and **never** imply this repository publishes a framework package to **npm** (subtree **`package.json`** **`private`**, README **non-goal**).

| Backlog acceptance criterion | Where specified | How verified (target — Builder / gate) |
| ---------------------------- | --------------- | --------------------------------------- |
| **P-07** / **P-08** registration + normative contract | **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)** — **P-07**, **P-08** | **Shipped**: **`docs/examples/vue/`** and **`docs/examples/svelte/`** + README per checklists |
| **`sessionData`** + **`replayt.player.init`** parity with **P-01** | **P-07** / **P-08** sections (by reference to **P-06** / **P-01**) | Code review |
| Scrubber UX aligned with **P-03** / **P-06** | **P-07** / **P-08** relationship sections | Code review |
| **Vite**-first, **static-build**-friendly | **P-07** [Vue and tooling](examples/PATTERNS.md#p-07-vue-and-tooling-normative), **P-08** [Svelte and tooling](examples/PATTERNS.md#p-08-svelte-and-tooling-normative) | README runbook; `npm run build` documented |
| **Published** replayt JS only; explicit symbols | **P-07** / **P-08** replayt surface sections | Code review |
| **README**: copy-paste, pins, runbook, non-goal | **P-07** / **P-08** README and folder layout sections | **Spec gate** / review |
| **`replayt`** pins in subtree **`*.html`**, **`*.md`**, **`*.vue`**, **`*.svelte`** | [Vanilla examples: integrator-facing replayt pins](#vanilla-examples-integrator-facing-replayt-pins) | **`tests/test_docs_examples_replayt_pins.py`** |
| **MISSION** / **README** / **compat** digest | **[`docs/MISSION.md`](MISSION.md#pattern-coverage-tracking)**, **[`README.md`](../README.md)**, **[`docs/compat.md`](compat.md#vanilla-ui-pattern-catalog)** | **Shipped** rows when examples land |
| Directory boundary: **not** a published npm package | [Module and directory boundaries](#module-and-directory-boundaries); **P-07** / **P-08** | **`private`**: **true**; no misleading **scope** name |

#### Backlog traceability: Normalize session schema examples (Python demo and basic-player.html)

**Scope:** [`docs/examples/SESSION_SCHEMA.md`](examples/SESSION_SCHEMA.md), [`docs/examples/basic-player.html`](examples/basic-player.html) (**P-01**), **[`docs/examples/player-session-metadata-bar.html`](examples/player-session-metadata-bar.html)** (**P-02** viewport **`w`/`h`** fallback), related rows in **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)** (**P-03**, **P-06** cross-links), **[`docs/demo.md`](demo.md)**; optional follow-up: **`rux-showcase-session-fixture`** + drift test for other offline examples (**P-09**, etc.).

**Normalized user story:** As an integrator, I want **one documented JSON shape** that matches the **Python** console
demo (`SAMPLE_SESSION_DATA`) and the **minimal** vanilla player example, so I do not copy conflicting field names
(**`start_ts`** vs **`startTs`**, **`viewport.w`/`h`** vs **`width`/`height`**, **`ts`** vs ad hoc timestamps). As a
maintainer, I want **CI** to catch drift between **`basic-player.html`** and **`demo.py`**.

| Backlog acceptance criterion | Where specified | How verified (target — Builder / gate) |
| ---------------------------- | --------------- | --------------------------------------- |
| Canonical doc for §1 fixture + §2 **init** wire notes | **[`docs/examples/SESSION_SCHEMA.md`](examples/SESSION_SCHEMA.md)** | Spec / review (**phase 2** **Shipped** in spec tree) |
| **`basic-player.html`** sample **`sessionData`** uses §1 keys; **`init`** adapter documented if needed | **SESSION_SCHEMA** §2–§4, [P-01](examples/PATTERNS.md#pattern-inventory) | Code review + **pytest** |
| **pytest** drift guard (**`SAMPLE_SESSION_DATA`** vs registered HTML) | **SESSION_SCHEMA** §5 | **`tests/test_session_schema_examples.py`** in default **`pytest`** |
| **PATTERNS** / **demo.md** / **compat** cross-links | [PATTERNS — Canonical session fixture](examples/PATTERNS.md#canonical-session-fixture-cross-surface), **demo.md**, **compat.md** | Spec gate |
| **CHANGELOG** **Unreleased** when copy-paste contract changes | [Changelog, semver, and release notes](#changelog-semver-and-release-notes) | **`CONTRIBUTING.md`** |

**Shipped:** Spec (**phase 2**) added **`SESSION_SCHEMA.md`** and catalog cross-links. Builder (**phase 3**) shipped **`basic-player.html`**
fixture + adapter, **`player-session-metadata-bar.html`** viewport fallback, and **`tests/test_session_schema_examples.py`**.

#### Backlog traceability: Event overlay pattern (vanilla **P-09** + optional `demo.py` hook)

**Scope:** **[P-09](examples/PATTERNS.md#p-09--event-overlay-lane-scrub-hover-tooltips-keyboard)** in **`docs/examples/PATTERNS.md`** (primary file **`docs/examples/event-overlay.html`** — **Shipped**).

**Normalized user story:** As an integrator, I want a **second dedicated vanilla doc example** for **event overlays**
(scrub-linked callouts, **hover** tooltips, **keyboard** focus and **Escape**) consistent with **[LLM boundaries](#llm-boundaries)**
and **[offline / deterministic fixture](#offline-deterministic-fixture-page-for-llm-and-reviewer-workflows)** norms; optionally I want the **console** demo narrative in **`docs/demo.md`** / **`demo.py`** to use the **same vocabulary** for teaching.

| Backlog acceptance criterion | Where specified | How verified (target — Builder / gate) |
| ---------------------------- | --------------- | --------------------------------------- |
| **P-09** registration + normative contract | **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)** — **P-09** | **Shipped**: **`event-overlay.html`** (or approved rename) on disk; inventory → **Shipped** |
| Scrub + overlay UX + a11y | **P-09** [Overlay UX](examples/PATTERNS.md#p-09-overlay-ux-normative), **[`keyboard-model.md`](a11y/keyboard-model.md)**, **[`component-anatomy.md` §2](playbook/component-anatomy.md#2-overlays-dialogs-popovers-event-callouts)** | Code review; **`tests/test_examples.py`** markers |
| Inline **`sessionData`** (preferred); **LLM**-safe | **P-09** [Data and offline / LLM boundary](examples/PATTERNS.md#p-09-data-and-offline--llm-boundary-normative) | No session **`fetch`** on primary path; determinism like **P-05** |
| **Published** replayt JS; **CDN** pin in range | **P-09** [replayt JS surface and pin](examples/PATTERNS.md#p-09-replayt-js-surface-and-pin-normative) | **`tests/test_docs_examples_replayt_pins.py`** |
| Optional **`demo.py`** hook | **P-09** [Optional demo.py console hook](examples/PATTERNS.md#optional-demopy-console-hook-normative-intent-optional-deliverable), **[`docs/demo.md`](demo.md#cross-surface-operator-story-console-demo-and-web-embed)** | Additive **`docs/demo.md`** rows + **`tests/test_demo.py`** when implemented (**Shipped** with overlay teaching line) |
| **MISSION** / **compat** / **README** | **[`docs/MISSION.md`](MISSION.md#pattern-coverage-tracking)**, **[`docs/compat.md`](compat.md#vanilla-ui-pattern-catalog)**, **[`README.md`](../README.md)** | Vanilla count **6** when **P-09** **Shipped** |

**Shipped (phase 3):** **`docs/examples/event-overlay.html`**, **P-09** **Shipped** in **`docs/examples/PATTERNS.md`**, **[`docs/MISSION.md`](MISSION.md#pattern-coverage-tracking)** vanilla count **6**, **`tests/test_examples.py`** markers, **`tests/test_docs_examples_replayt_pins.py`**, **`demo.py`** / **`docs/demo.md`** overlay teaching line + **`tests/test_demo.py`**, **CHANGELOG** **Unreleased**, **[`README.md`](../README.md)** and **[`docs/compat.md`](compat.md#vanilla-ui-pattern-catalog)** digest updated.

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
4. **Semver** — See [Changelog, semver, and release notes](#changelog-semver-and-release-notes) for how **PATCH** vs
   **MINOR** apply to the **Python package surface** versus **docs/examples**; the bullets above remain the deprecation
   *process*.

---

## Changelog, semver, and release notes

This repository is a **reference**: integrators **copy** `docs/examples/` and sometimes **vendor** snippets without
installing **`replayt-ux-showcase`** from PyPI. Release notes and version bumps must stay legible for **both** audiences.

**Canonical changelog:** [`CHANGELOG.md`](../CHANGELOG.md) ([Keep a Changelog](https://keepachangelog.com/en/1.0.0/)).
**Package version:** `[project].version` in **`pyproject.toml`**, kept aligned with **`replayt_ux_showcase.__version__`**
(see [Traceability to automated checks](#traceability-to-automated-checks)).

### Python package API (`replayt_ux_showcase`)

SemVer applies to **documented, stable** Python behavior: imports, **`__version__`**, and **CLI** / **`python -m`**
entrypoints described as supported in **README** or package docs.

| Bump | Use when |
| ---- | -------- |
| **MAJOR** | Breaking changes to that stable surface (removed symbols, incompatible CLI defaults) after any announced deprecation horizon, or other SemVer-major semantics maintainers adopt. |
| **MINOR** | Backward-compatible **API** additions, new optional behaviors, or maintainer decisions that **expand** what tag consumers may rely on (without breaking existing use). |
| **PATCH** | Bug fixes and internal refactors that do **not** change the stable contract; **narrow** dependency or docs-only fixes that do not remove integrator-facing guarantees. |

### Docs and examples (integrator copy-paste surface)

Treat **`docs/examples/`** (and registered **P-xx** patterns in **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)**)
as **user-facing deliverables**, not “internal docs,” when choosing a semver bump—even when the PyPI wheel is unchanged.

| Bump (for a **tagged** showcase release) | Typical triggers |
| ---------------------------------------- | ---------------- |
| **MINOR** | A pattern moves to **Shipped** (new **P-xx** row or new framework subtree), **additive** copy-paste contracts integrators are expected to adopt, **widening** the declared **replayt** PEP 508 range, new **CI** matrix coordinates that **expand** documented support, or **filename / contract** changes that are **breaking** for vendored snippets (prefer deprecation first—see [Deprecation and removal](#deprecation-and-removal)). |
| **PATCH** | Corrections to examples that fix **bugs** in copied snippets without changing the pattern **ID** or **intent**; typo/clarity edits; **pin updates** that keep snippets **inside** the same declared **replayt** band; dependency pins that are **compatible** tightening only. |

**MAJOR** for the package is reserved for rare, explicit breaking events on the **Python** surface (or a coordinated
maintainer decision to signal large integrator migration). Do **not** use **MAJOR** for routine HTML example churn;
prefer **MINOR** + migration notes when vendored filenames or contracts must change.

### Unreleased: pattern coverage and mission tracking

Mission success includes **5+** distinct vanilla UI patterns, tracked in **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)**,
**[`docs/MISSION.md`](MISSION.md#pattern-coverage-tracking)**, **[`docs/compat.md` — vanilla catalog](compat.md#vanilla-ui-pattern-catalog)**,
and **CHANGELOG**.

When a pattern moves to **Shipped** (or a **new** **P-xx** is registered as **Spec only** in a user-visible way), add
**`CHANGELOG.md`** bullets under **`[Unreleased]`** in the **same change set** as the inventory / mission / digest
updates, so release consumers can see **trajectory toward** (and maintenance of) the **5+** goal. Prefer **`### Added`**
or **`### Documentation`** per Keep a Changelog; name the **pattern ID**, primary artifact path, and cross-surface
updates (**PATTERNS**, **MISSION**, **compat** when applicable).

Maintainer checklist: **[`CONTRIBUTING.md`](../CONTRIBUTING.md)** — *When to edit `docs/DESIGN_PRINCIPLES.md` in the same
change set as pins*.

#### Backlog traceability: CHANGELOG and release process for integrator-facing semver

**Normalized user story:** As a maintainer or integrator, I want a **written** semver and **CHANGELOG** policy that
separates **Python package** bumps from **docs/examples** impact, and **Unreleased** notes that track **pattern**
milestones toward the mission **5+** goal, with a contributor checklist for **DESIGN_PRINCIPLES** when **pins** move.

| Backlog acceptance criterion | Where specified | How verified (target) |
| ---------------------------- | --------------- | --------------------- |
| **MINOR** vs **PATCH** rules for **Python** vs **examples** | [Python package API](#python-package-api-replayt_ux_showcase), [Docs and examples](#docs-and-examples-integrator-copy-paste-surface) | **`tests/test_changelog_release_policy_docs.py`** keeps normative headings and tables present; release tagging stays maintainer review |
| **Unreleased** tracks **Shipped** / mission-relevant pattern work | [Unreleased: pattern coverage and mission tracking](#unreleased-pattern-coverage-and-mission-tracking); **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)** release-note blurb | **`tests/test_changelog_release_policy_docs.py`** + **CHANGELOG** hygiene in PRs that ship patterns |
| **CONTRIBUTING** + **pins** ↔ **DESIGN_PRINCIPLES** same change set | [`CONTRIBUTING.md`](../CONTRIBUTING.md) — *When to edit `docs/DESIGN_PRINCIPLES.md` in the same change set as pins* | **`tests/test_changelog_release_policy_docs.py`** |

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
