---
description: "課題リポジトリをリリース可能な状態とするために、不要なファイルを削除し、必要なファイルを整理します。"
---

# /release.admin

## 目的
本リポジトリには、本プロンプトファイルを含む開発用やテスト用のファイルが複数含まれます。  
また、開発中は学生が課題を実施する際に Agent の動作を制限するための AGENTS.md ファイルを退避し、開発時専用の AGENTS.md を使用しています。  
リポジトリをリリース可能な状態とするために、学生にとって不要なファイルを削除し、退避中の必要なファイルを元の場所に戻す作業を行います。

## 手順

リリース準備は、以下のシェルスクリプトを実行することで自動化されています:

```bash
./scripts/release.sh
```

このスクリプトは以下の処理を自動的に行います:

1. 作業用ブランチ `feature/remove-admin-prompts` を作成
2. 管理者用プロンプトファイル (`.github/prompts/*.admin.prompt.md`) を削除
3. `agent-input/*` ディレクトリを削除
4. `agent-output/*` ディレクトリを削除
5. `templates/*` ディレクトリを削除
6. 開発用 `AGENTS.md` と `README.md` を削除
7. 空の `TUTORIAL.md` を削除（存在し、かつ空の場合のみ）
8. `release/evac.AGENTS.md` → `AGENTS.md` に移動
9. `release/README.md` → `README.md` に移動
10. 変更をコミット (コミットメッセージ: "fix: remove admin prompt files")
11. リモートリポジトリにプッシュ

スクリプト実行後は、GitHub上でプルリクエストを作成し、レビュー後にmainブランチにマージしてください。

## 手動実行（スクリプトが使用できない場合）

万が一スクリプトが実行できない場合は、以下の手順で手動実行してください:

<details>
<summary>手動実行手順を表示</summary>

1. 以下のブランチ名で作業用の新しいブランチを作成してください。  
   - `feature/remove-admin-prompts`

2. 以下のファイルをリポジトリから削除してください。
   - `.github/prompts/*.admin.prompt.md` （管理者用プロンプトファイル）
   - `agent-input/*` （エージェント入力用ファイル群）
   - `agent-output/*` （エージェント出力用ファイル群）
   - `templates/*` （テンプレートファイル群）
   - `AGENTS.md` （エージェント動作制御ファイル）
   - `README.md`

3. チュートリアルが存在しない課題の場合は、以下の空ファイルを削除してください。
   - `TUTORIAL.md` （チュートリアル用ドキュメント）

4. 以下のファイル名を変更してください。
   - `release/evac.AGENTS.md` → `AGENTS.md` (リポジトリのルートディレクトリへ移動)
   - `release/README.md` → `README.md` (リポジトリのルートディレクトリへ移動)

5. 変更内容を確認し、コミットメッセージ "fix: remove admin prompt files" で変更を保存してください。

6. 最後に、リポジトリのルートディレクトリで `git push origin feature/remove-admin-prompts` を実行し、変更をリモートリポジトリにプッシュしてください。

</details>