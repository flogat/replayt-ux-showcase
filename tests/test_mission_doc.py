"""Contract tests: docs/MISSION.md and docs/README.md content and cross-links."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MISSION_DOC = REPO_ROOT / "docs" / "MISSION.md"
DOCS_INDEX_DOC = REPO_ROOT / "docs" / "README.md"
ROOT_README = REPO_ROOT / "README.md"


def test_mission_doc_exists() -> None:
    """Mission document ships under docs/ (CONTRIBUTOR handoff)."""
    assert MISSION_DOC.is_file(), f"Missing {MISSION_DOC}"


def test_docs_index_exists() -> None:
    """Documentation index ships under docs/ for navigation."""
    assert DOCS_INDEX_DOC.is_file(), f"Missing {DOCS_INDEX_DOC}"


def test_mission_doc_has_core_sections() -> None:
    """Contract: mission doc covers users, scope, non-goals, success criteria."""
    text = MISSION_DOC.read_text(encoding="utf-8")
    assert "# Mission:" in text
    assert "## Users / problem" in text
    assert "## Replayt's role" in text
    assert "## Scope" in text
    assert "## Non-goals" in text
    assert "## Success" in text


def test_mission_doc_non_goals_explicit() -> None:
    """Contract: non-goals list covers hosted product, npm package, upstream replacement."""
    text = MISSION_DOC.read_text(encoding="utf-8")
    # Typical non-goal markers
    assert "hosted product" in text.lower() or "standalone" in text.lower()
    assert "npm" in text.lower()
    assert "replacement" in text.lower() or "upstream" in text.lower()


def test_docs_index_links_mission() -> None:
    """Contract: docs/README.md navigation table links to MISSION.md."""
    text = DOCS_INDEX_DOC.read_text(encoding="utf-8")
    assert "MISSION.md" in text
    assert "[MISSION.md](MISSION.md)" in text or "MISSION.md" in text


def test_docs_index_has_navigation_tables() -> None:
    """Contract: docs/README.md has 'Start here' and integrator/contributor tables."""
    text = DOCS_INDEX_DOC.read_text(encoding="utf-8")
    assert "## Start here" in text
    assert "## For integrators" in text
    assert "## For contributors" in text
    assert "## By concern" in text


def test_root_readme_links_mission_and_docs_index() -> None:
    """Contract: root README links to both MISSION.md and docs/README.md."""
    text = ROOT_README.read_text(encoding="utf-8")
    assert "docs/MISSION.md" in text
    assert "docs/README.md" in text


def test_mission_patterns_tracking_section() -> None:
    """Contract: mission doc has pattern coverage tracking table."""
    text = MISSION_DOC.read_text(encoding="utf-8")
    assert "Pattern coverage tracking" in text
    assert "PATTERNS.md" in text


def test_mission_links_examples_patterns() -> None:
    """Contract: mission doc references the canonical patterns inventory."""
    text = MISSION_DOC.read_text(encoding="utf-8")
    assert "docs/examples/PATTERNS.md" in text


def test_root_readme_project_layout_table_includes_mission() -> None:
    """Contract: README.md project layout table includes MISSION.md and docs/README.md."""
    text = ROOT_README.read_text(encoding="utf-8")
    # Check layout table context
    assert "## Project layout" in text
    assert "`docs/README.md`" in text
    assert "`docs/MISSION.md`" in text


def test_mission_success_links_playbook_and_design_kit() -> None:
    """Contract: success criteria mention playbook and design-kit deliverables."""
    text = MISSION_DOC.read_text(encoding="utf-8")
    assert "playbook" in text.lower()
    assert "design-kit" in text.lower() or "design kit" in text.lower()


def test_mission_references_replayt_ecosystem() -> None:
    """Contract: mission doc links to ecosystem positioning doc."""
    text = MISSION_DOC.read_text(encoding="utf-8")
    assert "REPLAYT_ECOSYSTEM_IDEA.md" in text
