---
description: "課題をCIで自動採点するためのテストコードを実装し、実際に実行することで課題内容との整合性を検証します。"
---

# /implement-test.admin

## 目的
本リポジトリは、学生のプログラミング課題をCIで自動採点します。  
`/implement-test.admin` では、`release/README.md` に記載された課題内容を基に、  
言語プロファイルで定義されたテストフレームワークを使用してテストコードを実装し、  
実際にテストを実行することで課題内容との整合性を検証します。

## 前提条件
- `/readme.admin` が実行済みで `release/README.md` が作成されていること
- `/plan.admin` が実行済みで `agent-output/plan.md` が作成されていること（言語プロファイル情報を含む）

## 手順

### 1. 課題内容と言語プロファイルの確認

1. `release/README.md` の内容を確認し、課題内容を理解してください。

2. `agent-output/plan.md` のセクション2「使用言語/フレームワーク」を確認し、使用する言語プロファイルを特定してください。

3. `lang-profiles/{プロファイル名}.yml` を読み込み、以下の設定を確認してください:
   - `testing.framework`: テストフレームワーク名
   - `testing.run_command`: テスト実行コマンド
   - `testing.marker_format`: ステージマーカー形式
   - `testing.test_directory`: テストディレクトリ
   - `testing.stage_directory_format`: ステージディレクトリ形式
   - `source.directory`: ソースディレクトリ
   - `test_implementation.example`: テストコード例
   - `test_implementation.marker_decorator`: マーカーデコレータ形式
   - `test_implementation.import_location`: インポート位置

### 2. ブランチ作成

[共通ワークフロー](.github/prompts/WORKFLOW.md) に従い、ブランチ `feature/implement-tests` を作成してください。

### 3. テストコードの実装

言語プロファイルの設定に従って、テストディレクトリ配下にテストコードを実装してください。

#### 3.1 共通ルール

- 各ステージ用ディレクトリには、対応するステージ番号に基づいたテストファイルを作成してください。
- 各テストには、プロファイルで定義されたマーカー形式を使用してください。
- 1つのテスト関数/メソッド内には、基本的に1つのアサーションのみを含めてください。
- 各アサーションの上の行には、何をテストしているのかが学生にとって明確になるよう、日本語のコメントを追加してください。

#### 3.2 言語別テスト実装例

プロファイルの `test_implementation.example` を参照してください。以下は各言語の実装例です：

**Python/pytest の場合:**
```python
# tests/stages/stage-01/test_example.py
import pytest

@pytest.mark.stage01
def test_example_class_exists():
    from kadai.example import ExampleClass

    # ExampleClassが存在することを確認
    assert ExampleClass is not None
```

**Java/JUnit の場合:**
```java
// src/test/java/kadai/stage01/ExampleTest.java
package kadai.stage01;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Tag;
import static org.junit.jupiter.api.Assertions.*;

import kadai.Example;

@Tag("Stage01")
class ExampleTest {
    @Test
    void testExampleClassExists() {
        // Exampleクラスが存在することを確認
        assertNotNull(Example.class);
    }
}
```

**JavaScript/Jest の場合:**
```javascript
// tests/stages/stage-01/example.test.js
describe('Stage01: Example', () => {
  test('Exampleクラスが存在すること', () => {
    const { Example } = require('../../../src/kadai/example');
    
    // Exampleクラスが存在することを確認
    expect(Example).toBeDefined();
  });
});
```

**Go/testing の場合:**
```go
// kadai/example_test.go
package kadai

import "testing"

func TestStage01_ExampleExists(t *testing.T) {
    // Example型が存在することを確認
    var _ Example
}

func TestStage01_ExampleMethodReturnsExpected(t *testing.T) {
    instance := NewExample("test")
    
    // メソッドが期待通りの値を返すことを確認
    got := instance.GetValue()
    want := "test"
    if got != want {
        t.Errorf("GetValue() = %q, want %q", got, want)
    }
}
```

### 4. テストの検証

実際に生徒が課題を実施する手順を想定して、以下のフローでテストを検証してください。

#### 4.1 ステージ1の検証

##### 4.1.1 テスト実行前の確認
まず、リポジトリのルートディレクトリにいることを確認します。
```bash
pwd
# 期待される出力: /path/to/Meta-Template-for-Assignment
```

##### 4.1.2 テストの失敗を確認（RED）
実装前の状態で、ステージ1のテストを実行し、テストが失敗することを確認します。

**テスト実行コマンド**（言語プロファイルの `testing.run_command` を参照）:
- Python/pytest: `pytest -m stage01 -v`
- Java/JUnit: `mvn test -Dgroups='Stage01'`
- JavaScript/Jest: `npm test -- --testPathPattern='stage-01'`
- Go/testing: `go test -v -run 'Stage01' ./...`

> **Note:** この時点でテストが失敗するのは正常です。学生は空の実装ファイルから始めるため、必要なモジュールやクラスがまだ存在しません。

##### 4.1.3 最低限の実装（GREEN）
ソースディレクトリ配下に、ステージ1をクリアするために必要な最低限の実装を行います。

##### 4.1.4 テストの成功を確認（GREEN）
再度ステージ1のテストを実行し、全てのテストが成功することを確認します。

#### 4.2 ステージ2以降の検証

ステージ2以降も同様の手順で検証を行います。各ステージについて以下を実施してください：

1. **RED確認**: 実装前にテストを実行し、失敗を確認
2. **実装**: ソースディレクトリ配下に該当ステージの機能を実装
3. **GREEN確認**: テストを実行し、成功を確認

#### 4.3 累積的なテスト確認
各ステージ完了後、それまでの全てのステージのテストが通ることを確認します。

#### 4.4 検証完了の確認
全てのステージの検証が完了したら、最終確認を行います。

### 5. 設定ファイルの更新

すべてのステージのテストが成功したら、以下のファイルを更新してください。

#### 5.1 模範解答の保存
ソースディレクトリの実装を模範解答として `agent-output/` 配下にコピーしてください。
その後、元のソースディレクトリの実装済みファイルは全て空ファイルの状態に戻してください。

#### 5.2 テスト設定ファイルの更新（言語別）

**Python/pytest の場合:**
`pytest.ini` のマーカー定義 `markers` に、実装した全てのステージマーカーを記述してください。

**Java/JUnit の場合:**
`pom.xml` のテスト設定を確認し、必要に応じてグループ設定を追加してください。

**JavaScript/Jest の場合:**
`jest.config.js` のテスト設定を確認してください。

#### 5.3 CIワークフローの更新

`.github/workflows/classroom.yml` を更新してください:
1. `lang-profiles/{プロファイル名}.yml` から `ci.setup_commands` を参照し、Setup environment ステップを設定
2. 各ステージのテストコマンドをプロファイルの `testing.run_command` に基づいて設定
3. `agent-output/plan.md` のステージ構成に基づいた配点（`max-score`）を設定

**参考**: `templates/workflows/template.classroom.yml` を基にワークフローを構成できます。

### 6. コミット・プッシュ

[共通ワークフロー](.github/prompts/WORKFLOW.md) に従い、変更をコミット（メッセージ: "feat: implement and verify tests for $課題名"）し、リモートリポジトリにプッシュしてください。