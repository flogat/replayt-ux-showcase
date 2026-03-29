"""Contract tests: root package.json matches docs/examples/build.md (B1–B4, pin band).

Normative spec: docs/examples/build.md — Deliverables B1–B8; DESIGN_PRINCIPLES — optional private bundler recipe.
CI remains pytest-first: no npm steps in .github/workflows/ci.yml (see test_ci_workflow_has_no_npm_steps).
"""

from __future__ import annotations

import json
from pathlib import Path

import tomllib
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.version import Version

REPO_ROOT = Path(__file__).resolve().parents[1]


def _pyproject_replayt_specifier() -> SpecifierSet:
    raw = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    project = tomllib.loads(raw)["project"]
    lines = [
        d for d in project["dependencies"] if d.strip().lower().startswith("replayt")
    ]
    assert len(lines) == 1
    req = Requirement(lines[0].strip())
    return req.specifier


def _package_json() -> dict:
    path = REPO_ROOT / "package.json"
    assert path.is_file(), (
        "expected repository-root package.json (docs/examples/build.md B1)"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def test_package_json_is_private_with_non_publishing_name() -> None:
    data = _package_json()
    assert data.get("private") is True
    name = data.get("name", "")
    assert name != "replayt-ux-showcase", (
        "npm name must not read as the published showcase package (build.md B1)"
    )
    assert name


def test_package_json_has_build_and_preview_or_dev_scripts() -> None:
    data = _package_json()
    scripts = data.get("scripts") or {}
    assert "build" in scripts, "package.json must define a build script (build.md B4)"
    assert "dev" in scripts or "preview" in scripts, (
        "package.json must define dev or preview for local verification (build.md B4)"
    )
    assert "dev" in scripts and "preview" in scripts


def test_package_json_replayt_dependency_within_pyproject_band() -> None:
    """npm replayt range must not admit versions outside pyproject replayt PEP 508 range."""
    data = _package_json()
    deps = data.get("dependencies") or {}
    assert "replayt" in deps, "replayt must be a direct dependency (build.md B3)"
    npm_range = deps["replayt"].strip()
    assert npm_range == ">=0.1.0 <0.5.0", (
        "keep npm replayt aligned with pyproject.toml replayt>=0.1.0,<0.5.0 "
        f"(exact string for review); got {npm_range!r}"
    )

    showcase_spec = _pyproject_replayt_specifier()
    for v in (Version("0.1.0"), Version("0.4.25")):
        assert showcase_spec.contains(v), (
            f"probe {v} should satisfy pyproject replayt spec"
        )
    assert not showcase_spec.contains(Version("0.5.0"))
    assert not showcase_spec.contains(Version("0.0.1"))


def test_bundler_preview_sources_exist() -> None:
    """Minimal esbuild recipe (build.md B2, B5)."""
    for rel in (
        "scripts/replayt-bundler-preview/entry.mjs",
        "scripts/replayt-bundler-preview/build.mjs",
        "scripts/replayt-bundler-preview/serve.mjs",
        "scripts/replayt-bundler-preview/index.html",
    ):
        assert (REPO_ROOT / rel).is_file(), f"missing {rel}"


def test_ci_workflow_has_no_npm_steps() -> None:
    """Default CI stays pytest-first (build.md B7)."""
    ci = (REPO_ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "npm ci" not in ci
    assert "npm install" not in ci
    assert "actions/setup-node" not in ci


def test_readme_mentions_optional_package_json_and_build_doc() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "package.json" in readme
    assert "docs/examples/build.md" in readme
