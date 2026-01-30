# メタテンプレート汎用化計画

> **ステータス**: ✅ 完了（Phase 1-5 実装済み）
>
> **最終更新**: 2026-01-30
>
> **実装内容**:
> - 言語プロファイルシステムの構築
> - 4言語対応（Python, Java, JavaScript, Go）
> - 全プロンプトファイルの汎用化
> - ドキュメント整備

---

## 1. 現状分析

### 1.1 Python特化要素の洗い出し

現在のメタテンプレートには、以下のPython/pytest固有要素が含まれています：

| カテゴリ | ファイル/項目 | Python固有の内容 |
|---------|-------------|-----------------|
| **開発環境** | `.devcontainer/devcontainer.json` | Python 3.12 イメージ、pytest設定、Python拡張機能 |
| **テスト設定** | `pytest.ini` | pytestマーカー定義、pythonpath設定 |
| **ビルド設定** | `pyproject.toml` | setuptools設定 |
| **依存関係** | `requirements.txt`, `requirements-dev.txt` | pytest依存 |
| **CI/CD** | `.github/workflows/classroom.yml` | `pip install pytest`, `pytest -m 'stageXX'` |
| **テンプレート** | `templates/template.classroom.yml` | pytest実行コマンド |
| **プロンプト** | `implement-test.admin.prompt.md` | pytest固有のテスト実装手順、デコレータ説明 |
| **ソース構造** | `src/kadai/` | Pythonモジュール構成を前提 |
| **テスト構造** | `tests/stages/stage-XX/` | pytestのディレクトリ規約 |
| **スキル** | `.claude/skills/assignment-types/` | Pythonコード例 |

### 1.2 汎用化の対象範囲

以下の要素は言語に依存しないため、そのまま維持できます：

- 課題実施方式（プログラム実装/リファクタリング/テスト実装/TDD）の概念
- ワークフロー構造（topics → plan → readme → implement-test → verify → release）
- GitHub Classroom連携の仕組み
- ステージ別採点の概念
- エージェント用プロンプトの基本構造

---

## 2. 汎用化アーキテクチャ

### 2.1 言語プロファイル方式

言語/フレームワークごとの設定を「プロファイル」として定義し、動的に適用する方式を提案します。

```
Meta-Template-for-Assignment/
├── lang-profiles/                    # 言語プロファイル定義
│   ├── python-pytest.yml             # Python/pytest
│   ├── java-junit.yml                # Java/JUnit
│   ├── javascript-jest.yml           # JavaScript/Jest
│   ├── go-testing.yml                # Go/testing
│   ├── csharp-xunit.yml              # C#/xUnit
│   └── README.md                     # プロファイル作成ガイド
│
├── templates/
│   ├── devcontainer/                 # DevContainer テンプレート
│   │   ├── python.devcontainer.json
│   │   ├── java.devcontainer.json
│   │   ├── javascript.devcontainer.json
│   │   └── ...
│   ├── workflows/                    # CI ワークフローテンプレート
│   │   └── template.classroom.yml    # 汎用テンプレート（変数化）
│   └── ...
```

### 2.2 言語プロファイルスキーマ

```yaml
# lang-profiles/python-pytest.yml
name: Python/pytest
display_name: "Python 3.12 + pytest"
language: python
version: "3.12"

# 開発環境設定
devcontainer:
  image: "mcr.microsoft.com/devcontainers/python:3.12"
  extensions:
    - "ms-python.python"
    - "ms-python.vscode-pylance"
  settings:
    "python.testing.pytestEnabled": true
    "python.testing.pytestArgs": ["tests"]

# テスト設定
testing:
  framework: pytest
  install_command: "pip install pytest"
  run_command: "pytest -m '{marker}'"
  marker_format: "stage{num:02d}"  # stage01, stage02, ...
  test_file_pattern: "test_*.py"
  test_directory: "tests/stages"
  
# 依存関係管理
dependencies:
  file: "requirements.txt"
  dev_file: "requirements-dev.txt"
  install_command: "pip install -r requirements.txt"
  
# ソースコード構成
source:
  directory: "src/kadai"
  file_extension: ".py"
  
# CI/CD設定
ci:
  setup_commands:
    - "pip install pytest"
  timeout_default: 10
  
# テスト実装ガイド（プロンプト用）
test_implementation:
  example: |
    ```python
    import pytest

    @pytest.mark.stage01
    def test_example():
        from kadai.example import ExampleClass
        
        # テスト対象が存在することを確認
        assert ExampleClass is not None
    ```
  marker_decorator: "@pytest.mark.{marker}"
  import_location: "inside_function"  # テスト関数内でインポート
```

