#!/usr/bin/env python3
"""Prepare repository for student release.

Reads .releaseignore for deletion patterns and moves release/ files to root.

Usage:
    python scripts/release.py           # Execute release
    python scripts/release.py --dry-run # Preview without changes
"""
import argparse
import fnmatch
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
RELEASEIGNORE = REPO_ROOT / ".releaseignore"
RELEASE_DIR = REPO_ROOT / "release"

# Files to move from release/ to root
RELEASE_MOVES = {
    "README.md": "README.md",
    "student.AGENTS.md": "AGENTS.md",
    "student.CLAUDE.md": "CLAUDE.md",
}


def load_patterns(path: Path) -> list[str]:
    """Load deletion patterns from .releaseignore."""
    if not path.exists():
        print(f".releaseignore not found: {path}", file=sys.stderr)
        sys.exit(1)
    patterns = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
    return patterns


def find_targets(root: Path, patterns: list[str]) -> list[Path]:
    """Find files/directories matching .releaseignore patterns."""
    targets = []
    for pattern in patterns:
        matches = sorted(root.glob(pattern))
        targets.extend(matches)
    return sorted(set(targets))


def execute_release(dry_run: bool = False) -> bool:
    """Execute the release process. Returns True on success."""
    patterns = load_patterns(RELEASEIGNORE)
    targets = find_targets(REPO_ROOT, patterns)

    # Phase 1: Move release files to root
    print("=== Move release files ===")
    for src_name, dst_name in RELEASE_MOVES.items():
        src = RELEASE_DIR / src_name
        dst = REPO_ROOT / dst_name
        if src.exists():
            print(f"  {src.relative_to(REPO_ROOT)} -> {dst_name}")
            if not dry_run:
                shutil.move(str(src), str(dst))
        else:
            print(f"  skip: {src_name} (not found)")

    # Phase 2: Delete matched files/directories
    print("\n=== Delete files ===")
    for target in targets:
        if not target.exists():
            continue
        rel = target.relative_to(REPO_ROOT)
        kind = "dir" if target.is_dir() else "file"
        print(f"  delete ({kind}): {rel}")
        if not dry_run:
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()

    # Phase 3: Clean up empty release/ directory
    if RELEASE_DIR.exists():
        remaining = list(RELEASE_DIR.iterdir())
        if not remaining:
            print(f"\n  delete (dir): {RELEASE_DIR.relative_to(REPO_ROOT)}")
            if not dry_run:
                RELEASE_DIR.rmdir()

    print("\n" + ("=== Dry run complete ===" if dry_run else "=== Release complete ==="))
    return True


def main():
    parser = argparse.ArgumentParser(description="Prepare repository for release")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview changes without executing",
    )
    args = parser.parse_args()
    success = execute_release(dry_run=args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
