"""release.py のテスト"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from release import load_patterns, find_targets, RELEASEIGNORE


def test_releaseignore_exists():
    """.releaseignore ファイルが存在することを確認"""
    assert RELEASEIGNORE.exists(), f".releaseignore が見つかりません: {RELEASEIGNORE}"


def test_releaseignore_has_patterns():
    """.releaseignore にパターンが定義されていることを確認"""
    patterns = load_patterns(RELEASEIGNORE)
    assert len(patterns) > 0


def test_releaseignore_includes_key_patterns():
    """.releaseignore に必要なパターンが含まれていることを確認"""
    patterns = load_patterns(RELEASEIGNORE)
    # 主要な削除対象が含まれていること
    assert "prompts/" in patterns
    assert "scripts/" in patterns
    assert "agent-input/" in patterns
    assert "agent-output/" in patterns
    assert "templates/" in patterns


def test_find_targets_matches(tmp_path):
    """find_targets がパターンに一致するファイルを見つけることを確認"""
    # テスト用ディレクトリ構造を作成
    (tmp_path / "prompts").mkdir()
    (tmp_path / "prompts" / "design.md").write_text("test")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "validate.py").write_text("test")
    (tmp_path / "keep.txt").write_text("keep")

    patterns = ["prompts/", "scripts/"]
    targets = find_targets(tmp_path, patterns)

    target_names = [t.name for t in targets]
    assert "prompts" in target_names
    assert "scripts" in target_names
    assert "keep.txt" not in target_names


def test_find_targets_glob_pattern(tmp_path):
    """find_targets がグロブパターンを正しく処理することを確認"""
    prompts_dir = tmp_path / ".github" / "prompts"
    prompts_dir.mkdir(parents=True)
    (prompts_dir / "build.admin.prompt.md").write_text("test")
    (prompts_dir / "keep.md").write_text("keep")

    patterns = [".github/prompts/*.admin.prompt.md"]
    targets = find_targets(tmp_path, patterns)

    assert len(targets) == 1
    assert targets[0].name == "build.admin.prompt.md"


def test_release_py_exists():
    """release.py が存在することを確認"""
    script_path = Path(__file__).parent.parent.parent / "scripts" / "release.py"
    assert script_path.exists()
