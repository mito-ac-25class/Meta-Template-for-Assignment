---
description: "リリース準備: 包括的検証を行い、開発用ファイルを削除して学生向けリポジトリを完成させます"
allowed-tools: Read, Edit, Write, Bash, Glob, Grep
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

{{GIT_WORKFLOW}}

**ブランチ名:** `feature/release-assignment`

```bash
git checkout -b feature/release-assignment
git add -A
git commit -m "clean: prepare repository for student release"
git push origin feature/release-assignment
```

{{REVIEW_PROCESS}}
