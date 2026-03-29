"""Contract tests: integrator-facing replayt pins under docs/examples/ stay in pyproject range.

Normative spec: docs/DESIGN_PRINCIPLES.md — Vanilla examples: integrator-facing replayt pins.
Scans **HTML**, **Markdown**, **Vue SFC**, and **Svelte** sources under **docs/examples/** for CDN **replayt@…** segments
and inline PEP 508-style **replayt** requirement fragments.

Intersection / subset rule (PEP 508 snippets)
    Full range algebra is optional. This module uses a **probe grid** of :class:`packaging.version.Version`
    values plus any exact ``==`` versions parsed from the snippet string. For each probe *v*, if *v* satisfies
    the snippet's specifier set, it must satisfy the showcase ``replayt`` specifier from ``pyproject.toml``.
    The snippet must also match at least one probe (non-empty intent). If a real allowed version falls
    outside the grid, add it to :data:`_EXTRA_PROBE_VERSIONS` or extend the generator in the same change set
    as the new example.

Opt-out: the line immediately before a URL line, ``<script src=…>`` line, or fenced markdown block may be
``<!-- replayt-examples:pin-exempt -->`` (optional ``reason="..."``); that unit is not scanned for pins.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import tomllib
from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import InvalidSpecifier
from packaging.version import InvalidVersion, Version

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_ROOT = REPO_ROOT / "docs" / "examples"

_EXEMPT_LINE = re.compile(
    r"^\s*<!--\s*replayt-examples:pin-exempt(?:\s+reason=\"[^\"]*\")?\s*-->\s*$"
)

# CDN / npm-style path segment: replayt@<version> (PEP 440-ish; no 'latest')
_CDN_REPLAYT_AT = re.compile(r"(?i)replayt@(\d[\w.-]*)")

_REPLAYT_WORD = re.compile(r"\breplayt\b", re.IGNORECASE)


def _pyproject_replayt_requirement() -> Requirement:
    raw = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    project = tomllib.loads(raw)["project"]
    lines = [
        d for d in project["dependencies"] if d.strip().lower().startswith("replayt")
    ]
    assert len(lines) == 1, (
        "expected exactly one replayt dependency line in pyproject.toml"
    )
    return Requirement(lines[0].strip())


def _version_probe_grid() -> list[Version]:
    """Versions used to approximate 'snippet allowed ⊆ showcase allowed'."""
    out: list[Version] = []
    for minor in range(0, 6):
        for patch in (0, 1, 2, 5, 9, 10, 15, 25, 99, 999):
            try:
                out.append(Version(f"0.{minor}.{patch}"))
            except InvalidVersion:
                pass
    for s in (
        "0.0.1",
        "0.5.0a1",
        "0.5.0b1",
        "0.5.0rc1",
        "0.5.0",
        "0.6.0",
        "1.0.0",
    ):
        out.append(Version(s))
    # de-dupe preserving order
    seen: set[Version] = set()
    unique: list[Version] = []
    for v in out:
        if v not in seen:
            seen.add(v)
            unique.append(v)
    return unique


_EXTRA_PROBE_VERSIONS: tuple[str, ...] = ()


def _probes_for_requirement(req: Requirement, base: list[Version]) -> list[Version]:
    probes = list(base)
    for lit in _EXTRA_PROBE_VERSIONS:
        try:
            probes.append(Version(lit))
        except InvalidVersion:
            pass
    text = str(req.specifier)
    for m in re.finditer(r"==\s*([^\s,]+)", text):
        try:
            probes.append(Version(m.group(1).strip("\"'")))
        except InvalidVersion:
            pass
    seen: set[Version] = set()
    out: list[Version] = []
    for v in probes:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def _assert_pep508_snippet_inside_showcase(
    snippet: Requirement, showcase: Requirement, path: Path, line_no: int
) -> None:
    if snippet.name.lower() != "replayt":
        return
    if not snippet.specifier:
        return
    probes = _probes_for_requirement(snippet, _version_probe_grid())
    any_in_snippet = False
    violations: list[str] = []
    for v in probes:
        if v in snippet.specifier:
            any_in_snippet = True
            if v not in showcase.specifier:
                violations.append(str(v))
    assert any_in_snippet, (
        f"{path}:{line_no}: PEP 508 snippet {snippet!s} matched no probe versions "
        f"(extend tests/test_docs_examples_replayt_pins.py probes if this is a valid range)."
    )
    assert not violations, (
        f"{path}:{line_no}: snippet {snippet!s} allows probe version(s) outside "
        f"pyproject.toml replayt range {showcase.specifier!s}: {violations}"
    )


def _assert_cdn_version_inside_showcase(
    ver: str, showcase: Requirement, path: Path, line_no: int
) -> None:
    try:
        v = Version(ver)
    except InvalidVersion as e:
        pytest.fail(
            f"{path}:{line_no}: not a PEP 440 version in CDN pin replayt@{ver!r}: {e}"
        )
    assert v in showcase.specifier, (
        f"{path}:{line_no}: CDN pin replayt@{ver} is outside pyproject.toml replayt range "
        f"{showcase.specifier!s}"
    )


def _replayt_requirements_from_line(line: str) -> list[Requirement]:
    """Parse replayt PEP 508 fragments; skip bare name mentions (no specifier)."""
    out: list[Requirement] = []
    pos = 0
    while pos < len(line):
        m = _REPLAYT_WORD.search(line, pos)
        if not m:
            break
        start = m.start()
        before = line[max(0, start - 1) : start]
        if before and (before[-1].isalnum() or before[-1] in "._-"):
            pos = start + 1
            continue
        sub = line[start:].split("#", 1)[0]
        matched = False
        for length in range(len(sub), len("replayt") + 1, -1):
            raw = sub[:length]
            frag = raw.strip().rstrip(",;)]}\"'")
            if len(frag) <= len("replayt"):
                continue
            try:
                req = Requirement(frag)
            except (InvalidRequirement, InvalidSpecifier):
                continue
            if req.name.lower() != "replayt" or not req.specifier:
                continue
            out.append(req)
            matched = True
            pos = start + length
            break
        if not matched:
            pos = start + 1
    return out


def _lines_to_scan(path: Path) -> list[tuple[int, str]]:
    """Return (1-based line number, text) pairs that are subject to pin detection."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out: list[tuple[int, str]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if _EXEMPT_LINE.match(line):
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i >= len(lines):
                break
            nxt = lines[i].strip()
            if nxt.startswith("```"):
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    i += 1
                if i < len(lines):
                    i += 1
            else:
                i += 1
            continue
        out.append((i + 1, line))
        i += 1
    return out


