# Python 課題テンプレート

本リポジトリは、学生のプログラミング課題および課題採点用のCIを作成するための複数のプロンプトファイルを含むテンプレート・ツールキットです。  
GitHub Copilot Agents を使用して、初学者の学生が最先端のコーディング技術を身に着けることが出来るような課題リポジトリを効率的に作成できます。

## リポジトリ構成

```text
.
├─ .devcontainer          # 開発コンテナ設定
├─ .github
│   ├─ prompts           # エージェント用プロンプトファイル
│   │   ├─ implement-test.admin.prompt.md # テスト実装と検証
│   │   ├─ plan.admin.prompt.md           # 課題プラン作成
│   │   ├─ readme.admin.prompt.md         # release/README.md 作成
│   │   ├─ release.admin.prompt.md        # リリース準備
│   │   ├─ suggest-scenario.admin.prompt.md # シナリオ案提案（Optional）
│   │   ├─ topics.admin.prompt.md         # トピック整理
│   │   ├─ tutorial.admin.prompt.md       # TUTORIAL.md 作成
│   │   └─ verify.admin.prompt.md         # 包括的検証
│   └─ workflows         # GitHub Actions 設定
├─ agent-input           # エージェント入力ファイル
│   └─ topics.md        # 学習トピック定義
├─ agent-output          # エージェント出力ファイル
│   ├─ plan.md          # 課題実施プラン
│   └─ scenario0.md, scenario1.md, scenario2.md # シナリオ案（/suggest-scenario.admin 使用時）
├─ release               # リリース用ファイル
│   ├─ README.md        # 学生向けREADME
│   └─ evac.AGENTS.md   # 学生向けAGENTS.md
├─ src
│   ├─ kadai            # 課題実装用ディレクトリ
│   └─ tutorial         # チュートリアル用ディレクトリ
├─ templates             # テンプレートファイル
│   ├─ template.plan.md  # プランテンプレート
│   ├─ template.README.md # README テンプレート
│   ├─ template.scenario.md # シナリオ案テンプレート
│   └─ template.TUTORIAL.md # TUTORIAL テンプレート
├─ tests                 # テストファイル
│   ├─ stages           # ステージ別テスト
│   └─ tutorial         # チュートリアルテスト
├─ AGENTS.md             # エージェント動作制御（開発用）
├─ README.md             # 本ファイル
└─ TUTORIAL.md           # チュートリアルドキュメント
```

## ローカル開発環境のセットアップ

### 依存関係のインストール

ローカル環境でテストを実行する場合は、事前に開発用の依存関係をインストールする必要があります。

```bash
pip install -r requirements-dev.txt
```

このコマンドにより、pytest などのテスト実行に必要なパッケージがインストールされます。

### GitHub Codespaces / Dev Container を使用する場合

GitHub Codespaces または Dev Container を使用している場合は、`.devcontainer/devcontainer.json` の設定により依存関係が自動的にインストールされるため、手動でのインストールは不要です。

## 教員向け: GitHub Classroom 課題作成手順

### 大まかなフロー

```mermaid
flowchart TD
    Start([開始]) --> Step1[1. トピック記入<br/>agent-input/topics.md<br/>⏱️ 15-30分]
    Step1 --> Step2[2. トピッククリーン<br/>/topics.admin<br/>⏱️ 2-3分]
    Step2 --> Optional1{シナリオ案<br/>必要?}
    
    Optional1 -->|はい| Step3[3. シナリオ案提案<br/>/suggest-scenario.admin<br/>⏱️ 3-5分]
    Optional1 -->|いいえ| Step4
    Step3 --> Step3Review[シナリオ選択と<br/>topics.md更新<br/>⏱️ 5-10分]
    Step3Review --> Step4
    
    Step4[4. 課題プラン作成<br/>/plan.admin<br/>⏱️ 5-10分]
    Step4 --> Step5[5. 教員レビュー<br/>plan.md確認・調整<br/>⏱️ 10-30分]
    
    Step5 --> Optional2{チュートリアル<br/>必要?}
    Optional2 -->|はい| Step6[6. チュートリアル作成<br/>/tutorial.admin<br/>⏱️ 10-15分]
    Optional2 -->|いいえ| Step7
    Step6 --> Step7
    
    Step7[7. README作成<br/>/readme.admin<br/>⏱️ 3-5分]
    Step7 --> Step8[8. CIテスト実装・検証<br/>/implement-test.admin<br/>⏱️ 15-30分]
    Step8 --> Step9[9. 包括的チェック<br/>/verify.admin<br/>⏱️ 10-15分]
    Step9 --> Step10[10. リリース準備<br/>/release.admin<br/>⏱️ 2-3分]
    Step10 --> End([完了])
    
    classDef optionalStep fill:#ffd700,stroke:#ff8c00,stroke-width:2px
    classDef requiredStep fill:#87ceeb,stroke:#4682b4,stroke-width:2px
    classDef reviewStep fill:#ffb6c1,stroke:#ff69b4,stroke-width:2px
    classDef decisionStep fill:#98fb98,stroke:#228b22,stroke-width:2px
    
    class Step3,Step6 optionalStep
    class Step1,Step2,Step4,Step7,Step8,Step9,Step10 requiredStep
    class Step5,Step3Review reviewStep
    class Optional1,Optional2 decisionStep
```

