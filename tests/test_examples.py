import os
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]


def test_basic_player_html_exists():
    """Smoke test: vanilla example path from docs/DESIGN_PRINCIPLES.md."""
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
