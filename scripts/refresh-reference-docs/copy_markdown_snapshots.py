#!/usr/bin/env python3
"""Copy *.md from a local upstream tree into docs/reference-documentation/replayt/<version>/.

This does not download anything. Point --source at a **replayt** git checkout, extracted sdist, or
any folder tree that already contains the markdown you intend to vendor (after license review).

See docs/reference-documentation/README.md for provenance and checklist.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tomllib
from pathlib import Path


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Copy markdown files from --source into "
            "docs/reference-documentation/<subdir>/<version>/ preserving relative paths."
        )
    )
    p.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Root directory to scan for **/*.md (recursive).",
    )
    p.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (directory containing pyproject.toml). "
        "Default: walk upward from this script.",
    )
    p.add_argument(
        "--version",
        default=None,
        help="Subfolder name for this snapshot (e.g. 0.4.25). "
        "Default: replayt.__version__ from the active environment.",
    )
    p.add_argument(
        "--subdir",
        default="replayt",
        help="Directory under docs/reference-documentation/ (default: replayt).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned copies; do not write files.",
    )
    return p.parse_args(argv)


def _resolve_repo_root(explicit: Path | None) -> Path:
    if explicit is not None:
        root = explicit.resolve()
        marker = root / "pyproject.toml"
        if not marker.is_file():
            raise SystemExit(
                f"--repo-root is not a directory with pyproject.toml: {root}"
            )
        data = tomllib.loads(marker.read_text(encoding="utf-8"))
        name = data.get("project", {}).get("name")
        if name != "replayt-ux-showcase":
            raise SystemExit(
                f"--repo-root pyproject [project].name must be replayt-ux-showcase, got {name!r}"
            )
        return root

    here = Path(__file__).resolve().parent
    for p in [here, *here.parents]:
        marker = p / "pyproject.toml"
        if not marker.is_file():
            continue
        data = tomllib.loads(marker.read_text(encoding="utf-8"))
        if data.get("project", {}).get("name") == "replayt-ux-showcase":
            return p
    raise SystemExit(
        "Could not locate replayt-ux-showcase repo root. Pass --repo-root explicitly."
    )


def _default_replayt_version() -> str:
    try:
        import replayt
    except ImportError as e:  # pragma: no cover - defensive for misconfigured env
        raise SystemExit(
            "replayt is not importable; pass --version explicitly "
            "(use an environment where the pinned replayt is installed)."
        ) from e
    v = getattr(replayt, "__version__", None)
    if not v or not isinstance(v, str):
        raise SystemExit("replayt.__version__ missing or not a string; pass --version.")
    return v


def _iter_markdown_files(source_root: Path) -> list[Path]:
    root = source_root.resolve()
    if not root.is_dir():
        raise SystemExit(f"--source must be a directory: {root}")
    out: list[Path] = []
    for p in root.rglob("*.md"):
        if any(part.startswith(".") for part in p.relative_to(root).parts):
            continue
        out.append(p)
    return sorted(out)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    repo_root = _resolve_repo_root(args.repo_root)
    version = args.version if args.version is not None else _default_replayt_version()
    dest_root = repo_root / "docs" / "reference-documentation" / args.subdir / version

    md_files = _iter_markdown_files(args.source)
    if not md_files:
        print("No *.md files found under --source.", file=sys.stderr)
        return 1

    source_root = args.source.resolve()
    for src in md_files:
        rel = src.relative_to(source_root)
        dest = dest_root / rel
        if args.dry_run:
            print(f"copy: {src} -> {dest}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    if not args.dry_run:
        print(f"Wrote {len(md_files)} file(s) under {dest_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
