import os


def test_basic_player_html_exists():
    """Smoke test: vanilla example path from docs/DESIGN_PRINCIPLES.md."""
    path = "docs/examples/basic-player.html"
    assert os.path.exists(path), f"Demo missing: {path}"
