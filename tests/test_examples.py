from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

_KEYBOARD_MODEL_DOC = REPO_ROOT / "docs/a11y/keyboard-model.md"


def test_basic_player_html_exists():
    """Smoke test: vanilla example path from docs/DESIGN_PRINCIPLES.md."""
    path = REPO_ROOT / "docs/examples/basic-player.html"
    assert path.is_file(), f"Demo missing: {path}"


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
    """P-01–P-05 vanilla examples reference the shared keyboard/focus doc."""
    html_names = [
        "basic-player.html",
        "player-session-metadata-bar.html",
        "timeline-scrubber.html",
        "embed-container-states.html",
        "fixture-replay.html",
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