### 2.3 プロファイル追加例

```yaml
# lang-profiles/java-junit.yml
name: Java/JUnit
display_name: "Java 21 + JUnit 5"
language: java
version: "21"

devcontainer:
  image: "mcr.microsoft.com/devcontainers/java:21"
  extensions:
    - "vscjava.vscode-java-pack"
  settings:
    "java.test.config": {}

testing:
  framework: junit
  install_command: "mvn dependency:resolve"
  run_command: "mvn test -Dgroups='{marker}'"
  marker_format: "Stage{num:02d}"
  test_file_pattern: "*Test.java"
  test_directory: "src/test/java"
  
dependencies:
  file: "pom.xml"
  dev_file: null
  install_command: "mvn install -DskipTests"
  
source:
  directory: "src/main/java/kadai"
  file_extension: ".java"
  
ci:
  setup_commands:
    - "mvn dependency:resolve"
  timeout_default: 30

test_implementation:
  example: |
    ```java
    import org.junit.jupiter.api.Test;
    import org.junit.jupiter.api.Tag;
    import static org.junit.jupiter.api.Assertions.*;

    @Tag("Stage01")
    class ExampleTest {
        @Test
        void testExampleExists() {
            // テスト対象が存在することを確認
            assertNotNull(Example.class);
        }
    }
    ```
  marker_decorator: "@Tag(\"{marker}\")"
  import_location: "top_of_file"
```

---

## 3. 実装計画

### Phase 1: 設計・仕様策定（優先度：高）

#### 3.1.1 言語プロファイルスキーマの正式定義
- [ ] YAML スキーマ定義の作成
- [ ] 必須/オプションフィールドの明確化
- [ ] バリデーションルールの定義

#### 3.1.2 topics.md への言語選択セクション追加
```markdown
## 使用言語/フレームワーク
<!-- 
    課題で使用するプログラミング言語とテストフレームワークを指定します。
    対応プロファイル一覧は lang-profiles/ を参照してください。
-->

**使用するプロファイル**: {{ プロファイル名（例: python-pytest, java-junit）}}
```

#### 3.1.3 プロファイル選択フローの設計
- `/topics.admin` 実行時にプロファイルの妥当性チェック
- `/plan.admin` 実行時にプロファイル読み込みと設定適用

### Phase 2: テンプレート抽象化（優先度：高）

#### 3.2.1 template.classroom.yml の汎用化
```yaml
name: Autograding Tests
'on':
  - push
  - repository_dispatch
permissions:
  checks: write
  actions: read
  contents: read
jobs:
  run-autograding-tests:
    runs-on: ubuntu-latest
    if: github.actor != 'github-classroom[bot]'
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Setup environment
      run: |
        $SETUP_COMMANDS
    
    # ステージテスト（動的生成）
    $STAGE_TESTS
       
    - name: Autograding Reporter
      uses: classroom-resources/autograding-grading-reporter@v1
      env:
        $TEST_RESULTS_ENV
      with:
        runners: $TEST_RUNNERS
```

#### 3.2.2 DevContainer テンプレートの抽象化
- 言語別テンプレートファイルの作成
- プロファイルからの動的生成スクリプト

