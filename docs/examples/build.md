# Optional local bundler recipe (npm + Vite or esbuild)

This document is the **normative spec** for an **optional** maintainer path: bundle **replayt** from the **public npm
registry** with **Vite** or **esbuild** for **local preview** of static examples, without turning this repository into
a **published npm product**.

**Related:** [Frontend supply chain](../FRONTEND_SUPPLY_CHAIN.md) (CDN vs bundled **replayt**, single compatibility story),
[Design principles — module boundaries](../DESIGN_PRINCIPLES.md#module-and-directory-boundaries),
[Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins)
(**`tests/test_docs_examples_replayt_pins.py`** scans this file for pins).

---

## Goals

- Give maintainers a **repeatable** way to run **`import`**-style workflows against **replayt**’s npm package while
  developing future framework examples.
- Keep **default CI** **pytest-first** — no **npm install** / **npm audit** / bundler steps required in
  **`.github/workflows/`** for this backlog (optional **npm** jobs remain a **future** backlog).
- Keep **`docs/examples/`** the **home** for copy-paste **HTML** demos; the bundler output is **preview** glue, not a
  second canonical snippet tree.

## Explicit non-goals (module boundary)

- **Do not** present the repository as shipping a **supported npm package** named like **`replayt-ux-showcase`** on the
  public registry unless maintainers **explicitly** publish and document that in **CHANGELOG** (contradicts
  [Module and directory boundaries](../DESIGN_PRINCIPLES.md#module-and-directory-boundaries) until then).
- **Do not** replace **CDN**-first vanilla examples for integrators; bundling is **optional** and **maintainer-oriented**.
- **Do not** require contributors to install **Node** for **pytest**, **ruff**, or **`pip install -e ".[dev]"`**.

---

## Single compatibility story (pins)

- **`[project].dependencies`** **`replayt`** in **`pyproject.toml`** remains **authoritative** for the supported consumer
  band (PEP 508), same as [Frontend supply chain](../DESIGN_PRINCIPLES.md#frontend-supply-chain-javascript--cdn).
- The **npm** dependency on **`replayt`** in **`package.json`** MUST use a **semver range** whose resolved versions stay
  **inside** that band (see [PEP 508 vs caret-style wording](../DESIGN_PRINCIPLES.md#pep-508-vs-caret-style-wording) for
  mental model). Example alignment for today’s policy: depend on a **0.4.x** line compatible with **`>=0.1.0,<0.5.0`**
  (e.g. **`0.4.25`** exact, or **`^0.4.25`** if maintainers accept compatible npm resolution within **0.4**).
- Any **versioned CDN** URL in examples under this doc MUST use **`replayt@<version>`** with **`<version>`** satisfying
  **`pyproject.toml`** (same rule as other **`docs/examples/*.md`** files).

---

## Deliverables (Builder — phase 3)

| # | Deliverable | Normative rules |
| - | ----------- | ---------------- |
| **B1** | **`package.json`** at the **repository root** | **`"private": true`**. **`name`** MUST NOT read as an official public package for this showcase (avoid **`replayt-ux-showcase`** as the npm **`name`** unless publishing is intentional and recorded). |
| **B2** | **Bundling tool** | Implement **one** primary recipe using **Vite** *or* **esbuild** (maintainer choice). The doc and config SHOULD stay small; the other tool MAY be noted as an alternate paragraph if cost is low. |
| **B3** | **Direct dependency** | Declare **`replayt`** as a **direct** **npm** dependency with an explicit **semver** range per [Single compatibility story](#single-compatibility-story-pins). |
| **B4** | **Scripts** | **`package.json`** **`scripts`** include at least **`build`** (produce bundled assets) and a **`preview`** or **`dev`** script that serves or watches for **local** verification. |
| **B5** | **Scope of inputs** | Entry can **import** **`replayt`** and **wrap** or **re-export** for local demos; **do not** fork **replayt** internals. Prefer starting from existing static examples under **`docs/examples/`** as fixtures when wiring the first bundle. |
| **B6** | **Lockfile policy** | If maintainers commit a **lockfile** (**`package-lock.json`**, **`pnpm-lock.yaml`**, etc.), document **who** updates it when **replayt** minors move (same change-set spirit as [Single change set when replayt minors move](../FRONTEND_SUPPLY_CHAIN.md#single-change-set-when-replayt-minors-move)). Lockfiles are **not** required by this spec until the Builder adds them. |
| **B7** | **CI** | **Default** GitHub Actions workflow **continues** to run **Python** **pytest** (with **`[tool.pytest.ini_options]`** coverage gate), **ruff**, and **pip-audit** only — **no** new **npm** job **required** here. |
| **B8** | **Cross-links** | **README** project layout row (or adjacent contributor note) points to this file; **CHANGELOG** **Unreleased** records the optional recipe when **`package.json`** lands. |

---

## Acceptance criteria (backlog — documentation + optional implementation)

The backlog **Optional npm workspace or build recipe without publishing a package** is satisfied when:

| # | Criterion |
| - | --------- |
| **C1** | This spec (**`docs/examples/build.md`**) states **goals**, **non-goals**, **pin alignment** with **`pyproject.toml`**, and **CI pytest-first** policy. |
| **C2** | **Design principles** and **`docs/FRONTEND_SUPPLY_CHAIN.md`** link or reference this spec so contributors find it next to the existing **CDN** / **bundler** story. |
| **C3** | **Module boundaries** clarify that a root **`package.json`** is **optional**, **`private`**, and **not** a supported public **npm** surface unless explicitly published. |
| **C4** | **Builder** (phase **3**) adds **`package.json`** (and minimal config) meeting **B1**–**B8**, or a follow-up ticket documents deliberate deferral with **CHANGELOG** / **handoff** traceability. |

**Automated checks (today):** **`tests/test_docs_examples_replayt_pins.py`** applies to this **Markdown** file. **No**
contract test yet asserts **`package.json`** presence or **`npm run build`** — optional future backlog.

---

## Contributor quick path (informative — after Builder ships files)

After phase **3** implements **B1**–**B8**, contributors who opt in typically:

1. Install a supported **Node** toolchain (version band documented by the Builder next to **`package.json`**).
2. Run **`npm install`** (or **pnpm** / **yarn** if the recipe standardizes one).
3. Run the documented **`dev` / `preview`** script to verify bundled **replayt** against local fixtures.

Exact commands are **intentionally** left to the shipped **`package.json`** and **README** so they stay executable and
reviewable in one place.
