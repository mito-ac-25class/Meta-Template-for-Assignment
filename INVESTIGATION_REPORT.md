# リリーススクリプト調査報告書

## 調査日時
2026-01-05

## 調査概要
`scripts/release.sh` 実行時に学生に見せるべきではないファイルが削除されない問題を調査し、修正案を提案する。

## 問題となるファイル一覧

### 1. 削除されていない重要ファイル

| ファイル/ディレクトリ | 現状 | 影響 | 優先度 |
|-------------------|------|------|--------|
| `REVIEW_FLOW.md` | 削除されない | 教員向けレビュープロセスが学生に公開される | **高** |
| `scripts/README.md` | 削除されない | 管理者向けスクリプト説明が学生に公開される | **高** |
| `scripts/check_html_comments.py` | 削除されない | 検証用ツールが学生に公開される | 中 |
| `copilot.log` | 削除されない | エージェント実行ログが学生に公開される可能性 | **高** |
| `.github/prompts/WORKFLOW.md` | 削除されない | 教員向けワークフロー説明が学生に公開される | **高** |
| `.github/prompts/ASSIGNMENT_TYPES.md` | 削除されない | 教員向け課題タイプ説明が学生に公開される | **高** |
| `release/` ディレクトリ | 空のまま残る | 不要な空ディレクトリが残存 | 中 |

### 2. release/README.md の欠落問題

**重大な問題**: `scripts/release.sh` は `release/README.md` が存在することを前提としているが、現時点でこのファイルが存在しない。これにより、スクリプトが実行時にエラーで停止する。

```bash
$ ls -la release/
total 16
drwxrwxr-x  2 runner runner 4096 Jan  5 00:08 .
drwxr-xr-x 12 runner runner 4096 Jan  5 00:08 ..
-rw-rw-r--  1 runner runner 4951 Jan  5 00:08 student.AGENTS.md
```

スクリプトの該当部分（211-222行目）:
```bash
# release/README.md → README.md
if [ -f "release/README.md" ]; then
    git mv release/README.md README.md
    echo -e "${GREEN}release/README.md を README.md に移動しました。${NC}"
else
    echo -e "${RED}エラー: release/README.md が見つかりません。${NC}"
    echo -e "${RED}リリース準備を中止します。${NC}"
    echo -e "${YELLOW}ロールバック方法：${NC}"
    echo -e "  git reset --hard"
    echo -e "  git clean -fd"
    exit 1
fi
```

## 現在の削除コマンドの分析

### 削除される項目（現状）
1. `.github/prompts/*.admin.prompt.md` - 管理者用プロンプト ✓
2. `agent-input/` - エージェント入力ディレクトリ ✓
3. `agent-output/` - エージェント出力ディレクトリ ✓
4. `templates/` - テンプレートディレクトリ ✓
5. `AGENTS.md` - 開発用エージェント指示書 ✓
6. `README.md` - 開発用README ✓
7. `TUTORIAL.md` - 空の場合のみ削除 ✓
8. `tests/infrastructure/` - インフラテスト ✓

### 削除されない項目（問題あり）
1. `.github/prompts/WORKFLOW.md` - **教員向けワークフロー説明**
2. `.github/prompts/ASSIGNMENT_TYPES.md` - **教員向け課題タイプ説明**
3. `REVIEW_FLOW.md` - **教員向けレビューフロー説明**
4. `scripts/README.md` - **管理者向けスクリプト説明**
5. `scripts/check_html_comments.py` - 検証用ツール
6. `copilot.log` - エージェント実行ログ
7. `release/` ディレクトリ - 空ディレクトリとして残存

## 修正提案

### 提案1: 追加削除項目の実装

`scripts/release.sh` に以下の削除処理を追加：

