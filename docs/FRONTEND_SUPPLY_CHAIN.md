# Frontend supply chain (replayt browser bundle)

Integrators load **replayt**’s web player from the **published npm package** (same versioning family as the **PyPI**
**`replayt`** distribution this repo depends on) using either a **versioned CDN `<script>`** or a **bundled** install.
This document is the **normative supplement** for **JavaScript delivery**; the **supported semver band** for
**replayt** is still declared in **`pyproject.toml`** and summarized in **[README.md](../README.md)**,
**[docs/DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md)**, and **[docs/compat.md](compat.md)** (**single compatibility
story**).

**Python-only supply chain** (**`pip-audit`** after **`pip install -e ".[dev]"`**) is documented in
**[docs/DEPENDENCY_AUDIT.md](DEPENDENCY_AUDIT.md)** — it does **not** audit the **npm** tarball your browser loads.

---

## Single change set when replayt minors move

When maintainers change the supported **replayt** consumer range or bump example pins:

1. **`pyproject.toml`** — **`[project].dependencies`** **`replayt`** PEP 508 line.
2. **Matrices and digest** — [Replayt and Python matrix](DESIGN_PRINCIPLES.md#replayt-and-python-matrix),
   **[docs/compat.md](compat.md)** quick reference, and any **README** wording that restates the range.
3. **`docs/examples/`** — every in-scope **`replayt@<version>`** (or equivalent) URL per
   [Vanilla examples: integrator-facing replayt pins](DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins)
   (**`tests/test_docs_examples_replayt_pins.py`** enforces alignment with **`pyproject.toml`**).
4. **Optional SRI** — any **`integrity="…"`** on example `<script>` tags MUST be recomputed for the new artifact and
   updated **together** with the **versioned** URL (see [Subresource Integrity (SRI)](#subresource-integrity-sri)).
5. **CHANGELOG** — **Unreleased** notes for integrators.
6. **`tests/`** — only if pin **detection** rules or exempt snippets change.

Avoid updating **only** prose or **only** examples: pins, spec tables, and **CHANGELOG** drift creates a false
compatibility story.

---

## CDN delivery (e.g. jsDelivr)

Static examples in this repo (e.g. **`docs/examples/basic-player.html`**) use **jsDelivr** URLs of the form
`https://cdn.jsdelivr.net/npm/replayt@<version>/…` so the **npm** version is visible in the path.

### When to pin the CDN URL

- **Do** use a **concrete** **`replayt@<version>`** segment in maintainer-owned **`docs/examples/`** snippets so the
  file stays inside the showcase’s declared PEP 508 range and **pytest** can fail on drift.
- **Prefer** **HTTPS** script URLs only.
- **Discourage** **`@latest`** or other **unpinned** CDN URLs in shipped examples: they hide semver skew from
  **`pyproject.toml`**. If you must show **`latest`** for teaching, add clear prose that it is **not** the supported
  integration pattern; if the line would be scanned as a pin, use the **`<!-- replayt-examples:pin-exempt -->`**
  opt-out on the line **immediately before** the snippet (per design principles).

### CDN trust boundaries

- **Availability**, **TLS**, and **CDN compromise** are **third-party** operational risks. **SRI** (below) mitigates
  **content substitution** at the edge **when** you opt in.
- This repository does **not** commit to mirroring **replayt** on a first-party CDN unless a future backlog says so.

---

## Subresource Integrity (SRI)

**SRI** is **optional** for integrators and **optional** in this repo’s vanilla HTML examples.

- **When to use:** High-assurance pages that load **replayt** from a **CDN** without a bundler may add
  **`integrity="sha384-…"`** (or other supported algorithms) and matching **`crossorigin`** on **`<script src="…">`**
  so the browser rejects unexpected bytes.
- **When you add SRI in an example:** The hash MUST match the **exact** file served at that **versioned** URL.
  **Bumping** **replayt** in an example requires **both** a new **`replayt@<version>`** path **and** a new **SRI**
  hash in the **same** commit / change set as **`pyproject.toml`** / other pins when the bump is policy-driven.
- **How to obtain a hash:** Use any trustworthy workflow (e.g. download the pinned URL and run OpenSSL **`dgst`**, or
  a browser **DevTools** / generator you trust). The doc does not mandate a specific tool.

**Not required by spec:** CI does **not** today verify **SRI** attributes; review and optional future automation are
separate backlogs.

---

## Bundling alternative (npm + Vite, webpack, etc.)

Instead of a runtime CDN `<script>`, integrators may **`npm install replayt`** (or **pnpm** / **yarn**) and **`import`**
the player through **Vite**, **esbuild**, **webpack**, **Rollup**, or similar.

- **Repository-local optional recipe:** Maintainers may add a **private** root **`package.json`** and a **Vite** or **esbuild**
  workflow for **local preview** only — normative spec **[`docs/examples/build.md`](examples/build.md)** (**CI** stays
  **pytest-first**; this is **not** a published **npm** product unless explicitly released).
- **Semver alignment:** Choose an **npm** semver range **compatible** with the showcase’s **PyPI**-declared band (see
  [PEP 508 vs caret-style wording](DESIGN_PRINCIPLES.md#pep-508-vs-caret-style-wording) for mapping **caret**/**tilde**
  mental models to numeric bounds). The **`pyproject.toml`** line remains the **authoritative** supported range for
  **this** repository’s story; **npm** ranges in **your** app should not advertise versions **outside** that policy.
- **Lockfiles:** **`package-lock.json`** / **`pnpm-lock.yaml`** / etc. live in **integrator** repos. This repo’s
  **`docs/examples/`** tree does **not** require an npm lockfile **unless** a shipped pattern introduces a **build-step**
  demo (future backlog) or the optional **[`docs/examples/build.md`](examples/build.md)** recipe commits one per **B6**.
- **CI scope:** Default **GitHub Actions** does **not** install **npm** deps or run **`npm audit`** on **replayt**;
  integrators should run **npm** supply-chain tooling in their own pipelines when they bundle.

---

## Acceptance criteria (backlog — documentation)

The backlog **Document CDN vs bundled replayt with SRI and supply-chain notes** is satisfied when:

| # | Criterion |
| - | --------- |
| **A1** | **`docs/FRONTEND_SUPPLY_CHAIN.md`** exists and covers **versioned CDN URLs**, **optional SRI** (co-bump with URL), and **npm + bundler** as an alternative, with **CDN trust** and **lockfile** notes. |
| **A2** | The doc states the **single compatibility story**: **`pyproject.toml`** **`replayt`** PEP 508 range is authoritative; **`docs/examples/`** CDN pins stay inside it per **`tests/test_docs_examples_replayt_pins.py`**. |
| **A3** | The doc distinguishes **Python** **`pip-audit`** (**[DEPENDENCY_AUDIT.md](DEPENDENCY_AUDIT.md)**) from **front-end** (**CDN** / **npm**) choices. |
| **A4** | **README.md** and **`docs/DESIGN_PRINCIPLES.md`** link here (project layout + **Frontend supply chain** section) so contributors find the guidance next to the **README** compatibility pointers. |
| **A5** | **CHANGELOG** **Unreleased** records this documentation addition. |

**Automated checks (phase 3):** **`tests/test_frontend_supply_chain_doc.py`** enforces **A1–A4** (sections, keywords,
links) and **A5** (an **Unreleased** mention of this doc). **SRI** hash correctness for real `<script>` tags stays manual
/ optional future work.

**Explicit non-goals (this backlog):** Require **SRI** on every example; add **npm** jobs to **CI**; vendor **replayt**
into this repo.