**凡例:**
- 🔵 青色: 必須ステップ
- 🟡 黄色: オプショナルステップ
- 🟢 緑色: 条件分岐
- 🔴 ピンク: レビュー・手動確認

**詳細ステップ:**

1. 課題で取り扱うトピックを記入 -> [topics.md](agent-input/topics.md)
2. トピックをクリーン -> `/topics.admin`
3. (Optional) シナリオ案を提案 -> `/suggest-scenario.admin`
4. 課題プランを作成 -> `/plan.admin`
5. **教員によるレビュー** -> [plan.md](agent-output/plan.md)
6. (Optional)チュートリアルの作成 -> `/tutorial.admin`
7. READMEの作成 -> `/readme.admin`
8. CIテストの実装と検証 -> `/implement-test.admin`
9. 課題の整合性を包括的にチェック -> `/verify.admin`
10. リリース用にファイルの整理 -> `/release.admin`

### 1. 課題テンプレートリポジトリの作成

1. GitHub 上の本リポジトリから **Use this template** > **Create a new repository** を選択
2. **Repository name** に課題名、**Description** にリポジトリの説明を記述
3. **visibility** で **Private** が選択されていることを確認し、**Create repository** を選択
4. 作成したリポジトリの **Settings** > **General** から **Template repository** に✅を入れる

### 2. 課題の設計と実装

#### 2.1 トピックの定義

1. `agent-input/topics.md` を開き、課題で取り扱うトピックを記入する
   - 学習トピック一覧
   - 事前知識レベル
   - 学習目標
   - 難易度
   - 想定学習時間
   - 補足情報（任意）

#### 2.2 トピックのクリーンアップ

1. GitHub Copilot Chat で `/topics.admin` を実行
   - `agent-input/topics.md` から入力例やコメントを削除
   - クリーンなトピック定義を作成

#### 2.2.1 シナリオ案の提案（Optional）

1. GitHub Copilot Chat で `/suggest-scenario.admin` を実行
   - トピックに基づいて3つのシナリオ案を自動生成
   - `agent-output/scenario0.md`, `scenario1.md`, `scenario2.md` に出力される
2. 出力されたシナリオ案をレビューし、採用するシナリオを決定
3. `agent-input/topics.md` の末尾に採用シナリオのパスを追記:
   ```markdown
   ## 採用シナリオ
   agent-output/scenario{N}.md
   ```

#### 2.3 課題プランの作成

1. GitHub Copilot Chat で `/plan.admin` を実行
   - トピックに基づいて課題実施プランを自動生成
   - `agent-output/plan.md` に出力される

#### 2.3.1 README 作成（テンプレート利用）

1. GitHub Copilot Chat で `/readme.admin` を実行
   - プランに基づいてリリース用 `release/README.md` を自動作成

#### 2.4 プランの確認と調整

1. `agent-output/plan.md` を確認し、必要に応じて課題実施プランを修正

#### 2.5 チュートリアルの作成（必要に応じて）

1. `agent-output/plan.md` の「チュートリアルの必要性」で「必要」と判断された場合、GitHub Copilot Chat で `/tutorial.admin` を実行
   - 課題の前提知識をインプットするためのチュートリアルを自動作成
   - `TUTORIAL.md` に出力される

#### 2.6 テストの実装

1. GitHub Copilot Chat で `/implement-test.admin` を実行
   - 課題に沿ったテストを実装・検証
   - 検証用の模範解答コードが `agent-output/` に出力される

### 3. 課題の検証

1. GitHub Copilot Chat で `/verify.admin` を実行
   - 課題内容の明確性を確認
   - CIテストの設定と妥当性を検証
   - 不要なファイルの有無を確認
   - 必要に応じて修正