```bash
# 9.5. .github/prompts/ 内の非管理者用プロンプトファイルの削除
echo -e "\n${YELLOW}[9.5/12] .github/prompts/ 内の教員向けドキュメントを削除中...${NC}"
if [ -f ".github/prompts/WORKFLOW.md" ]; then
    git rm .github/prompts/WORKFLOW.md
    echo -e "${GREEN}WORKFLOW.md を削除しました。${NC}"
fi

if [ -f ".github/prompts/ASSIGNMENT_TYPES.md" ]; then
    git rm .github/prompts/ASSIGNMENT_TYPES.md
    echo -e "${GREEN}ASSIGNMENT_TYPES.md を削除しました。${NC}"
fi

# 10. REVIEW_FLOW.md の削除
echo -e "\n${YELLOW}[10/12] REVIEW_FLOW.md を削除中...${NC}"
if [ -f "REVIEW_FLOW.md" ]; then
    git rm REVIEW_FLOW.md
    echo -e "${GREEN}REVIEW_FLOW.md を削除しました。${NC}"
else
    echo -e "${YELLOW}REVIEW_FLOW.md が見つかりません。スキップします。${NC}"
fi

# 11. scripts/ ディレクトリ全体の削除
echo -e "\n${YELLOW}[11/12] scripts/ ディレクトリを削除中...${NC}"
if [ -d "scripts" ]; then
    # 実行中のスクリプト自体があるため、削除は最後に行う
    git rm -r scripts
    echo -e "${GREEN}scripts/ ディレクトリを削除しました。${NC}"
else
    echo -e "${YELLOW}scripts/ ディレクトリが見つかりません。スキップします。${NC}"
fi

# 12. ログファイルの削除
echo -e "\n${YELLOW}[12/12] ログファイルを削除中...${NC}"
if [ -f "copilot.log" ]; then
    git rm copilot.log
    echo -e "${GREEN}copilot.log を削除しました。${NC}"
else
    echo -e "${YELLOW}copilot.log が見つかりません。スキップします。${NC}"
fi

# 13. release/ ディレクトリの削除
echo -e "\n${YELLOW}[13/13] 空の release/ ディレクトリを削除中...${NC}"
if [ -d "release" ] && [ -z "$(ls -A release)" ]; then
    git rm -r release
    echo -e "${GREEN}release/ ディレクトリを削除しました。${NC}"
else
    echo -e "${YELLOW}release/ ディレクトリが空でないか、存在しません。スキップします。${NC}"
fi
```

### 提案2: .gitignore の更新

`copilot.log` などの一時ファイルが誤ってコミットされないよう、`.gitignore` を更新：

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so

# Virtual env
.env/
.venv/
venv/

# pytest cache
.pytest_cache/

# VS Code
.vscode/

# Copilot logs
copilot.log

# Temporary files
*.tmp
*.log
```

### 提案3: release/README.md の作成確認

スクリプト実行前の事前チェックに、`release/README.md` の存在確認を追加（既に実装済み）。

## 今後の再発防止策

### 1. チェックリストの整備

リリース前チェックリストを作成し、削除すべきファイルを明確化：

- [ ] 管理者用プロンプト（`.github/prompts/*.admin.prompt.md`）
- [ ] 教員向けドキュメント（`WORKFLOW.md`, `ASSIGNMENT_TYPES.md`, `REVIEW_FLOW.md`）
- [ ] エージェント入出力ディレクトリ（`agent-input/`, `agent-output/`）
- [ ] テンプレートディレクトリ（`templates/`）
- [ ] 開発用README・AGENTS.md
- [ ] 管理スクリプト（`scripts/`）
- [ ] インフラテスト（`tests/infrastructure/`）
- [ ] ログファイル（`copilot.log`）

### 2. 自動テストの追加

`tests/infrastructure/test_release_script.py` を拡張し、以下を検証：

```python
def test_release_removes_all_admin_files():
    """リリース後に管理者向けファイルが残っていないことを確認"""
    admin_files = [
        'REVIEW_FLOW.md',
        'scripts/README.md',
        'scripts/check_html_comments.py',
        '.github/prompts/WORKFLOW.md',
        '.github/prompts/ASSIGNMENT_TYPES.md',
        'copilot.log',
    ]
    # テスト実装
```

### 3. ドキュメント整備

README.md に「学生に見せるべきではないファイル」の整理基準を明記：

- **評価用**: テストコード（`tests/infrastructure/`）、採点用スクリプト
- **採点用**: 解答例、評価基準
- **中間生成物**: エージェント出力（`agent-output/`）、ログファイル
- **管理用**: プロンプトファイル、ワークフロードキュメント、レビューフロー

### 4. リリース後の検証手順

リリース後、以下を確認：

```bash
# 1. 学生向けファイルのみが存在することを確認
ls -la

# 期待される構成:
# - README.md (学生向け)
# - AGENTS.md (学生向け)
# - TUTORIAL.md (チュートリアルがある場合)
# - src/
# - tests/stages/
# - .github/workflows/

# 2. 管理者向けファイルが存在しないことを確認
test ! -f REVIEW_FLOW.md && echo "✓ REVIEW_FLOW.md は削除済み"
test ! -d scripts && echo "✓ scripts/ は削除済み"
test ! -f .github/prompts/WORKFLOW.md && echo "✓ WORKFLOW.md は削除済み"
```

## まとめ

### 発見された問題点
1. **7つのファイル/ディレクトリが削除されていない**（うち5つは優先度高）
2. **release/README.md が存在しない**ため、スクリプトが実行不可
3. **.gitignore が不十分**でログファイルがコミットされる可能性

### 推奨される対応
1. `scripts/release.sh` に追加削除処理を実装（提案1）
2. `.gitignore` を更新してログファイルを除外（提案2）
3. 自動テストを追加して再発防止（提案3）
4. リリース後検証手順を確立（提案4）

### 影響範囲
- **学生への影響**: 教員向け情報が公開されることで、課題の意図や評価基準が漏洩する可能性
- **教員への影響**: 管理情報の漏洩、課題の信頼性低下

### 緊急度
**高**: 次回リリース前に必ず対応が必要
