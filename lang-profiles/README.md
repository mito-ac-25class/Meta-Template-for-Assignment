# 言語プロファイル ガイド

## 概要

このディレクトリには、課題で使用する言語/テストフレームワークの設定を定義する「言語プロファイル」が格納されています。

言語プロファイルは、以下の要素を言語に依存しない形で抽象化します：
- 開発環境（DevContainer）設定
- テストフレームワーク設定
- CI/CD ワークフロー設定
- 依存関係管理
- ソースコード構成

## 利用可能なプロファイル

| プロファイル | 言語 | テストフレームワーク | 状態 |
|-------------|-----|-------------------|------|
| `python-pytest.yml` | Python 3.12 | pytest | ✅ 利用可能 |
| `java-junit.yml` | Java 21 | JUnit 5 | 🔧 参考実装 |
| `javascript-jest.yml` | JavaScript/Node.js 20 | Jest | 🔧 参考実装 |
| `go-testing.yml` | Go 1.21 | testing | 🔧 参考実装 |

> **凡例**
> - ✅ 利用可能: 本番運用可能な状態
> - 🔧 参考実装: テンプレートとして利用可能だが、実際の使用前に検証が必要

## プロファイルの使用方法

### 1. topics.md での指定

課題のトピック定義（`agent-input/topics.md`）で使用するプロファイルを指定します：

```markdown
## 使用言語/フレームワーク

python-pytest
```

### 2. 自動適用

`/plan.admin` 実行時に指定されたプロファイルが読み込まれ、以下が自動設定されます：
- テスト実行コマンド
- DevContainer 設定
- CI ワークフロー
- テスト実装ガイド

---

## スキーマ詳細

### 必須フィールド

#### プロファイル識別情報

| フィールド | 型 | 説明 | 例 |
|-----------|---|------|-----|
| `name` | string | プロファイル識別子（ファイル名と一致） | `python-pytest` |
| `display_name` | string | 人間が読みやすい表示名 | `Python 3.12 + pytest` |
| `language` | string | プログラミング言語名 | `python`, `java`, `javascript`, `go` |
| `version` | string | 言語バージョン | `3.12`, `21`, `20`, `1.21` |

#### 開発環境設定（devcontainer）

| フィールド | 型 | 説明 | 例 |
|-----------|---|------|-----|
| `devcontainer.image` | string | DevContainer用Dockerイメージ | `mcr.microsoft.com/devcontainers/python:3.12` |
| `devcontainer.extensions` | list | VS Code拡張機能 | `["ms-python.python"]` |
| `devcontainer.settings` | object | VS Code設定 | `{python.testing.pytestEnabled: true}` |
| `devcontainer.post_create_command` | string | コンテナ起動後の実行コマンド | `pip install -r requirements.txt` |

#### テスト設定（testing）

| フィールド | 型 | 説明 | 例 |
|-----------|---|------|-----|
| `testing.framework` | string | テストフレームワーク名 | `pytest`, `junit`, `jest`, `testing` |
| `testing.install_command` | string\|null | テストフレームワークのインストールコマンド | `pip install pytest` |
| `testing.run_command` | string | テスト実行コマンド（`{marker}` プレースホルダ使用） | `pytest -m '{marker}' -v` |
| `testing.marker_format` | string | ステージマーカー形式（`{num:02d}` で2桁ゼロ埋め） | `stage{num:02d}` → `stage01` |
| `testing.test_file_pattern` | string | テストファイル名パターン | `test_*.py`, `*Test.java` |
| `testing.test_directory` | string | テストファイル格納ディレクトリ | `tests/stages` |
| `testing.stage_directory_format` | string | ステージディレクトリ形式 | `stage-{num:02d}` |

#### 依存関係管理（dependencies）

| フィールド | 型 | 説明 | 例 |
|-----------|---|------|-----|
| `dependencies.file` | string | 依存関係定義ファイル | `requirements.txt`, `pom.xml`, `package.json` |
| `dependencies.dev_file` | string\|null | 開発用依存関係ファイル | `requirements-dev.txt` |
| `dependencies.install_command` | string | 依存関係インストールコマンド | `pip install -r requirements.txt` |

#### ソースコード構成（source）

