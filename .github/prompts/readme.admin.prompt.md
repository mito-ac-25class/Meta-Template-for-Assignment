---
description: "release/README.md に記載する課題の説明文を作成します。"
---

# /readme.admin

## 目的
`/readme.admin` では、課題の実施プランを `agent-output/plan.md` から取得し、  
学生が課題を理解しやすいように、`release/README.md` に記載する課題の説明文を作成します。

## 手順
1. `agent-output/plan.md` を読み込みます。Markdownに記述されている以下項目を取得します。
   - 学習トピック一覧

2. 以下のブランチ名で作業用の新しいブランチを作成してください。  
   - `feature/make-readme`

3. `templates/template.readme.md` を `release/README.md` にコピーします。

4. `release/README.md` の `$` プレースホルダを埋める形で、課題説明文を作成します。

5. `release/README.md` 内のコメント（`<!-- ... -->`）を全て削除します。
  
6. 変更内容を確認し、`feat:` プレフィックスのコミットメッセージを追加して変更を保存してください。

7. 最後に、リポジトリのルートディレクトリで `git push origin feature/make-readme` を実行し、変更をリモートリポジトリにプッシュしてください。