### 4. リリースの準備

1. **方法1: シェルスクリプトで自動実行（推奨）**
   ```bash
   ./scripts/release.sh
   ```
   - 開発用ファイル（`.admin.prompt.md`、`agent-input/*`、`agent-output/*`、`templates/*`）を削除
   - `release/README.md` → `README.md` に移動
   - `release/evac.AGENTS.md` → `AGENTS.md` に移動
   - 学生向けの状態に整理
   - 自動的にコミット・プッシュまで実行

2. **方法2: GitHub Copilot Chat で実行**
   - GitHub Copilot Chat で `/release.admin` を実行
   - 上記と同様の処理をエージェントが実行

### 5. 課題の割り当て

1. [Github Classroom](https://classroom.github.com/classrooms) のクラスから **+ New assignment** を選択
2. **Assignment title**, **Deadline** をそれぞれ設定し、**Individual assignment** が選択されていることを確認して **Continue**
3. **Find a Github repository** から作成したリポジトリを検索して選択
4. **visibility** が **Private**、**Copy the default branch only** にのみ✅が付いていることを確認
5. **Add a supported editor** で **Github Codespaces** を選択して **Continue**
6. **Add autograding tests** に表示される YAML にテストが設定されていることを確認し **Create assignment**

### 6. 課題の配布

1. 課題の **Copy invite link** を生徒に共有
2. 学生は招待を Accept 後、**Open in Github Codespaces** ボタンから課題実施

## プロンプトファイル概要

### `.admin` プロンプト（開発用）

開発用の `.admin` プロンプトは `/release.admin` によってリリース時に削除されます。

- **`/topics.admin`** (`topics.admin.prompt.md`)
  - `agent-input/topics.md` の内容から入力例・コメントなどのノイズを削除
  - `/plan.admin` で利用できるクリーンなトピック定義を出力

- **`/suggest-scenario.admin`** (`suggest-scenario.admin.prompt.md`)
  - トピック定義を基に、課題のシナリオ案を3つ提案
  - `agent-output/scenario[0-2].md` に出力し、教員のレビューを待つ
  - `/topics.admin` と `/plan.admin` の間にオプションで実行

- **`/plan.admin`** (`plan.admin.prompt.md`)
  - 課題で取り扱うトピックを基に課題実施手法を選定
  - ユーザーストーリーやテストシナリオをドラフト

- **`/readme.admin`** (`readme.admin.prompt.md`)
  - `agent-output/plan.md` の内容から課題説明用 `release/README.md` を作成

- **`/tutorial.admin`** (`tutorial.admin.prompt.md`)
  - 課題の前提知識をインプットするためのチュートリアル（`TUTORIAL.md`）を作成
  - プランでチュートリアルが「必要」と判断された場合に実行

- **`/implement-test.admin`** (`implement-test.admin.prompt.md`)
  - 課題用テストコードの実装
  - テストの実行・検証と修正
  - テスト周辺設定ファイルの修正

- **`/verify.admin`** (`verify.admin.prompt.md`)
  - 課題リポジトリの課題内容、CIテストの内容や設定に問題点が無いかを包括的にチェック
  - 必要に応じて修正を実施

- **`/release.admin`** (`release.admin.prompt.md`)
  - 課題リポジトリをリリース可能な状態とするために、不要なファイルを削除
  - 学生向けファイルを適切な位置に移動

## 課題実施方式

本テンプレートでは、以下の実施方式から選択できます：

### プログラム実装課題

- 学生は `README.md` の仕様や `tests/` のREDテストを前提に、`src/kadai/` 配下にプログラムを実装
- RED確認 → 1ステージGREEN → コミットのサイクルで進行
- CI で自動採点

### リファクタリング課題

- 実装済みのプログラムをリファクタリング
- GREEN状態のテストを維持しながら品質を改善
- ASTによるコード品質チェックで採点

### テスト実装課題

- バグのあるプログラムに対してテストを記述
- バグを検出できるかどうかで採点

### テスト駆動開発課題

- RED → GREEN → リファクタリングのサイクルで実装
- 現状はCI採点なし

## 注意事項

- 各ステップは教員が慎重に確認し、修正や続行の判断を下してください
- エージェントはフローの範囲を超えた作業や提案をしません
- `/verify.admin` でのチェックは必ず実施してください
- `/release.admin` 実行前に、必ずコミットして変更を保存してください
