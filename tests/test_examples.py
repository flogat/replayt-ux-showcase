from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


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
