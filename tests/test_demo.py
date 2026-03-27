"""Tests for demo module per docs/demo.md test plan."""

import subprocess
import sys

from replayt_ux_showcase import SAMPLE_SESSION_DATA, render_console_timeline


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
