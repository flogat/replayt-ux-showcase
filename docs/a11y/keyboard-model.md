# Keyboard and focus model (timeline / player controls)

**Audience:** Designers, frontend integrators, and maintainers copying **`docs/examples/`** vanilla patterns.  
**Goal:** One **checklist-level** contract so handoffs stay under **one dev-day** without re-deriving tab order, list focus, scrubber keys, or **Escape** behavior per pattern.

**Normative companions:** Per-pattern rules and Builder checklists live in **[`docs/examples/PATTERNS.md`](../examples/PATTERNS.md)** (**P-01**–**P-05**). This document is the **shared** accessibility story; where they differ, **PATTERNS.md** wins for that pattern’s scope.

---

## Scope

| In scope | Out of scope (unless a pattern explicitly adds it) |
| -------- | ---------------------------------------------------- |
| Focus order for **page-level** embeds: chrome → scrubber / primary controls → player container | Pixel-perfect focus styling beyond **`:focus-visible`** (theme is integrator-owned) |
| **Roving** `tabindex` for **composite** event lists built as many focusable rows | Full **WCAG** audit criteria for arbitrary host apps |
| **Arrow** / **Home** / **End** / **Page Up / Page Down** on **sliders** and **ARIA `slider`** | **replayt** player **internal** keyboard handling (upstream); we only specify **our** DOM around it |
| **Escape** for **dismissible** UI **we** add (dialogs, popovers opened from chrome) | Rebinding browser or OS shortcuts |

---

## 1. Tab order (default: DOM order)

**Rule:** Focusable controls **must** follow a **logical reading** and **operator** order in the **flat** tab sequence (no positive `tabindex` except the roving pattern below).

**Stacking convention (showcase patterns):**

1. **Page chrome** — instructions, toolbars, **Retry**, scenario buttons (**P-04**), metadata actions (**P-02**).
2. **Timeline / scrubber** — when present (**P-03**), the scrub control **before** the player container so keyboard users can seek before tabbing into the embedded player’s focusables (matches shipped **`timeline-scrubber.html`**).
3. **Player container** — **`#player`** (or equivalent) **after** outer controls unless a pattern documents a **deliberate** exception in **`PATTERNS.md`** and in-snippet comments.

**P-01** (**`basic-player.html`**): With only the player, tab order is whatever the **replayt** build exposes inside the container. When you **add** chrome or a scrubber, re-read this section and update DOM order **or** document an exception.

**Anti-patterns:**

- Positive `tabindex` on marketing copy or decorative nodes.
- Focusable controls **visually** above the player but **after** it in DOM (unless **PATTERNS.md** allows and comments explain why).

**Handoff artifact:** Each shipped example **must** keep a short **“Tab order (handoff):”** comment block (already required for **P-02**, **P-03**, **P-04**).

---

## 2. Roving `tabindex` for event lists

**When it applies:** If a pattern introduces a **long** list of **focusable** event rows (or cells) that share one toolbar, use a **single** tab stop for the list **container** and **roving** focus among rows with **Arrow** keys — per **[WAI-ARIA Practices — Listbox](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/)** or **Tree / Grid** as appropriate. None of the current **P-01**–**P-05** snippets ship such a list; this is **forward-looking** for timeline/event-picker extensions.

**Normative minimum when you ship a roving list:**

| Concern | Requirement |
| ------- | ----------- |
| **One tab stop** | Container (`tabindex="0"`) **or** first item `tabindex="0"`, siblings `tabindex="-1"` until focused. |
| **Arrow navigation** | **Up/Down** (or **Left/Right** for horizontal strips) moves aria-activedescendant or roved focus; **Home/End** jump to first/last when lists are large enough to matter. |
| **Typeahead** | Optional; document if implemented. |
| **Label** | Expose **`aria-label`** or **`aria-labelledby`** on the composite. |

If the list is **non-interactive** (read-only log), keep rows **non-focusable** and expose updates via **`aria-live`** where appropriate (**P-04** status region is the precedent).

---

## 3. Scrubber / seek control (sliders)

**Native `<input type="range">`** (used in **P-03**):

- **Tab** focuses the slider.
- **Arrow Left/Right** (and **Up/Down** in many UAs) **nudge** the value by `step`.
- **Home** / **End** typically jump to **min** / **max** (browser-dependent; document in-snippet if you rely on it).
- **Page Down** / **Page Up** often step by a **larger** increment.

**Custom-drawn scrubber:** Implement **`role="slider"`**, set **`aria-valuemin`**, **`aria-valuemax`**, **`aria-valuenow`** (and **`aria-valuetext`** if showing timecodes), and match **Arrow** / **Home** / **End** / **Page** behavior to the **[ARIA slider pattern](https://www.w3.org/WAI/ARIA/apg/patterns/slider/)**.

**Throttling:** Keyboard repeats can flood seek APIs; reuse the same **coalescing** story as pointer scrub (**P-03** — e.g. **rAF** or debounce) and **always** commit the **final** value on **keyup** or **`change`**.

---

## 4. `Escape`

| Context | Expected behavior |
| ------- | ----------------- |
| **Modal / dialog** opened from chrome (e.g. session details) | **Escape** **closes** the dialog and returns focus to the **opener** (see **ARIA dialog pattern**). |
| **Popover / menu** (non-modal) | **Escape** **dismisses** and returns focus to the **activator**. |
| **No layer open** | **Do not** call **`preventDefault()`** on **Escape** unless you document a **global** shortcut policy; let the event bubble so host apps keep their own handlers. |
| **Fullscreen / immersive** wrapper (if added) | **Escape** **exits** immersive mode and restores focus to the control that entered it. |

---

## 5. Focus visibility

Focusable controls **must** remain visibly focused: browser default **or** explicit **`:focus-visible`** styles (see **P-02** / **P-03** / **P-04** examples).

---

## 6. Builder acceptance checklist (cross-pattern)

Use this in **Spec gate** / **Build gate** when touching player + timeline examples:

- [ ] **Tab order** comment block present and consistent with DOM.
- [ ] No stray **positive** `tabindex` except **roving** composites (section 2).
- [ ] **Scrubber** is keyboard-operable (native range **or** full **ARIA slider** + documented keys).
- [ ] **Seek** throttling does not drop **final** keyboard commits.
- [ ] **Escape** documented for any dismissible layer **this** snippet adds.
- [ ] **Focus rings** visible for custom-styled buttons/sliders.

---

## Related links

- **[`docs/examples/PATTERNS.md`](../examples/PATTERNS.md)** — **P-02** (chrome focus), **P-03** (scrubber keyboard), **P-04** (retry + live region).
- **[`docs/DESIGN_PRINCIPLES.md`](../DESIGN_PRINCIPLES.md)** — traceability row *Timeline / player keyboard and focus*.
- **[`docs/compat.md`](../compat.md#vanilla-ui-pattern-catalog)** — pattern digest.
