# Scripts

このディレクトリには、リポジトリ管理を自動化するためのスクリプトが含まれています。

## release.sh

課題リポジトリをリリース可能な状態にするための自動化スクリプトです。

### 使用方法

```bash
./scripts/release.sh
```

### 実行内容

1. 作業用ブランチ `feature/remove-admin-prompts` を作成
2. 管理者用プロンプトファイル (`.github/prompts/*.admin.prompt.md`) を削除
3. `agent-input/*` ディレクトリを削除
4. `agent-output/*` ディレクトリを削除
5. `templates/*` ディレクトリを削除
6. 開発用 `AGENTS.md` と `README.md` を削除
7. 空の `TUTORIAL.md` を削除（存在し、かつ空の場合のみ）
8. `tests/infrastructure/*` ディレクトリを削除
9. `release/evac.AGENTS.md` → `AGENTS.md` に移動
10. `release/README.md` → `README.md` に移動
11. 変更をコミット
12. リモートリポジトリにプッシュ

### 前提条件

- リポジトリがgit管理されていること
- `release/evac.AGENTS.md` と `release/README.md` が存在すること
- リモートリポジトリへのプッシュ権限があること

### エラーハンドリング

スクリプトは `set -e` を使用しており、エラーが発生した場合は即座に終了します。  
必要なファイル（`release/evac.AGENTS.md`, `release/README.md`）が見つからない場合もエラーで終了します。

### テスト

スクリプトのテストは `tests/infrastructure/test_release_script.py` に含まれています。

```bash
pytest tests/infrastructure/test_release_script.py -v
```

## check_html_comments.py

リリース前に学生向けファイルにHTMLコメントが残存していないかをチェックするスクリプトです。

### 使用方法

```bash
python scripts/check_html_comments.py
```

または

```bash
./scripts/check_html_comments.py
```

### 実行内容

1. リポジトリの状態（リリース前/後）を自動判定
2. 以下のファイルからHTMLコメント（`<!-- ... -->`）を検出：
   - リリース前: `release/README.md`, `TUTORIAL.md`
   - リリース後: `README.md`, `TUTORIAL.md`
3. HTMLコメントが見つかった場合：
   - ファイルパスと行番号を表示
   - 終了コード 1 で終了
4. HTMLコメントがない場合：
   - 終了コード 0 で終了

### チェック対象

- 教員向けの指示や注意書きとして残されたHTMLコメント
- テンプレートファイルから削除されるべきコメント

### 使用場面

- `/verify.admin` プロンプト実行時の包括的チェック
- リリース前の最終確認
- CI/CDパイプラインでの自動チェック

### テスト

スクリプトのテストは `tests/infrastructure/test_html_comment_checker.py` に含まれています。

```bash
pytest tests/infrastructure/test_html_comment_checker.py -v
```

### エラーメッセージ例

```
❌ release/README.md
   2個のHTMLコメントが見つかりました:
   - 行 3: <!-- これはコメントです -->
   - 行 7: <!-- 複数行の...
```

### 対処方法

HTMLコメントが検出された場合：
1. 該当ファイルを開く
2. HTMLコメント（`<!-- ... -->`）を削除
3. プレースホルダー（`$変数名`）は残す
4. 再度スクリプトを実行して確認
