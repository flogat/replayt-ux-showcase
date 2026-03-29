"""Contract tests: matrices in docs/DESIGN_PRINCIPLES.md stay aligned with repo files."""

from __future__ import annotations

import re
from pathlib import Path

import tomllib
from packaging.requirements import Requirement

REPO_ROOT = Path(__file__).resolve().parents[1]

# Must match `strategy.matrix` in `.github/workflows/ci.yml` and inventory IDs in `docs/compat.md`.
CI_TEST_JOB_PYTHON_VERSIONS = ("3.11", "3.12")
CI_TEST_JOB_REPLAYT_VERSIONS = ("0.1.0", "0.2.0", "0.4.25")


def _compat_exercise_row_inventory_ids() -> tuple[str, ...]:
    """Stable **EX-*** IDs for each `jobs.test` matrix cell (Python × replayt pin)."""
    ids: list[str] = []
    for py in CI_TEST_JOB_PYTHON_VERSIONS:
        py_compact = py.replace(".", "")
        for rt in CI_TEST_JOB_REPLAYT_VERSIONS:
            rt_part = rt.replace(".", "-")
            ids.append(f"EX-{py_compact}-RT-{rt_part}")
    return tuple(ids)


def _pyproject_root() -> dict:
    raw = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    return tomllib.loads(raw)


def _project_table() -> dict:
    return _pyproject_root()["project"]


def _assert_each_line_has_pep508_version_constraint(lines: list[str]) -> None:
    for line in lines:
        req = Requirement(line.strip())
        assert len(req.specifier) > 0, f"missing PEP 508 version constraint: {line!r}"


def test_requires_python_matches_design_principles_matrix() -> None:
    assert _project_table()["requires-python"] == ">=3.11"


def test_replayt_dependency_matches_design_principles_matrix() -> None:
    deps = _project_table()["dependencies"]
    replayt_lines = [d for d in deps if d.strip().lower().startswith("replayt")]
    assert len(replayt_lines) == 1
    req = Requirement(replayt_lines[0])
    assert req.name.lower() == "replayt"
    spec = str(req.specifier)
    assert re.search(r">=\s*0\.1\.0", spec)
    assert re.search(r"<\s*0\.5", spec)


def test_replayt_importable() -> None:
    import importlib

    importlib.import_module("replayt")


def test_package_version_matches_pyproject() -> None:
    """Releases and CHANGELOG: __version__ matches [project].version."""
    import importlib

    pkg = importlib.import_module("replayt_ux_showcase")
    assert pkg.__version__ == _project_table()["version"]


def test_project_dependencies_have_version_constraints() -> None:
    _assert_each_line_has_pep508_version_constraint(_project_table()["dependencies"])


def test_dev_optional_dependencies_have_version_constraints() -> None:
    dev = _project_table()["optional-dependencies"]["dev"]
    _assert_each_line_has_pep508_version_constraint(dev)


def test_dev_optional_dependencies_match_baseline_package_set() -> None:
    """Aligns with DESIGN_PRINCIPLES.md Dev optional dependency set (baseline)."""
    dev = _project_table()["optional-dependencies"]["dev"]
    names = {Requirement(d.strip()).name.lower() for d in dev}
    assert names == {"pip-audit", "pytest", "pytest-cov", "ruff"}, (
        f"dev extras must be exactly pytest, pytest-cov, ruff, pip-audit; got {sorted(names)}"
    )


def test_build_system_requires_have_version_constraints() -> None:
    requires = _pyproject_root()["build-system"]["requires"]
    _assert_each_line_has_pep508_version_constraint(requires)


def test_ci_test_job_matrix_matches_design_principles_matrix() -> None:
    """Replayt and Python matrix: CI test job exercises declared Python and replayt pins."""
    ci = (REPO_ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "strategy:" in ci
    assert "matrix:" in ci
    assert "python-version:" in ci
    assert "${{ matrix.python-version }}" in ci
    assert "replayt-version:" in ci
    assert "${{ matrix.replayt-version }}" in ci
    assert "replayt-constraint.txt" in ci
    assert 'pip install -e ".[dev]"' in ci and "-c" in ci
    for py in CI_TEST_JOB_PYTHON_VERSIONS:
        assert f'"{py}"' in ci, f"missing python matrix entry {py}"
    for rt in CI_TEST_JOB_REPLAYT_VERSIONS:
        assert f'"{rt}"' in ci, f"missing replayt matrix entry {rt}"


def test_compat_ci_exercise_inventory_ids_match_ci_matrix() -> None:
    """docs/compat.md CI exercise inventory stays aligned with the test job matrix."""
    compat = (REPO_ROOT / "docs" / "compat.md").read_text(encoding="utf-8")
    for inv_id in _compat_exercise_row_inventory_ids():
        assert f"**{inv_id}**" in compat, f"compat.md CI inventory missing {inv_id}"
    assert "**EX-EXAMPLES-PINS**" in compat
    assert "**EX-REPLAYT-PY-API**" in compat
    assert "**EX-SUPPLY-CHAIN**" in compat


def test_ci_installs_editable_with_dev_extras() -> None:
    """Supported contributor entrypoint: pip install -e ".[dev]" (quoted extras)."""
    ci = (REPO_ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert 'pip install -e ".[dev]"' in ci


def test_ci_runs_ruff_lint_and_format_check() -> None:
    ci = (REPO_ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "ruff check" in ci
    assert "ruff format --check" in ci


def test_readme_ci_badge_uses_repository_slug() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "OWNER/REPO" not in readme
    assert "github.com/flogat/replayt-ux-showcase/actions/workflows/ci.yml" in readme


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
