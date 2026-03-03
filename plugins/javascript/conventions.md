# JavaScript テスト規約

## ディレクトリ構造

```
tests/
└── stages/
    ├── stage01/
    │   └── test_<module>.test.js
    ├── stage02/
    │   └── test_<module>.test.js
    └── ...
```

## テストファイル規約

### グループ化

- `describe("StageXX: <テスト対象>", () => { ... })` で囲む
- ステージ外のテストは書かない

### import

- `const { ... } = require("../../../src/kadai/<module>");` （CommonJS）
- テストファイルのトップレベルで require する
- 被テスト側モジュールも CommonJS 形式で `module.exports = { ... }` または `exports.foo = ...` としてエクスポートすること（ESM の `export` は使用しない）

### アサーション

- 1テストにつき1アサーション（推奨）
- アサーション前に日本語コメントで検証内容を説明

### 命名規則

- ファイル: `test_<module_name>.test.js`
- describe: `"StageXX: <テスト対象>"`
- test: `"<検証対象>が<期待結果>"`

## テストパターン例

```javascript
const { add, subtract } = require("../../../src/kadai/calculator");

describe("Stage01: 基本的な四則演算", () => {
  test("addが2つの数値の和を返す", () => {
    // 1 + 2 の結果が 3 であることを確認する
    expect(add(1, 2)).toBe(3);
  });

  test("subtractが2つの数値の差を返す", () => {
    // 5 - 3 の結果が 2 であることを確認する
    expect(subtract(5, 3)).toBe(2);
  });
});
```

## Jest 設定

- Jest の設定は `src/kadai/package.json` 内に記述する
- CI/ローカルともに「リポジトリルート」をカレントディレクトリとして `npx jest --config src/kadai/package.json` を実行する前提とする
- Jest の設定では `rootDir` をリポジトリルートを指すように設定し（例: `"rootDir": "../.."`）、`testMatch` で `<rootDir>/tests/stages/**/test_*.test.js` を対象にする
