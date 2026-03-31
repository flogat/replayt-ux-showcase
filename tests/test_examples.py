<<<<<<< HEAD
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

_KEYBOARD_MODEL_DOC = REPO_ROOT / "docs/a11y/keyboard-model.md"
=======
import os
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
>>>>>>> origin/mc/backlog-b7eb5287


def test_basic_player_html_exists():
    """Smoke test: vanilla example path from docs/DESIGN_PRINCIPLES.md."""
<<<<<<< HEAD
    path = REPO_ROOT / "docs/examples/basic-player.html"
    assert path.is_file(), f"Demo missing: {path}"


def test_basic_player_tailwind_html_exists():
    """P-11 example ships under docs/examples/ (see docs/examples/PATTERNS.md)."""
    path = REPO_ROOT / "docs/examples/basic-player-tailwind.html"
    assert path.is_file(), f"P-11 demo missing: {path}"


def test_basic_player_tailwind_contract_markers():
    """P-11 keeps the shipped Tailwind story explicit: same teaching points as P-01 plus both scan-path cases."""
    text = (REPO_ROOT / "docs/examples/basic-player-tailwind.html").read_text(
        encoding="utf-8"
    )
    assert "P-11:" in text
    assert "cdn.tailwindcss.com" in text
    assert "tailwind.config" in text
    assert "@source" in text
    assert '"./docs/examples/basic-player-tailwind.html"' in text
    assert '"./src/**/*.{html,js,ts,jsx,tsx}"' in text
    assert "--content" in text
    assert "no safelist required for this snippet" in text
    assert "rux-showcase-session-fixture" in text
    assert "adaptConsoleSessionToReplaytMs" in text
    assert "replayt.player.init" in text
    assert 'href="SESSION_SCHEMA.md"' in text
    assert 'href="../playbook/tokens.md"' in text
    assert 'href="../a11y/keyboard-model.md"' in text
    assert "same object as <code>replayt_ux_showcase.demo.SAMPLE_SESSION_DATA</code>" in text
    assert "often expects ms timestamps and camelCase metadata" in text
    assert "wired to <code>--replayt-primary</code> for the player" in text
    assert "Add timeline scrubber via replayt events API." in text
    assert "tab order, scrubber keys, Escape" in text
    assert "keyboard-model.md" in text
    assert "cdn.jsdelivr.net/npm/replayt@" in text


def test_player_session_metadata_bar_html_exists():
    """P-02 example ships under docs/examples/ (see docs/examples/PATTERNS.md)."""
    path = REPO_ROOT / "docs/examples/player-session-metadata-bar.html"
    assert path.is_file(), f"P-02 demo missing: {path}"


def test_player_session_metadata_bar_contract_markers():
    """Light contract: loading, validation, tab-order comment, replayt script pin (P-02 / PATTERNS.md)."""
    text = (REPO_ROOT / "docs/examples/player-session-metadata-bar.html").read_text(
        encoding="utf-8"
    )
    assert "Loading session…" in text
    assert "sessionId" in text
    assert "durationMs" in text
    assert "viewport" in text
    assert "validateChromeMetadata" in text
    assert "Tab order (handoff)" in text
    assert "focus-visible" in text
    assert "cdn.jsdelivr.net/npm/replayt@" in text


def test_timeline_scrubber_html_exists():
    """P-03 example ships under docs/examples/ (see docs/examples/PATTERNS.md)."""
    path = REPO_ROOT / "docs/examples/timeline-scrubber.html"
    assert path.is_file(), f"P-03 demo missing: {path}"


def test_timeline_scrubber_contract_markers():
    """Light contract: ordering handoff comment, rAF throttling, limitations, scrub id, tab-order comment, pin (P-03)."""
    text = (REPO_ROOT / "docs/examples/timeline-scrubber.html").read_text(
        encoding="utf-8"
    )
    assert "Event ordering (handoff):" in text
    assert "requestAnimationFrame" in text
    assert "Limitations" in text
    assert 'id="timeline-scrubber"' in text
    assert "Tab order (handoff):" in text
    assert "applySeekMs" in text
    assert "metadata.durationMs" in text
    assert "cdn.jsdelivr.net/npm/replayt@" in text


