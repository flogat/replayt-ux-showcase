"""Contract tests for docs/playbook/ (design-to-code handoff).

Locks structure implied by acceptance rows **T1–T3** (**tokens.md**), **A1–A3**
(**component-anatomy.md**), **H1–H3** (**handoff-checklist.md**), the playbook
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
    """T1: spacing, typography, and color sections with --rux- naming."""
    text = _TOKENS.read_text(encoding="utf-8")
    for heading in ("## Spacing scale", "## Typography", "## Color (semantic)"):
        assert heading in text, f"missing section: {heading}"
    assert "--rux-" in text
    for label in ("T1", "T2", "T3"):
        assert label in text, f"missing acceptance row marker: {label}"


def test_component_anatomy_timeline_overlays_and_links() -> None:
    """A1–A3: timeline + overlays; keyboard-model cross-links."""
    text = _ANATOMY.read_text(encoding="utf-8")
    assert "## 1. Timeline / scrubber strip" in text
    assert "## 2. Overlays (dialogs, popovers, event callouts)" in text
    assert "keyboard-model.md" in text
    assert "P-03" in text
    for label in ("A1", "A2", "A3"):
        assert label in text, f"missing acceptance row marker: {label}"


def test_handoff_checklist_sections_and_normative_links() -> None:
    """H1–H3: a11y, loading, error; print path; keyboard-model + P-04."""
    text = _CHECKLIST.read_text(encoding="utf-8")
    for heading in ("## Accessibility", "## Loading", "## Error and recovery"):
        assert heading in text, f"missing section: {heading}"
    assert "Print" in text
    assert "keyboard-model" in text
    assert "P-04" in text
    for label in ("H1", "H2", "H3"):
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
