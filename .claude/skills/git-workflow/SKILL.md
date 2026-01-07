---
name: git-workflow
description: |
  課題作成時のGitブランチ・コミット・プッシュの標準手順を提供します。
  ブランチ作成、コミットメッセージ作成、プルリクエスト作成時に自動参照されます。
  「ブランチを作成」「コミット」「プッシュ」などのキーワードで自動的に適用されます。
---

# Git ワークフロー

課題作成プロジェクトで使用する共通のGitワークフローです。

## ブランチ命名規則

| コマンド | ブランチ名 |
|---------|-----------|
| `/topics` | _(手動でブランチ作成、例: `feature/define-topics`)_ |
| `/suggest-scenario` | `feature/suggest-scenarios` |
| `/plan` | `feature/make-a-plan` |
| `/readme` | `feature/make-readme` |
| `/tutorial` | `feature/make-tutorial` |
| `/implement-test` | `feature/implement-tests` |
| `/verify` | `feature/verify-assignment` |
| `/release` | `feature/remove-admin-prompts` |

## 基本ワークフロー

### 1. ブランチの作成

```bash
git checkout -b <ブランチ名>
```

**注意**: `/topics` のみ、教員が `agent-input/topics.md` を手動で記入してからコマンドを実行するため、ブランチの作成も手動で行います。

### 2. 変更の確認とコミット

```bash
git status
git diff
git add .
git commit -m "<コミットメッセージ>"
```

### コミットメッセージのプレフィックス

- `add:` - 新しいファイルやコンテンツを追加した場合
- `feat:` - 新機能を追加した場合
- `fix:` - 修正を行った場合
- `update:` - 既存の内容を更新した場合
- `clean:` - クリーンアップ処理を行った場合

### 3. リモートリポジトリへのプッシュ

```bash
git push origin <ブランチ名>
```

### 4. プルリクエストの作成

GitHubのウェブインターフェースまたは `gh` コマンドでプルリクエストを作成し、レビューを依頼します。

## レビュー後の修正プロセス

### ケース1: 軽微な修正が必要な場合

タイポの修正、コメントの追加、フォーマットの調整など：

```bash
git checkout <ブランチ名>
# ファイルを編集
git add .
git commit -m "fix: レビュー指摘事項の修正"
git push origin <ブランチ名>
```

### ケース2: 大幅な修正が必要な場合

課題の方向性が間違っている、テストシナリオの大幅な再構成が必要など：

```bash
git checkout main
git branch -D <ブランチ名>
# 入力ファイルを修正後、コマンドを再実行
```

### ケース3: 前のステップに戻る必要がある場合

`/verify` で問題が見つかり、特定のステップに戻る必要がある場合は [REVIEW_FLOW.md](../../REVIEW_FLOW.md) を参照してください。

## 注意事項

- ブランチ名は各コマンドで一貫性を保つため、上記の命名規則に従ってください
- コミット前には必ず `git status` と `git diff` で変更内容を確認してください
- 不要なファイル（ビルド成果物、一時ファイルなど）がコミットされないよう注意してください
