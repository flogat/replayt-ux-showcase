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
| Extension points documented | [Extension points](#extension-points) |
| Audience needs extended | [Audience](#audience) |

### Traceability to automated checks

These alignments are **enforced in CI** today (the principles doc is broader):

| Check | Enforced by |
| ----- | ----------- |
| `requires-python` matches the Python row in [Replayt and Python matrix](#replayt-and-python-matrix) | `tests/test_design_principles_contract.py` |
| **`replayt`** dependency lower bound matches that matrix | Same |
| CI **Python** version in `.github/workflows/ci.yml` matches that matrix | Same |
| Section headings for the two matrices, extension points, and audience | Same |
| Subsection **replayt Python API boundary** under [Module and directory boundaries](#module-and-directory-boundaries) | Same |
| Extension points row for packaged **`replayt_ux_showcase`** surface | Same |
| Audience rows for **Release / tag consumers** and **Automation agents (LLM tooling)** | Same |
| Each line in **`[project].dependencies`** and **`[project.optional-dependencies].dev`** carries a PEP 508 version constraint | Same |
| **`[build-system].requires`** entries carry a PEP 508 version constraint | Same |
| **`replayt` is importable** after install (integration smoke) | Same |

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
| **`.github/workflows/`** | CI that installs the package and runs **pytest** (and future matrix jobs) | Store long-lived tokens (read-only `contents` is the default contract) |

**Dependency direction:** showcase code and tests **→** **replayt** (PyPI). Demos may document how integrators pull
**replayt** in their own apps; this repo does not re-export **replayt** as a different product.

### replayt Python API boundary

- Depend on **replayt** only through its **published** PyPI package and **documented** public surface (release notes,
  upstream reference docs). Do not rely on private modules, underscore-prefixed internals, or undocumented symbols.
- Workflow or mock-LLM helpers from **replayt** are allowed only when they stay **offline** and **deterministic** in
  default CI, per [LLM boundaries](#llm-boundaries).

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
| **ruff** | Lint/format (as adopted by the repo) |
| **pip-audit** | Supply-chain / vulnerability checks in contributor workflows |

Adding, renaming, or dropping a **dev** tool updates this table, **CHANGELOG**, and (when applicable) CI or docs that
mention the workflow.

### Out of scope for “pins” here

- Committing a **lock file** or **`pip freeze`** output is **not** required by this spec unless maintainers adopt that
  separately. **Pins** mean **declared constraints in `pyproject.toml`** for **direct** dependencies; transitive versions
  follow the resolver unless a stricter policy is adopted later.

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
