"""Chromium load smoke for shipped vanilla ``docs/examples/*.html`` over loopback HTTP."""

from __future__ import annotations

import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLES_ROOT = REPO_ROOT / "docs" / "examples"

# Shipped root ``*.html`` per ``docs/examples/PATTERNS.md`` (P-01–P-05, P-09, P-10).
SHIPPED_ROOT_HTML = frozenset(
    {
        "basic-player.html",
        "player-session-metadata-bar.html",
        "timeline-scrubber.html",
        "embed-container-states.html",
        "fixture-replay.html",
        "event-overlay.html",
        "click-heatmap-canvas.html",
    }
)


@pytest.fixture(scope="session")
def examples_http_base_url() -> str:
    """Serve ``docs/examples/`` on loopback (CDN ``<script>`` vs ``file://``)."""

    class QuietHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, directory=str(EXAMPLES_ROOT), **kwargs)

        def log_message(self, _format: str, *_args) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
    server.allow_reuse_address = True
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


def test_shipped_root_html_inventory_matches_allowlist() -> None:
    discovered = {p.name for p in EXAMPLES_ROOT.glob("*.html")}
    assert discovered == SHIPPED_ROOT_HTML, (
        "docs/examples/*.html set drifted vs SHIPPED_ROOT_HTML "
        f"(update PATTERNS.md + this test together): extra={discovered - SHIPPED_ROOT_HTML} "
        f"missing={SHIPPED_ROOT_HTML - discovered}"
    )


# If the pinned replayt bundle or the browser emits unavoidable console warnings,
# add ``(filename, substring)`` entries and a one-line rationale in a comment above.
_CONSOLE_WARNING_ALLOWLIST: tuple[tuple[str, str], ...] = ()


def _warning_allowed(filename: str, text: str) -> bool:
    return any(
        allow_fname == filename and substr in text
        for allow_fname, substr in _CONSOLE_WARNING_ALLOWLIST
    )


@pytest.mark.playwright
@pytest.mark.parametrize("filename", sorted(SHIPPED_ROOT_HTML))
def test_static_example_loads_without_console_errors_or_pageerrors(
    page,
    examples_http_base_url: str,
    filename: str,
) -> None:
    console_errors: list[str] = []
    console_warnings: list[str] = []
    pageerrors: list[str] = []

    def on_console(msg) -> None:
        if msg.type == "error":
            console_errors.append(msg.text)
        elif msg.type == "warning":
            console_warnings.append(msg.text)

    page.on("console", on_console)
    page.on("pageerror", lambda exc: pageerrors.append(str(exc)))

    page.goto(f"{examples_http_base_url}/{filename}", wait_until="load")

    assert not pageerrors, f"{filename} pageerror(s): {pageerrors}"
    assert not console_errors, f"{filename} console error(s): {console_errors}"

    disallowed = [w for w in console_warnings if not _warning_allowed(filename, w)]
    assert not disallowed, (
        f"{filename} console warning(s) (allowlist in this module if intentional): {disallowed}"
    )
