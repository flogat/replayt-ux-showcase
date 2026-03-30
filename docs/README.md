# Documentation

This directory contains the specification, design principles, and integration guides for the **replayt-ux-showcase** repository.

## Start here

| Document | Purpose |
|----------|---------|
| **[MISSION.md](MISSION.md)** | **Mission, scope, and boundaries.** Read this first to understand what this repository owns (copy-paste demos, design kits, handoff playbooks) and what it does not (hosted products, replayt core, npm packages). |
| **[REPLAYT_ECOSYSTEM_IDEA.md](REPLAYT_ECOSYSTEM_IDEA.md)** | Positioning of this showcase relative to replayt core and integrator workflows. |
| **[DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md)** | Canonical contract for integration boundaries, versioning, deprecation policy, and LLM boundaries. Update this when pins, matrices, or CI change. |
| **[compat.md](compat.md)** | Quick-reference compatibility matrix, CI coverage truth, shims, and upgrade paths for integrators. |

## For integrators

| Document | Purpose |
|----------|---------|
| **[examples/](examples/)** | Copy-paste UI patterns (vanilla JS, React, Vue, Svelte). Start with [examples/PATTERNS.md](examples/PATTERNS.md) for the canonical inventory. |
| **[playbook/README.md](playbook/README.md)** | Design-to-code handoff: tokens, component anatomy, and printable checklist (under one dev-day handoff target). |
| **[design-kit/README.md](design-kit/README.md)** | Figma library access, variable → `--rux-*` mapping, interim `design-tokens.json`, and component inventory. |
| **[a11y/keyboard-model.md](a11y/keyboard-model.md)** | Keyboard interaction and focus management for player/timeline embeds. |
| **[FRONTEND_SUPPLY_CHAIN.md](FRONTEND_SUPPLY_CHAIN.md)** | CDN vs bundled replayt, optional SRI, npm/Vite notes. |

## For contributors

| Document | Purpose |
|----------|---------|
| **[demo.md](demo.md)** | Console demo contract and test plan for `python -m replayt_ux_showcase.demo`. |
| **[DEPENDENCY_AUDIT.md](DEPENDENCY_AUDIT.md)** | Playbook for pip-audit failures: local reproduction, triage, fix vs override policy. |
| **[reference-documentation/README.md](reference-documentation/README.md)** | Optional bundled upstream reference docs workflow (license, provenance, refresh cadence). |
| **[examples/build.md](examples/build.md)** | Optional npm + Vite/esbuild local bundler spec for maintainers. |

## By concern

- **What is this project?** → [MISSION.md](MISSION.md)
- **What can I copy into my app?** → [examples/PATTERNS.md](examples/PATTERNS.md)
- **How do design tokens map to code?** → [playbook/tokens.md](playbook/tokens.md)
- **How do I hand off player UI from design to engineering?** → [playbook/README.md](playbook/README.md)
- **What replayt/Python versions are supported?** → [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md) matrices and [compat.md](compat.md)
- **How do I run the demo locally?** → [../README.md](../README.md#quick-start)
