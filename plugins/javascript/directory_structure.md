# JavaScript プロジェクト構成

## ディレクトリ構成

```
src/kadai/
├── package.json         # 依存関係 + Jest 設定
├── package-lock.json    # ロックファイル（npm install 後に生成・コミット推奨、必須ではない）
├── <module>.js          # 学生が実装するモジュール
└── ...

tests/
└── stages/
    ├── stage01/
    │   └── test_<module>.test.js
    ├── stage02/
    │   └── test_<module>.test.js
    └── ...
```

## 技術スタック

- Node.js 20+
- Jest 29+（テストフレームワーク）

## package.json 最小構成

```json
{
  "name": "kadai",
  "private": true,
  "scripts": {
    "test": "jest ../../tests/stages/ --verbose"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  },
  "jest": {
    "rootDir": "../..",
    "testMatch": ["<rootDir>/tests/stages/**/test_*.test.js"]
  }
}
```

## テスト実行

```bash
# 全テスト（リポジトリルートから実行）
cd src/kadai && npx jest ../../tests/stages/ --verbose

# ステージ別（リポジトリルートから実行）
cd src/kadai && npx jest ../../tests/stages/stage01/ --verbose
```

## CI（GitHub Classroom）

各ステージで Jest を実行し、全テストが通過した場合にステージクリアとする。
