"""Contract tests for docs/design-kit/ (Figma stub + interim token export).

Locks **F1–F8** section markers, cross-links, **`design-tokens.json`** shape, and
full coverage of playbook semantics from **`docs/playbook/tokens.md`**. See
**DESIGN_PRINCIPLES** — traceability to automated checks.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

_DESIGN_KIT_README = REPO_ROOT / "docs" / "design-kit" / "README.md"
_DESIGN_TOKENS_JSON = REPO_ROOT / "docs" / "design-kit" / "design-tokens.json"
_TOKENS_MD = REPO_ROOT / "docs" / "playbook" / "tokens.md"


# Canonical semantics from docs/playbook/tokens.md (Spacing, Typography, Color).
_EXPECTED_SEMANTICS: tuple[str, ...] = (
    "rux-space-0",
    "rux-space-1",
    "rux-space-2",
    "rux-space-3",
    "rux-space-4",
    "rux-space-6",
    "rux-space-8",
    "rux-font-sans",
    "rux-text-xs",
    "rux-text-sm",
    "rux-text-base",
    "rux-text-lg",
    "rux-font-medium",
    "rux-font-semibold",
    "rux-color-surface",
    "rux-color-surface-muted",
    "rux-color-border",
    "rux-color-text",
    "rux-color-text-muted",
    "rux-color-primary",
    "rux-color-danger",
    "rux-color-focus-ring",
)


def _unreleased_changelog_slice() -> str:
    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [Unreleased]" in changelog, "CHANGELOG must have an [Unreleased] section"
    start = changelog.index("## [Unreleased]") + len("## [Unreleased]")
    tail = changelog[start:]
    m = re.search(r"\n## \[\d", tail)
    return tail[: m.start()] if m else tail


def test_design_kit_files_exist() -> None:
    assert _DESIGN_KIT_README.is_file()
    assert _DESIGN_TOKENS_JSON.is_file()


@pytest.mark.parametrize("marker", [f"## F{n} —" for n in range(1, 9)])
def test_design_kit_readme_f_sections(marker: str) -> None:
    text = _DESIGN_KIT_README.read_text(encoding="utf-8")
    assert marker in text, f"missing section heading: {marker!r}"


def test_design_kit_readme_f_labels_in_acceptance_table() -> None:
    text = _DESIGN_KIT_README.read_text(encoding="utf-8")
    for n in range(1, 9):
        assert f"| F{n} |" in text, f"missing acceptance row for F{n}"


def test_design_kit_readme_cross_links_f7() -> None:
    text = _DESIGN_KIT_README.read_text(encoding="utf-8")
    assert "[`docs/playbook/README.md`](../playbook/README.md)" in text
    assert "[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)" in text
    assert "[`docs/playbook/tokens.md`](../playbook/tokens.md)" in text


def test_design_kit_readme_tokens_md_and_json_mentioned() -> None:
    text = _DESIGN_KIT_README.read_text(encoding="utf-8")
    assert "tokens.md" in text
    assert "design-tokens.json" in text


def test_design_kit_f3_mapping_covers_all_playbook_semantics() -> None:
    text = _DESIGN_KIT_README.read_text(encoding="utf-8")
    start = text.find("## F3 —")
    assert start != -1
    f3_block = text[start : text.find("## F4 —", start)]
    missing = [s for s in _EXPECTED_SEMANTICS if f"`{s}`" not in f3_block]
    assert not missing, f"F3 table missing semantics: {missing}"


def test_design_tokens_json_schema_and_tokens() -> None:
    raw = _DESIGN_TOKENS_JSON.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert data.get("schemaVersion")
    assert data.get("exportDate")
    assert isinstance(data.get("tokens"), list)
    sem_in_json = {t["semantic"] for t in data["tokens"]}
    expected = set(_EXPECTED_SEMANTICS)
    assert sem_in_json == expected, (
        f"JSON semantics mismatch: extra={sem_in_json - expected} "
        f"missing={expected - sem_in_json}"
    )
    for rec in data["tokens"]:
        assert "cssVar" in rec and str(rec["cssVar"]).startswith("--rux-")
        assert "value" in rec and rec["value"] is not None


def test_tokens_md_semantics_match_expected_contract() -> None:
    """If tokens.md drops or adds semantics, update _EXPECTED_SEMANTICS and JSON."""
    text = _TOKENS_MD.read_text(encoding="utf-8")
    found = set(re.findall(r"`(rux-(?:space|text|font|color)-[a-z0-9-]+)`", text))
    assert found == set(_EXPECTED_SEMANTICS), (
        f"tokens.md rux-* set drift vs test contract: "
        f"extra={found - set(_EXPECTED_SEMANTICS)} "
        f"missing={set(_EXPECTED_SEMANTICS) - found}"
    )


def test_design_principles_links_design_kit_and_test_module() -> None:
    principles = (REPO_ROOT / "docs" / "DESIGN_PRINCIPLES.md").read_text(
        encoding="utf-8"
    )
    assert "docs/design-kit/README.md" in principles
    assert "test_design_kit_docs.py" in principles


def test_readme_quick_start_links_design_kit() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/design-kit/README.md" in readme


def test_changelog_unreleased_mentions_design_kit_contract_tests() -> None:
    unreleased = _unreleased_changelog_slice()
    assert "test_design_kit_docs.py" in unreleased