#### 3.2.3 依存関係ファイルテンプレート
- `requirements.txt.template` (Python)
- `pom.xml.template` (Java)
- `package.json.template` (JavaScript)
- `go.mod.template` (Go)

### Phase 3: プロンプトファイル汎用化（優先度：高）

#### 3.3.1 implement-test.admin.prompt.md の汎用化

現在のPython固有記述を言語非依存化：

**Before (Python固有)**:
```markdown
3. `tests/stages/stage-XX` 配下に、課題内容に対応するテストコードを実装してください。  
   - 各テストは `pytest` フレームワークを使用して実装してください。
   - 全てのテスト関数には、`@pytest.mark.stageXX` デコレータを付与してください
```

**After (汎用化)**:
```markdown
3. テストディレクトリ配下に、課題内容に対応するテストコードを実装してください。
   - 選択された言語プロファイル（`agent-input/topics.md` の「使用言語/フレームワーク」参照）に従ってテストを実装してください。
   - 各ステージのテストには、プロファイルで定義されたマーカー形式を使用してください。
   - 詳細なテスト実装例は `lang-profiles/{profile}.yml` の `test_implementation.example` を参照してください。
```

#### 3.3.2 plan.admin.prompt.md への言語対応追加
- プロファイル読み込みステップの追加
- 言語固有の設定を plan.md に反映

#### 3.3.3 verify.admin.prompt.md の汎用化
- 言語固有のチェック項目を動的に生成
- プロファイルに基づく整合性検証

### Phase 4: リファレンス実装（優先度：中）

#### 3.4.1 Python/pytest プロファイル（既存ベース）
- 現在の実装をプロファイル形式に変換
- 後方互換性の確保

#### 3.4.2 追加言語プロファイル作成
優先度順：
1. Java/JUnit（広く使われている）
2. JavaScript/Jest（Web開発で人気）
3. Go/testing（シンプルで学習しやすい）
4. C#/xUnit（.NET開発用）

### Phase 5: ドキュメント・ガイド整備（優先度：中）

#### 3.5.1 新規プロファイル作成ガイド
- `lang-profiles/README.md` の作成
- スキーマ説明とサンプル

#### 3.5.2 README.md の更新
- 対応言語一覧の追加
- 言語選択手順の説明

#### 3.5.3 AGENTS.md の更新
- 言語プロファイル参照方法
- 汎用ワークフロー説明

---

## 4. 移行戦略

### 4.1 後方互換性

既存のPython課題リポジトリとの互換性を維持するため：

1. **デフォルトプロファイル**: `topics.md` に言語指定がない場合は `python-pytest` をデフォルトとする
2. **既存ファイル維持**: 現在の `pytest.ini`, `requirements.txt` などはそのまま維持
3. **段階的移行**: 新規課題作成時のみ新方式を適用

### 4.2 移行チェックリスト

- [x] 言語プロファイルスキーマの確定
- [x] Python/pytest プロファイルの作成（既存からの変換）
- [x] topics.md テンプレートの更新
- [x] implement-test.admin.prompt.md の汎用化
- [x] template.classroom.yml の変数化
- [x] 1つ以上の追加言語プロファイル作成（Java, JavaScript, Go）
- [ ] 統合テスト（Python以外での課題作成テスト）← 手動検証が必要
- [x] ドキュメント更新

---

## 5. 想定される課題と対策

### 5.1 言語間の差異への対応

| 課題 | 対策 |
|-----|------|
| テストマーカー形式の違い | プロファイルで `marker_format` を定義 |
| ディレクトリ構成の違い | プロファイルで `source.directory`, `testing.test_directory` を定義 |
| ビルド手順の違い | プロファイルで `ci.setup_commands` を定義 |
| IDEサポートの違い | DevContainerテンプレートを言語別に用意 |

### 5.2 プロンプト複雑化への対策

言語固有の詳細はプロファイルに委譲し、プロンプトは抽象的な指示のみを記載：

