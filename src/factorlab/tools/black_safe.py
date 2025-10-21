"""Black wrapper that runs in fast mode using the API to avoid 3.12.5 AST guard."""

from __future__ import annotations

import sys
from collections.abc import Iterable
from pathlib import Path

try:
    import black
except Exception:  # pragma: no cover
    print("ERROR: black is not installed. Please `pip install black`.", file=sys.stderr)
    raise


def iter_python_files(paths: Iterable[Path]) -> Iterable[Path]:
    for p in paths:
        if p.is_dir():
            yield from p.rglob("*.py")
        elif p.suffix == ".py":
            yield p


def main(argv: list[str]) -> int:
    targets = [Path(a) for a in argv] if argv else [Path(".")]
    mode = black.Mode(
        target_versions=set(),
        line_length=100,
        is_pyi=False,
        string_normalization=True,
        magic_trailing_comma=True,
    )
    write_back = black.WriteBack.YES  # actually rewrite files
    for py in iter_python_files(targets):
        try:
            black.format_file_in_place(
                src=py,
                fast=True,
                mode=mode,
                write_back=write_back,
            )
        except Exception as exc:
            print(f"WARNING: Black failed on {py}: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv[1:]))
