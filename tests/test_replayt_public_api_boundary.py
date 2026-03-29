"""AST guard: packaged showcase Python uses only replayt's published import surface.

Normative rules: ``docs/DESIGN_PRINCIPLES.md#normative-import-rules-showcase-python``.

Uses ``replayt.__all__`` from the installed matrix pin (0.1.0 / 0.2.0 / 0.4.25 in CI).

Does not flag dynamic access (``getattr``, ``importlib.import_module`` strings) or
non-import uses of ``replayt`` beyond simple ``import replayt`` / ``import replayt as …``
followed by one-level ``<alias>.<attr>`` loads.
"""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SHOWCASE_PY = sorted((REPO_ROOT / "src" / "replayt_ux_showcase").rglob("*.py"))

# Module introspection attributes — not replayt's integration API; omit from __all__ checks.
_MODULE_METADATA_ATTRS = frozenset(
    {
        "__path__",
        "__file__",
        "__doc__",
        "__name__",
        "__spec__",
        "__loader__",
        "__package__",
        "__cached__",
    }
)


@dataclass(frozen=True)
class _Violation:
    path: Path
    lineno: int
    detail: str


def _underscore_segment_in_replayt_module(module: str) -> bool:
    """True if the first dotted segment after ``replayt.`` starts with ``_`` (design principles rule 1)."""
    if module == "replayt":
        return False
    if not module.startswith("replayt."):
        return False
    rest = module.removeprefix("replayt.")
    first = rest.split(".", 1)[0]
    return first.startswith("_")


def _replayt_root_names(tree: ast.AST) -> set[str]:
    """Local names bound to the replayt package (import replayt / import replayt.sub …)."""
    roots: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Import):
            continue
        for alias in node.names:
            name = alias.name
            if name == "replayt" or name.startswith("replayt."):
                roots.add(alias.asname or "replayt")
    return roots


def _violations_in_tree(
    tree: ast.AST,
    source_path: Path,
    allowed: frozenset[str],
) -> list[_Violation]:
    out: list[_Violation] = []

    def add(node: ast.AST, detail: str) -> None:
        lineno = getattr(node, "lineno", 1) or 1
        out.append(_Violation(source_path, lineno, detail))

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mod = alias.name
                if mod == "replayt" or mod.startswith("replayt."):
                    if _underscore_segment_in_replayt_module(mod):
                        add(
                            node,
                            f"private replayt submodule path in import {mod!r}",
                        )
        elif isinstance(node, ast.ImportFrom):
            if (node.level or 0) != 0 or not node.module:
                continue
            mod = node.module
            if not (mod == "replayt" or mod.startswith("replayt.")):
                continue
            if _underscore_segment_in_replayt_module(mod):
                add(
                    node,
                    f"private replayt submodule path in from {mod!r} import …",
                )
            if mod == "replayt":
                if any(a.name == "*" for a in node.names):
                    add(
                        node,
                        "from replayt import * is not allowed (cannot check against __all__)",
                    )
                    continue
                for alias in node.names:
                    imported = alias.name
                    if imported not in allowed:
                        add(
                            node,
                            f"from replayt import: {imported!r} not in replayt.__all__",
                        )

    roots = _replayt_root_names(tree)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Attribute):
            continue
        if not isinstance(node.value, ast.Name) or not isinstance(node.ctx, ast.Load):
            continue
        if node.value.id not in roots:
            continue
        attr = node.attr
        if attr in _MODULE_METADATA_ATTRS:
            continue
        if attr.startswith("_") and attr not in allowed:
            add(
                node,
                f"attribute access {node.value.id!r}.{attr}: underscore name not in replayt.__all__",
            )
        elif not attr.startswith("_") and attr not in allowed:
            add(
                node,
                f"attribute access {node.value.id!r}.{attr}: {attr!r} not in replayt.__all__",
            )

    return out


def _scan_showcase(allowed: frozenset[str]) -> list[_Violation]:
    bad: list[_Violation] = []
    for path in SHOWCASE_PY:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
        bad.extend(_violations_in_tree(tree, path, allowed))
    return bad


def test_showcase_replayt_imports_respect_public_api() -> None:
    import replayt

    allowed = frozenset(replayt.__all__)
    violations = _scan_showcase(allowed)
    if violations:
        lines = [
            f"  {v.path.relative_to(REPO_ROOT)}:{v.lineno}: {v.detail}"
            for v in sorted(violations, key=lambda x: (str(x.path), x.lineno))
        ]
        pytest.fail(
            "replayt public API boundary violations:\n" + "\n".join(lines),
        )


def test_scanner_finds_private_submodule_violation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import replayt

    fake_pkg = tmp_path / "replayt_ux_showcase"
    fake_pkg.mkdir()
    bad_py = fake_pkg / "bad.py"
    bad_py.write_text("import replayt._private\n", encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "SHOWCASE_PY", [bad_py])
    v = _scan_showcase(frozenset(replayt.__all__))
    assert any("private replayt submodule" in x.detail for x in v)


def test_scanner_rejects_star_import(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import replayt

    fake_pkg = tmp_path / "replayt_ux_showcase"
    fake_pkg.mkdir()
    bad_py = fake_pkg / "bad.py"
    bad_py.write_text("from replayt import *\n", encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "SHOWCASE_PY", [bad_py])
    v = _scan_showcase(frozenset(replayt.__all__))
    assert any("import *" in x.detail for x in v)
