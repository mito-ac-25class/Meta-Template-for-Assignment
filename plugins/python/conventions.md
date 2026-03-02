# Python テスト規約

## ディレクトリ構造

```
tests/
├── conftest.py          # 動的マーカー登録 + 共通 fixture
└── stages/
    ├── stage01/
    │   └── test_<module>.py
    ├── stage02/
    │   └── test_<module>.py
    └── ...
```

## テストファイル規約

### マーカー

- 全テスト関数に `@pytest.mark.stageXX` デコレータを付与
- マーカーは `tests/conftest.py` が `agent-input/topics.yaml` から動的に登録

### import

- テスト関数内で `from kadai.<module> import <Class>` を行う
- トップレベル import は使わない（`pythonpath = src` による制約）

### アサーション

- 1テスト関数につき1アサーション（推奨）
- アサーション前に日本語コメントで検証内容を説明

### 命名規則

- ファイル: `test_<module_name>.py`
- クラス: `TestStageXX` (任意)
- 関数: `test_<検証対象>_<期待結果>`

## テストパターン例

```python
import pytest


@pytest.mark.stage01
def test_class_exists():
    from kadai.bank_account import BankAccount

    # 銀行口座クラスが存在することを確認する
    assert BankAccount is not None


@pytest.mark.stage02
def test_bank_name():
    from kadai.bank_account import BankAccount

    account = BankAccount("Taro", 1000, "123456789")
    # 銀行名が正しいことを確認する
    assert account.bank_name == "水戸電子銀行"
```

## fixture

- `kadai` fixture は `tests/conftest.py` で定義済み
- ステージ固有の fixture は `tests/stages/stageXX/conftest.py` に配置
