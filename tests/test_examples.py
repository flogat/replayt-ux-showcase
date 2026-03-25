import os

def test_basic_player_html_exists():
    """Smoke test: verify initial demo file exists (added in phase 3)."""
    path = "docs/examples/basic-player.html"
    assert os.path.exists(path), f"Demo missing: {path}"
