---
description: "リリース準備: 包括的検証を行い、開発用ファイルを削除して学生向けリポジトリを完成させます"
---

# /release コマンド

課題のリリースフェーズを実行します。包括的な検証を行った後、開発用ファイルを削除して学生向けリポジトリを完成させます。

## 入力

- /design と /build で作成された全ファイル

## 出力

- 学生向けにクリーンアップされたリポジトリ

## 手順

### Step 1: 包括的検証

以下の観点で課題リポジトリ全体を検証します。

#### 1a. ドキュメント検証

- `release/README.md` が明確で完全か
- `TUTORIAL.md`（該当時）が段階的で適切か
- HTML コメント（`<!-- ... -->`）が残っていないか
- プレースホルダー（`$変数名`、`{{ 変数名 }}`）が残っていないか

#### 1b. テスト検証

- テストがプランのステージ構成を正確に反映しているか
- 各ステージのテストが適切に分離されているか
- テストデコレータ（`@pytest.mark.stageXX`）が正しいか

#### 1c. CI 検証

- `.github/workflows/classroom.yml` のステージ数がテストと一致するか
- 点数配分が `topics.yaml` と一致するか

#### 1d. ファイル構成検証

- 不要なファイルが含まれていないか
- 必須ファイル（`release/README.md`, `release/student.AGENTS.md`）が存在するか

### Step 2: 問題の報告

検証で問題が見つかった場合、以下の形式で教員に報告します:

| 対象ファイル | 問題の概要 | 推奨する修正 |
|------------|-----------|------------|
| `release/README.md` | ステージ3の説明が不明瞭 | 具体例を追加 |

教員の承認を得てから修正を実施してください。

### Step 3: 問題の修正

承認された修正を実施します。修正後、再度検証を行い問題がないことを確認します。

### Step 4: リリース実行

リリーススクリプトを実行して開発用ファイルを削除します。

```bash
python scripts/release.py
```

リリーススクリプトは以下を実行します:

**ファイルの移動:**
- `release/student.AGENTS.md` → `AGENTS.md`
- `release/student.CLAUDE.md` → `CLAUDE.md`（存在する場合）
- `release/README.md` → `README.md`

**ファイルの削除（`.releaseignore` に基づく）:**
- `prompts/` — プロンプトソース
- `.claude/commands/`, `.claude/skills/` — 生成されたコマンド・スキル
- `.github/prompts/*.admin.prompt.md` — Copilot プロンプト
- `schema/`, `scripts/`, `plugins/` — 開発ツール
- `agent-input/`, `agent-output/`, `templates/` — 作業ファイル
- 開発用ドキュメント（`CLAUDE.md`, `AGENTS.md`, `README.md` の開発版）
- `tests/infrastructure/` — インフラテスト

### Step 5: リリース後の確認

リリース後のリポジトリに以下のファイルのみ存在することを確認:

```
README.md              (学生向け課題説明)
AGENTS.md              (AI利用ポリシー)
CLAUDE.md              (Claude Code ポリシー、存在する場合)
TUTORIAL.md            (チュートリアル、該当時)
src/kadai/__init__.py  (学生実装ディレクトリ)
tests/stages/          (ステージ別テスト)
.github/workflows/classroom.yml  (CI設定)
pyproject.toml
requirements-dev.txt
.devcontainer/
.gitignore
```

### Step 6: Git 操作

# Git ワークフロー

課題作成プロジェクトで使用する共通のGitワークフローです。

## ブランチ命名規則

| コマンド | ブランチ名 |
|---------|-----------|
| `/design` | `feature/design-assignment` |
| `/build` | `feature/build-assignment` |
| `/release` | `feature/release-assignment` |

## 基本ワークフロー

### 1. ブランチの作成

```bash
git checkout -b <ブランチ名>
```

### 2. 変更の確認とコミット

```bash
git status
git diff
git add <対象ファイル>
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

## 注意事項

- ブランチ名は各コマンドで一貫性を保つため、上記の命名規則に従ってください
- コミット前には必ず `git status` と `git diff` で変更内容を確認してください
- 不要なファイル（ビルド成果物、一時ファイルなど）がコミットされないよう注意してください


**ブランチ名:** `feature/release-assignment`

```bash
git checkout -b feature/release-assignment
git add -A
git commit -m "clean: prepare repository for student release"
git push origin feature/release-assignment
```

# レビュープロセス

各フェーズの実行後、教員は以下の3つの判断を下します。

## 判断基準

### 承認（Approve）
成果物に問題がなく、次のフェーズに進める状態。
→ PRをマージし、次のフェーズへ進む

### 修正要求（Request Changes）
成果物に修正が必要だが、フェーズのやり直しは不要。
→ 同じブランチで修正をコミットし、再レビュー

### 却下（Reject）
成果物の方向性が間違っており、フェーズをやり直す必要がある。
→ ブランチを削除し、入力ファイルを修正してから再実行

## フェーズ別レビュー観点

### /design フェーズ
- トピック定義が明確で具体的か
- 選定された課題実施方式が適切か
- ユーザーストーリーが理解しやすいか
- テストシナリオのステージ構成と点数配分が妥当か

### /build フェーズ
- README が学生にとって理解しやすいか
- チュートリアル（該当時）が段階的で適切か
- テストがプランのシナリオを正確に実装しているか
- CI設定が正しいか

### /release フェーズ
- 開発用ファイルが適切に削除されているか
- 学生向けファイルが正しく配置されているか

## 修正時の判断基準

**同じブランチで修正する場合:**
- タイポや文言の微調整
- テストケースの追加・削除（数個程度）
- CI設定の点数配分調整

**ブランチを破棄して再実行する場合:**
- 課題の方向性の大幅な変更
- テストシナリオの大規模な再構成
- 課題実施方式の変更

