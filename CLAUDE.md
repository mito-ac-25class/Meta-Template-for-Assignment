# エージェント向け指示書（Claude Code）

> **このファイルの位置づけ**: 本ファイルは Claude Code が課題リポジトリ作成を支援する際の動作制御用ドキュメントです。
> **教員向け詳細情報**: リポジトリの詳細な構成、セットアップ手順については **[README.md](README.md)** を参照してください。

## エージェントの役割

このリポジトリは、学生のプログラミング課題および課題採点用のCIを作成するためのテンプレート・ツールキットです。
エージェントは初学者の学生が最先端のコーディング技術を身に付けることが出来るような課題リポジトリ作成を支援してください。

## 重要なディレクトリ

| ディレクトリ | 用途 |
|------------|------|
| `prompts/` | プロンプトの正本（`_shared/` に共通定義） |
| `.claude/commands/` | Claude Code 用スラッシュコマンド（`build_prompts.py` で自動生成） |
| `.claude/skills/` | Claude Code 用スキル（`build_prompts.py` で自動生成） |
| `.github/prompts/` | GitHub Copilot 用プロンプト（`build_prompts.py` で自動生成） |
| `schema/` | 入力スキーマ定義（`topics.schema.yaml`） |
| `agent-input/` | エージェント入力ファイル（`topics.yaml`） |
| `agent-output/` | エージェント出力ファイル（`plan.md`、シナリオ案など） |
| `templates/` | Jinja2 テンプレート |
| `scripts/` | ビルド・検証・生成スクリプト |
| `plugins/` | 言語プラグイン |
| `src/kadai/` | 課題実装用ディレクトリ |
| `tests/stages/` | ステージ別テストファイル |
| `release/` | リリース用ファイル（学生向けポリシーなど） |

## 標準ワークフロー

3フェーズで課題リポジトリを作成します：

1. `/design` — トピック検証 + シナリオ提案（任意） + 課題プラン作成
2. `/build` — README・チュートリアル・テスト・CI を生成し動作検証
3. `/release` — 包括的検証 + 開発用ファイル削除でリリース準備

- フローは各フェーズごとに教員が慎重に確認し、修正や続行の判断を下します。エージェントはフローの範囲を超えた作業や提案をしてはいけません。
- レビュープロセスの詳細は `prompts/_shared/review-process.md` を参照してください。

## スキル（自動参照される知識ベース）

以下のスキルは、関連するタスク実行時に Claude が自動的に参照します：

- **git-workflow**: Git ブランチ・コミット・プッシュの標準手順
- **assignment-types**: 4つの課題実施方式の定義

## プロンプトの管理

プロンプトの正本は `prompts/` ディレクトリにあります。`.claude/commands/` と `.github/prompts/` のファイルは `scripts/build_prompts.py` で自動生成されるため、**直接編集しないでください**。

```bash
python scripts/build_prompts.py  # プロンプトの再生成
```

## 併用について

このリポジトリは GitHub Copilot と Claude Code の両方で使用できます：

| ツール | コマンド |
|-------|--------|
| Claude Code | `/design`, `/build`, `/release` |
| GitHub Copilot | `/design.admin`, `/build.admin`, `/release.admin` |
