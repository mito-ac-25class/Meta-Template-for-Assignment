---
description: 課題をCIで自動採点するためのテストコードを実装し、実際に実行することで課題内容との整合性を検証します
allowed-tools: Read, Edit, Write, Bash, Glob, Grep
---

# /implement-test コマンド

## 目的

本リポジトリは、学生のプログラミング課題をCIで自動採点します。
`/implement-test` では、`release/README.md` に記載された課題内容を基に、
学生が実装すべき機能に対応するテストコードを `tests/stages/stage-XX` 配下に実装し、
実際にテストを実行することで課題内容との整合性を検証します。

## 前提条件

- `/readme` が実行済みで `release/README.md` が作成されていること

## 手順

1. `release/README.md` の内容を確認し、課題内容を理解してください。

2. ブランチ `feature/implement-tests` を作成してください。
   ```bash
   git checkout -b feature/implement-tests
   ```

3. `tests/stages/stage-XX` 配下に、課題内容に対応するテストコードを実装してください。
   - 各テストは `pytest` フレームワークを使用して実装してください。
   - 各ステージのテストコードは、課題の各機能に対応するように設計してください。
   - 各ステージ用ディレクトリ `tests/stages/stage-XX` には、対応するステージ番号に基づいたテストファイルを1つのみ作成してください。
   - 各テストファイル内では、以下のルールでテストを実装してください。
     - 全てのテスト関数には、`@pytest.mark.stageXX` デコレータを付与してください（XXはステージ番号）。
     - テスト対象のモジュールやクラスのインポートは、`pytest.ini` のルールに従って、**必ず**テスト関数内で行ってください。
     - 1つのテスト関数内には、基本的に1つのアサーションのみを含めてください。
     - 各アサーションの上の行には、何をテストしているのかが学生にとって明確になるよう、日本語のコメントを追加してください。
   - 実装例:
      ```python
      # tests/stages/stage-01/test_bank_account.py
      import pytest

      @pytest.mark.stage01
      def test_bank_account_exists():
          from kadai.bank_account import BankAccount

          # 銀行口座クラスが存在することを確認する
          assert BankAccount is not None

      # <... 他の stage-01 テスト関数も同様に実装 ...>
      ```

4. テストコードを実装したら、実際に生徒が課題を実施する手順を想定して、以下のフローでテストを検証してください。
   検証中、テストコード側に問題が見つかった場合は、適宜修正を行ってください。

   ### 4.1 ステージ1の検証

   #### 4.1.1 テスト実行前の確認
   まず、リポジトリのルートディレクトリにいることを確認します。
   ```bash
   pwd
   ```

   #### 4.1.2 テストの失敗を確認（RED）
   実装前の状態で、ステージ1のテストを実行し、テストが失敗することを確認します。
   ```bash
   pytest -m stage01 -v
   ```

   > **Note:** この時点でテストが失敗するのは正常です。学生は空の実装ファイルから始めるため、必要なモジュールやクラスがまだ存在しません。

   #### 4.1.3 最低限の実装（GREEN）
   `src/kadai/` 配下に、ステージ1をクリアするために必要な最低限の実装を行います。

   #### 4.1.4 テストの成功を確認（GREEN）
   再度ステージ1のテストを実行し、全てのテストが成功することを確認します。
   ```bash
   pytest -m stage01 -v
   ```

   ### 4.2 ステージ2以降の検証

   ステージ2以降も同様の手順で検証を行います。

   #### 4.2.1 各ステージの検証手順
   1. **RED確認**: 実装前にテストを実行し、失敗を確認
      ```bash
      pytest -m stage02 -v  # ステージ2の場合
      pytest -m stage03 -v  # ステージ3の場合
      ```

   2. **実装**: `src/kadai/` 配下に該当ステージの機能を実装

   3. **GREEN確認**: テストを実行し、成功を確認

   #### 4.2.2 累積的なテスト確認
   各ステージ完了後、それまでの全てのステージのテストが通ることを確認します：
   ```bash
   # 全てのステージのテストを実行
   pytest tests/stages/ -v
   ```

   ### 4.3 テスト失敗時のデバッグガイド

   #### 4.3.1 エラーメッセージの確認
   ```bash
   pytest -m stage01 -vv --tb=long
   pytest -m stage01 -v -s
   ```

   #### 4.3.2 よくあるエラーと対処法

   **1. ModuleNotFoundError: No module named 'kadai.XXX'**
   - 原因: 必要なモジュールファイルが存在しない、またはファイル名が間違っている
   - 対処法: `src/kadai/` 配下に正しいファイル名でモジュールを作成

   **2. ImportError: cannot import name 'XXX' from 'kadai.YYY'**
   - 原因: クラスや関数が定義されていない、または名前が間違っている
   - 対処法: モジュール内に必要なクラス/関数が定義されているか確認

   **3. AssertionError**
   - 原因: テストの期待値と実際の戻り値が一致していない
   - 対処法: テストコード内のコメントを読み、何をテストしているか確認

   **4. AttributeError: 'XXX' object has no attribute 'YYY'**
   - 原因: クラスに必要なメソッドや属性が定義されていない
   - 対処法: クラスに必要なメソッド/属性を追加

5. すべてのステージのテストが成功したら、以下のファイルを更新してください。
   - `src/kadai/`: 全ステージをクリアするために必要な実装を含むファイルを模範解答として `agent-output/` 配下にコピーしてください。
     その後、元の `src/kadai/` 配下の実装済みファイルは全て空ファイルの状態に戻してください。
   - `pytest.ini`: ステージごとのマーカー定義 `markers` に、実装した全てのステージマーカーを記述してください。
   - `.github/workflows/classroom.yml`: `templates/template.classroom.yml` をベースとして、実装した全てのステージに対応するジョブを追加し、`README.md` の課題内容に基づいた配点を設定してください。

6. 変更をコミット・プッシュしてください：
   ```bash
   git add .
   git commit -m "feat: implement and verify tests"
   git push origin feature/implement-tests
   ```
