"""Drift guard: P-01 HTML stays aligned with SAMPLE_SESSION_DATA (SESSION_SCHEMA §5).

The canonical fixture is embedded as strict JSON in
``<script type="application/json" id="rux-showcase-session-fixture">`` so tests can
``json.loads`` and compare to ``replayt_ux_showcase.demo.SAMPLE_SESSION_DATA`` without
a JavaScript parser. Add paths to ``_FIXTURE_HTML_FILES`` when more examples adopt the
same pattern.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

_FIXTURE_HTML_FILES = (REPO_ROOT / "docs/examples/basic-player.html",)

_FIXTURE_SCRIPT_RE = re.compile(
    r'<script\s+type=["\']application/json["\']\s+id=["\']rux-showcase-session-fixture["\']\s*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)


def _parse_fixture_json(html_path: Path) -> dict:
    text = html_path.read_text(encoding="utf-8")
    m = _FIXTURE_SCRIPT_RE.search(text)
    assert m, (
        f'{html_path}: missing <script type="application/json" '
        f'id="rux-showcase-session-fixture"> block'
    )
    return json.loads(m.group(1))


@pytest.mark.parametrize("html_path", _FIXTURE_HTML_FILES)
def test_html_fixture_json_matches_sample_session_data(html_path: Path) -> None:
    from replayt_ux_showcase.demo import SAMPLE_SESSION_DATA

    assert html_path.is_file(), f"missing {html_path}"
    loaded = _parse_fixture_json(html_path)
    assert loaded == SAMPLE_SESSION_DATA
