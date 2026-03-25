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
- **One-paragraph pitch:** Replayt core excels at session capture and replay primitives but intentionally omits polished frontend UI patterns and design-engineering handoff materials to stay backend-focused. This repo fills that gap with copy-pasteable demos (e.g., timeline players, event overlays), themeable components for React/Vue/Svelte, Figma design kits, and a playbook (checklists, tokens) ensuring pixel-perfect handoffs from design to code. Replayt releases are tracked via a compatibility matrix (docs/) and CI matrix tests across pinned versions; upstream changes trigger re-tests/shims here (consumer-side maintenance).
