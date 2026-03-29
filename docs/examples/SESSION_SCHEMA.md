# Session data shape — showcase canonical fixture

This document is the **normative reference** for the **offline / teaching** session object that matches the Python
console demo (**`replayt_ux_showcase.demo.SAMPLE_SESSION_DATA`**) and **[`docs/demo.md`](../demo.md)**. Use it when
copy-pasting a **stable** JSON fixture that should stay aligned across **HTML**, **Python**, and framework examples.

**Related:** [Pattern catalog](PATTERNS.md) (**P-01**–**P-09**), [Vanilla examples: replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins), [P-06 console parity](PATTERNS.md#p-06--console-sample-parity-sample_session_data), [Compatibility digest](../compat.md#vanilla-ui-pattern-catalog).

---

## 1. Showcase session fixture (canonical)

**Source of truth (code):** `replayt_ux_showcase.demo.SAMPLE_SESSION_DATA` in
**`src/replayt_ux_showcase/demo.py`**.

**Source of truth (spec):** the same object is spelled out in **[`docs/demo.md`](../demo.md)** under
**`SAMPLE_SESSION_DATA: dict[str, Any]`**.

### Normative rules

- **Root:** an object with **`events`** (array) and **`metadata`** (object).
- **Events:** each event is an object with at least **`type`** (string) and **`ts`** (number, **seconds** from session
  start, floating point allowed). Additional keys depend on **`type`** (e.g. **`click`**: **`x`**, **`y`**;
  **`scroll`**: **`dy`**; **`resize`**: **`w`**, **`h`**) — see **`docs/demo.md`** event table.
- **Metadata (canonical keys):**
  - **`start_ts`** — number, session start offset in **seconds** (typically **`0.0`** for fixtures).
  - **`viewport`** — object with **`w`** and **`h`** (numbers, pixels).
  - **`duration`** — number, total session length in **seconds**.

### Canonical JSON (illustrative; must match `demo.py` / `docs/demo.md`)

The **Builder** backlog *Normalize session schema examples between Python demo and basic-player.html* requires that
any **normative** fenced or inline JSON labeled “showcase session” **byte-align** with this shape for the fields above.
When **`SAMPLE_SESSION_DATA`** changes, update **this fenced block** in the **same change set** as **`demo.py`**,
**`docs/demo.md`**, and the contract test described in §5.

```json
{
  "events": [
    {"type": "click", "ts": 1.0, "x": 100, "y": 200},
    {"type": "scroll", "ts": 5.0, "dy": 300},
    {"type": "keypress", "ts": 8.5, "key": "a"},
    {"type": "resize", "ts": 12.0, "w": 1920, "h": 1080},
    {"type": "click", "ts": 15.0, "x": 500, "y": 300},
    {"type": "scroll", "ts": 18.0, "dy": -150},
    {"type": "keypress", "ts": 22.0, "key": "Enter"},
    {"type": "click", "ts": 25.0, "x": 800, "y": 600},
    {"type": "scroll", "ts": 27.5, "dy": 200},
    {"type": "mousemove", "ts": 28.0, "x": 900, "y": 700},
    {"type": "click", "ts": 29.0, "x": 950, "y": 750},
    {"type": "scroll", "ts": 29.5, "dy": 50}
  ],
  "metadata": {
    "start_ts": 0.0,
    "viewport": {"w": 1920, "h": 1080},
    "duration": 30.0
  }
}
```

**Do not** use placeholder names from older snippets for this layer: e.g. **`startTs`** (camelCase),
**`metadata.viewport.width` / `height`**, or skipping **`duration`**, when claiming parity with **`SAMPLE_SESSION_DATA`**.

---

## 2. `replayt.player.init` wire shape (browser examples)

The **published** replayt browser player (see upstream release notes for the pinned version) may expect a **different**
in-memory object than §1 — commonly **millisecond** timestamps and **camelCase** metadata (**`startTs`**, **`durationMs`**,
**`viewport.width` / `height`**) plus per-event fields such as **`timestamp`** (ms). This repository does **not** redefine
upstream’s wire contract here.

**Showcase pattern:** framework and some vanilla examples keep a **pure adapter** from §1 → init payload (see
**`adaptConsoleSessionToReplaytMs`** in **`docs/examples/react/src/App.jsx`** and **`docs/examples/react/README.md`**).

**Builder guidance for [`basic-player.html`](basic-player.html):** the **inline sample** shown to integrators **must**
use §1 field names for the **fixture** story. If the pinned **replayt** build requires §2 for **`init`**, add a **small,
documented** adapter in the snippet (or pass through only if verified against that pin) and link to this doc — do **not**
reintroduce a second “canonical” shape that disagrees with **`SAMPLE_SESSION_DATA`** without updating §1 and Python.

---

## 3. Legacy placeholders (drift to remove)

Until the **basic-player** backlog ships, [`basic-player.html`](basic-player.html) may still show **`startTs`** /
**`viewport.width`**. That is **legacy** relative to §1. **[`player-session-metadata-bar.html`](player-session-metadata-bar.html)**
(**P-02**) and other patterns that mix **`durationMs`** + **`viewport.width`** remain valid for **chrome + init** demos
but should **cross-link** §1 when documenting **console parity** or **Python** alignment.

**Target end state:** P-01’s **commented** sample uses §1; any ms/camelCase shape is explicitly labeled **init wire** or
produced only via adapter. P-02 **viewport** display should prefer **`viewport.w` / `viewport.h`** when present, with
optional fallback to **`width` / `height`** documented in the same change set if both must be supported temporarily.

---

## 4. Builder acceptance (backlog: normalize session schema)

| # | Criterion | Verification (target) |
|---|-----------|------------------------|
| 1 | **`docs/examples/SESSION_SCHEMA.md`** (this file) is the integrator-facing canonical doc for §1 | Spec gate / review |
| 2 | **`docs/examples/basic-player.html`** — placeholder **`sessionData`** and surrounding comments use **`start_ts`**, **`viewport.w` / `h`**, **`duration`**, and **`events[].ts`** consistent with §1 | Code review + contract test (§5) |
| 3 | If **`init`** still needs §2, snippet documents adapter or upstream requirement with link to §2 | Code review |
| 4 | **`docs/demo.md`** and **`docs/examples/PATTERNS.md`** reference this file where they describe **`SAMPLE_SESSION_DATA`** / cross-surface parity | Spec gate |
| 5 | **Automated drift guard** — CI fails when **`basic-player.html`** (and any other file listed in the test) diverges from **`SAMPLE_SESSION_DATA`** for the agreed key set | **`pytest`** (new or extended module — §5) |
| 6 | **CHANGELOG** **Unreleased** when **Shipped** behavior or copy-paste contract changes | **`CONTRIBUTING.md`** |

---

## 5. Contract test (normative intent for implementation)

**Phase 3 (Builder)** should add or extend **`pytest`** so drift between §1 and integrator snippets cannot merge silently.

**Recommended approach (pick one in implementation; document choice in the test module docstring):**

1. **Golden substring / key guard:** For each registered file (minimum **`docs/examples/basic-player.html`**), assert
   presence of canonical key **substrings** (e.g. **`start_ts`**, **`"w":`**, **`"h":`**, **`"ts":`**) and **absence** of
   legacy placeholder patterns in the **`sessionData` literal** (e.g. **`startTs:`** inside the sample object), **or**
2. **Structured extraction:** Parse the inline object (heuristic or `ast` for Python) and compare required keys to
   **`replayt_ux_showcase.demo.SAMPLE_SESSION_DATA`** loaded from the installed package.

**Scope:** Start with **P-01** (**`basic-player.html`**) + **`SAMPLE_SESSION_DATA`**. Extending to additional HTML files
(**P-02**, **P-09**, etc.) is **optional** in the same backlog if the Builder can do so without fragile parsing; otherwise
record follow-up in **CHANGELOG** / **handoff**.

**Traceability:** [Design principles — backlog traceability](../DESIGN_PRINCIPLES.md#backlog-traceability-normalize-session-schema-examples-python-demo-and-basic-playerhtml).
