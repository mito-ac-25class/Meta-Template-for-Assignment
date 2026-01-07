# エージェント向け指示書（Claude Code）

> **このファイルの位置づけ**: 本ファイルは Claude Code が課題リポジトリ作成を支援する際の動作制御用ドキュメントです。
> **教員向け詳細情報**: リポジトリの詳細な構成、セットアップ手順、各プロンプトファイルの詳しい説明については、**[README.md](README.md)** を参照してください。

## エージェントの役割

このリポジトリは、学生のプログラミング課題および課題採点用のCIを作成するためのテンプレート・ツールキットです。
エージェントは初学者の学生が最先端のコーディング技術を身に付けることが出来るような課題リポジトリ作成を支援してください。

## 重要なディレクトリ

| ディレクトリ | 用途 |
|------------|------|
| `.claude/commands/` | Claude Code 用スラッシュコマンド |
| `.claude/skills/` | Claude Code 用スキル（知識ベース） |
| `.github/prompts/` | GitHub Copilot 用プロンプトファイル（`.admin.prompt.md`） |
| `agent-input/` | エージェント入力ファイル（`topics.md` など） |
| `agent-output/` | エージェント出力ファイル（`plan.md`、シナリオ案など） |
| `src/kadai/` | 課題実装用ディレクトリ |
| `tests/stages/` | ステージ別テストファイル |
| `release/` | リリース用ファイル（学生向け README など） |

## 標準ワークフロー

各コマンドは以下の順序で実行されます：

1. `/topics` - トピック定義のクリーンアップ
2. `/suggest-scenario` *(Optional)* - シナリオ案の提案
3. `/plan` - 課題プラン作成
4. `/tutorial` - チュートリアル作成
5. `/readme` - 学生向け README 作成
6. `/implement-test` - テスト実装・検証
7. `/verify` - 包括的検証
8. `/release` - リリース準備

- フローは各ステップごとに教員が慎重に確認し、修正や続行の判断を下します。エージェントはフローの範囲を超えた作業や提案をしてはいけません。
- 各ステップのレビューフロー、修正プロセス、問題発生時の対処方法については [REVIEW_FLOW.md](REVIEW_FLOW.md) を参照してください。

## スキル（自動参照される知識ベース）

以下のスキルは、関連するタスク実行時に Claude が自動的に参照します：

- **git-workflow**: Git ブランチ・コミット・プッシュの標準手順
- **assignment-types**: 4つの課題実施方式の定義

## 併用について

このリポジトリは GitHub Copilot と Claude Code の両方で使用できます：

| ツール | コマンド/プロンプト |
|-------|-------------------|
| Claude Code | `/topics`, `/plan`, `/readme` など |
| GitHub Copilot | `/topics.admin`, `/plan.admin`, `/readme.admin` など |
