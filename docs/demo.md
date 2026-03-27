# Minimal Replayt Demo Module Spec

## User Story

As demo author, I want `src/replayt_ux_showcase/demo.py` exercising core replayt primitives with canonical patterns.

**Notes:** Narrow public surface; document API.

## Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | Runs via `python -m replayt_ux_showcase.demo` | Execute: `python -m replayt_ux_showcase.demo`; expect exit code 0 |
| 2 | Logs observable console output | stderr/stdout contains `[replayt-demo]` prefixed lines |
| 3 | Module executable with `if __name__ == "__main__"` guard | Entry point calls `render_console_timeline(SAMPLE_SESSION_DATA)` |
| 4 | Logger uses `logging.getLogger("replayt_ux_showcase.demo")` | Logger name matches exactly |
| 5 | No direct LLM calls | Static data only, no API keys or network calls |
| 6 | Stdlib dependencies only | `logging`, `typing`; no heavy frameworks |
| 7 | Exports public API | `__init__.py` exposes `render_console_timeline` and `SAMPLE_SESSION_DATA` |

## Replayt Primitives Usage

This demo exercises replayt concepts at the **data schema level** (session/events), not the runtime level:

- **Session schema**: `SAMPLE_SESSION_DATA` follows replayt's session format with `events[]` and `metadata`
- **Event types**: Implements core replayt event types (`click`, `scroll`, `keypress`, `resize`, `mousemove`)
- **Timeline rendering**: Demonstrates how integrators visualize replayt session data

**Note**: This demo uses static mock data. For runtime integration with replayt primitives (`Runner`, `Workflow`, `MockLLMClient`), see future patterns in `docs/examples/`.

## Public API Contract

Expose in `src/replayt_ux_showcase/__init__.py`:

```python
from .demo import render_console_timeline, SAMPLE_SESSION_DATA

__all__ = ["render_console_timeline", "SAMPLE_SESSION_DATA"]
```

### `SAMPLE_SESSION_DATA: dict[str, Any]`

Canonical mock session (~30s, 12 events). Must match replayt session schema:

```python
{
    "events": [
        {"type": "click", "ts": 1.0, "x": 100, "y": 200},
        {"type": "scroll", "ts": 5.0, "dy": 300},
        {"type": "keypress", "ts": 8.5, "key": "a"},
        {"type": "resize", "ts": 12.0, "w": 1920, "h": 1080},
        {"type": "click", "ts": 15.0, "x": 500, "y": 300},
        {"type": "scroll", "ts": 18.0, "dy": -150},
        {"type": "keypress", "ts": 22.0, "key": "Enter"},
        {"type": "click", "ts": 25.0, "x": 800, "y": 600},
        {"type": "scroll", "ts": 27.5, "dy": 200},
        {"type": "mousemove", "ts": 28.0, "x": 900, "y": 700},
        {"type": "click", "ts": 29.0, "x": 950, "y": 750},
        {"type": "scroll", "ts": 29.5, "dy": 50},
    ],
    "metadata": {
        "start_ts": 0.0,
        "viewport": {"w": 1920, "h": 1080},
        "duration": 30.0,
    },
}
```

Requirements:
- Minimum 10 events, maximum 15 events
- Event types: `click`, `scroll`, `keypress`, `resize`, `mousemove`
- Events sorted chronologically by `ts` (ascending)
- Timestamp range: 0 to 30 seconds

### `render_console_timeline(session_data: dict[str, Any]) -> None`

Renders ASCII timeline to console via logging.

**Behavior:**
1. Log: `INFO [replayt-demo] Rendering demo timeline ({duration}s)`
2. Log: `INFO [replayt-demo] Processing {N} events`
3. Render ASCII progress bar (50 chars wide, snapshot at 6s/30s)
4. Log each event with formatted timestamp `MM:SS`

**Event rendering:**
| Type | Output format |
|------|---------------|
| click | `MM:SS click (x,y)` |
| scroll | `MM:SS scroll {dy}px` |
| keypress | `MM:SS keypress {key}` |
| resize | `MM:SS resize {w}x{h}` |
| mousemove | `MM:SS mousemove (x,y)` |
| unknown | `WARN MM:SS unknown: {type}` |

**Error handling:**
- Missing/invalid event data: log `WARNING`, continue processing
- Unrecoverable errors: propagate exception (caller handles)

## Implementation Constraints

- No network I/O
- No GUI/file I/O
- No external deps beyond `replayt >=0.1.0` (declared in pyproject.toml)
- Follow DESIGN_PRINCIPLES.md: small surface, observable logs

## Test Plan (Phase 4)

| Test | Description | Expected |
|------|-------------|----------|
| `test_demo_runs` | Subprocess: `subprocess.run([sys.executable, "-m", "replayt_ux_showcase.demo"], capture_output=True)` | `returncode == 0` |
| `test_exports` | Import check: `from replayt_ux_showcase import render_console_timeline, SAMPLE_SESSION_DATA` | Both symbols present; `len(SAMPLE_SESSION_DATA["events"]) in range(10, 16)` |
| `test_output_format` | Output contains expected log lines | stdout contains both `[replayt-demo]` and `"Rendering demo timeline"` |
| `test_event_count` | Validate event count in sample data | `10 <= len(SAMPLE_SESSION_DATA["events"]) <= 15` |
| `test_event_types` | Validate event types | All events have `type` in `('click', 'scroll', 'keypress', 'resize', 'mousemove')` |

## Integration Notes

- **Version compatibility**: Tested against `replayt >=0.1.0`
- **No runtime dependency**: Module imports without replayt installed (stdlib only)
- **Design principles**: Matches DESIGN_PRINCIPLES.md “small public surfaces” and “observable automation”

## Deprecation Notes

- None; initial implementation.
