---
description: "課題リポジトリをリリース可能な状態とするために、シェルスクリプトを使用して不要なファイルを削除し、必要なファイルを整理します。"
---

# /release.admin

## 目的
本リポジトリには、本プロンプトファイルを含む開発用やテスト用のファイルが複数含まれます。  
また、開発中は学生が課題を実施する際に Agent の動作を制限するための AGENTS.md ファイルを退避し、開発時専用の AGENTS.md を使用しています。  
リポジトリをリリース可能な状態とするために、学生にとって不要なファイルを削除し、退避中の必要なファイルを元の場所に戻す作業を行います。

**このプロンプトは、シェルスクリプトの実行をサポートするためのものです。基本的には `./scripts/release.sh` を実行してください。**

## 標準手順（推奨）

リリース準備は、以下のシェルスクリプトを実行することで自動化されています：

```bash
./scripts/release.sh
```

このスクリプトは以下の処理を自動的に行います：

1. **事前チェック**
   - 必須ファイル（`release/evac.AGENTS.md`, `release/README.md`）の存在確認
   - 未コミット変更の確認と警告
   - 実行前の確認プロンプト

2. **ブランチ作成**
   - ブランチ `feature/remove-admin-prompts` を作成
   - 既存ブランチがある場合の対応（削除/切り替え/中止の選択）

3. **ファイル削除**
   - 管理者用プロンプトファイル (`.github/prompts/*.admin.prompt.md`)
   - `agent-input/*` ディレクトリ
   - `agent-output/*` ディレクトリ
   - `templates/*` ディレクトリ
   - 開発用 `AGENTS.md` と `README.md`
   - 空の `TUTORIAL.md`（存在し、かつ空の場合のみ）
   - `tests/infrastructure/*` ディレクトリ

4. **ファイル移動**
   - `release/evac.AGENTS.md` → `AGENTS.md`
   - `release/README.md` → `README.md`

5. **コミットとプッシュ**
   - 変更をコミット（メッセージ: "fix: remove admin prompt files"）
   - リモートリポジトリにプッシュ

スクリプト実行後は、GitHub上でプルリクエストを作成し、レビュー後にmainブランチにマージしてください。

### スクリプトの主な機能

- ✅ **エラーハンドリング**: 各ステップでエラーをチェックし、問題があれば中止
- ✅ **既存ブランチ対応**: 同名ブランチが存在する場合、削除/切り替え/中止を選択可能
- ✅ **バックアップ推奨**: 実行前に確認プロンプトを表示
- ✅ **ロールバック手順**: エラー時のロールバック方法を表示

## トラブルシューティング

### スクリプト実行時のエラー対応

#### ケース1: 必須ファイルが見つからない
```
エラー: release/evac.AGENTS.md が見つかりません。
```
**対処法**: `/readme.admin` を実行して `release/README.md` を作成し、`release/evac.AGENTS.md` が正しく配置されているか確認してください。

#### ケース2: 既存ブランチが存在する
スクリプトが自動的に選択肢を提示します：
- オプション1（推奨）: 既存ブランチを削除して新規作成
- オプション2: 既存ブランチに切り替えて続行
- オプション3: スクリプトを中止

#### ケース3: プッシュに失敗
スクリプトがロールバック方法を表示します：
```bash
git reset --hard HEAD~1
git checkout main
git branch -D feature/remove-admin-prompts
```

### スクリプトが実行できない場合の代替手順

以下のような状況では手動実行が必要な場合があります：
- Git Bash / シェル環境が利用できない
- スクリプトに実行権限がない（`chmod +x scripts/release.sh` で解決）
- 特殊なファイル構成でスクリプトが正常動作しない

<details>
<summary>【代替手順】手動実行方法を表示</summary>

**⚠️ 警告**: 手動実行は推奨されません。可能な限り `./scripts/release.sh` を使用してください。

### 事前準備
1. すべての変更をコミットしてください
2. 必要に応じてバックアップを取得してください
3. `release/evac.AGENTS.md` と `release/README.md` が存在することを確認してください

### 手動実行手順

1. ブランチ `feature/remove-admin-prompts` を作成してください：
   ```bash
   git checkout -b feature/remove-admin-prompts
   ```

2. 以下のファイルをリポジトリから削除してください：
   ```bash
   git rm .github/prompts/*.admin.prompt.md
   git rm -r agent-input
   git rm -r agent-output
   git rm -r templates
   git rm -r tests/infrastructure
   git rm AGENTS.md
   git rm README.md
   ```

3. チュートリアルが存在しない課題の場合は、以下の空ファイルを削除してください：
   ```bash
   # TUTORIAL.md が空の場合のみ
   git rm TUTORIAL.md
   ```

4. 以下のファイルを移動してください：
   ```bash
   git mv release/evac.AGENTS.md AGENTS.md
   git mv release/README.md README.md
   ```

5. 変更をコミットし、リモートリポジトリにプッシュしてください：
   ```bash
   git commit -m "fix: remove admin prompt files"
   git push origin feature/remove-admin-prompts
   ```

6. GitHub上でプルリクエストを作成してください

### 手動実行時のロールバック

問題が発生した場合：
```bash
git reset --hard HEAD
git checkout main
git branch -D feature/remove-admin-prompts
```

</details>

## GitHub Copilot Agent による実行

GitHub Copilot Agent を使用してスクリプトを実行することもできます：

1. このプロンプト（`/release.admin`）を実行
2. エージェントが `./scripts/release.sh` を実行
3. 対話的な確認プロンプトに対して適切に応答

エージェントによる実行は、スクリプトの対話的なプロンプトに自動応答できない場合があります。その場合は、直接スクリプトを実行してください。

## 参考情報

詳細なワークフローについては、[共通ワークフロー](.github/prompts/WORKFLOW.md) を参照してください。