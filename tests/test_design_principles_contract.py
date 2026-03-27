"""Contract tests: matrices in docs/DESIGN_PRINCIPLES.md stay aligned with repo files."""

from __future__ import annotations

import re
from pathlib import Path

import tomllib

REPO_ROOT = Path(__file__).resolve().parents[1]


def _project_table() -> dict:
    raw = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    return tomllib.loads(raw)["project"]


def test_requires_python_matches_design_principles_matrix() -> None:
    assert _project_table()["requires-python"] == ">=3.11"


def test_replayt_dependency_matches_design_principles_matrix() -> None:
    deps = _project_table()["dependencies"]
    replayt_lines = [d for d in deps if d.strip().lower().startswith("replayt")]
    assert len(replayt_lines) == 1
    assert re.search(r"replayt\s*>=\s*0\.1\.0", replayt_lines[0], re.IGNORECASE)


def test_ci_python_version_matches_design_principles_matrix() -> None:
    ci = (REPO_ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert 'python-version: "3.12"' in ci


def test_design_principles_has_matrix_and_audience_headings() -> None:
    text = (REPO_ROOT / "docs" / "DESIGN_PRINCIPLES.md").read_text(encoding="utf-8")
    for heading in (
        "## Replayt and Python matrix",
        "## Showcase stack matrix",
        "## Extension points",
        "## Audience",
    ):
        assert heading in text, f"missing section: {heading}"


def test_design_principles_has_replayt_api_boundary_subsection() -> None:
    text = (REPO_ROOT / "docs" / "DESIGN_PRINCIPLES.md").read_text(encoding="utf-8")
    assert "### replayt Python API boundary" in text


def test_design_principles_extension_points_include_packaged_showcase() -> None:
    text = (REPO_ROOT / "docs" / "DESIGN_PRINCIPLES.md").read_text(encoding="utf-8")
    assert "**`replayt_ux_showcase`** entrypoints" in text


def test_design_principles_audience_includes_release_and_automation_rows() -> None:
    text = (REPO_ROOT / "docs" / "DESIGN_PRINCIPLES.md").read_text(encoding="utf-8")
    assert "**Release / tag consumers**" in text
    assert "**Automation agents (LLM tooling)**" in text
