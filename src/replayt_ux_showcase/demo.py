import logging
from typing import Any

logger = logging.getLogger("replayt_ux_showcase.demo")


def _active_event_type_at_scrub(
    events: list[dict[str, Any]], scrub_s: float
) -> str | None:
    """Last event at or before scrub_s (same selection rule as docs/examples/event-overlay.html)."""
    eligible = [
        e
        for e in events
        if isinstance(e.get("ts"), (int, float)) and e["ts"] <= scrub_s
    ]
    if not eligible:
        return None
    last = max(eligible, key=lambda e: float(e["ts"]))
    return str(last.get("type", "event"))


SAMPLE_SESSION_DATA: dict[str, Any] = {
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


def render_console_timeline(session_data: dict[str, Any]) -> None:
    logger.info(
        f"[replayt-demo] Rendering demo timeline ({session_data['metadata']['duration']}s)"
    )
    events = sorted(
        session_data.get("events", []), key=lambda e: e.get("ts", float("inf"))
    )
    logger.info(f"[replayt-demo] Processing {len(events)} events")

    bar_width = 50
    sample_pos = 6.0
    progress = int((sample_pos / session_data["metadata"]["duration"]) * bar_width)
    bar = "[" + "=" * progress + " " * (bar_width - progress) + "]"
    min_ts = f"{int(sample_pos // 60):02d}:{int(sample_pos % 60):02d}"
    total_min = f"{int(session_data['metadata']['duration'] // 60):02d}:{int(session_data['metadata']['duration'] % 60):02d}"
    logger.info(f"Timeline: {bar} {min_ts} / {total_min} (speed: 2x)")
    scrub_snapshot_s = 6.0
    active_type = _active_event_type_at_scrub(events, scrub_snapshot_s)
    if active_type is not None:
        logger.info(
            "[replayt-demo] Overlay teaching: at scrub %.1fs the active event type is %r "
            "(callout / tooltip in docs/examples/event-overlay.html follows the same rule).",
            scrub_snapshot_s,
            active_type,
        )
    else:
        logger.info(
            "[replayt-demo] Overlay teaching: at scrub %.1fs no event at or before playhead.",
            scrub_snapshot_s,
        )
    logger.info("Events:")
    for event in events:
        ts = event.get("ts", 0.0)
        m, s = divmod(int(ts), 60)
        tstr = f"{m:02d}:{s:02d}"
        etype = event["type"]
        if etype == "click":
            logger.info(f"  {tstr} click ({event.get('x', 0)},{event.get('y', 0)})")
        elif etype == "scroll":
            logger.info(f"  {tstr} scroll {event.get('dy', 0)}px")
        elif etype == "keypress":
            logger.info(f"  {tstr} keypress {event.get('key', '?')}")
        elif etype == "resize":
            logger.info(f"  {tstr} resize {event.get('w', 0)}x{event.get('h', 0)}")
        elif etype == "mousemove":
            logger.info(f"  {tstr} mousemove ({event.get('x', 0)},{event.get('y', 0)})")
        else:
            logger.warning(f"  {tstr} unknown: {etype}")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        render_console_timeline(SAMPLE_SESSION_DATA)
    except Exception as e:
        logger.error(f"[replayt-demo] Error: {e}")
        raise


if __name__ == "__main__":  # pragma: no cover
    main()
