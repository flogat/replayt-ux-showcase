"""Fixtures for docs/examples static HTML Playwright tests."""

from __future__ import annotations

import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

pytest_plugins = ["pytest_playwright"]

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def docs_examples_base_url() -> str:
    """Serve ``docs/examples/`` at the URL root (HTTP), same layout integrators use."""
    root = REPO_ROOT / "docs" / "examples"

    class _Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(root), **kwargs)

    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_port
    base = f"http://127.0.0.1:{port}"
    try:
        yield base
    finally:
        server.shutdown()
        server.server_close()
