---
description: 課題ビルド: README・チュートリアル・テスト・CIを生成し、動作検証します
allowed-tools: Read, Edit, Write, Bash, Glob, Grep
---

# /build コマンド

課題のビルドフェーズを実行します。プランに基づいて学生向けドキュメント、テストコード、CI設定を生成し、動作検証します。

## 入力

- `agent-input/topics.yaml`（/design で検証済み）
- `agent-output/plan.md`（/design で作成済み）

## 出力

- `release/README.md`（学生向け課題説明）
- `TUTORIAL.md`（チュートリアル、必要な場合のみ）
- `tests/stages/stageXX/test_*.py`（ステージ別テスト）
- `.github/workflows/classroom.yml`（CI設定）
- `agent-output/` 内に模範解答のバックアップ

## 手順

### Step 1: CI 設定の生成

`agent-input/topics.yaml` から CI 設定を生成します。

```bash
python scripts/generate.py classroom
```

生成された `.github/workflows/classroom.yml` を確認し、ステージ数・点数配分が `topics.yaml` と一致していることを検証します。

### Step 2: README の作成

`agent-output/plan.md` の内容を基に `release/README.md` を作成します。

README に含める内容:
- 課題タイトルとトピック説明（NOTE callout、3行程度）
- 学習目標（箇条書き）
- チュートリアルへのリンク（該当時）
- 実践課題の説明とユーザーストーリー
- ステージ別の機能・受け入れ条件・点数の表
- 仕様（詳細な動作説明）
- 動作例（コード例と期待出力）
- 実装上の注意事項
- トラブルシューティング

**重要**: HTML コメント（`<!-- ... -->`）は全て除去してください。

### Step 3: チュートリアルの作成（必要な場合）

`agent-output/plan.md` のチュートリアル必要性を確認します。

**不要の場合:** このステップをスキップ

**必要な場合:** `TUTORIAL.md` を作成します。

チュートリアル設計の原則:
- **段階的学習**: 簡単な概念から複雑な概念へ
- **具体例重視**: コピー＆ペーストで実行可能なコード例
- **hands-on形式**: 各セクションに練習問題を含む
- **適切な分量**: 想定学習時間内に完了可能

**重要**: チュートリアルは前提知識を教えるものであり、課題の解答を含めないこと

### Step 4: テストの実装

`release/README.md` の仕様に基づき、ステージ別テストを実装します。

#### テスト実装ルール

`agent-input/topics.yaml` の `stack` フィールドに対応するプラグインのテスト規約に従います。

- `stack: python` → `plugins/python/conventions.md`
- `stack: django-react` → `plugins/django-react/conventions.md`

対応するプラグインの `conventions.md` を必ず読み、記載されたルールに従ってテストを実装してください。

**Python（stack: python）の主なルール:**

1. テストファイルの配置: `tests/stages/stageXX/test_<モジュール名>.py`
2. 全テスト関数に `@pytest.mark.stageXX` デコレータを付与
3. import はテスト関数内で行う（`pythonpath = src` 設定による制約）
4. 各アサーションの前に日本語コメントで検証内容を説明
5. 1テスト関数につき1アサーション（推奨）

**Django + React（stack: django-react）の主なルール:**

1. バックエンドテスト: `tests/stages/stageXX/test_backend_<モジュール名>.py`（pytest + pytest-django）
2. フロントエンドテスト: `tests/stages/stageXX/test_frontend_<コンポーネント名>.test.ts`（Jest）
3. バックエンドは `@pytest.mark.stageXX` デコレータ、フロントエンドは `describe("StageXX: ...")` で分類
4. 詳細は `plugins/django-react/conventions.md` を参照

#### テストコード例（stack: python）

```python
import pytest

@pytest.mark.stage01
def test_class_exists():
    from kadai.bank_account import BankAccount

    # 銀行口座クラスが存在することを確認する
    assert BankAccount is not None

@pytest.mark.stage01
def test_initial_balance():
    from kadai.bank_account import BankAccount

    account = BankAccount()
    # 初期残高が0であることを確認する
    assert account.balance == 0
```

### Step 5: テストの動作検証（RED→GREEN サイクル）

各ステージについて以下のサイクルを実行します:

#### 5a. RED 確認

テストを実行し、実装前の状態で失敗することを確認:

```bash
pytest -m stage01 -v
```

#### 5b. 最小限の実装

テストを通すための最小限のコードを `src/kadai/` に実装:

```bash
pytest -m stage01 -v  # GREEN を確認
```

#### 5c. 累積テスト

全ステージの累積テストが通ることを確認:

```bash
pytest tests/stages/ -v
```

#### デバッグオプション

```bash
pytest -m stage01 -vv --tb=long   # 詳細なトレースバック
pytest -m stage01 -v -s           # print出力を表示
pytest -k "bank_account" -v       # キーワードで絞り込み
```

#### よくあるエラーと対処

| エラー | 原因 | 対処 |
|-------|------|------|
| ModuleNotFoundError | モジュールが `src/kadai/` に存在しない | ファイルを作成 |
| ImportError | クラス/関数名が不一致 | 名前を確認 |
| AssertionError | 実装が仕様と不一致 | 実装を修正 |

### Step 6: 検証後の整理

1. `src/kadai/` の実装ファイルを `agent-output/` にコピー（模範解答として保存）
2. `src/kadai/` のファイルを空の状態にリセット（`__init__.py` のみ残す）

### Step 7: Git 操作

# Git ワークフロー

課題作成プロジェクトで使用する共通のGitワークフローです。

## ブランチ命名規則

| コマンド | ブランチ名 |
|---------|-----------|
| `/design` | `feature/design-assignment` |
| `/build` | `feature/build-assignment` |
| `/release` | `feature/release-assignment` |

## 基本ワークフロー

### 1. ブランチの作成

```bash
git checkout -b <ブランチ名>
```

### 2. 変更の確認とコミット

```bash
git status
git diff
git add <対象ファイル>
git commit -m "<コミットメッセージ>"
```

### コミットメッセージのプレフィックス

- `add:` - 新しいファイルやコンテンツを追加した場合
- `feat:` - 新機能を追加した場合
- `fix:` - 修正を行った場合
- `update:` - 既存の内容を更新した場合
- `clean:` - クリーンアップ処理を行った場合

### 3. リモートリポジトリへのプッシュ

```bash
git push origin <ブランチ名>
```

### 4. プルリクエストの作成

GitHubのウェブインターフェースまたは `gh` コマンドでプルリクエストを作成し、レビューを依頼します。

## レビュー後の修正プロセス

### ケース1: 軽微な修正が必要な場合

タイポの修正、コメントの追加、フォーマットの調整など：

```bash
git checkout <ブランチ名>
# ファイルを編集
git add .
git commit -m "fix: レビュー指摘事項の修正"
git push origin <ブランチ名>
```

### ケース2: 大幅な修正が必要な場合

課題の方向性が間違っている、テストシナリオの大幅な再構成が必要など：

```bash
git checkout main
git branch -D <ブランチ名>
# 入力ファイルを修正後、コマンドを再実行
```

## 注意事項

- ブランチ名は各コマンドで一貫性を保つため、上記の命名規則に従ってください
- コミット前には必ず `git status` と `git diff` で変更内容を確認してください
- 不要なファイル（ビルド成果物、一時ファイルなど）がコミットされないよう注意してください


**ブランチ名:** `feature/build-assignment`

```bash
git checkout -b feature/build-assignment
git add release/README.md TUTORIAL.md tests/ .github/workflows/classroom.yml src/ agent-output/
git commit -m "feat: build assignment (README, tests, CI)"
git push origin feature/build-assignment
```