def test_embed_container_states_html_exists():
    """P-04 example ships under docs/examples/ (see docs/examples/PATTERNS.md)."""
    path = REPO_ROOT / "docs/examples/embed-container-states.html"
    assert path.is_file(), f"P-04 demo missing: {path}"


def test_embed_container_states_contract_markers():
    """Light contract: loading copy, status live region, Retry, tab-order comment, announcement contract, pin (P-04)."""
    text = (REPO_ROOT / "docs/examples/embed-container-states.html").read_text(
        encoding="utf-8"
    )
    assert "Loading replay…" in text
    assert 'role="status"' in text
    assert "aria-live=" in text
    assert "Retry</button>" in text
    assert "Tab order (handoff):" in text
    assert "Announcement contract (handoff):" in text
    assert "replayt.player.init" in text
    assert "data-demo-state" in text
    assert "cdn.jsdelivr.net/npm/replayt@" in text


def test_fixture_replay_html_exists():
    """P-05 example ships under docs/examples/ (see docs/examples/PATTERNS.md)."""
    path = REPO_ROOT / "docs/examples/fixture-replay.html"
    assert path.is_file(), f"P-05 demo missing: {path}"


def test_fixture_replay_contract_markers():
    """Light contract: deterministic fixture header, no session fetch(, stable literals story, pin (P-05)."""
    text = (REPO_ROOT / "docs/examples/fixture-replay.html").read_text(encoding="utf-8")
    assert "Deterministic offline fixture" in text
    assert "synthetic and stable" in text
    assert "fetch(" not in text
    assert "Date.now(" not in text
    assert "Math.random(" not in text
    assert "sessionData" in text
    assert "replayt.player.init" in text
    assert "cdn.jsdelivr.net/npm/replayt@" in text


def test_event_overlay_html_exists():
    """P-09 example ships under docs/examples/ (see docs/examples/PATTERNS.md)."""
    path = REPO_ROOT / "docs/examples/event-overlay.html"
    assert path.is_file(), f"P-09 demo missing: {path}"


def test_event_overlay_contract_markers():
    """Light contract: P-03-style scrub, overlay tab order, callout/Escape, no session fetch, pin (P-09)."""
    text = (REPO_ROOT / "docs/examples/event-overlay.html").read_text(encoding="utf-8")
    assert "Event ordering (handoff):" in text
    assert "requestAnimationFrame" in text
    assert "Limitations" in text
    assert 'id="event-overlay-scrubber"' in text
    assert "Tab order (handoff):" in text
    assert "applySeekMs" in text
    assert "focus return" in text
    assert "Escape" in text
    assert "active event" in text
    assert "callout" in text
    assert "fetch(" not in text
    assert "Date.now(" not in text
    assert "Math.random(" not in text
    assert "replayt.player.init" in text
    assert "metadata.durationMs" in text
    assert "keyboard-model.md" in text
    assert "cdn.jsdelivr.net/npm/replayt@" in text


def test_click_heatmap_canvas_html_exists():
    """P-10 example ships under docs/examples/ (see docs/examples/PATTERNS.md)."""
    path = REPO_ROOT / "docs/examples/click-heatmap-canvas.html"
    assert path.is_file(), f"P-10 demo missing: {path}"


