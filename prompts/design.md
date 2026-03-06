---
description: "課題設計: トピック検証 + シナリオ提案(任意) + 課題プラン作成を一括で行います"
allowed-tools: Read, Edit, Write, Bash, Glob
---

# Design フェーズ

課題の設計フェーズを実行します。トピック定義の検証、シナリオ提案（任意）、課題プランの作成までを一括で行います。

## 入力

- `agent-input/topics.yaml`（教員が記入済み）

## 出力

- `agent-input/topics.yaml`（検証済み、assignment_type・scenario が設定される）
- `agent-output/plan.md`（課題実施プラン）
- `agent-output/scenario0.md` 〜 `scenario2.md`（シナリオ提案時のみ）

## 手順

### Step 1: 入力バリデーション

`agent-input/topics.yaml` を検証します。

```bash
python scripts/validate.py
```

- エラーがあれば教員に報告し、修正を依頼してください
- 必須フィールドが空の場合は、文脈からドラフトして教員の確認を得てください

### Step 2: トピック確認

`agent-input/topics.yaml` の内容を教員に提示し、以下を確認します:

- 学習トピック一覧が明確で具体的か
- 事前知識レベルと学習目標が整合しているか
- 難易度が適切か
- 想定学習時間が妥当か

### Step 3: シナリオ提案（任意）

教員に「シナリオ案を提案しますか？」と確認してください。

**提案する場合:**

1. 3つの異なるシナリオ案を作成し、以下に出力:
   - `agent-output/scenario0.md`
   - `agent-output/scenario1.md`
   - `agent-output/scenario2.md`

2. 各シナリオは以下を含むこと:
   - シナリオタイトル
   - シチュエーション（3〜5行）
   - 課題概要（タイトル案、説明、到達目標）
   - 想定される実装内容（対象ファイル、ステップ概要、動作イメージ）
   - テストシナリオ案（ステージ・機能・テスト観点の表）
   - メリットと考慮事項
   - 推奨される課題実施方式

3. シナリオの多様性を確保:
   - ドメインの違い（ゲーム、業務システム、日常生活、科学）
   - スケールの違い（単機能 vs 複数連携機能）
   - アプローチの違い（データ中心 vs 振る舞い中心、手続き型 vs OOP）

4. 評価マトリクスを作成し `agent-output/scenario-evaluation.md` に出力:

   | 評価基準 | 重み |
   |---------|------|
   | 具体性 | 1.0 |
   | 親しみやすさ | 1.0 |
   | 実現可能性 | 1.5 |
   | 学習効果 | 2.0 |
   | 拡張性 | 0.5 |

5. 教員が採用シナリオを選択したら、その内容を `agent-input/topics.yaml` の `scenario` フィールドに反映

**提案しない場合:** Step 4 に進む

### Step 4: 課題実施方式の選定

トピックの難易度・学習目標に基づき、以下の4つから最適な方式を選定し、教員に提案します。

{{ASSIGNMENT_TYPES}}

選定した方式を `agent-input/topics.yaml` の `assignment_type` フィールドに設定します。

### Step 5: 課題プランの作成

`agent-input/topics.yaml` の全情報を基に `agent-output/plan.md` を作成します。

プランに含める内容:
1. 学習トピック一覧
2. 選定した課題実施方式と選定理由
3. 課題概要（タイトル、説明、到達目標）
4. ユーザーストーリー（動機、対象ファイル、初期状態）
5. テストシナリオ（ステージ構成、機能、受け入れ条件、点数配分）
6. 動作例（コード例と期待出力）
7. 実装方針・注意事項
8. チュートリアルの必要性と想定内容
9. CI設定方針
10. 次のステップ

プランの作成後、教員のレビューを待ちます。

### Step 6: Git 操作

{{GIT_WORKFLOW}}

**ブランチ名:** `feature/design-assignment`

```bash
git checkout -b feature/design-assignment
git add agent-input/topics.yaml agent-output/
git commit -m "feat: design assignment plan"
git push origin feature/design-assignment
```