| フィールド | 型 | 説明 | 例 |
|-----------|---|------|-----|
| `source.directory` | string | ソースコード格納ディレクトリ | `src/kadai` |
| `source.file_extension` | string | ソースファイル拡張子 | `.py`, `.java`, `.js`, `.go` |
| `source.import_format` | string | インポート文形式 | `from kadai.{module} import {class}` |

#### CI/CD設定（ci）

| フィールド | 型 | 説明 | 例 |
|-----------|---|------|-----|
| `ci.setup_commands` | list | CIでのセットアップコマンド | `["pip install pytest"]` |
| `ci.timeout_default` | number | テストタイムアウト（秒） | `10` |
| `ci.default_score_per_stage` | number | ステージ当たりのデフォルト配点 | `20` |

#### テスト実装ガイド（test_implementation）

| フィールド | 型 | 説明 | 例 |
|-----------|---|------|-----|
| `test_implementation.example` | string | テストコード例（Markdownコードブロック） | （下記参照） |
| `test_implementation.marker_decorator` | string | マーカーデコレータ形式 | `@pytest.mark.{marker}` |
| `test_implementation.import_location` | string | インポート位置 | `inside_function`, `top_of_file` |
| `test_implementation.function_naming` | string | テスト関数命名規則 | `test_{description}` |

### オプションフィールド（additional）

| フィールド | 型 | 説明 | 例 |
|-----------|---|------|-----|
| `additional.lint_command` | string | Lintコマンド | `flake8 src/` |
| `additional.format_command` | string | フォーマットコマンド | `black src/` |
| `additional.build_command` | string | ビルドコマンド | `mvn compile` |
| `additional.coverage_command` | string | カバレッジ取得コマンド | `pytest --cov` |

---

## 新規プロファイル作成ガイド

### ステップ1: テンプレートをコピー

```bash
cp lang-profiles/python-pytest.yml lang-profiles/{new-lang}-{framework}.yml
```

### ステップ2: 各フィールドを言語に合わせて修正

必須フィールドをすべて適切な値に変更します。特に以下に注意：

- **`testing.run_command`**: `{marker}` プレースホルダを適切に配置
- **`testing.marker_format`**: ステージ番号の形式を定義
- **`test_implementation.example`**: 実際に動作するテストコード例を記述

### ステップ3: DevContainer テンプレートを作成

```bash
cp templates/devcontainer/python.devcontainer.json templates/devcontainer/{new-lang}.devcontainer.json
```

DevContainerテンプレートを言語に合わせて編集します。

### ステップ4: 依存関係テンプレートを作成（必要に応じて）

```bash
# 例: Ruby/RSpec の場合
touch templates/dependencies/Gemfile.template
```

### ステップ5: 動作確認

1. `agent-input/topics.md` で新プロファイルを指定
2. `/plan.admin` を実行して設定が正しく読み込まれることを確認
3. `/implement-test.admin` でテストが正しく生成されることを確認
4. CIワークフローが正しく動作することを確認

### ステップ6: lang-profile-schema.yml を更新

新しい言語を `language` フィールドの `enum` に追加します。

---

## プレースホルダ

プロファイル内で使用できるプレースホルダ：

| プレースホルダ | 説明 | 例 |
|---------------|------|-----|
| `{marker}` | ステージマーカー（`marker_format` で定義された形式） | `stage01`, `Stage01` |
| `{num:02d}` | 2桁ゼロ埋めのステージ番号 | `01`, `02`, ... |
| `{module}` | モジュール名（ソースファイル名から拡張子を除いたもの） | `example` |
| `{class}` / `{class_name}` | クラス名 | `ExampleClass` |
| `{description}` | テストの説明（テスト関数名に使用） | `example_class_exists` |

---

## スキーマバージョン

現在のスキーマバージョン: **1.0**

スキーマの詳細定義は `lang-profile-schema.yml` を参照してください。

---

## トラブルシューティング

### プロファイルが読み込まれない

1. `agent-input/topics.md` の「使用言語/フレームワーク」セクションにプロファイル名が正しく記載されているか確認
2. プロファイル名と `lang-profiles/` 内のファイル名が一致しているか確認（例: `python-pytest` → `python-pytest.yml`）

### テストが実行されない

1. `testing.run_command` のコマンドが正しいか確認
2. `testing.marker_format` のマーカー形式がテストコードと一致しているか確認

### DevContainerが起動しない

1. `devcontainer.image` のDockerイメージが存在するか確認
2. `devcontainer.post_create_command` のコマンドが正しいか確認
