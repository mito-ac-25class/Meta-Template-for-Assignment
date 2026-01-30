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
| `java-junit.yml` | Java 21 | JUnit 5 | 📋 計画中 |
| `javascript-jest.yml` | JavaScript/Node.js | Jest | 📋 計画中 |
| `go-testing.yml` | Go | testing | 📋 計画中 |

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

## 新規プロファイル作成ガイド

### 必須フィールド

新しい言語/フレームワークをサポートするには、以下のフィールドを定義する必要があります：

```yaml
# プロファイル識別情報
name: string              # プロファイル識別子（例: python-pytest）
display_name: string      # 表示名（例: Python 3.12 + pytest）
language: string          # 言語名
version: string           # 言語バージョン

# 開発環境設定
devcontainer:
  image: string           # Docker イメージ
  extensions: list        # VS Code 拡張機能
  settings: object        # VS Code 設定

# テスト設定
testing:
  framework: string       # テストフレームワーク名
  install_command: string # インストールコマンド
  run_command: string     # 実行コマンド（{marker} プレースホルダ使用）
  marker_format: string   # マーカー形式（{num:02d} で2桁ゼロ埋め）
  test_file_pattern: string
  test_directory: string

# 依存関係管理
dependencies:
  file: string
  dev_file: string|null
  install_command: string

# ソースコード構成
source:
  directory: string
  file_extension: string

# CI設定
ci:
  setup_commands: list
  timeout_default: number

# テスト実装ガイド
test_implementation:
  example: string         # コード例
  marker_decorator: string
  import_location: string # inside_function | top_of_file
```

### プロファイル作成手順

1. **テンプレートをコピー**
   ```bash
   cp lang-profiles/python-pytest.yml lang-profiles/{new-lang}.yml
   ```

2. **各フィールドを言語に合わせて修正**

3. **DevContainer テンプレートを作成**（必要に応じて）
   ```bash
   cp templates/devcontainer/python.devcontainer.json templates/devcontainer/{new-lang}.devcontainer.json
   ```

4. **動作確認**
   - `topics.md` で新プロファイルを指定
   - `/plan.admin` を実行して設定が正しく読み込まれることを確認
   - `/implement-test.admin` でテストが正しく生成されることを確認

## スキーマバージョン

現在のスキーマバージョン: **1.0**

スキーマの詳細定義は `lang-profile-schema.yml` を参照してください。