```markdown
# 汎用プロンプト例
テストを実装する際は、以下の手順に従ってください：
1. `lang-profiles/` から該当プロファイルを読み込む
2. プロファイルの `test_implementation.example` を参考にテストを作成
3. プロファイルの `testing.marker_format` に従ってステージマーカーを付与
```

### 5.3 新言語追加の容易さ

新しい言語/フレームワークを追加する際に必要な作業を最小化：

1. `lang-profiles/{new-lang}.yml` を作成
2. `templates/devcontainer/{new-lang}.devcontainer.json` を作成
3. 依存関係テンプレートを作成（必要に応じて）
4. 動作確認

---

## 6. 実装優先度マトリクス

| タスク | 重要度 | 緊急度 | 工数 | 優先度 |
|-------|-------|-------|-----|-------|
| 言語プロファイルスキーマ定義 | 高 | 高 | 中 | 1 |
| topics.md 更新 | 高 | 高 | 小 | 2 |
| implement-test.admin.prompt.md 汎用化 | 高 | 高 | 中 | 3 |
| template.classroom.yml 汎用化 | 高 | 中 | 中 | 4 |
| Python/pytest プロファイル作成 | 中 | 高 | 小 | 5 |
| DevContainer テンプレート抽象化 | 中 | 中 | 中 | 6 |
| 追加言語プロファイル (Java) | 中 | 低 | 中 | 7 |
| 追加言語プロファイル (JS) | 中 | 低 | 中 | 8 |
| ドキュメント整備 | 中 | 低 | 中 | 9 |

---

## 7. 次のステップ

この計画のレビュー・承認後、以下の順序で実装を進めます：

1. **言語プロファイルスキーマの正式版作成**
2. **topics.md への言語選択セクション追加**
3. **Python/pytest プロファイルの作成**（既存設定から変換）
4. **implement-test.admin.prompt.md の汎用化**
5. **template.classroom.yml の変数化**
6. **統合テスト実施**
7. **追加言語プロファイルの作成**（Java/JUnit を最初の例として）

---

## 付録: 言語プロファイル完全スキーマ（案）

```yaml
# 言語プロファイル完全スキーマ v1.0
$schema: "https://json-schema.org/draft/2020-12/schema"

# 必須フィールド
name: string              # プロファイル識別子（例: python-pytest）
display_name: string      # 表示名（例: Python 3.12 + pytest）
language: string          # 言語名（例: python, java, javascript）
version: string           # 言語バージョン

# 開発環境設定（必須）
devcontainer:
  image: string           # Docker イメージ
  extensions: list        # VS Code 拡張機能
  settings: object        # VS Code 設定
  post_create_command: string  # コンテナ作成後コマンド（オプション）

# テスト設定（必須）
testing:
  framework: string       # テストフレームワーク名
  install_command: string # フレームワークインストールコマンド
  run_command: string     # テスト実行コマンド（{marker} をプレースホルダ）
  marker_format: string   # マーカー形式（{num} をプレースホルダ）
  test_file_pattern: string  # テストファイルパターン
  test_directory: string  # テストディレクトリ

# 依存関係管理（必須）
dependencies:
  file: string            # メイン依存関係ファイル
  dev_file: string|null   # 開発用依存関係ファイル
  install_command: string # 依存関係インストールコマンド

# ソースコード構成（必須）
source:
  directory: string       # ソースディレクトリ
  file_extension: string  # ファイル拡張子

# CI/CD設定（必須）
ci:
  setup_commands: list    # セットアップコマンドリスト
  timeout_default: number # デフォルトタイムアウト（秒）

# テスト実装ガイド（必須）
test_implementation:
  example: string         # テストコード例（Markdown コードブロック）
  marker_decorator: string # マーカー記法（{marker} をプレースホルダ）
  import_location: string # インポート位置（inside_function, top_of_file）
  
# 追加設定（オプション）
additional:
  lint_command: string    # Lintコマンド（オプション）
  format_command: string  # フォーマットコマンド（オプション）
  build_command: string   # ビルドコマンド（オプション）
```
