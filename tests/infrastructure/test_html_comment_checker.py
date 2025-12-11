"""
HTMLコメントチェッカースクリプトのテスト
"""
import os
import tempfile
from pathlib import Path
import sys

# スクリプトのパスをインポートパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))

from check_html_comments import find_html_comments, check_repository


def test_find_html_comments_with_comments(tmp_path):
    """HTMLコメントが含まれるファイルを正しく検出できることを確認"""
    test_file = tmp_path / "test.md"
    test_content = """# テストファイル

<!-- これはコメントです -->

本文

<!-- 
    複数行の
    コメント
-->
"""
    test_file.write_text(test_content, encoding='utf-8')
    
    comments = find_html_comments(test_file)
    
    # 2つのコメントが検出されること
    assert len(comments) == 2
    
    # 最初のコメントは3行目にあること
    assert comments[0][0] == 3
    assert "<!-- これはコメントです -->" in comments[0][1]
    
    # 2番目のコメントは7行目にあること
    assert comments[1][0] == 7


def test_find_html_comments_without_comments(tmp_path):
    """HTMLコメントが含まれないファイルで何も検出されないことを確認"""
    test_file = tmp_path / "test.md"
    test_content = """# テストファイル

本文のみ

コメントなし
"""
    test_file.write_text(test_content, encoding='utf-8')
    
    comments = find_html_comments(test_file)
    
    # コメントが検出されないこと
    assert len(comments) == 0


def test_find_html_comments_file_not_exists(tmp_path):
    """存在しないファイルに対して空のリストを返すことを確認"""
    non_existent_file = tmp_path / "non_existent.md"
    
    comments = find_html_comments(non_existent_file)
    
    # 空のリストが返ること
    assert len(comments) == 0


def test_check_repository_before_release_with_comments(tmp_path):
    """リリース前のリポジトリでHTMLコメントを検出できることを確認"""
    # リリース前の構造を作成
    release_dir = tmp_path / "release"
    release_dir.mkdir()
    
    readme = release_dir / "README.md"
    readme.write_text("# Test\n<!-- コメント -->", encoding='utf-8')
    
    # チェック実行
    result = check_repository(tmp_path)
    
    # コメントが見つかったのでFalseが返ること
    assert result is False


def test_check_repository_before_release_without_comments(tmp_path):
    """リリース前のリポジトリでHTMLコメントがない場合にパスすることを確認"""
    # リリース前の構造を作成
    release_dir = tmp_path / "release"
    release_dir.mkdir()
    
    readme = release_dir / "README.md"
    readme.write_text("# Test\n本文のみ", encoding='utf-8')
    
    # チェック実行
    result = check_repository(tmp_path)
    
    # コメントがないのでTrueが返ること
    assert result is True


def test_check_repository_after_release_with_comments(tmp_path):
    """リリース後のリポジトリでHTMLコメントを検出できることを確認"""
    # リリース後の構造を作成（release/ディレクトリがない）
    readme = tmp_path / "README.md"
    readme.write_text("# Test\n<!-- コメント -->", encoding='utf-8')
    
    # チェック実行
    result = check_repository(tmp_path)
    
    # コメントが見つかったのでFalseが返ること
    assert result is False


def test_check_repository_after_release_without_comments(tmp_path):
    """リリース後のリポジトリでHTMLコメントがない場合にパスすることを確認"""
    # リリース後の構造を作成（release/ディレクトリがない）
    readme = tmp_path / "README.md"
    readme.write_text("# Test\n本文のみ", encoding='utf-8')
    
    # チェック実行
    result = check_repository(tmp_path)
    
    # コメントがないのでTrueが返ること
    assert result is True


def test_check_repository_with_tutorial(tmp_path):
    """TUTORIAL.mdも正しくチェックできることを確認"""
    # リリース前の構造を作成
    release_dir = tmp_path / "release"
    release_dir.mkdir()
    
    readme = release_dir / "README.md"
    readme.write_text("# Test", encoding='utf-8')
    
    tutorial = tmp_path / "TUTORIAL.md"
    tutorial.write_text("# Tutorial\n<!-- コメント -->", encoding='utf-8')
    
    # チェック実行
    result = check_repository(tmp_path)
    
    # TUTORIAL.mdのコメントが見つかったのでFalseが返ること
    assert result is False


def test_check_repository_missing_files(tmp_path):
    """ファイルが存在しない場合でもエラーにならないことを確認"""
    # 空のディレクトリ（release/もない）
    
    # チェック実行（エラーにならずにTrueが返ること）
    result = check_repository(tmp_path)
    
    # ファイルがないので問題なしとしてTrueが返ること
    assert result is True


def test_script_exists():
    """チェックスクリプトが存在することを確認"""
    script_path = Path(__file__).parent.parent.parent / 'scripts' / 'check_html_comments.py'
    assert script_path.exists(), f"スクリプトが見つかりません: {script_path}"


def test_script_is_executable():
    """チェックスクリプトが実行可能であることを確認"""
    script_path = Path(__file__).parent.parent.parent / 'scripts' / 'check_html_comments.py'
    file_stat = os.stat(script_path)
    is_executable = bool(file_stat.st_mode & 0o111)  # 実行可能ビットがセットされているか
    assert is_executable, "スクリプトが実行可能ではありません"