def _collect_violations(path: Path, showcase: Requirement) -> list[str]:
    errors: list[str] = []
    for line_no, line in _lines_to_scan(path):
        for m in _CDN_REPLAYT_AT.finditer(line):
            ver = m.group(1)
            try:
                _assert_cdn_version_inside_showcase(ver, showcase, path, line_no)
            except AssertionError as e:
                errors.append(str(e))
        for req in _replayt_requirements_from_line(line):
            try:
                _assert_pep508_snippet_inside_showcase(req, showcase, path, line_no)
            except AssertionError as e:
                errors.append(str(e))
    return errors


def _iter_example_files() -> list[Path]:
    if not EXAMPLES_ROOT.is_dir():
        return []
    found: list[Path] = []
    for pattern in ("*.html", "*.md", "*.vue", "*.svelte"):
        found.extend(EXAMPLES_ROOT.rglob(pattern))
    return sorted({p.resolve() for p in found if p.is_file()})


def test_docs_examples_replayt_pins_match_pyproject() -> None:
    """Every machine-extractable replayt pin in docs/examples is inside the declared replayt range."""
    showcase = _pyproject_replayt_requirement()
    files = _iter_example_files()
    all_errors: list[str] = []
    for path in files:
        all_errors.extend(_collect_violations(path, showcase))
    assert not all_errors, "docs/examples replayt pin contract failed:\n" + "\n".join(
        all_errors
    )


def test_contract_scans_expected_example_files() -> None:
    """Guardrail: keep at least the known vanilla + framework examples under scan (scope regression)."""
    paths = {p.relative_to(REPO_ROOT) for p in _iter_example_files()}
    assert Path("docs/examples/basic-player.html") in paths, (
        f"expected docs/examples/basic-player.html in scan set, got {sorted(paths)!r}"
    )
    assert Path("docs/examples/vue/index.html") in paths
    assert Path("docs/examples/svelte/index.html") in paths


def test_pin_exempt_skips_following_cdn_line(tmp_path: Path) -> None:
    showcase = _pyproject_replayt_requirement()
    p = tmp_path / "narrative.html"
    p.write_text(
        '<!-- replayt-examples:pin-exempt reason="migration demo" -->\n'
        '<script src="https://cdn.jsdelivr.net/npm/replayt@9.0.0/dist/player.min.js"></script>\n',
        encoding="utf-8",
    )
    assert _collect_violations(p, showcase) == []


def test_pin_exempt_skips_following_fenced_block(tmp_path: Path) -> None:
    showcase = _pyproject_replayt_requirement()
    p = tmp_path / "narrative.md"
    p.write_text(
        "<!-- replayt-examples:pin-exempt -->\n```txt\nreplayt>=9.0.0\n```\n",
        encoding="utf-8",
    )
    assert _collect_violations(p, showcase) == []


def test_cdn_pin_outside_showcase_range_is_error(tmp_path: Path) -> None:
    showcase = _pyproject_replayt_requirement()
    p = tmp_path / "bad.html"
    p.write_text(
        '<script src="https://cdn.jsdelivr.net/npm/replayt@9.0.0/dist/player.min.js"></script>\n',
        encoding="utf-8",
    )
    err = _collect_violations(p, showcase)
    assert len(err) == 1
    assert "9.0.0" in err[0]
