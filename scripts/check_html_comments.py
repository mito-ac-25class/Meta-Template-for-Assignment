#!/usr/bin/env python3
"""
HTMLコメント残存チェックスクリプト

リリース前に学生向けファイルにHTMLコメントが残っていないかをチェックします。
教員向けの指示や注意書きがHTMLコメントとして残っていると、
学生向けの成果物としては不適切なため、これを検出します。
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

# チェック対象のファイルパターン
CHECK_PATTERNS = [
    "release/README.md",
    "release/TUTORIAL.md",  # 存在する場合のみ
    "TUTORIAL.md",  # リリース後の位置
    "README.md",  # リリース後の位置（開発用のものは除外）
]

# HTMLコメントを検出する正規表現
# NOTE: この正規表現は単純なHTMLコメント（<!-- ... -->）を検出します。
# ネストしたコメントや特殊なケースには対応していませんが、
# テンプレートファイルでは単純なコメントのみを使用しているため十分です。
HTML_COMMENT_PATTERN = re.compile(r'<!--.*?-->', re.DOTALL)

# コメントプレビューの最大文字数
COMMENT_PREVIEW_LENGTH = 50


def find_html_comments(file_path: Path) -> List[Tuple[int, str]]:
    """
    指定されたファイル内のHTMLコメントを検出する
    
    Args:
        file_path: チェック対象のファイルパス
        
    Returns:
        (行番号, コメント内容)のタプルのリスト
    """
    if not file_path.exists():
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"エラー: {file_path} の読み込みに失敗しました: {e}", file=sys.stderr)
        return []
    
    comments = []
    lines = content.split('\n')
    
    # HTMLコメントを検出
    for match in HTML_COMMENT_PATTERN.finditer(content):
        comment_text = match.group(0)
        # コメントの開始位置までの改行数を数えて行番号を取得
        line_num = content[:match.start()].count('\n') + 1
        # コメントの最初のN文字を表示用に取得（長すぎる場合は省略）
        preview = comment_text[:COMMENT_PREVIEW_LENGTH] + (
            '...' if len(comment_text) > COMMENT_PREVIEW_LENGTH else ''
        )
        comments.append((line_num, preview))
    
    return comments


def check_repository(repo_root: Path) -> bool:
    """
    リポジトリ全体をチェックする
    
    Args:
        repo_root: リポジトリのルートディレクトリ
        
    Returns:
        問題がなければTrue、HTMLコメントが見つかればFalse
    """
    all_clear = True
    
    # release/README.md が存在するかで、リリース前か後かを判定
    release_readme = repo_root / "release" / "README.md"
    is_before_release = release_readme.exists()
    
    # チェック対象ファイルを決定
    if is_before_release:
        # リリース前: release/ 配下をチェック
        target_files = [
            repo_root / "release" / "README.md",
            repo_root / "TUTORIAL.md",  # チュートリアルはルートにある
        ]
    else:
        # リリース後: ルート直下をチェック
        target_files = [
            repo_root / "README.md",
            repo_root / "TUTORIAL.md",
        ]
    
    print("=" * 60)
    print("HTMLコメント残存チェック")
    print("=" * 60)
    print(f"リポジトリ: {repo_root}")
    print(f"チェックモード: {'リリース前' if is_before_release else 'リリース後'}")
    print()
    
    for file_path in target_files:
        if not file_path.exists():
            print(f"⏭️  スキップ: {file_path.relative_to(repo_root)} (ファイルが存在しません)")
            continue
        
        comments = find_html_comments(file_path)
        
        if comments:
            all_clear = False
            print(f"❌ {file_path.relative_to(repo_root)}")
            print(f"   {len(comments)}個のHTMLコメントが見つかりました:")
            for line_num, preview in comments:
                print(f"   - 行 {line_num}: {preview}")
            print()
        else:
            print(f"✅ {file_path.relative_to(repo_root)}")
    
    print("=" * 60)
    
    if all_clear:
        print("✅ チェック完了: HTMLコメントは見つかりませんでした。")
        return True
    else:
        print("❌ チェック失敗: HTMLコメントが見つかりました。")
        print()
        print("対処方法:")
        print("  1. 該当ファイルを開き、HTMLコメント (<!-- ... -->) を削除してください")
        print("  2. プレースホルダー ($変数名) は残し、コメントのみを削除します")
        print("  3. /readme.admin や /tutorial.admin は自動的にコメントを削除するはずです")
        print("  4. エージェントがコメントを削除し忘れている場合は手動で削除してください")
        return False


def main():
    """メイン処理"""
    # リポジトリのルートディレクトリを取得
    repo_root = Path(__file__).parent.parent.resolve()
    
    # チェック実行
    success = check_repository(repo_root)
    
    # 終了コードを返す
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
