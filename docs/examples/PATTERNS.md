# Examples — UI pattern catalog

This file is the **canonical inventory** for distinct, copy-paste integrator examples under `docs/examples/`: **vanilla
HTML/JS** files (default path) and **registered framework subtrees** (**React** — **P-06**). It supports the mission
success criterion “**5+**” **vanilla** patterns and gives **Spec gate** / **Builder** a single place to check
**what counts as a pattern**, **what ships where**, and **acceptance criteria** before code lands.

**Related:** [Mission — Success](../MISSION.md#pattern-coverage-tracking), [Showcase stack matrix](../DESIGN_PRINCIPLES.md#showcase-stack-matrix), [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins), [Keyboard and focus model](../a11y/keyboard-model.md) (shared a11y checklist for player / timeline embeds), [Optional local bundler recipe](build.md) (maintainer **npm** + **Vite** / **esbuild** — not a UI pattern ID).

## Pattern inventory

A **pattern** is a **standalone** integrator-facing example with its own **primary user job** (not a one-line tweak of
another file). Filename changes follow [Deprecation and removal](../DESIGN_PRINCIPLES.md#deprecation-and-removal).

| ID | Artifact | Status | Summary |
| -- | -------- | ------ | ------- |
| **P-01** | [`basic-player.html`](basic-player.html) | **Shipped** | Minimal embedded player: container, `sessionData`, `replayt.player.init`, theme note. |
| **P-02** | [`player-session-metadata-bar.html`](player-session-metadata-bar.html) | **Shipped** | Session **metadata chrome**: compact bar **above** the player, same `sessionData` contract as P-01, plus loading / error / focus rules below. |
| **P-03** | [`timeline-scrubber.html`](timeline-scrubber.html) | **Shipped** | **Timeline scrubber strip**: seek/scrub UX driven by **replayt public JS** + `sessionData.events`, with documented ordering/throttling assumptions and CDN **limitations** note. |
| **P-04** | [`embed-container-states.html`](embed-container-states.html) | **Shipped** | **Embed container** lifecycle: skeleton while **loading**, user-visible **failure** + **retry**, **`aria-live`** / **`role="status"`** status for operators and **automation agents**; **published** replayt JS only. |
| **P-05** | [`fixture-replay.html`](fixture-replay.html) | **Shipped** | **Offline fixture** for **reviewers** and **LLM** harnesses: **inlined** synthetic **`sessionData`**, **no** runtime session fetch, **no** secrets, **no** live/stochastic model calls; pinned **replayt** player script only. |
| **P-06** | [`react/`](react/) ([`README.md`](react/README.md), [`src/App.jsx`](react/src/App.jsx)) | **Shipped** | **React 18** timeline player: same **`sessionData`** / **`replayt.player.init`** contract as **P-01**, timeline scrub UX aligned with **P-03**; **Vite**-first (or **esbuild** notes); **not** an npm-published package. |

**Mission trajectory:** **P-01** through **P-05** are shipped (**5** distinct **vanilla** patterns), satisfying the mission **5+** target for HTML examples. **P-06** is a **framework** subtree; it does not change the vanilla count. Additional patterns stay **future** backlogs until registered in this table first.

---

## P-02 — Session metadata chrome (viewport, duration, session id)

### User story

As an integrator, I want a **second vanilla snippet** that layers a **compact metadata bar** above the replay player
so operators see **session id**, **viewport**, and **duration** without opening devtools, using the same data object I
already pass to the player as in **P-01**.

### `sessionData` contract (compatibility with P-01)

- **Same root shape** as [`basic-player.html`](basic-player.html): an object with at least:
  - **`events`** — array (may be empty in the snippet; real apps pass replayt event arrays).
  - **`metadata`** — object.
- **P-01 baseline keys** inside `metadata` (from `basic-player.html`): `startTs`, `viewport` (`width`, `height`).
- **Extensions for P-02** (additive; must not break P-01 copies):
  - **`metadata.sessionId`** — string, human-readable stable id for the session row in the chrome.
  - **`metadata.durationMs`** — non-negative number, **session duration in milliseconds**, shown in the bar (preferred;
    avoids guessing from empty `events` in static demos).

Integrators may omit `sessionId` or `durationMs` only where the **error / empty-state rules** below still produce a
clear UX (see **Required chrome inputs**).

### Layout and visual intent

- **Metadata bar** sits **immediately above** the player container (same horizontal width as the player or its wrapper).
- **Compact**: one row (wrapping allowed on small widths), typographic hierarchy secondary to the player.
- **Themeable** via the same CSS-variable story as P-01 where practical (e.g. bar border/background uses neutral
  surfaces; document any vars the snippet introduces).

### Required chrome inputs (normative)

After the integrator has finished loading (not during the loading placeholder), the bar **must** be able to show:

| Field | Source | Rule |
| ----- | ------ | ---- |
| Viewport | `metadata.viewport.width` × `metadata.viewport.height` | **Required** after load. If missing, show **error state** (not an empty bar pretending success). |
| Session id | `metadata.sessionId` | **Required** after load for this pattern. If missing, show **error state** (integrators must supply for this demo’s contract). |
| Duration | `metadata.durationMs` | **Required** after load. If missing, show **error state**. Format for display: human-readable (e.g. `m:ss` or `H:MM:SS` for long sessions) — exact formatting is implementation detail as long as it is consistent and documented in the snippet comments. |

**Rationale:** P-02 is explicitly about **viewport, duration, session id**; treating them as required after load keeps
the pattern testable and aligned with the backlog title.

### Loading state (normative)

- Before `sessionData` is available (e.g. async fetch), the metadata bar region **must** show **visible placeholder
  text** (e.g. “Loading session…”), not a blank strip.
- The player area may use an equivalent placeholder or stay empty until init — **document in-snippet** which approach
  is used; at least one of bar or player must make the loading phase obvious.

### Error state (normative)

- If, after load, **any required chrome input** is missing or invalid (e.g. `durationMs` negative, `viewport` without
  numeric width/height), the snippet **must** show a **user-visible error message** in or above the bar (not only a
  `console.error`).
- Errors **must not** silently fall back to an “empty” bar that looks like a successful zeroed session.

### Keyboard focus and accessibility (normative)

Shared checklist: **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)** (tab order, **Escape** for dismissible UI, focus visibility). The bullets below are **P-02**-specific.

- **Tab order:** Elements in the **metadata bar** that are **focusable** (links, buttons, inputs) **must** appear **before**
  the player’s focusable controls in **DOM order** (bar first, then player). If the bar has no focusable controls, the
  first focusable control **inside** the player container follows naturally — do not trap focus in the player before
  the bar when the bar contains interactive elements.
- **Focus visibility:** Focusable controls **must** keep a visible focus ring (browser default or snippet CSS).
- **Copy-paste comment:** The HTML/JS **must** include a short comment block summarizing tab order intent for
  design-engineering handoff.

### replayt pin and file placement

- New file lives under **`docs/examples/`** with the **planned name** `player-session-metadata-bar.html` (adjust only
  if a naming collision requires it; if renamed, update this catalog and **CHANGELOG** in the same change set).
- **replayt** script URL **must** satisfy [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins) (same PEP 508 range as `pyproject.toml`).

### Builder acceptance checklist (implementation)

**P-02** is **Shipped**; the original PR met the items below. Use the same bar when you change this pattern:

1. `docs/examples/player-session-metadata-bar.html` implements the normative sections above.
2. [Pattern inventory](#pattern-inventory) lists **P-02** as **Shipped** with the correct filename.
3. **CHANGELOG** **Unreleased** records notable example or contract changes; note pattern count / mission tracking when the inventory changes.
4. **[`docs/MISSION.md`](../MISSION.md#pattern-coverage-tracking)** reflects the shipped count.

**Automated checks today:** **`tests/test_docs_examples_replayt_pins.py`** (CDN pin vs **`pyproject.toml`**) and
**`tests/test_examples.py`** (example files on disk plus light **P-02** contract strings). Full browser automation remains
out of scope until the [Showcase stack matrix](../DESIGN_PRINCIPLES.md#showcase-stack-matrix) adds it.

---

## Backlog traceability: Ship session metadata chrome pattern

| Backlog acceptance criterion | Where specified |
| ---------------------------- | ---------------- |
| Second vanilla snippet, metadata bar above player | [P-02 — Session metadata chrome](#p-02--session-metadata-chrome-viewport-duration-session-id) |
| Same `sessionData` shape as `basic-player.html` (additive metadata) | [`sessionData` contract](#sessiondata-contract-compatibility-with-p-01) |
| Loading placeholder text | [Loading state](#loading-state-normative) |
| Error when metadata missing / invalid | [Error state](#error-state-normative) |
| Keyboard-focus order | [Keyboard focus and accessibility](#keyboard-focus-and-accessibility-normative) |
| Progress toward **5+** patterns | [Pattern inventory](#pattern-inventory), [Mission](../MISSION.md#pattern-coverage-tracking) |
| **CHANGELOG** / mission tracking | [Builder acceptance checklist](#builder-acceptance-checklist-implementation), [Mission](../MISSION.md#pattern-coverage-tracking) |

---

## P-03 — Timeline scrubber strip (events-driven seek)

### User story

As an integrator, I want a **copy-paste vanilla** example that adds a **horizontal timeline scrubber** (slider / track)
below or above the player so operators can **seek** through the replay using **`sessionData.events`** and **replayt’s
published browser/JS API**, with **explicit assumptions** about event ordering and **input throttling** so my fork
behaves predictably across replayt minors inside the supported range.

### Relationship to P-01

[`basic-player.html`](basic-player.html) already mentions extending with a timeline via the replayt events API. **P-03**
is the **dedicated** pattern for that job: it **must not** silently redefine P-01’s init contract; it **layers** scrubber
UX and documented event handling on top of the same **`sessionData` root** (`events` + `metadata`) unless the Builder
documents a deliberate, additive extension in-snippet.

### Delivery shape (normative)

- **Preferred:** new file **`docs/examples/timeline-scrubber.html`**.
- **Allowed alternative:** extend **`basic-player.html`** only if the scrubber is a **clearly separated** section
  (distinct `<section>` or major comment banner + self-contained script block) and **P-03** acceptance criteria still
  read as a single pattern in review; if this path is chosen, update this inventory row to point at the anchor filename
  and **CHANGELOG** **Unreleased** in the same change set.

### `sessionData` and events (normative)

- **Root shape:** Same as P-01: `events` (array) and `metadata` (object). The scrubber **must** use **`events`** (not
  only empty placeholder arrays in the shipped snippet—include **synthetic or documented sample events** sufficient to
  demonstrate a non-trivial timeline, or document how to substitute real API payloads).
- **Documented ordering assumption:** The HTML/JS **must** include a short **comment block** (design-handoff style)
  stating what ordering integrators should assume for `events` (e.g. “replayt guarantees monotonic timestamps” vs
  “sort client-side by field X before mapping to the scrubber”). If the showcase cannot assert upstream guarantees,
  state **“integrators should verify against replayt release notes for their pin”** and implement **defensive ordering**
  (e.g. sort once before building the time range) **in the example** so the demo is stable.
- **Time range:** The snippet **must** document which **timestamp(s)** define scrubber min/max and playhead position
  (e.g. first/last event time, `metadata.startTs` + duration, or API described in comments). Ambiguous mapping is not
  acceptable for **Shipped**—pick one approach and document it.

### Scrub / seek interactions (normative)

- **Primary control:** A **range** or **single-thumb** slider (or equivalent ARIA **`slider`**) spanning the session
  timeline; dragging or keyboard adjustment **seeks** the replay.
- **Keyboard:** Slider (or focusable scrub control) **must** be reachable and adjustable without a pointer; document
  expected keys (native range behavior is enough if documented). Full scrubber / **Escape** guidance: **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)** (sections 3–4).
- **Published JS only:** All **replayt** calls **must** use **documented public** browser/JS entry points (same boundary
  as [Upstream boundary](../DESIGN_PRINCIPLES.md#one-way-to-do-it-canonical-patterns)—no minified private hooks). The file
  **must** list **exact symbols** used (e.g. `window.replayt.…`) in a header or comment block and tie them to **replayt**
  docs or release notes where possible.
- **Graceful degradation:** If init fails or `events` is empty, show a **user-visible** message (not only `console.error`).

### Throttling and coalescing (normative)

- **During scrub:** High-frequency input (pointer move, `input` events) **must** be **throttled or debounced** before
  calling seek APIs (e.g. `requestAnimationFrame`, debounced handler, or documented “at most N seeks per second”
  strategy). Document the chosen approach in comments so integrators can tune it.
- **End of gesture:** On **pointer up** / **change** (commit), **must** perform a **final** seek to the committed value
  so the player ends on the operator’s chosen frame.

### Limitations and CDN builds (normative)

- Include a visible **“Limitations”** short note (prose in the page or comment visible in “view source”) stating that
  **some CDN builds may omit or rename seek/event APIs**; integrators should **pin** a **replayt** version whose **JS**
  surface matches the snippet and **upgrade** if methods are missing. Align the **`<script src=…replayt@…>`** pin with
  [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins).

### replayt pin and file placement

- **CDN / npm pin** in the shipped HTML **must** satisfy **`pyproject.toml`** **replayt** PEP 508 range (enforced by
  **`tests/test_docs_examples_replayt_pins.py`** once the file exists).

### Builder acceptance checklist (implementation)

**P-03** is **Shipped**; the original delivery met the items below. Use the same markers when you change this pattern:

1. **`docs/examples/timeline-scrubber.html`** (or approved alternate per [Delivery shape](#delivery-shape-normative))
   implements the normative sections above.
2. [Pattern inventory](#pattern-inventory) lists **P-03** as **Shipped** with the correct filename.
3. **`tests/test_examples.py`** includes file presence and **light contract markers** aligned with this spec
   (ordering comment block, throttling note, limitations note, scrub control, **replayt** script pin)—mirror the **P-02**
   approach; full browser automation remains optional per [Showcase stack matrix](../DESIGN_PRINCIPLES.md#showcase-stack-matrix).
4. **CHANGELOG** **Unreleased** records notable example or contract changes; note pattern count / mission tracking when the inventory changes.

**Automated checks today:** **`tests/test_docs_examples_replayt_pins.py`**; **`tests/test_examples.py`** markers for **P-03**.

---

## Backlog traceability: Timeline scrubber strip example (replayt public events API)

| Backlog acceptance criterion | Where specified |
| ---------------------------- | ---------------- |
| New example or clearly separated section | [Delivery shape](#delivery-shape-normative) |
| Seek/scrub interactions | [Scrub / seek interactions](#scrub--seek-interactions-normative) |
| Documented event ordering assumptions | [`sessionData` and events](#sessiondata-and-events-normative) |
| Throttling / coalescing | [Throttling and coalescing](#throttling-and-coalescing-normative) |
| Published replayt JS surface only | [Scrub / seek interactions](#scrub--seek-interactions-normative) |
| Short limitations note if CDN lacks API | [Limitations and CDN builds](#limitations-and-cdn-builds-normative) |
| **replayt** pin in range | [replayt pin and file placement](#replayt-pin-and-file-placement) |
| Progress toward **5+** patterns | [Pattern inventory](#pattern-inventory), [Mission](../MISSION.md#pattern-coverage-tracking) |

---

## P-04 Embed container states (empty, loading, failure, recovery)

### User story

As an **operator** or **integrator**, I want the **replay player embed container** (the DOM subtree passed to
`replayt.player.init` as `container`, per **P-01**) to have **predictable UX** while `sessionData` is **not yet**
available, when **fetch fails**, and when **init or data** fails after load— including **skeleton** affordances,
**retry**, and **accessible status announcements**—without relying on **undocumented** replayt internals.

### Relationship to P-01 and P-02

- **P-01** ([`basic-player.html`](basic-player.html)) shows a minimal init with inline `sessionData`. It does **not**
  yet normatively define loading/error/retry for the **embed container** itself; **P-04** is the dedicated contract for
  that job.
- **P-02** defines loading/error for the **metadata bar** and “at least one of bar or player must make loading obvious.”
  **P-04** tightens the **player/embed** side: even when no metadata bar exists, the **container** must communicate
  **loading**, **failure**, and **recovery** per below.
- **P-04** may ship as **`docs/examples/embed-container-states.html`** or as a **clearly delimited** section inside
  **`basic-player.html`** (same rules as **P-03** [Delivery shape](#delivery-shape-normative): if merged into **P-01**,
  update this inventory row to point at the anchor file and keep acceptance criteria in one place).

### P-04 async sessionData acquisition (normative)

- The example **must** model **async** acquisition of `sessionData` (e.g. `fetch` to a placeholder URL or a **documented**
  `setTimeout` fake loader)—**no** suggestion that operators should call private replayt HTTP helpers not described in
  **published** replayt docs.
- **Empty vs not-yet-loaded:** Before the async source resolves, the UI **must not** look like a **successful** session
  with zero events unless the snippet explicitly demonstrates **“loaded empty”** as a **distinct** labeled state from
  **“still loading.”**
- **On success:** Pass the resolved object to **`replayt.player.init`** (or the **documented** equivalent public entry
  for the pinned version) using only **published** JS symbols; list those symbols in a header or comment block (same
  boundary as **P-03**).

### P-04 embed skeleton and loading (normative)

- While `sessionData` is **in flight**, the **embed container** (or a dedicated child **wrapper** that fills the same
  visual box as the player) **must** show **skeleton UI**: non-empty placeholder **structure** (e.g. muted blocks,
  shimmer optional) and **visible text** such as “Loading replay…”—not a blank white box.
- **Automation / design handoff:** Include a short comment that **operators** and **automation agents** should treat the
  loading placeholder as **non-final** UI (stable **hook** optional: e.g. `data-demo-state="loading"` on the wrapper—
  not required unless the Builder documents it as the scrape contract).

### P-04 embed failure surface (normative)

- If **fetch** fails (network / non-OK HTTP) or **`replayt.player.init`** throws / rejects per the snippet’s error
  handling, the embed region **must** show a **user-visible** error message (not only `console.error`).
- The copy **must** distinguish **network/load failure** from **invalid payload** when both are demonstrated (can be
  two separate demo buttons or commented alternate code paths).

### P-04 retry affordance (normative)

- After a **recoverable** failure (at minimum: **failed fetch**), the snippet **must** expose a **keyboard-focusable**
  control (e.g. `<button type="button">`) labeled for **retry** (e.g. “Retry”) that **re-runs** the load path.
- **Tab order:** Retry control **must** appear in **logical** order (typically **before** any secondary chrome that is
  disabled while broken)—document intent in a comment block for handoff.
- Broader **keyboard / focus** checklist (toolbar vs player, **Escape**): **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)**.

### P-04 status live region (normative)

- The snippet **must** include an element with **`role="status"`** (preferred) or equivalent **`aria-live="polite"`**
  region dedicated to **high-level phase changes**: at least **loading**, **ready** (or **playing** / **initialized**),
  and **failed** (exact strings are implementation-defined but **must** be listed in-snippet as the **announcement
  contract**).
- **Polite** by default; use **`assertive`** only if the snippet documents **why** (e.g. synchronous fatal error)—avoid
  noisy announcements on every micro-interaction.
- **Audience — automation agents ([`DESIGN_PRINCIPLES.md`](../DESIGN_PRINCIPLES.md#audience)):** Document that LLM/CI
  scrapers may rely on **this live region’s text** (or the optional `data-demo-state` hook) **only** as described in
  the file’s comment block—do not invent parallel hidden channels.

### P-04 replayt pin and file placement

- Planned primary file: **`docs/examples/embed-container-states.html`**. **replayt** script URL **must** satisfy
  [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins).
- **No private APIs:** All replayt usage **must** match **published** player/init docs for the pinned version; if the
  snippet checks for optional APIs, document **graceful** fallback (message + retry or doc link)—not deep object
  probing of minified internals.

### Builder acceptance checklist (implementation)

**P-04** is **Shipped**; delivery met the items below. Keep **PATTERNS.md**, **MISSION**, **CHANGELOG**, and pin tests aligned when this pattern changes.

1. **`docs/examples/embed-container-states.html`** implements the normative sections above (new file per [Relationship to P-01 and P-02](#relationship-to-p-01-and-p-02)).
2. [Pattern inventory](#pattern-inventory) lists **P-04** as **Shipped** with the correct filename.
3. **[`docs/demo.md`](../demo.md#cross-surface-operator-story-console-demo-and-web-embed)** stays aligned with the
   shipped **operator story** table (same vocabulary: loading / failure / retry / ready).
4. **CHANGELOG** **Unreleased** records the example; **`docs/MISSION.md`** pattern count includes **P-04** as a **fourth**
   shipped vanilla file.
5. **`tests/test_docs_examples_replayt_pins.py`** scans the new **`*.html`**. **`tests/test_examples.py`** includes file presence and light contract markers (loading copy, live region, **Retry**, tab-order comment, **replayt** script pin).

**Automated checks today:** **`tests/test_docs_examples_replayt_pins.py`**; **`tests/test_examples.py`** markers for **P-04**.

---

## Backlog traceability: Empty, loading, and failure states for the embed container

| Backlog acceptance criterion | Where specified |
| ---------------------------- | --------------- |
| Skeleton / loading UX for embed container | [P-04 embed skeleton and loading](#p-04-embed-skeleton-and-loading-normative) |
| User-visible failure + distinguish load vs validation where applicable | [P-04 embed failure surface](#p-04-embed-failure-surface-normative) |
| Retry affordance (focusable) | [P-04 retry affordance](#p-04-retry-affordance-normative) |
| Accessible announcements (`role="status"` / `aria-live`) | [P-04 status live region](#p-04-status-live-region-normative) |
| **Automation agents** + operators: documented scrape/announcement contract | [P-04 status live region](#p-04-status-live-region-normative), [P-04 embed skeleton and loading](#p-04-embed-skeleton-and-loading-normative) |
| **Published** replayt JS only | [P-04 async sessionData acquisition](#p-04-async-sessiondata-acquisition-normative), [P-04 replayt pin and file placement](#p-04-replayt-pin-and-file-placement) |
| Same operator story as **console** demo doc | **[`docs/demo.md`](../demo.md#cross-surface-operator-story-console-demo-and-web-embed)** |
| Pattern inventory + mission trajectory | [Pattern inventory](#pattern-inventory), [Mission](../MISSION.md#pattern-coverage-tracking) |

---

## P-05 Offline deterministic fixture page for LLM and reviewer workflows

### User story

As a **reviewer** or **automation agent**, I want a **single vanilla HTML** file that renders a replay using **only**
inlined, synthetic **`sessionData`** (no API or `fetch` for the session payload), aligned with
**[LLM boundaries](../DESIGN_PRINCIPLES.md#llm-boundaries)**, so local opens and harness runs are **predictable** and
**secret-free**.

### Relationship to P-01 and P-04

- **P-01** ([`basic-player.html`](basic-player.html)) may mention fetching real **`sessionData`** from a backend. **P-05**
  is the **dedicated** pattern for the **opposite** job: **fixture** data lives **entirely in the document** (or in
  **static** literals the script assigns without I/O).
- **P-04** models **async** acquisition (including simulated `fetch`). **P-05** **must not** use that acquisition story
  for **`sessionData`**—no staged “loading” that resolves from the network for the payload. A **minimal** “ready” UI is
  allowed once **`sessionData`** is a constant and **`replayt.player.init`** (or equivalent public API) has run.

### P-05 sessionData and offline boundary (normative)

- **`sessionData` source:** The object passed to **`replayt.player.init`** (or the **documented** public equivalent for
  the pinned **replayt** JS version) **must** originate from an **inline** JavaScript literal or **static** assignment in
  the same file (or a **non-network** embedding pattern documented in-snippet, e.g. a `const` assembled only from fixed
  primitives—**not** loaded from another URL).
- **Forbidden for session payloads:** `fetch`, **`XMLHttpRequest`**, **`WebSocket`**, **`EventSource`**, **`import()`** to
  remote modules, or any other runtime I/O whose purpose is to obtain or mutate **`sessionData`** from a **network** or
  **environment-specific** source.
- **Allowed:** One **pinned** **replayt** browser bundle via **`<script src="…">`** (same **CDN** / semver story as
  **P-01**–**P-04** and [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins)). That script load is **not** a **session** fetch; it is the **player** dependency. Optional future work (separate backlog) may vendor the bundle for air-gapped workflows; this spec does **not** require it for **Shipped**.

### P-05 forbidden behaviors (normative)

- **No secrets:** No API keys, bearer tokens, signed URLs with secrets, private hostnames tied to credentials, or
  **`import.meta.env`** / **`process.env`**-style reads that could pull real credentials into the page.
- **No live model calls:** No `fetch` or SDK calls to hosted **LLM** / inference endpoints, telemetry that sends session
  content off-device, or **replayt** workflow runners that invoke non-deterministic models **from this file**.
- **No non-reproducible model paths:** Do not embed or call helpers whose **default** behavior is stochastic or
  time-dependent **model** output (contrast with fixed **`MockLLMClient`** narratives elsewhere—**P-05** stays **static
  replay** only unless this spec is revised).

### P-05 determinism (normative)

- **`sessionData`:** Use **fixed** timestamps, ids, and event payloads (e.g. numeric literals, fixed strings). **Do not**
  use `Date.now()`, `new Date()`, `Math.random()`, or environment-derived values **inside `sessionData`** or in
  **harness-scraped** visible strings that are meant to be stable across runs.
- **Comments:** The file **must** include a short **header comment** stating that the page is a **deterministic fixture**
  for reviewers and agents and that **`sessionData`** is **synthetic** and **stable**.

### P-05 replayt pin and open instructions (normative)

- **Primary path:** **`docs/examples/fixture-replay.html`**. If renamed, update this inventory row, **CHANGELOG**
  **Unreleased**, and cross-links in **`README.md`** / **`docs/REPLAYT_ECOSYSTEM_IDEA.md`** in the same change set.
- **Pin:** **`<script src=…>`** **must** satisfy [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins) (**`tests/test_docs_examples_replayt_pins.py`** once the file exists).
- **Local open (documentation, not code):** **`README.md`** and **`docs/REPLAYT_ECOSYSTEM_IDEA.md`** **must** tell reviewers
  and harness authors to open the page via a **local static server** rooted sensibly (e.g. from the repo: `cd docs/examples`
  then `python -m http.server`, then browse to `/fixture-replay.html`) so the **CDN** **replayt** script can load under
  typical browser **mixed-content / file URL** rules. **Optional:** note that **`file://`** may fail to load **CDN**
  scripts in some browsers—do not claim **fully air-gapped** behavior unless a **vendored** script path is also shipped
  (future backlog).

### Builder acceptance checklist (implementation)

**P-05** is **Shipped**; delivery met the items below. Keep **PATTERNS.md**, **MISSION**, **CHANGELOG**, and pin tests aligned when this pattern changes.

1. **`docs/examples/fixture-replay.html`** implements the normative sections above.
2. [Pattern inventory](#pattern-inventory) lists **P-05** as **Shipped** with the correct filename.
3. **`README.md`** and **`docs/REPLAYT_ECOSYSTEM_IDEA.md`** include **local open** instructions (static server under **`docs/examples/`**).
4. **CHANGELOG** **Unreleased** records the example; **[`docs/MISSION.md`](../MISSION.md#pattern-coverage-tracking)**
   pattern table reflects **5** shipped vanilla patterns.
5. **`tests/test_docs_examples_replayt_pins.py`** scans the **`*.html`**. **`tests/test_examples.py`** includes file presence and light **P-05** contract markers (determinism header, no session **`fetch(`**, **replayt** script pin).

**Automated checks today:** **`tests/test_docs_examples_replayt_pins.py`**; **`tests/test_examples.py`** markers for **P-05**.

---

## Backlog traceability: Offline deterministic fixture page for LLM and reviewer workflows

| Backlog acceptance criterion | Where specified |
| ---------------------------- | ---------------- |
| Inlined synthetic **`sessionData`**, no session over the wire | [P-05 sessionData and offline boundary](#p-05-sessiondata-and-offline-boundary-normative) |
| **No secrets**; **no** live / stochastic model usage in this path | [P-05 forbidden behaviors](#p-05-forbidden-behaviors-normative), [LLM boundaries](../DESIGN_PRINCIPLES.md#llm-boundaries) |
| **Deterministic** fixture | [P-05 determinism](#p-05-determinism-normative) |
| **replayt** pin + local open docs | [P-05 replayt pin and open instructions](#p-05-replayt-pin-and-open-instructions-normative), **`README.md`**, **`docs/REPLAYT_ECOSYSTEM_IDEA.md`** |
| Traceability in design principles | [Offline deterministic fixture page](../DESIGN_PRINCIPLES.md#offline-deterministic-fixture-page-for-llm-and-reviewer-workflows) |
---

## P-06 — React timeline player (basic-player + scrubber parity)

### User story

As a **React** integrator, I want a **self-contained** example under **`docs/examples/react/`** that embeds the replayt
player with a **timeline scrubber**, using the **same** `sessionData` root shape and **published** **`window.replayt`**
consumer APIs as **[`basic-player.html`](basic-player.html)**, with **copy-paste**-friendly layout, **pin** guidance for
**replayt** (npm and/or CDN), and optional **local preview** notes (**Vite** preferred; **esbuild** alternative prose
allowed) — **without** implying this repository publishes a **React** or **showcase** package to npm.

### Relationship to P-01 and P-03

- **P-01** defines the **minimal** embed: `sessionData` with `events` + `metadata`, `replayt.player.init({ container, data, theme })`, theme note, and links to the shared a11y checklist. **P-06** **must** keep that **init** contract and data root; React-specific wiring (e.g. `useRef` for `container`) is an implementation detail.
- **P-03** defines **timeline** behavior: scrub control, defensive ordering of `events`, **throttling** / final seek on commit, **limitations** note for CDN builds, and **tab order** (scrub before player when both are focusable). **P-06** **must** meet the same **normative intent** in React (hooks/effects/components), citing **P-03** in comments where behavior is mirrored.

### `sessionData` and event shapes (normative)

- **Root shape:** Same as **P-01**: an object with **`events`** (array) and **`metadata`** (object). Use the same field names illustrated in [`basic-player.html`](basic-player.html) (`metadata.startTs`, `metadata.viewport.width` / `height`) unless the Builder documents an **additive** extension; do **not** invent a parallel schema.
- **Event payloads:** Event objects should be **compatible** with the **schema-level** story in **[`docs/demo.md`](../demo.md#replayt-primitives-usage)** and **replayt** docs for the pinned version (types such as `click`, `scroll`, `keypress`, etc.). The shipped snippet should include **enough non-empty `events`** to exercise the scrubber (not an empty array as the only shipped state).
- **Synthetic vs live:** A **static** literal in source (recommended for copy-paste stability) or a clearly marked placeholder for `fetch` is acceptable; if the snippet uses **`fetch`**, it **must** remain a **documented** public HTTP pattern (no private replayt endpoints), consistent with **P-04** spirit for errors (user-visible failure path documented in README or in-app).

### replayt JavaScript surface (normative)

- **Published consumer API only:** All replayt calls **must** use **documented public** browser entry points — same boundary as **P-03** (e.g. `window.replayt.player.init`, optional seek helpers such as `seekToMs` / `goto` on the object returned from `init` if present). List **exact symbols** used in a file header or top-of-module comment block.
- **No Python / no showcase package imports:** The example is **front-end** only; it does **not** import `replayt_ux_showcase` or assume this repo is installed as a **Python** package for the snippet to run.

### React and tooling (normative)

- **React:** Target **React 18** (`react` / `react-dom` ^18) — aligns with [Showcase stack matrix](../DESIGN_PRINCIPLES.md#showcase-stack-matrix).
- **Bundler:** **Preferred** delivery: **Vite** (`npm create vite@latest` style) with a short README path: install, `npm run dev`, expected URL. **Allowed:** a concise **esbuild** (or similar) subsection in **`docs/examples/react/README.md`** for integrators who skip Vite.
- **Script loading:** Either (a) **pinned** **CDN** `<script>` in **`index.html`** that loads **`replayt`**’s browser bundle before the app bundle, or (b) **npm** dependency on **`replayt`** and import from the package path documented by **replayt** for the pinned version. Any **explicit** **replayt** version in **`docs/examples/react/*.{html,md}`** must satisfy [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins) (**`tests/test_docs_examples_replayt_pins.py`** once files exist).
- **Repository boundary:** Files live only under **`docs/examples/react/`** (plus cross-links from **README** / this catalog). Do **not** add a second canonical snippet tree at the repo root; optional root **`package.json`** remains the **maintainer** bundler recipe per **[`build.md`](build.md)**, not a substitute for **`react/`**.

### P-06 README and folder layout (normative)

- **`docs/examples/react/README.md`** (Builder **must** add when moving **P-06** to **Shipped**):
  - **Copy-paste** orientation: what to copy into an existing app vs run as a standalone mini-project.
  - **Version pins:** **replayt** semver (npm and/or CDN) **inside** the PEP 508 band in **`pyproject.toml`**; **React 18** range; link to **[`docs/FRONTEND_SUPPLY_CHAIN.md`](../FRONTEND_SUPPLY_CHAIN.md)** for CDN vs bundled tradeoffs.
  - **Runbook:** `npm install`, `npm run dev` (or equivalent), and any prerequisite (**Node** version) in one place.
  - **Non-goal:** State explicitly that this folder is **not** a published npm package from this repository.
- **Source files:** At minimum, one **React** module (or **JSX**/**TSX** if the Builder chooses TypeScript) that mounts the player and implements the timeline; **`index.html`** + small entry (**`main.jsx`**) acceptable. Exact filenames are a **Builder** choice; update the [Pattern inventory](#pattern-inventory) row if the primary entry differs from “see README.”

### Accessibility and keyboard (normative)

- Follow **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)** — scrubber keys, focus visibility, **Escape** where overlays exist, tab order consistent with **P-03** (scrub control before player focusables when both exist).
- Include a short **handoff comment** (JSX comment or README bullet) describing **tab order** intent.

### Limitations note (normative)

- Include the same **class** of **CDN / build limitations** callout as **P-03** (visible copy or view-source comment): some builds may omit or rename seek APIs; integrators should **pin** a **replayt** version whose JS matches the snippet.

### Builder acceptance checklist (implementation)

**P-06** is **Shipped**; delivery met the items below. Keep **PATTERNS.md**, **MISSION**, **CHANGELOG**, pin tests, and **`tests/test_examples.py`** aligned when this pattern changes.

1. **`docs/examples/react/`** exists with **`README.md`** meeting [P-06 README and folder layout](#p-06-readme-and-folder-layout-normative).
2. React source implements **`sessionData`** + **`replayt.player.init`** per [Relationship to P-01 and P-03](#relationship-to-p-01-and-p-03) and timeline behavior per **P-03** intent.
3. [Pattern inventory](#pattern-inventory) lists **P-06** as **Shipped** with the correct paths.
4. **`tests/test_docs_examples_replayt_pins.py`** scans **`*.html`**, **`*.md`** under **`docs/examples/react/`**; **`tests/test_examples.py`** includes file-presence and light **P-06** contract markers.
5. **CHANGELOG** **Unreleased** records the example; **[`docs/MISSION.md`](../MISSION.md#pattern-coverage-tracking)** framework row is **Shipped**.
6. **[`README.md`](../../README.md)** project layout mentions **`docs/examples/react/`** as **Shipped**.

**Automated checks today:** **`tests/test_docs_examples_replayt_pins.py`**; **`tests/test_examples.py`** markers for **P-06**.

---

## Backlog traceability: Ship React timeline player snippet under docs/examples/react/

| Backlog acceptance criterion | Where specified |
| ---------------------------- | ---------------- |
| Self-contained **React** example under **`docs/examples/react/`** | [P-06 README and folder layout](#p-06-readme-and-folder-layout-normative), [React and tooling](#react-and-tooling-normative) |
| **Vite** or **esbuild** notes | [React and tooling](#react-and-tooling-normative) |
| Mirrors **basic-player** `sessionData` + **`replayt.player.init`** | [Relationship to P-01 and P-03](#relationship-to-p-01-and-p-03), [`sessionData` and event shapes](#sessiondata-and-event-shapes-normative) |
| Timeline / scrub UX aligned with **P-03** | [Relationship to P-01 and P-03](#relationship-to-p-01-and-p-03), [Limitations note](#limitations-note-normative) |
| **Published** replayt JS only | [replayt JavaScript surface](#replayt-javascript-surface-normative) |
| README: copy-paste + **version pin** guidance | [P-06 README and folder layout](#p-06-readme-and-folder-layout-normative) |
| **Not** an npm-published showcase package | [React and tooling](#react-and-tooling-normative) |
| Shared **keyboard / focus** checklist | [Accessibility and keyboard](#accessibility-and-keyboard-normative) |
| Traceability in design principles | [Backlog traceability: Ship React timeline player snippet](../DESIGN_PRINCIPLES.md#backlog-traceability-ship-react-timeline-player-snippet) |