def test_click_heatmap_canvas_contract_markers():
    """Light contract: binned heatmap handoff, viewport mapping, a11y, tab order, no session fetch (P-10)."""
    text = (REPO_ROOT / "docs/examples/click-heatmap-canvas.html").read_text(
        encoding="utf-8"
    )
    assert "Heatmap algorithm (design–engineering handoff):" in text
    assert "metadata.viewport" in text
    assert "2D histogram" in text
    assert "box blur" in text
    assert "Tab order (handoff):" in text
    assert 'role="img"' in text
    assert 'aria-labelledby="heatmap-title"' in text
    assert "keyboard-model.md" in text
    assert "focus-visible" in text
    assert "fetch(" not in text
    assert "Date.now(" not in text
    assert "Math.random(" not in text


def test_keyboard_model_doc_exists():
    """Shared a11y checklist ships (docs/DESIGN_PRINCIPLES.md traceability)."""
    assert _KEYBOARD_MODEL_DOC.is_file(), f"Missing {_KEYBOARD_MODEL_DOC}"


def test_keyboard_model_doc_core_sections():
    """Contract: tab order, roving lists, scrubber, Escape, focus visibility, Builder checklist."""
    text = _KEYBOARD_MODEL_DOC.read_text(encoding="utf-8")
    assert "## 1. Tab order" in text
    assert "## 2. Roving" in text
    assert "## 3. Scrubber" in text
    assert "## 4. `Escape`" in text
    assert "## 5. Focus visibility" in text
    assert "## 6. Builder acceptance checklist" in text


def test_examples_link_keyboard_model_checklist():
    """P-01–P-05, P-09–P-11 vanilla examples reference the shared keyboard/focus doc."""
    html_names = [
        "basic-player.html",
        "basic-player-tailwind.html",
        "player-session-metadata-bar.html",
        "timeline-scrubber.html",
        "embed-container-states.html",
        "fixture-replay.html",
        "event-overlay.html",
        "click-heatmap-canvas.html",
    ]
    needle = "keyboard-model.md"
    for name in html_names:
        path = REPO_ROOT / "docs/examples" / name
        text = path.read_text(encoding="utf-8")
        assert needle in text, f"{name} should reference {needle}"


def test_patterns_md_links_keyboard_model():
    """PATTERNS.md links the shared checklist from Related and per-pattern notes."""
    text = (REPO_ROOT / "docs/examples/PATTERNS.md").read_text(encoding="utf-8")
    assert "a11y/keyboard-model.md" in text


def test_react_timeline_player_p06_files_exist():
    """P-06 ships under docs/examples/react/ (see docs/examples/PATTERNS.md)."""
    base = REPO_ROOT / "docs/examples/react"
    for rel in (
        "README.md",
        "package.json",
        "index.html",
        "vite.config.js",
        "src/main.jsx",
        "src/App.jsx",
    ):
        path = base / rel
        assert path.is_file(), f"P-06 file missing: {path}"


def test_react_timeline_player_p06_contract_markers():
    """Light contract: P-03 parity strings, replayt init, tab order, limitations, scrub id, CDN pin (P-06)."""
    app = (REPO_ROOT / "docs/examples/react/src/App.jsx").read_text(encoding="utf-8")
    assert "Event ordering (P-03):" in app
    assert "requestAnimationFrame" in app
    assert "Limitations" in app
    assert 'id="timeline-scrubber-react"' in app
    assert "Tab order (handoff):" in app
    assert "applySeekMs" in app
    assert "durationMs" in app and "metadata" in app
    assert "replayt.player.init" in app
    assert "SAMPLE_SESSION_DATA" in app
    assert "adaptConsoleSessionToReplaytMs" in app
    assert "start_ts" in app
    assert "ts: 1.0" in app
    assert "duration: 30.0" in app
    idx = (REPO_ROOT / "docs/examples/react/index.html").read_text(encoding="utf-8")
    assert "cdn.jsdelivr.net/npm/replayt@" in idx


