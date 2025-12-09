"""
リリーススクリプトの存在と基本的な健全性をテストする
"""
import os
import stat
import subprocess


def test_release_script_exists():
    """リリーススクリプトが存在することを確認"""
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'release.sh')
    assert os.path.exists(script_path), f"リリーススクリプトが見つかりません: {script_path}"


def test_release_script_is_executable():
    """リリーススクリプトが実行可能であることを確認"""
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'release.sh')
    file_stat = os.stat(script_path)
    is_executable = bool(file_stat.st_mode & stat.S_IXUSR)
    assert is_executable, "リリーススクリプトが実行可能ではありません"


def test_release_script_has_shebang():
    """リリーススクリプトが正しいshebangを持つことを確認"""
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'release.sh')
    with open(script_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
    assert first_line == '#!/bin/bash', f"不正なshebang: {first_line}"


def test_release_script_syntax():
    """リリーススクリプトの構文が正しいことを確認"""
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'release.sh')
    result = subprocess.run(
        ['bash', '-n', script_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"スクリプトの構文エラー: {result.stderr}"


def test_release_script_contains_required_operations():
    """リリーススクリプトが必要な操作を含むことを確認"""
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'release.sh')
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 必須の操作が含まれているか確認
    required_patterns = [
        'git checkout -b',  # ブランチ作成
        '.admin.prompt.md',  # 管理者プロンプトファイルの削除
        'agent-input',  # agent-input の削除
        'agent-output',  # agent-output の削除
        'templates',  # templates の削除
        'release/evac.AGENTS.md',  # AGENTS.md の移動元
        'release/README.md',  # README.md の移動元
        'git commit',  # コミット
        'git push',  # プッシュ
    ]
    
    for pattern in required_patterns:
        assert pattern in content, f"スクリプトに必要なパターンが見つかりません: {pattern}"
