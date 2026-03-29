"""Contract tests for docs/DEPENDENCY_AUDIT.md (pip-audit playbook **D1–D10**).

Mirrors **`tests/test_frontend_supply_chain_doc.py`**: doc structure, **CI** command parity
with **`.github/workflows/ci.yml`**, cross-links, and **CHANGELOG** **Unreleased** mention.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

_DEPENDENCY_AUDIT = REPO_ROOT / "docs" / "DEPENDENCY_AUDIT.md"
_CI_YML = REPO_ROOT / ".github" / "workflows" / "ci.yml"


def _unreleased_changelog_slice() -> str:
    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [Unreleased]" in changelog, "CHANGELOG must have an [Unreleased] section"
    start = changelog.index("## [Unreleased]") + len("## [Unreleased]")
    tail = changelog[start:]
    m = re.search(r"\n## \[\d", tail)
    return tail[: m.start()] if m else tail


def _ci_pip_audit_run_line() -> str:
    yml = _CI_YML.read_text(encoding="utf-8")
    m = re.search(r"^\s*run:\s*(pip-audit[^\n]*)$", yml, re.MULTILINE)
    assert m, "ci.yml must contain a pip-audit run: line"
    return m.group(1).strip()


def _ignore_vuln_ids_from_pip_audit_cli(cli: str) -> list[str]:
    return re.findall(r"--ignore-vuln\s+(CVE-\d{4}-\d+)", cli)


def test_d1_doc_states_supply_chain_audits_editable_dev_graph() -> None:
    """D1: **CI** audits the editable **`.[dev]`** graph with **pip-audit**."""
    text = _DEPENDENCY_AUDIT.read_text(encoding="utf-8")
    lower = text.lower()
    assert "editable" in lower
    assert "pip-audit" in text
    assert 'pip install -e ".[dev]"' in text
    assert "supply-chain" in text or "`supply-chain`" in text


def test_d2_doc_quotes_same_pip_audit_invocation_as_ci_yml() -> None:
    """D2: doc shows the same **pip-audit** CLI as **ci.yml** (including **--ignore-vuln**)."""
    doc = _DEPENDENCY_AUDIT.read_text(encoding="utf-8")
    ci_cmd = _ci_pip_audit_run_line()
    assert ci_cmd in doc, (
        f"docs/DEPENDENCY_AUDIT.md must contain the ci.yml pip-audit line verbatim:\n{ci_cmd!r}"
    )
    ci_ids = _ignore_vuln_ids_from_pip_audit_cli(ci_cmd)
    assert ci_ids, (
        "ci.yml pip-audit line should declare at least one --ignore-vuln when used"
    )
    for vid in ci_ids:
        assert vid in doc, (
            f"ignored CVE {vid!r} must be documented in DEPENDENCY_AUDIT.md"
        )


def test_d3_local_reproduction_and_triage_commands() -> None:
    """D3: **venv**, editable **dev** install, **CI**-equivalent **pip-audit**, optional no-ignore run."""
    text = _DEPENDENCY_AUDIT.read_text(encoding="utf-8")
    assert "python -m venv" in text
    assert 'pip install -e ".[dev]"' in text
    ci_cmd = _ci_pip_audit_run_line()
    assert ci_cmd in text
    assert "pip-audit --desc" in text
    # Triage without repo ignores (second fenced block in "Reproduce locally")
    assert re.search(r"pip-audit\s+--desc", text)


def test_d4_d5_d6_reading_failures_and_fix_paths() -> None:
    """D4–D6: read failures; bump / transitive / **pyproject**; upstream vs pin + **CHANGELOG**."""
    text = _DEPENDENCY_AUDIT.read_text(encoding="utf-8")
    assert "## Reading a failure" in text
    for needle in ("CVE", "pyproject.toml", "transitive", "direct"):
        assert needle in text, f"missing D4/D5 keyword: {needle!r}"
    lower = text.lower()
    assert "bump" in lower
    assert "upstream" in lower
    assert "CHANGELOG" in text
    assert "PEP 508" in text


def test_d7_overrides_section_and_ignore_policy() -> None:
    """D7: **--ignore-vuln** rules and stable **Documented vulnerability overrides** heading."""
    text = _DEPENDENCY_AUDIT.read_text(encoding="utf-8")
    assert "## Documented vulnerability overrides" in text
    assert "#documented-vulnerability-overrides" in text
    assert "--ignore-vuln" in text
    assert ".github/workflows/ci.yml" in text


def test_d8_d9_cross_links_and_readme_troubleshooting() -> None:
    """D8–D9: **FRONTEND_SUPPLY_CHAIN**, **DESIGN_PRINCIPLES**, **compat**; **README** troubleshooting."""
    dep = _DEPENDENCY_AUDIT.read_text(encoding="utf-8")
    assert "FRONTEND_SUPPLY_CHAIN.md" in dep
    assert "DESIGN_PRINCIPLES.md" in dep
    assert "compat.md" in dep

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Troubleshooting" in readme
    assert "docs/DEPENDENCY_AUDIT.md" in readme

    principles = (REPO_ROOT / "docs" / "DESIGN_PRINCIPLES.md").read_text(
        encoding="utf-8"
    )
    assert "DEPENDENCY_AUDIT.md" in principles

    digest = (REPO_ROOT / "docs" / "compat.md").read_text(encoding="utf-8")
    assert "DEPENDENCY_AUDIT.md" in digest
    assert "EX-SUPPLY-CHAIN" in digest


def test_d10_changelog_unreleased_mentions_dependency_audit_doc() -> None:
    """D10: **Unreleased** records the playbook (contract mirrors **A5** in supply-chain tests)."""
    unreleased = _unreleased_changelog_slice()
    assert "DEPENDENCY_AUDIT" in unreleased
