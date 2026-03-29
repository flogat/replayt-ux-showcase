"""Contract tests for bundled upstream reference docs workflow.

Guards [`docs/reference-documentation/README.md`](../docs/reference-documentation/README.md) structure,
cross-links from **README** / **CONTRIBUTING**, the optional refresh helper under **`scripts/`**, and the
rule that default **CI** does not invoke that helper. Snapshot **presence** stays optional (no test requires
committed upstream copies).
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
_REF_README = REPO_ROOT / "docs" / "reference-documentation" / "README.md"
_ROOT_README = REPO_ROOT / "README.md"
_CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"
_CI_YML = REPO_ROOT / ".github" / "workflows" / "ci.yml"
_SCRIPT = (
    REPO_ROOT / "scripts" / "refresh-reference-docs" / "copy_markdown_snapshots.py"
)


def test_reference_documentation_readme_normative_sections() -> None:
    text = _REF_README.read_text(encoding="utf-8")
    for heading in (
        "## Layout (normative for maintainers)",
        "## License and attribution",
        "## Refresh cadence (recommended)",
        "## Maintenance checklist (contributors / Mission Control)",
        "## Acceptance criteria (Builder / gate)",
    ):
        assert heading in text, f"missing section: {heading}"
    assert "scripts/refresh-reference-docs/copy_markdown_snapshots.py" in text


def test_root_readme_and_contributing_link_reference_docs() -> None:
    root = _ROOT_README.read_text(encoding="utf-8")
    assert "docs/reference-documentation/README.md" in root
    con = _CONTRIBUTING.read_text(encoding="utf-8")
    assert "docs/reference-documentation/README.md" in con
    assert "backlog-traceability-bundled-upstream-reference-docs-workflow" in con


def test_design_principles_traceability_lists_reference_doc_tests() -> None:
    dp = (REPO_ROOT / "docs" / "DESIGN_PRINCIPLES.md").read_text(encoding="utf-8")
    assert "test_reference_documentation_docs.py" in dp


def test_default_ci_does_not_run_refresh_reference_docs_script() -> None:
    ci = _CI_YML.read_text(encoding="utf-8")
    assert "refresh-reference-docs" not in ci
    assert "copy_markdown_snapshots.py" not in ci


def test_copy_markdown_snapshots_writes_under_reference_tree(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        textwrap.dedent(
            """
            [project]
            name = "replayt-ux-showcase"
            version = "0.0.0"
            """
        ).strip(),
        encoding="utf-8",
    )
    (tmp_path / "docs" / "reference-documentation").mkdir(parents=True)
    src = tmp_path / "upstream"
    (src / "docs").mkdir(parents=True)
    (src / "docs" / "api.md").write_text("# API\n", encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            "--repo-root",
            str(tmp_path),
            "--source",
            str(src),
            "--version",
            "9.9.9-test",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    out = (
        tmp_path
        / "docs"
        / "reference-documentation"
        / "replayt"
        / "9.9.9-test"
        / "docs"
        / "api.md"
    )
    assert out.is_file()
    assert out.read_text(encoding="utf-8") == "# API\n"


def test_copy_markdown_snapshots_dry_run_creates_no_files(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        textwrap.dedent(
            """
            [project]
            name = "replayt-ux-showcase"
            version = "0.0.0"
            """
        ).strip(),
        encoding="utf-8",
    )
    (tmp_path / "docs" / "reference-documentation").mkdir(parents=True)
    src = tmp_path / "upstream"
    src.mkdir()
    (src / "x.md").write_text("x", encoding="utf-8")

    subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            "--repo-root",
            str(tmp_path),
            "--source",
            str(src),
            "--version",
            "dry",
            "--dry-run",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert not (tmp_path / "docs" / "reference-documentation" / "replayt").exists()


def test_copy_markdown_snapshots_errors_when_no_markdown(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        textwrap.dedent(
            """
            [project]
            name = "replayt-ux-showcase"
            version = "0.0.0"
            """
        ).strip(),
        encoding="utf-8",
    )
    (tmp_path / "docs" / "reference-documentation").mkdir(parents=True)
    src = tmp_path / "empty"
    src.mkdir()
    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            "--repo-root",
            str(tmp_path),
            "--source",
            str(src),
            "--version",
            "v",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 1
