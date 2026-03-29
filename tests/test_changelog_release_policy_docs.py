"""Contract tests for CONTRIBUTING, CHANGELOG policy, and DESIGN_PRINCIPLES semver section.

Locks structure from [Changelog, semver, and release notes](docs/DESIGN_PRINCIPLES.md#changelog-semver-and-release-notes)
and [`CONTRIBUTING.md`](../CONTRIBUTING.md) so integrator-facing release guidance and the pins ↔ principles
table do not drift without CI signal. Semver tagging decisions stay human review; these tests only assert
stable headings, tables, and cross-links.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

_CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"
_DESIGN_PRINCIPLES = REPO_ROOT / "docs" / "DESIGN_PRINCIPLES.md"
_CHANGELOG = REPO_ROOT / "CHANGELOG.md"


def _unreleased_changelog_slice() -> str:
    changelog = _CHANGELOG.read_text(encoding="utf-8")
    assert "## [Unreleased]" in changelog, "CHANGELOG must have an [Unreleased] section"
    start = changelog.index("## [Unreleased]") + len("## [Unreleased]")
    tail = changelog[start:]
    m = re.search(r"\n## \[\d", tail)
    return tail[: m.start()] if m else tail


def test_contributing_exists_with_pins_principles_table() -> None:
    text = _CONTRIBUTING.read_text(encoding="utf-8")
    assert "docs/DESIGN_PRINCIPLES.md" in text
    assert "## Changelog" in text
    assert "When to edit `docs/DESIGN_PRINCIPLES.md`" in text
    assert "`[project].dependencies`" in text and "replayt" in text
    assert "`.github/workflows/ci.yml`" in text
    assert (
        "unreleased-pattern-coverage-and-mission-tracking" in text
        or "DESIGN_PRINCIPLES.md#unreleased-pattern-coverage-and-mission-tracking" in text
    )


def test_design_principles_changelog_semver_section_structure() -> None:
    text = _DESIGN_PRINCIPLES.read_text(encoding="utf-8")
    assert "## Changelog, semver, and release notes" in text
    assert "### Python package API (`replayt_ux_showcase`)" in text
    assert "### Docs and examples (integrator copy-paste surface)" in text
    assert "### Unreleased: pattern coverage and mission tracking" in text
    assert "**MAJOR**" in text and "**MINOR**" in text and "**PATCH**" in text
    assert "docs/examples/PATTERNS.md" in text
    assert "Backlog traceability: CHANGELOG and release process" in text


def test_design_principles_traceability_lists_this_module() -> None:
    text = _DESIGN_PRINCIPLES.read_text(encoding="utf-8")
    assert "test_changelog_release_policy_docs.py" in text
    assert "CONTRIBUTING.md" in text


def test_changelog_unreleased_mentions_policy_contract_tests() -> None:
    unreleased = _unreleased_changelog_slice()
    assert "test_changelog_release_policy_docs.py" in unreleased
