# P-06 — React timeline player (copy-paste example)

Self-contained **React 18** + **Vite** sample under `docs/examples/react/`. It mirrors the vanilla
[`basic-player.html`](../basic-player.html) contract (`sessionData` with `events` + `metadata`, `replayt.player.init`)
and the timeline scrub intent from [`timeline-scrubber.html`](../timeline-scrubber.html) (P-03).

**Not an npm package:** this folder is documentation and sample source for integrators. The repository does not publish
a React or showcase package to npm.

## Copy into your app

- **CDN + bundler:** Keep a pinned **replayt** player script in **`index.html`** before the Vite module entry (same
  pattern as this tree). Then copy **`src/App.jsx`** (and **`src/main.jsx`** if you align with Vite’s default mount).
- **Standalone:** Clone the files under `docs/examples/react/`, run **`npm install`** and **`npm run dev`** from this
  directory.

Replace **`SESSION_DATA`** in **`App.jsx`** with data from your backend, or wire **`fetch`** to a documented public HTTP
API. Pin **replayt** to a version whose browser bundle matches the symbols listed in the **`App.jsx`** header comment.

## Version pins

| Surface | Pin (example) | Notes |
| ------- | ------------- | ----- |
| **replayt** (CDN) | `replayt@0.4.25` in **`index.html`** | Must stay inside the **`replayt`** range in the repo root **`pyproject.toml`** (currently `>=0.1.0,<0.5.0`). |
| **React** | `react` / `react-dom` **^18.3** in **`package.json`** | React 18 per [Showcase stack matrix](../../DESIGN_PRINCIPLES.md#showcase-stack-matrix). |

CDN vs **npm** bundling, optional **SRI**, and lockfile habits: **[`docs/FRONTEND_SUPPLY_CHAIN.md`](../FRONTEND_SUPPLY_CHAIN.md)**.

## Runbook

- **Node:** 18 or newer (see **`package.json`** **`engines`**).
- **Install:** `npm install`
- **Dev server:** `npm run dev` → open the URL Vite prints (default **http://127.0.0.1:5173**).
- **Production-shaped build:** `npm run build` then `npm run preview` to serve the **`dist/`** output locally.

Use a static server if you change the setup; **`file://`** may block the CDN script in some browsers.

## esbuild (no Vite)

To bundle without Vite: install **`esbuild`**, point an entry at **`src/main.jsx`**, externalize **`react`** /
**`react-dom`** or bundle them, and load **`replayt`** from the same pinned CDN **`script`** in your **`index.html`**
before your bundle. This repo’s maintainer **esbuild** recipe lives at the repository root and **`docs/examples/build.md`**;
it targets the generic bundler preview, not this React subtree.

## Accessibility

Timeline and player keyboard expectations: **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)**.
