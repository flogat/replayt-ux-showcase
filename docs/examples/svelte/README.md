# P-08 — Svelte 4 timeline player (copy-paste example)

Self-contained **Svelte 4** + **Vite** sample under `docs/examples/svelte/`. It matches **P-07** depth for the **Svelte**
stack: same **`sessionData`** / **`replayt.player.init`** contract as [`basic-player.html`](../basic-player.html) (P-01),
scrubber behavior aligned with [`timeline-scrubber.html`](../timeline-scrubber.html) (P-03) and **P-06** / **P-07**.

**Not an npm package:** this folder is documentation and sample source for integrators. The repository does not publish
a Svelte or showcase package to npm.

## Copy into your app

- **CDN + bundler:** Keep a pinned **replayt** player script in **`index.html`** before the Vite module entry (same
  pattern as this tree). Then copy **`src/App.svelte`** (and **`src/main.js`** if you align with Vite’s default mount).
- **Standalone:** Clone the files under `docs/examples/svelte/`, run **`npm install`** and **`npm run dev`** from this
  directory.

Replace **`SESSION_DATA`** in **`App.svelte`** with data from your backend, or wire **`fetch`** to a documented public
HTTP API. Pin **replayt** to a version whose browser bundle matches the symbols listed in the **`App.svelte`** header
comment.

## Version pins

| Surface | Pin (example) | Notes |
| ------- | ------------- | ----- |
| **replayt** (CDN) | `replayt@0.4.25` in **`index.html`** | Must stay inside the **`replayt`** range in the repo root **`pyproject.toml`** (currently `>=0.1.0,<0.5.0`). |
| **Svelte** | `svelte` **^4.2** in **`package.json`** | Svelte 4 per [Showcase stack matrix](../../DESIGN_PRINCIPLES.md#showcase-stack-matrix). |
| **Vite** | **^5.4** in this subtree | **@sveltejs/vite-plugin-svelte** **^3** tracks **Svelte 4**; **Vite** **6** is optional in a future pin pass if the plugin matrix allows. |

CDN vs **npm** bundling, optional **SRI**, and lockfile habits: **[`docs/FRONTEND_SUPPLY_CHAIN.md`](../FRONTEND_SUPPLY_CHAIN.md)**.

## Runbook

- **Node:** 18 or newer (see **`package.json`** **`engines`**).
- **Install:** `npm install`
- **Dev server:** `npm run dev` → open the URL Vite prints (default **http://127.0.0.1:5173**).
- **Production-shaped build:** `npm run build` then `npm run preview` to serve the **`dist/`** output locally.

Use a static server if you change the setup; **`file://`** may block the CDN script in some browsers.

## esbuild / Rollup (no Vite)

To bundle without Vite: use **esbuild** or **Rollup** with a Svelte plugin, load **`replayt`** from the same pinned CDN
**`script`** in your **`index.html`** before your bundle. **`docs/examples/build.md`** describes the maintainer **esbuild**
path at the repository root.

## Accessibility

Timeline and player keyboard expectations: **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)**.