def test_p06_react_sample_session_literals_match_demo_module():
    """P-06 console parity: App.jsx event types and metadata match replayt_ux_showcase.demo.SAMPLE_SESSION_DATA."""
    from replayt_ux_showcase.demo import SAMPLE_SESSION_DATA

    app = (REPO_ROOT / "docs/examples/react/src/App.jsx").read_text(encoding="utf-8")
    for ev in SAMPLE_SESSION_DATA["events"]:
        assert f'type: "{ev["type"]}"' in app
    meta = SAMPLE_SESSION_DATA["metadata"]
    assert meta["duration"] == 30.0
    assert meta["start_ts"] == 0.0
    assert "30.0" in app
    w, h = meta["viewport"]["w"], meta["viewport"]["h"]
    assert f"w: {w}" in app and f"h: {h}" in app


def test_react_timeline_player_readme_private_and_runbook():
    """README states non-goal and documents install + dev server (P-06)."""
    text = (REPO_ROOT / "docs/examples/react/README.md").read_text(encoding="utf-8")
    assert "Not an npm package" in text or "not published" in text.lower()
    assert "npm install" in text
    assert "npm run dev" in text
    assert "FRONTEND_SUPPLY_CHAIN.md" in text


def test_p06_react_links_keyboard_model():
    """P-06 subtree references the shared keyboard / focus checklist."""
    readme = (REPO_ROOT / "docs/examples/react/README.md").read_text(encoding="utf-8")
    app = (REPO_ROOT / "docs/examples/react/src/App.jsx").read_text(encoding="utf-8")
    needle = "keyboard-model.md"
    assert needle in readme, "react/README.md should link keyboard-model.md"
    assert needle in app, "react/src/App.jsx should link keyboard-model.md"


def test_vue_timeline_player_p07_files_exist():
    """P-07 ships under docs/examples/vue/ (see docs/examples/PATTERNS.md)."""
    base = REPO_ROOT / "docs/examples/vue"
    for rel in (
        "README.md",
        "package.json",
        "index.html",
        "vite.config.js",
        "src/main.js",
        "src/App.vue",
    ):
        path = base / rel
        assert path.is_file(), f"P-07 file missing: {path}"


def test_vue_timeline_player_p07_contract_markers():
    """Light contract: P-03 parity strings, replayt init, tab order, limitations, scrub id, CDN pin (P-07)."""
    app = (REPO_ROOT / "docs/examples/vue/src/App.vue").read_text(encoding="utf-8")
    assert "Event ordering (P-03):" in app
    assert "requestAnimationFrame" in app
    assert "Limitations" in app
    assert 'id="timeline-scrubber-vue"' in app
    assert "Tab order (handoff):" in app
    assert "applySeekMs" in app
    assert "durationMs" in app and "metadata" in app
    assert "replayt.player.init" in app
    idx = (REPO_ROOT / "docs/examples/vue/index.html").read_text(encoding="utf-8")
    assert "cdn.jsdelivr.net/npm/replayt@" in idx


def test_vue_timeline_player_readme_private_and_runbook():
    """README states non-goal and documents install + dev server (P-07)."""
    text = (REPO_ROOT / "docs/examples/vue/README.md").read_text(encoding="utf-8")
    assert "Not an npm package" in text or "not published" in text.lower()
    assert "npm install" in text
    assert "npm run dev" in text
    assert "npm run build" in text
    assert "FRONTEND_SUPPLY_CHAIN.md" in text


def test_p07_vue_links_keyboard_model():
    """P-07 subtree references the shared keyboard / focus checklist."""
    readme = (REPO_ROOT / "docs/examples/vue/README.md").read_text(encoding="utf-8")
    app = (REPO_ROOT / "docs/examples/vue/src/App.vue").read_text(encoding="utf-8")
    needle = "keyboard-model.md"
    assert needle in readme, "vue/README.md should link keyboard-model.md"
    assert needle in app, "vue/src/App.vue should link keyboard-model.md"


