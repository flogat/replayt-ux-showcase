# Positioning — Polished demos and UI patterns for replayt integrators with design-engineering handoff playbook

This project **uses** [replayt](https://pypi.org/project/replayt/). It is **not** a fork of replayt. Compatibility,
version pins, and CI are **your** responsibility here.

**Test coverage (required):** ship automated tests for behavior you claim (unit, contract/integration at replayt
boundaries, smoke where useful). Document how to run them in the README and CI.

Pick **one primary** pattern below (you may blend—say which leads):

## 1) Core-gap

_Use when replayt core intentionally omits a capability._

- What is out of core and why?
- What does **this** repo provide instead?
- How do you track replayt releases?

## 2) LLM showcase

_Concrete demo that needs model calls._

- One-sentence use case; which replayt primitives you exercise
- LLM boundaries: secrets, cost, redaction
- What a reviewer runs to verify

## 3) Framework bridge

_Adapter to another framework or runtime._

- Target framework; public API of the bridge
- How **you** maintain consumer-side compatibility (pins, CI matrix)

## 4) Combinator

_Novel composition of replayt + other tools._

- What is stronger together; shared conventions; integration tests where feasible

## Your choice

- **Primary pattern:** 1) Core-gap
- **One-paragraph pitch:** Replayt core excels at session capture and replay primitives but intentionally omits polished frontend UI patterns and design-engineering handoff materials to stay backend-focused. This repo fills that gap with copy-pasteable demos (e.g., timeline players, event overlays), themeable components for React/Vue/Svelte, Figma design kits, and a playbook (checklists, tokens) ensuring pixel-perfect handoffs from design to code. Compatibility is spelled out in **docs/DESIGN_PRINCIPLES.md** (supported ranges vs what CI runs today); pytest locks key cells to **pyproject.toml** and **.github/workflows/ci.yml**, and matrix jobs grow when the mission needs more coverage; upstream changes still mean re-tests and shims here (consumer-side maintenance).

## Reviewers and LLM harnesses — offline fixture page

**DESIGN_PRINCIPLES** defaults to **offline**, **deterministic** tooling for agents: see **[LLM boundaries](DESIGN_PRINCIPLES.md#llm-boundaries)** and **[P-05](examples/PATTERNS.md#p-05-offline-deterministic-fixture-page-for-llm-and-reviewer-workflows)** in **`docs/examples/PATTERNS.md`**.

- **Artifact (planned):** **`docs/examples/fixture-replay.html`** — **inlined** synthetic **`sessionData`** only (**no** `fetch` / **XHR** / **WebSocket** for the session payload), **no** committed secrets, **no** calls to hosted **LLM** or other non-reproducible model paths **in that page**. A **pinned** **replayt** player **`<script src=…>`** is allowed (same semver story as other vanilla examples); that is **not** “session over the wire.”
- **How to open:** Use a **local static server** under **`docs/examples/`** (e.g. `cd docs/examples && python -m http.server`) and browse to **`/fixture-replay.html`** so **CDN** scripts load reliably; **`file://`** is discouraged for the same reason as in **[README.md](../README.md#reviewer-and-llm-harness-fixture-vanilla)**. **Builder** flips **P-05** from **Spec only** to **Shipped** using the checklist under **[P-05](examples/PATTERNS.md#p-05-offline-deterministic-fixture-page-for-llm-and-reviewer-workflows)** in **`docs/examples/PATTERNS.md`**.

This path is **not** a substitute for integrator **production** embedding patterns (**P-01**–**P-04**); it is the **canonical** **fixture** surface for **human review** and **automation** that must not depend on live backends or model calls.
