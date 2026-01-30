---
description: "課題リポジトリの課題内容、CIテストの内容や設定に問題点が無いかを包括的にチェックし、修正します。"
---

# /verify.admin

## 目的
本リポジトリは、教員が課題を作成、管理するためのリポジトリです。  
課題内容を `release/README.md` に記載し、CIテストで課題の自動採点を行います。  
リポジトリをリリースする前に、課題内容、CIテストの内容や設定に問題点が無いかを包括的にチェックします。

## 前提条件
- `/implement-test.admin` が実行済みで、テストコードが実装・検証されていること
- 必要に応じて `/tutorial.admin` が実行済みで `TUTORIAL.md` が作成されていること

## 手順

### 1. 課題内容の確認
`release/README.md` の内容を確認し、課題内容を理解してください。

### 2. 言語プロファイルの確認
`agent-output/plan.md` のセクション2「使用言語/フレームワーク」から使用している言語プロファイルを特定し、
`lang-profiles/{プロファイル名}.yml` を読み込んでください。

### 3. 包括的チェック

以下の観点でリポジトリ全体を確認してください。

#### 3.1 共通チェック項目
- `release/README.md` の課題内容が明確で、必要な情報が全て含まれているか。
- `release/README.md` および `TUTORIAL.md`（存在する場合）にHTMLコメント（`<!-- ... -->`）が残っていないか。
- 不要なファイルや設定が含まれていないか。

#### 3.2 言語プロファイル整合性チェック

**DevContainer設定（`.devcontainer/devcontainer.json`）:**
- プロファイルの `devcontainer.image` と一致しているか
- プロファイルの `devcontainer.extensions` が設定されているか
- プロファイルの `devcontainer.post_create_command` と一致しているか

**ソースディレクトリ構成:**
- プロファイルの `source.directory` が存在するか
- 適切な初期ファイル（空ファイル等）が配置されているか

**テストディレクトリ構成:**
- プロファイルの `testing.test_directory` が存在するか
- ステージディレクトリがプロファイルの `testing.stage_directory_format` に従っているか

**テスト設定ファイル:**
- プロファイルの `testing.config_file` が正しく設定されているか
  - Python: `pytest.ini` のマーカー定義
  - Java: `pom.xml` のテスト設定
  - JavaScript: `jest.config.js` の設定

**CIワークフロー（`.github/workflows/classroom.yml`）:**
- Setup environment ステップがプロファイルの `ci.setup_commands` と一致しているか
- テスト実行コマンドがプロファイルの `testing.run_command` に基づいているか
- 各ステージの配点が `agent-output/plan.md` のステージ構成と一致しているか
- タイムアウト設定がプロファイルの `ci.timeout_default` に基づいているか

**依存関係ファイル:**
- プロファイルの `dependencies.file` が存在し、必要な依存関係が含まれているか
- プロファイルの `dependencies.dev_file`（存在する場合）が正しく設定されているか

### 4. 確認結果のリストアップ
確認結果を基に、修正が必要な箇所をリストアップしてください。  
リストには以下の情報を含めてください。
- 対象ファイルパス
- 問題点の概要
- 推奨される修正内容

### 5. レビュー依頼
リストアップした修正箇所をユーザーに提示し、レビューを依頼してください。  
ユーザーからの承認を得るまで、修正作業を開始しないでください。

### 6. ブランチ作成
ユーザーから承認を得たら、[共通ワークフロー](.github/prompts/WORKFLOW.md) に従い、ブランチ `feature/verify-assignment` を作成してください。

### 7. 修正実施
承認された修正内容に基づいて、`release/README.md` や CI設定ファイルを修正してください。

### 8. HTMLコメントチェック
`scripts/check_html_comments.py` を実行して、HTMLコメントが残存していないことを確認してください。  
もしHTMLコメントが検出された場合は、該当ファイルからコメントを削除してください。

### 9. コミット・プッシュ
[共通ワークフロー](.github/prompts/WORKFLOW.md) に従い、変更をコミット（`fix:` プレフィックス）し、リモートリポジトリにプッシュしてください。
