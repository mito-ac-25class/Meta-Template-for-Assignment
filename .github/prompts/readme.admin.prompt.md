---
description: "release/README.md に記載する課題の説明文を作成します。"
---

# /readme.admin

## 目的
`/readme.admin` では、課題の実施プランを `agent-output/plan.md` から取得し、  
学生が課題を理解しやすいように、`release/README.md` に記載する課題の説明文を作成します。

## 前提条件
- `/plan.admin` が実行済みで `agent-output/plan.md` が作成されていること

## 手順

### 1. プランと言語プロファイルの読み込み

`agent-output/plan.md` を読み込み、以下の情報を取得します：
- 学習トピック一覧
- 使用言語/フレームワーク（プロファイル名）
- テストシナリオ（ステージ構成）
- 動作例

`agent-output/plan.md` のセクション2「使用言語/フレームワーク」から言語プロファイル名を取得し、
`lang-profiles/{プロファイル名}.yml` を読み込んで以下の情報を確認します：
- `source.directory`: ソースコードディレクトリ
- `source.file_extension`: ソースファイル拡張子
- `testing.test_directory`: テストディレクトリ

### 2. ブランチ作成

[共通ワークフロー](.github/prompts/WORKFLOW.md) に従い、ブランチ `feature/make-readme` を作成してください。

### 3. READMEの作成

`templates/template.README.md` を `release/README.md` にコピーします。

### 4. プレースホルダの置換

`release/README.md` の `$` プレースホルダを埋める形で、課題説明文を作成します。
- テンプレート内のコメント（`<!-- ... -->`）を参照し、各セクションの記載内容とガイドラインを確認してください。
- **言語固有の箇所について**:
  - ソースファイルのパスは言語プロファイルの `source.directory` に合わせて設定
  - コードブロックの言語指定は使用言語に合わせて設定（例: `python`, `java`, `javascript`）
  - 動作例のコードは `agent-output/plan.md` の内容を基に、使用言語で記述
  - テストディレクトリの参照は言語プロファイルの `testing.test_directory` に合わせて設定

### 5. コメントの削除

`release/README.md` 内のコメント（`<!-- ... -->`）を全て削除します。
  
### 6. コミット・プッシュ

[共通ワークフロー](.github/prompts/WORKFLOW.md) に従い、変更をコミット（`feat:` プレフィックス）し、リモートリポジトリにプッシュしてください。