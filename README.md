# Python 課題テンプレート

## 教員向け: GitHub Classroom 課題作成手順

### 1. テンプレートリポジトリ設定
1. GitHub の本リポジトリの Settings → General → Template repository を ON
2. GitHub Classroom で「Use an existing repository」を選択し、このリポジトリを指定

### 2. 課題作成の流れ
1. `src/kadai/` に Python プログラムの雛形を配置
2. `tests/stages/` に段階的なテストを配置
3. README の「課題内容」部分を更新
4. GitHub Classroom で Assignment を作成

### 3. テスト構成
- `tests/stages/stage-01/` ～ `stage-05/`: 段階別テスト
- 各ステージは pytest マーカーで識別（`@pytest.mark.stage01` など）

---

## 課題内容

<!-- ここに具体的な課題内容を記載してください -->

**例: 四則演算関数の実装**

`src/kadai/` 内に以下の関数を実装してください：
1. `add_one(x)`: 引数に1を加算する関数
2. その他、段階的に要求される関数

## セットアップ

### 必要な環境
- Python 3.12+
- pytest

### 依存関係のインストール
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 実行方法

### 段階別テスト実行
```bash
# Stage 1 のテストのみ実行
./scripts/test 1

# Stage 2 のテストのみ実行  
./scripts/test 2

# （以下、stage 3-5 も同様）
```

### 全ステージ一括テスト実行
```bash
# 全てのテストを実行
./scripts/test-all
```

または

```bash
python -m pytest
```

### 個別テストファイル実行
```bash
# 特定のテストファイルのみ実行
python -m pytest tests/stages/stage-01/test_*.py
```

## プログラム作成ガイド

1. `src/kadai/` ディレクトリ内にPythonファイルを作成
2. 段階的にテストを実行して動作確認
3. 必要に応じて `tests/` 内に独自のテストを追加

## 提出方法

GitHub Classroom の指示に従って提出してください。自動テストが実行され、各段階の達成度が評価されます。

