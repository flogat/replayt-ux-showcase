"""Headless smoke for P-01 ``docs/examples/basic-player.html`` (CDN + DOM + light interaction)."""

from __future__ import annotations

import re

import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.browser_smoke


def test_basic_player_smoke(page: Page, docs_examples_base_url: str) -> None:
    """Load over HTTP, wait for public replayt player API, assert mount + copy + focus, no uncaught errors."""
    errors: list[str] = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))

    page.goto(f"{docs_examples_base_url}/basic-player.html", wait_until="domcontentloaded")

    page.wait_for_function(
        "() => !!(window.replayt && window.replayt.player"
        " && typeof window.replayt.player.init === 'function')",
        timeout=90_000,
    )

    expect(page.locator("#player")).to_be_visible()
    expect(page.get_by_role("heading", name=re.compile(r"Basic Replayt Player"))).to_be_visible()
    expect(page.get_by_text("Copy-paste ready:", exact=False)).to_be_visible()

    link = page.get_by_role("link", name="docs/a11y/keyboard-model.md")
    link.focus()
    expect(link).to_be_focused()

    assert not errors, f"uncaught page errors: {errors}"
