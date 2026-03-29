"""Tests for demo module per docs/demo.md test plan."""

import ast
import logging
import subprocess
import sys
from pathlib import Path

import pytest

from replayt_ux_showcase import SAMPLE_SESSION_DATA, render_console_timeline
from replayt_ux_showcase import demo as demo_module


REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO_PY = REPO_ROOT / "src" / "replayt_ux_showcase" / "demo.py"


def test_demo_runs():
    """Subprocess: python -m replayt_ux_showcase.demo exits 0."""
    result = subprocess.run(
        [sys.executable, "-m", "replayt_ux_showcase.demo"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Demo failed: {result.stderr}"


def test_exports():
    """Import check: render_console_timeline and SAMPLE_SESSION_DATA exported."""
    assert callable(render_console_timeline)
    assert isinstance(SAMPLE_SESSION_DATA, dict)
    events = SAMPLE_SESSION_DATA.get("events", [])
    assert 10 <= len(events) <= 15, f"Event count {len(events)} not in range(10, 16)"


def test_output_format():
    """Output contains expected log lines with [replayt-demo] prefix."""
    result = subprocess.run(
        [sys.executable, "-m", "replayt_ux_showcase.demo"],
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    assert "[replayt-demo]" in output
    assert "Rendering demo timeline" in output
    assert "Overlay teaching" in output
    assert "event-overlay.html" in output


def test_event_count():
    """Validate event count in sample data (10-15 events per spec)."""
    events = SAMPLE_SESSION_DATA.get("events", [])
    assert 10 <= len(events) <= 15, f"Expected 10-15 events, got {len(events)}"


def test_event_types():
    """Validate all event types are from the allowed set."""
    allowed = {"click", "scroll", "keypress", "resize", "mousemove"}
    events = SAMPLE_SESSION_DATA.get("events", [])
    for event in events:
        etype = event.get("type")
        assert etype in allowed, f"Event type '{etype}' not in allowed types: {allowed}"


def test_demo_logger_name_matches_spec():
    """docs/demo.md: logger name is replayt_ux_showcase.demo."""
    assert demo_module.logger.name == "replayt_ux_showcase.demo"


def test_demo_source_does_not_import_replayt_package():
    """Design principles: demo stays off private replayt imports; module is stdlib-only."""
    tree = ast.parse(DEMO_PY.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                assert root != "replayt", f"unexpected import: {alias.name!r}"
        elif isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".", 1)[0]
            assert root != "replayt", f"unexpected import from: {node.module!r}"


def test_render_console_timeline_in_process(caplog: pytest.LogCaptureFixture):
    """Exercise timeline rendering in-process for coverage (subprocess runs are not traced)."""
    caplog.set_level(logging.INFO, logger="replayt_ux_showcase.demo")
    render_console_timeline(SAMPLE_SESSION_DATA)
    joined = " ".join(r.message for r in caplog.records)
    assert "[replayt-demo] Rendering demo timeline" in joined
    assert "[replayt-demo] Processing" in joined
    assert "Timeline:" in joined
    assert "Overlay teaching" in joined
    assert "Events:" in joined


def test_overlay_teaching_when_no_event_before_scrub(caplog: pytest.LogCaptureFixture):
    """Branch: scrub snapshot before first event logs the empty-overlay message."""
    caplog.set_level(logging.INFO, logger="replayt_ux_showcase.demo")
    data = {
        "events": [{"type": "click", "ts": 10.0}],
        "metadata": {"duration": 30.0},
    }
    render_console_timeline(data)
    assert any("no event at or before playhead" in r.message for r in caplog.records)


def test_unknown_event_type_logs_warning(caplog: pytest.LogCaptureFixture):
    caplog.set_level(logging.DEBUG, logger="replayt_ux_showcase.demo")
    data = {
        "events": [{"type": "bogus", "ts": 1.0}],
        "metadata": {"duration": 30.0},
    }
    render_console_timeline(data)
    warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert any("unknown: bogus" in r.message for r in warnings)


def test_main_runs_timeline(caplog: pytest.LogCaptureFixture):
    caplog.set_level(logging.INFO, logger="replayt_ux_showcase.demo")
    demo_module.main()
    assert any("Rendering demo timeline" in r.message for r in caplog.records)


def test_main_propagates_errors(monkeypatch: pytest.MonkeyPatch):
    def boom(_data):
        raise RuntimeError("fail")

    monkeypatch.setattr(demo_module, "render_console_timeline", boom)
    with pytest.raises(RuntimeError, match="fail"):
        demo_module.main()
