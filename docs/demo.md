# Minimal Replayt Demo Module Spec (Phase 2)

## User Story

As demo author, I want `src/replayt_ux_showcase/demo.py` exercising core replayt primitives with canonical patterns.

**Notes:** Narrow public surface; document API.

## Acceptance Criteria

- Runs via `python -m replayt_ux_showcase.demo` → logs observable console output
- Module executable (`if __name__ == \"__main__\": render_console_timeline(SAMPLE_SESSION_DATA)`)
- Logs use `logging.getLogger(\"replayt_ux_showcase.demo\")` (prefix [replayt-demo] in output)
- No direct LLM calls (N/A)
- Deps: `replayt >=0.1.0` (in pyproject.toml); stdlib only besides

## Public API

Exposed in `__init__.py`:

```python
from .demo import render_console_timeline, SAMPLE_SESSION_DATA
```

- `SAMPLE_SESSION_DATA: dict[str, Any]`  
  Canonical mock (~30s session):  
  ```python
  {
      \"events\": [
          {\"type\": \"click\", \"ts\": 1.0, \"x\": 100, \"y\": 200},
          {\"type\": \"scroll\", \"ts\": 5.0, \"dy\": 300},
          # ... 10+ events: mouse, key, viewport resize
      ],
      \"metadata\": {\"start_ts\": 0, \"viewport\": {\"w\": 1920, \"h\": 1080}, \"duration\": 30.0}
  }
  ```
  Matches replayt session schema.

- `def render_console_timeline(session_data: dict[str, Any]) -> None`  
  Parses via replayt SDK → renders ASCII progress bar timeline + logs key events.  
  Uses `logging.INFO`: f\"[replayt-demo] Processing {len(events)} events\"  
  Console output example:  
  ```
  [replayt-demo] Rendering demo timeline (30s)
  Timeline: [===>     ] 00:06 / 00:30 (speed: 2x)
  Events:
    00:01 click (100,200)
    00:05 scroll +300px
    ...
  ```

## Implementation Notes

- Import `replayt` → load/parse session_data → iterate events chronologically
- Stdlib: `logging`, `time`, `os`, `json` for output formatting
- No network/GUI/file I/O
- Error handling: log WARN on invalid data, exit 1 if unrecoverable
- Follow DESIGN_PRINCIPLES.md: small surface, observable logs

## Test Plan (phase 4)

- `test_demo_runs()`: subprocess.call([sys.executable, -m, ...]) == 0; check logs
- `test_exports()`: import ok, len(SAMPLE_SESSION_DATA[\"events\"]) == N
- Snapshot output

No risks; precise, testable for builder.