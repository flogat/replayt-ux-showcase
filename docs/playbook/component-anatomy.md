# Component anatomy — timeline and overlays

**Purpose:** Shared vocabulary for **design ↔ engineering** handoffs so layout, DOM order, and layering match [keyboard-model.md](../a11y/keyboard-model.md) and shipped patterns (**P-02**, **P-03**, **P-04**, **P-09** **`event-overlay.html`**).

---

## 1. Timeline / scrubber strip

**Reference implementation:** **P-03** [`timeline-scrubber.html`](../examples/timeline-scrubber.html), **P-06** React scrubber (parity with **P-03**).

| Region | Responsibility | Typical DOM / role | Handoff notes |
| ------ | -------------- | ------------------- | ------------- |
| **Track container** | Hit target for pointer scrub; optional tick marks | Wrapper around the control | Keep **min/max** time aligned with `sessionData` metadata / events (see **P-03** contract). |
| **Seek control** | User-adjustable current time | `<input type="range">` **or** `role="slider"` | Keyboard behavior in [keyboard-model.md §3](../a11y/keyboard-model.md#3-scrubber--seek-control-sliders); throttle seeks to avoid API floods. |
| **Time readout** | Elapsed / duration (optional) | Text node or `aria-live="polite"` region | Prefer **visible** labels for operators; don’t rely on color alone for state. |
| **Context label** | “Session timeline”, scenario name | `aria-labelledby` / visible heading | Helps screen reader users in dense dashboards. |

**Vertical stacking (default):** Metadata chrome (**P-02**) → **Timeline strip** → **Player container** — matches [keyboard-model.md — Tab order](../a11y/keyboard-model.md#1-tab-order-default-dom-order).

**Data boundary:** Scrubber logic consumes **`sessionData.events`** (sorted by timestamp per **P-03**); do not assume private **replayt** internals.

### Scrubber interaction states (handoff vocabulary)

Design specs SHOULD name these states so engineering and QA share one timeline UX contract (maps to **P-03** / **P-06**–**P-08** scrubber behavior unless a product doc overrides).

| State | Operator-visible behavior | Handoff notes |
| ----- | --------------------------- | ------------- |
| **Resting** | Thumb / fill reflects current time; no active drag | Baseline for comps and visual regression baselines. |
| **Hover / focus on track** | Optional preview or enlarged hit target; **focus** MUST remain keyboard-visible per [`keyboard-model.md`](../a11y/keyboard-model.md) | Do not rely on hover alone for critical information. |
| **Active scrub (drag / pointer down)** | Value updates continuously; player may **throttle** seeks (see **P-03** `requestAnimationFrame` pattern) | Document whether audio/video sync or network-backed seeks allow **partial** updates vs commit-on-release. |
| **Committed seek** | Final time applied after `change` / `pointerup` / keyboard step | Pair with **Time readout** and any **aria-valuetext** policy. |
| **Disabled / no timeline** | Control inert when there is no range, empty **`events`**, or load failure | Match **P-04** error shell — no silent no-op scrubber. |
| **Loading / indeterminate** (optional) | Track visible but not yet seekable | If used, tie to **Loading** checklist in [`handoff-checklist.md`](handoff-checklist.md). |

---

## 2. Overlays (dialogs, popovers, event callouts)

**Use cases:** Session detail drawer, event inspector, “jump to click” tooltip, **non-modal** popovers over the player.

| Region | Responsibility | Handoff notes |
| ------ | -------------- | ------------- |
| **Backdrop** (modal only) | Dim host; block pointer to content below | Optional for **modal** dialogs; omit for **non-modal** popovers so player remains visible. |
| **Overlay surface** | Focusable content, actions | Use **`role="dialog"`** + **`aria-modal="true"`** when modal; link **`aria-labelledby`**. |
| **Dismiss control** | Close affordance | **Must** be focusable; **Escape** closes per [keyboard-model.md §4](../a11y/keyboard-model.md#4-escape). |
| **Anchor** (popover) | Element that opened the layer | Return focus here on dismiss; do not trap tab **unless** modal. |
| **Z-index layer** | Stacking above player | Document integer bands (e.g. chrome `10`, overlay `40`, toast `50`) in design specs to avoid fights with host app nav. |

**Player interaction:** If the overlay is **non-modal**, clicks on the player may still reach **replayt**; document whether scrubbing is allowed while the overlay is open.

**Event callouts:** If listing events is **interactive** (many rows), plan for **roving** `tabindex` per [keyboard-model.md §2](../a11y/keyboard-model.md#2-roving-tabindex-for-event-lists); read-only logs may use **`aria-live`** instead.

**Hover vs focus (event overlays — P-09):** Callouts triggered from the **event lane** MUST treat **pointer hover** and **keyboard focus** as **first-class**: a focused event chip or marker shows the **same class of information** as hover (timestamps, labels, preview), not a reduced stub. Scrub-linked “active” state should stay in sync with the scrubber per **[P-09](../examples/PATTERNS.md#p-09--event-overlay-lane-scrub-hover-tooltips-keyboard)**.

---

## 3. Relationship to shipped patterns

| Pattern | Anatomy focus |
| ------- | ------------- |
| **P-02** | Metadata **bar** above player — loading placeholder, validation errors, tab order comment |
| **P-03** | **Timeline** strip + range input + player |
| **P-04** | **Embed shell** — skeleton, status region, **Retry** |
| **P-01** | Minimal player only — anatomy starts at single `#player` container |
| **P-09** | **Event overlay** lane — scrub-linked markers, hover/focus callouts (**Shipped** — **[`event-overlay.html`](../examples/event-overlay.html)**, **[P-09](../examples/PATTERNS.md#p-09--event-overlay-lane-scrub-hover-tooltips-keyboard)**) |

---

## Acceptance (Builder / spec gate)

| # | Criterion |
| --- | --------- |
| A1 | **Timeline** section names **track**, **seek control**, **time readout**, and ties to **P-03** / **P-06**. |
| A2 | **Overlay** section covers **modal vs non-modal**, **dismiss**, **Escape**, **focus return**, and **z-index** layering. |
| A3 | Cross-links to **`keyboard-model.md`** for tab order, scrubber keys, roving lists, and **Escape**. |
| A4 | **Scrubber interaction states** (resting, hover/focus, active scrub, committed seek, disabled, optional loading) are named for handoff. |
| A5 | **Event overlay** handoff calls out **hover + focus parity** for callouts and points to **P-09**. |
