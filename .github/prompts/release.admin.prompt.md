---
description: "課題リポジトリをリリース可能な状態とするために、不要なファイルを削除し、必要なファイルを整理します。"
---

# /release.admin

## 目的
本リポジトリには、本プロンプトファイルを含む開発用やテスト用のファイルが複数含まれます。  
また、開発中は学生が課題を実施する際に Agent の動作を制限するための AGENTS.md ファイルを退避し、開発時専用の AGENTS.md を使用しています。  
リポジトリをリリース可能な状態とするために、学生にとって不要なファイルを削除し、退避中の必要なファイルを元の場所に戻す作業を行います。

## 手順
1. 以下のブランチ名で作業用の新しいブランチを作成してください。  
   - `feature/remove-admin-prompts`

2. 以下のファイルをリポジトリから削除してください。
   - `.github/prompts/*.admin.prompt.md` （管理者用プロンプトファイル）
   - `AGENTS.md` （エージェント動作制御ファイル）
   - `README.md`

3. 以下のファイル名を変更してください。
   - `evac.AGENTS.md` → `AGENTS.md`
   - `evac.README.md` → `README.md`

4. 変更内容を確認し、コミットメッセージ "fix: remove admin prompt files" で変更を保存してください。

5. 最後に、リポジトリのルートディレクトリで `git push origin feature/remove-admin-prompts` を実行し、変更をリモートリポジトリにプッシュしてください。