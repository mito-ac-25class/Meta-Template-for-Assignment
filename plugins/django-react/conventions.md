# Django + React (Next.js) テスト規約

## ディレクトリ構造

```
tests/
├── conftest.py              # 動的マーカー登録 + 共通 fixture
└── stages/
    ├── stage01/
    │   ├── test_backend_<module>.py    # Django バックエンドテスト
    │   └── test_frontend_<module>.test.ts  # React フロントエンドテスト
    ├── stage02/
    │   ├── test_backend_<module>.py
    │   └── test_frontend_<module>.test.ts
    └── ...
```

## バックエンドテスト規約（Django / pytest）

### マーカー

- 全テスト関数に `@pytest.mark.stageXX` デコレータを付与
- マーカーは `tests/conftest.py` が `agent-input/topics.yaml` から動的に登録

### import

- テスト関数内で `from kadai.backend.<app>.<module> import <Class>` を行う
- トップレベル import は使わない（`pythonpath = src` による制約）

### アサーション

- 1テスト関数につき1アサーション（推奨）
- アサーション前に日本語コメントで検証内容を説明

### 命名規則

- ファイル: `test_backend_<module_name>.py`
- クラス: `TestStageXX` (任意)
- 関数: `test_<検証対象>_<期待結果>`

### テストパターン例

```python
import pytest


@pytest.mark.stage01
def test_model_exists():
    from kadai.backend.api.models import Task

    # Taskモデルが存在することを確認する
    assert Task is not None


@pytest.mark.stage02
def test_api_endpoint_returns_200(client):
    from kadai.backend.api.views import TaskViewSet

    # タスク一覧APIが200を返すことを確認する
    response = client.get("/api/tasks/")
    assert response.status_code == 200
```

### fixture

- `kadai` fixture は `tests/conftest.py` で定義済み
- Django テスト用に `client` fixture を使用（`pytest-django` 提供）
- ステージ固有の fixture は `tests/stages/stageXX/conftest.py` に配置

## フロントエンドテスト規約（React / Jest）

### テストファイル配置

- `tests/stages/stageXX/test_frontend_<module>.test.ts` に配置
- Jest の `testPathPattern` でステージ別実行

### 命名規則

- ファイル: `test_frontend_<component_name>.test.ts` または `test_frontend_<component_name>.test.tsx`
- describe: `StageXX: <機能名>`
- test: `<検証対象>が<期待結果>`

### テストパターン例

```typescript
import { render, screen } from "@testing-library/react";
import TaskList from "@/components/TaskList";

describe("Stage01: タスク一覧コンポーネント", () => {
  test("タスク一覧が表示される", () => {
    render(<TaskList tasks={[{ id: 1, title: "テスト" }]} />);

    // タスクのタイトルが画面に表示されることを確認する
    expect(screen.getByText("テスト")).toBeInTheDocument();
  });
});
```

### 実行コマンド

```bash
# 全フロントエンドテスト
npx jest tests/stages/ --passWithNoTests

# ステージ単体
npx jest tests/stages/stage01/ --passWithNoTests

# 特定ファイル
npx jest tests/stages/stage01/test_frontend_task_list.test.ts
```

## ステージのテスト対象

各ステージは backend のみ、frontend のみ、または両方のテストを持てます。
`topics.yaml` のステージ定義に基づき、適切なテストファイルを配置してください。
