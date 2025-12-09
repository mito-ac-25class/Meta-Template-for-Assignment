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
