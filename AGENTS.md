# エージェント向け指示書

> **このファイルの位置づけ**: 本ファイルは AGENTS.md を読むエージェント（Codex / GitHub Copilot など）が課題リポジトリ作成を支援する際の動作制御用ドキュメントです。
> **教員向け詳細情報**: リポジトリの詳細な構成、セットアップ手順については **[README.md](README.md)** を参照してください。

## エージェントの役割

このリポジトリは、学生のプログラミング課題および課題採点用のCIを作成するためのテンプレート・ツールキットです。
エージェントは初学者の学生が最先端のコーディング技術を身に付けることが出来るような課題リポジトリ作成を支援してください。

## 重要なディレクトリ

| ディレクトリ | 用途 |
|------------|------|
| `prompts/` | プロンプトの正本（`_shared/` に共通定義） |
| `.agents/skills/` | Codex 用スキル（`build_prompts.py` で自動生成） |
| `.github/prompts/` | GitHub Copilot 用プロンプト（`build_prompts.py` で自動生成） |
| `.claude/commands/`, `.claude/skills/` | Claude Code 用生成物（`build_prompts.py` で自動生成） |
| `schema/` | 入力スキーマ定義（`topics.schema.yaml`） |
| `agent-input/` | エージェント入力ファイル（`topics.yaml`） |
| `agent-output/` | エージェント出力ファイル（`plan.md`、シナリオ案など） |
| `templates/` | Jinja2 テンプレート |
| `scripts/` | ビルド・検証・生成スクリプト |
| `plugins/` | 技術スタック別プラグイン（`python/`, `django-react/` 等） |
| `src/kadai/` | 課題実装用ディレクトリ |
| `tests/stages/` | ステージ別テストファイル |
| `release/` | リリース用ファイル（学生向けポリシーなど） |

## 標準ワークフロー

3フェーズで課題リポジトリを作成します：

| ツール | Design | Build | Release |
|-------|--------|-------|---------|
| Codex | `$design-admin` | `$build-admin` | `$release-admin` |
| GitHub Copilot | `/design.admin` | `/build.admin` | `/release.admin` |

- フローは各フェーズごとに教員が慎重に確認し、修正や続行の判断を下します。エージェントはフローの範囲を超えた作業や提案をしてはいけません。
- レビュープロセスの詳細は `prompts/_shared/review-process.md` を参照してください。

## Codex での利用

- Codex では custom slash command ではなく、repo-local な `.agents/skills/` を使います。
- Design / Build / Release は `$design-admin`, `$build-admin`, `$release-admin` を明示的に起動してください。
- 共有知識として `assignment-types`, `git-workflow` を利用できます。

## プロンプトの管理

プロンプトの正本は `prompts/` ディレクトリにあります。`.agents/skills/`、`.claude/commands/`、`.claude/skills/`、`.github/prompts/` は `scripts/build_prompts.py` で自動生成されるため、**直接編集しないでください**。

```bash
python scripts/build_prompts.py  # プロンプトの再生成
```
