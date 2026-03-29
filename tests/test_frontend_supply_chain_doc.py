"""Contract tests for docs/FRONTEND_SUPPLY_CHAIN.md (backlog: CDN, SRI, bundling).

Maps to acceptance rows **A1–A5** in that document: required sections, keywords,
cross-links from README / DESIGN_PRINCIPLES / compat, and an **Unreleased**
CHANGELOG mention. **SRI** hash correctness stays out of CI per spec.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

_SUPPLY_CHAIN = REPO_ROOT / "docs" / "FRONTEND_SUPPLY_CHAIN.md"


def _unreleased_changelog_slice() -> str:
    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [Unreleased]" in changelog, "CHANGELOG must have an [Unreleased] section"
    start = changelog.index("## [Unreleased]") + len("## [Unreleased]")
    tail = changelog[start:]
    m = re.search(r"\n## \[\d", tail)
    return tail[: m.start()] if m else tail


def test_frontend_supply_chain_doc_exists_with_normative_sections() -> None:
    """A1: file exists; major sections and topical keywords stay present."""
    text = _SUPPLY_CHAIN.read_text(encoding="utf-8")
    for heading in (
        "## Single change set when replayt minors move",
        "## CDN delivery (e.g. jsDelivr)",
        "## Subresource Integrity (SRI)",
        "## Bundling alternative (npm + Vite, webpack, etc.)",
    ):
        assert heading in text, f"missing section heading: {heading}"
    for needle in (
        "jsDelivr",
        "integrity",
        "npm",
        "lockfile",
        "CDN trust",
        "pip-audit",
        "DEPENDENCY_AUDIT.md",
        "pyproject.toml",
    ):
        assert needle in text, f"missing expected keyword or link target: {needle!r}"


def test_frontend_supply_chain_doc_states_single_compatibility_story() -> None:
    """A2: authoritative range tied to pyproject + pin contract test name."""
    text = _SUPPLY_CHAIN.read_text(encoding="utf-8")
    assert "single compatibility" in text.lower()
    assert "test_docs_examples_replayt_pins.py" in text


def test_readme_and_design_principles_link_frontend_supply_chain_doc() -> None:
    """A4: entry points point integrators at the supply-chain doc."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/FRONTEND_SUPPLY_CHAIN.md" in readme

    principles = (REPO_ROOT / "docs" / "DESIGN_PRINCIPLES.md").read_text(
        encoding="utf-8"
    )
    assert "## Frontend supply chain (JavaScript / CDN)" in principles
    assert "FRONTEND_SUPPLY_CHAIN.md" in principles


def test_compat_digest_links_frontend_supply_chain_doc() -> None:
    """A4 (compat digest row): vanilla examples row links the same doc."""
    digest = (REPO_ROOT / "docs" / "compat.md").read_text(encoding="utf-8")
    assert "FRONTEND_SUPPLY_CHAIN.md" in digest


def test_changelog_unreleased_mentions_frontend_supply_chain_doc() -> None:
    """A5: Unreleased records the documentation (phase 2 spec bullet or later)."""
    unreleased = _unreleased_changelog_slice()
    assert "FRONTEND_SUPPLY_CHAIN" in unreleased
