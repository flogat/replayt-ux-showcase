# P-07 — Vue 3 timeline player (copy-paste example)

Self-contained **Vue 3** + **Vite** sample under `docs/examples/vue/`. It mirrors the vanilla
[`basic-player.html`](../basic-player.html) contract (`sessionData` with `events` + `metadata`, `replayt.player.init`)
and the timeline scrub intent from [`timeline-scrubber.html`](../timeline-scrubber.html) (P-03), aligned with the shipped
**P-06** React example.

**Not an npm package:** this folder is documentation and sample source for integrators. The repository does not publish
a Vue or showcase package to npm.

## Copy into your app

- **CDN + bundler:** Keep a pinned **replayt** player script in **`index.html`** before the Vite module entry (same
  pattern as this tree). Then copy **`src/App.vue`** (and **`src/main.js`** if you align with Vite’s default mount).
- **Standalone:** Clone the files under `docs/examples/vue/`, run **`npm install`** and **`npm run dev`** from this
  directory.

Replace **`SESSION_DATA`** in **`App.vue`** with data from your backend, or wire **`fetch`** to a documented public HTTP
API. Pin **replayt** to a version whose browser bundle matches the symbols listed in the **`App.vue`** header comment.

## Version pins

| Surface | Pin (example) | Notes |
| ------- | ------------- | ----- |
| **replayt** (CDN) | `replayt@0.4.25` in **`index.html`** | Must stay inside the **`replayt`** range in the repo root **`pyproject.toml`** (currently `>=0.1.0,<0.5.0`). |
| **Vue** | `vue` **^3.5** in **`package.json`** | Vue 3 per [Showcase stack matrix](../../DESIGN_PRINCIPLES.md#showcase-stack-matrix). |

CDN vs **npm** bundling, optional **SRI**, and lockfile habits: **[`docs/FRONTEND_SUPPLY_CHAIN.md`](../FRONTEND_SUPPLY_CHAIN.md)**.

## Runbook

- **Node:** 18 or newer (see **`package.json`** **`engines`**).
- **Install:** `npm install`
- **Dev server:** `npm run dev` → open the URL Vite prints (default **http://127.0.0.1:5173**).
- **Production-shaped build:** `npm run build` then `npm run preview` to serve the **`dist/`** output locally.

Use a static server if you change the setup; **`file://`** may block the CDN script in some browsers.

## esbuild / Rollup (no Vite)

To bundle without Vite: use **esbuild** or **Rollup** with a Vue plugin, load **`replayt`** from the same pinned CDN
**`script`** in your **`index.html`** before your bundle. The repository root **`package.json`** and
**`docs/examples/build.md`** describe a maintainer **esbuild** recipe for generic preview, not this Vue subtree.

## Accessibility

Timeline and player keyboard expectations: **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)**.