def test_svelte_timeline_player_p08_files_exist():
    """P-08 ships under docs/examples/svelte/ (see docs/examples/PATTERNS.md)."""
    base = REPO_ROOT / "docs/examples/svelte"
    for rel in (
        "README.md",
        "package.json",
        "index.html",
        "vite.config.js",
        "svelte.config.js",
        "src/main.js",
        "src/App.svelte",
    ):
        path = base / rel
        assert path.is_file(), f"P-08 file missing: {path}"


def test_svelte_timeline_player_p08_contract_markers():
    """Light contract: P-03 parity strings, replayt init, tab order, limitations, scrub id, CDN pin (P-08)."""
    app = (REPO_ROOT / "docs/examples/svelte/src/App.svelte").read_text(
        encoding="utf-8"
    )
    assert "Event ordering (P-03):" in app
    assert "requestAnimationFrame" in app
    assert "Limitations" in app
    assert 'id="timeline-scrubber-svelte"' in app
    assert "Tab order (handoff):" in app
    assert "applySeekMs" in app
    assert "durationMs" in app and "metadata" in app
    assert "replayt.player.init" in app
    idx = (REPO_ROOT / "docs/examples/svelte/index.html").read_text(encoding="utf-8")
    assert "cdn.jsdelivr.net/npm/replayt@" in idx


def test_svelte_timeline_player_readme_private_and_runbook():
    """README states non-goal and documents install + dev server (P-08)."""
    text = (REPO_ROOT / "docs/examples/svelte/README.md").read_text(encoding="utf-8")
    assert "Not an npm package" in text or "not published" in text.lower()
    assert "npm install" in text
    assert "npm run dev" in text
    assert "npm run build" in text
    assert "FRONTEND_SUPPLY_CHAIN.md" in text


def test_p08_svelte_links_keyboard_model():
    """P-08 subtree references the shared keyboard / focus checklist."""
    readme = (REPO_ROOT / "docs/examples/svelte/README.md").read_text(encoding="utf-8")
    app = (REPO_ROOT / "docs/examples/svelte/src/App.svelte").read_text(
        encoding="utf-8"
    )
    needle = "keyboard-model.md"
    assert needle in readme, "svelte/README.md should link keyboard-model.md"
    assert needle in app, "svelte/src/App.svelte should link keyboard-model.md"
=======
    path = "docs/examples/basic-player.html"
    assert os.path.exists(path), f"Demo missing: {path}"


def test_tailwind_player_html_exists():
    """Smoke test: Tailwind example from DESIGN_PRINCIPLES showcase stack + backlog traceability."""
    path = "docs/examples/tailwind-player.html"
    assert os.path.exists(path), f"Demo missing: {path}"


def _read_example(name: str) -> str:
    return (_REPO_ROOT / "docs" / "examples" / name).read_text(encoding="utf-8")


def test_tailwind_player_matches_basic_player_contract():
    """Contract parity: sessionData shape and init hook align with basic-player.html (DESIGN_PRINCIPLES)."""
    basic = _read_example("basic-player.html")
    tailwind = _read_example("tailwind-player.html")

    contract_markers = [
        "https://cdn.jsdelivr.net/npm/replayt@0.1.0/dist/player.min.js",
        "const sessionData = {",
        "events: [],",
        "metadata: { startTs: Date.now(), viewport: { width: 1920, height: 1080 } }",
        "window.replayt?.player?.init({",
        "container: document.getElementById('player')",
        "data: sessionData,",
        "theme: 'light'",
    ]
    for needle in contract_markers:
        assert needle in basic, f"basic-player.html missing contract fragment: {needle!r}"
        assert needle in tailwind, f"tailwind-player.html missing contract fragment: {needle!r}"

    assert 'id="player"' in tailwind
    assert "cdn.tailwindcss.com" in tailwind
    assert "--replayt-primary" in tailwind
    assert "not a published" in tailwind.lower() or "not an npm package" in tailwind.lower()
>>>>>>> origin/mc/backlog-b7eb5287
