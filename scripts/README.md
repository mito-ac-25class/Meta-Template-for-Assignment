# Scripts

このディレクトリには、リポジトリ管理を自動化するスクリプトが含まれています。

## release.py

課題リポジトリを学生配布用に整えるスクリプトです。`.releaseignore` に基づく削除と、`release/` 配下の公開ファイル配置をまとめて行います。

### 使用方法

```bash
python scripts/release.py
python scripts/release.py --dry-run
```

### 実行内容

1. `release/README.md` をルートの `README.md` に移動
2. `release/student.AGENTS.md` をルートの `AGENTS.md` に移動
3. `release/student.CLAUDE.md` が存在する場合はルートの `CLAUDE.md` に移動
4. `.releaseignore` に一致する開発用ファイルを削除
5. 空になった `release/` ディレクトリを削除

### 主な削除対象

- `prompts/`
- `.claude/commands/`, `.claude/skills/`
- `.agents/skills/`
- `.github/prompts/*.admin.prompt.md`
- `schema/`, `scripts/`, `plugins/`, `templates/`
- `agent-input/`, `agent-output/`
- `tests/infrastructure/`, `tests/conftest.py`

### dry-run

`--dry-run` を付けると、実際には変更せずに移動・削除予定のみを表示します。リリース前の確認用として使います。

### テスト

```bash
pytest tests/infrastructure/test_release.py -v
```
