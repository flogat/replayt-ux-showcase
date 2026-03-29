"""Contract tests for docs/playbook/ (design-to-code handoff).

Locks structure implied by acceptance rows **T1–T5** (**tokens.md**), **A1–A5**
(**component-anatomy.md**), **H1–H5** (**handoff-checklist.md**), the playbook
**README** index, integrator entry points, and **CHANGELOG** **Unreleased**
mention of this automation (see **DESIGN_PRINCIPLES** traceability table).
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

_PLAYBOOK = REPO_ROOT / "docs" / "playbook"
_TOKENS = _PLAYBOOK / "tokens.md"
_ANATOMY = _PLAYBOOK / "component-anatomy.md"
_CHECKLIST = _PLAYBOOK / "handoff-checklist.md"
_README_PLAYBOOK = _PLAYBOOK / "README.md"


def _unreleased_changelog_slice() -> str:
    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [Unreleased]" in changelog, "CHANGELOG must have an [Unreleased] section"
    start = changelog.index("## [Unreleased]") + len("## [Unreleased]")
    tail = changelog[start:]
    m = re.search(r"\n## \[\d", tail)
    return tail[: m.start()] if m else tail


def test_playbook_files_exist() -> None:
    for path in (_TOKENS, _ANATOMY, _CHECKLIST, _README_PLAYBOOK):
        assert path.is_file(), f"missing playbook file: {path.relative_to(REPO_ROOT)}"


def test_tokens_doc_spacing_typography_color_tables() -> None:
    """T1–T3: spacing, typography, and color sections with --rux- naming."""
    text = _TOKENS.read_text(encoding="utf-8")
    for heading in ("## Spacing scale", "## Typography", "## Color (semantic)"):
        assert heading in text, f"missing section: {heading}"
    assert "--rux-" in text
    for label in ("T1", "T2", "T3"):
        assert label in text, f"missing acceptance row marker: {label}"


def test_tokens_doc_viewport_and_canonical_basic_player() -> None:
    """T4–T5: viewport semantics vs host layout; P-01 basic-player as canonical wiring."""
    text = _TOKENS.read_text(encoding="utf-8")
    assert "## Viewport and session frame" in text
    assert "metadata.viewport" in text
    assert "P-01" in text and "P-02" in text
    assert "## Canonical `--rux-*` usage" in text
    assert "basic-player.html" in text
    assert "--replayt-primary" in text
    for label in ("T4", "T5"):
        assert label in text, f"missing acceptance row marker: {label}"


def test_component_anatomy_timeline_overlays_and_links() -> None:
    """A1–A5: timeline + overlays; scrubber states; P-09 hover/focus parity."""
    text = _ANATOMY.read_text(encoding="utf-8")
    assert "## 1. Timeline / scrubber strip" in text
    assert "## 2. Overlays (dialogs, popovers, event callouts)" in text
    assert "keyboard-model.md" in text
    assert "P-03" in text
    assert "### Scrubber interaction states" in text
    assert "Resting" in text and "Committed seek" in text
    assert "Hover vs focus" in text
    assert "P-09" in text
    for label in ("A1", "A2", "A3", "A4", "A5"):
        assert label in text, f"missing acceptance row marker: {label}"


def test_handoff_checklist_sections_and_normative_links() -> None:
    """H1–H5: a11y, viewport, scrubber, loading, error; normative links + P-09."""
    text = _CHECKLIST.read_text(encoding="utf-8")
    for heading in ("## Accessibility", "## Loading", "## Error and recovery"):
        assert heading in text, f"missing section: {heading}"
    assert "## Viewport and session frame" in text
    assert "## Timeline scrubber" in text
    assert "tokens.md" in text
    assert "component-anatomy.md" in text
    assert "P-01" in text and "P-02" in text and "P-03" in text
    assert "P-09" in text
    assert "Print" in text
    assert "keyboard-model" in text
    assert "P-04" in text
    for label in ("H1", "H2", "H3", "H4", "H5"):
        assert label in text, f"missing acceptance row marker: {label}"


def test_playbook_readme_indexes_core_docs() -> None:
    text = _README_PLAYBOOK.read_text(encoding="utf-8")
    for needle in (
        "[`tokens.md`](tokens.md)",
        "[`component-anatomy.md`](component-anatomy.md)",
        "[`handoff-checklist.md`](handoff-checklist.md)",
        "keyboard-model.md",
        "PATTERNS.md",
    ):
        assert needle in text, f"missing README link or reference: {needle!r}"


def test_readme_quick_start_links_playbook() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/playbook/README.md" in readme


def test_design_principles_links_playbook_and_test_module() -> None:
    principles = (REPO_ROOT / "docs" / "DESIGN_PRINCIPLES.md").read_text(
        encoding="utf-8"
    )
    assert "docs/playbook/README.md" in principles
    assert "test_playbook_docs.py" in principles


def test_changelog_unreleased_mentions_playbook_contract_tests() -> None:
    unreleased = _unreleased_changelog_slice()
    assert "test_playbook_docs.py" in unreleased
