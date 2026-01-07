---
description: release/README.md に記載する課題の説明文を作成します
allowed-tools: Read, Edit, Write, Bash, Glob
---

# /readme コマンド

## 目的

`/readme` では、課題の実施プランを `agent-output/plan.md` から取得し、
学生が課題を理解しやすいように、`release/README.md` に記載する課題の説明文を作成します。

## 前提条件

- `/plan` が実行済みで `agent-output/plan.md` が作成されていること

## 手順

1. `agent-output/plan.md` を読み込みます。Markdownに記述されている以下項目を取得します。
   - 学習トピック一覧

2. ブランチ `feature/make-readme` を作成してください。
   ```bash
   git checkout -b feature/make-readme
   ```

3. `templates/template.README.md` を `release/README.md` にコピーします。

4. `release/README.md` の `$` プレースホルダを埋める形で、課題説明文を作成します。
   - テンプレート内のコメント（`<!-- ... -->`）を参照し、各セクションの記載内容とガイドラインを確認してください。

5. `release/README.md` 内のコメント（`<!-- ... -->`）を全て削除します。

6. 変更をコミット・プッシュしてください：
   ```bash
   git add release/README.md
   git commit -m "feat: create student README"
   git push origin feature/make-readme
   ```
