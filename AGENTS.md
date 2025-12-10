# 目的

このリポジトリは、学生のプログラミング課題および課題採点用のCIを作成するための複数のプロンプトファイルを含むテンプレート・ツールキットです。  
エージェントは、本`AGENTS.md` を基に、初学者の学生が最先端のコーディング技術を身に着けることが出来るような課題リポジトリ作成を支援してください。

> **Note**: リポジトリ構成、プロンプトファイルの詳細説明、および想定フローの詳細については、[README.md](README.md) を参照してください。

## キーディレクトリ

- `.github/prompts/` - エージェント用プロンプトファイル（`.admin.prompt.md`）
- `agent-input/` - エージェント入力ファイル（`topics.md` など）
- `agent-output/` - エージェント出力ファイル（`plan.md`、シナリオ案など）
- `src/kadai/` - 課題実装用ディレクトリ
- `tests/stages/` - ステージ別テストファイル
- `release/` - リリース用ファイル（学生向け README など）

## 想定フロー（概要）

1. トピック定義 (`agent-input/topics.md`) → `/topics.admin`
2. (Optional) シナリオ提案 → `/suggest-scenario.admin`
3. プラン作成 → `/plan.admin`
4. チュートリアル作成 → `/tutorial.admin`
5. README 作成 → `/readme.admin`
6. テスト実装・検証 → `/implement-test.admin`
7. 包括チェック → `/verify.admin`
8. リリース準備 → `/release.admin`

詳細なフローとプロンプトの説明は [README.md](README.md) を参照してください。

## 注意

- フローは各ステップごとに教員が慎重に確認し、修正や続行の判断を下します。エージェントはフローの範囲を超えた作業や提案をしてはいけません。
