# Printable handoff checklist — accessibility, loading, error

**How to print:** Open this file in GitHub, your docs site, or a local preview, then use the browser’s **Print** dialog (e.g. **Ctrl+P** / **Cmd+P**). For a paperless review, copy the checkbox lines into your issue or PR template.

**Normative detail:** [keyboard-model.md](../a11y/keyboard-model.md) (a11y), **P-04** [embed-container-states.html](../examples/embed-container-states.html) (loading / errors).

---

## Accessibility

- [ ] **Tab order** follows reading / operator order: chrome → scrubber (if any) → player — [keyboard-model §1](../a11y/keyboard-model.md#1-tab-order-default-dom-order).
- [ ] **No positive `tabindex`** on non-interactive or decorative nodes.
- [ ] **Scrubber** is keyboard-operable (**Arrow**, **Home** / **End**, **Page Up** / **Page Down** as applicable) — [keyboard-model §3](../a11y/keyboard-model.md#3-scrubber--seek-control-sliders).
- [ ] **Escape** closes dismissible layers and returns focus to the opener — [keyboard-model §4](../a11y/keyboard-model.md#4-escape).
- [ ] **Focus visible** on all focusable controls (`:focus-visible` or equivalent).
- [ ] **Long interactive event lists** use roving `tabindex` (or documented exception) — [keyboard-model §2](../a11y/keyboard-model.md#2-roving-tabindex-for-event-lists).
- [ ] **Images / icons** that convey meaning have text alternatives; decorative assets are hidden from AT.
- [ ] **Color contrast** meets team policy for text and interactive states (don’t rely on color alone for errors).

---

## Loading

- [ ] **Loading state** is announced (e.g. `role="status"` + `aria-live="polite"`) and **visibly** distinct from ready and error — see **P-04** [`PATTERNS.md` §P-04](../examples/PATTERNS.md#p-04-embed-container-states-empty-loading-failure-recovery).
- [ ] **Skeleton / placeholder** does not trap focus; when load completes, focus moves predictably (document if unchanged).
- [ ] **Slow networks:** copy explains what is loading (“Loading replay…”) and optional cancel / timeout behavior if product requires it.

---

## Error and recovery

- [ ] **User-visible error** text for failed session fetch, invalid payload, or player init failure — **P-04** precedent.
- [ ] Errors use **safe text** (e.g. `textContent`), not untrusted HTML, when showing server messages.
- [ ] **Retry** (or equivalent recovery) is **keyboard-reachable** and labeled.
- [ ] **Status region** announces errors to AT without duplicating noise on every minor keystroke.
- [ ] **Developer-only** details (stack traces) stay in **console** or collapsed debug panels, not the default operator surface.

---

## Tokens and anatomy (quick verify)

- [ ] Spacing / type / color mapped per [`tokens.md`](tokens.md) (or documented deltas).
- [ ] Timeline and overlay regions named per [`component-anatomy.md`](component-anatomy.md).

---

## Sign-off

| Role | Name | Date |
| ---- | ---- | ---- |
| Design | | |
| Engineering | | |

---

## Acceptance (Builder / spec gate)

| # | Criterion |
| --- | --------- |
| H1 | Checklist sections exist for **Accessibility**, **Loading**, and **Error / recovery** with actionable bullets. |
| H2 | **Print** path documented (browser print). |
| H3 | **keyboard-model** and **P-04** linked as normative references for a11y and load/error UX. |
