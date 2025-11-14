
## 目的
このリポジトリは、学生のプログラミング課題および課題採点用のCIを作成するための複数のプロンプトファイルを含むテンプレート・ツールキットです。  
エージェントは、本`AGENTS.md` を基に、初学者の学生が最先端のコーディング技術を身に着けることが出来るような課題リポジトリ作成を支援してください。

## リポジトリ構成
```
.
├─ .devcontainer
├─ .github
│   ├─ prompts
│   │   ├─ plan.admin.prompt.md
│   │   ├─ release.admin.prompt.md
│   │   ├─ topics.admin.prompt.md
│   │   └─ verify.admin.prompt.md
│   └─ workflows
├─ agent-input
│   └─ topics.md
├─ agent-output
│   └─ plan.md
├─ release
│   ├─ README.md
│   └─ evac.AGENTS.md
├─ src
│   ├─ kadai
│   └─ tutorial
├─ templates
│   └─ template.plan.md
├─ tests
│   ├─ stages
│   │   └─ stage-0X
│   └─ tutorial
├─ .gitignore
├─ AGENTS.md
├─ README.md
├─ TUTORIAL.md
├─ copilot.log
├─ pyproject.toml
├─ pytest.ini
├─ requirements-dev.txt
└─ requirements.txt
```

## プロンプトファイル概要 (`.github/prompts`)

### `.admin` プロンプト (開発用)
開発用 `.admin` プロンプトは `release.admin.prompt.md` によって削除されます。

- `plan.admin.prompt.md`
	- 課題で取り扱うトピックを基に課題実施手法を選定し、ユーザーストーリーやテストシナリオをドラフトします。

- `release.admin.prompt.md`
	- 課題リポジトリをリリース可能な状態とするために、不要なファイルを削除し、必要なファイルを整理します。

- `topics.admin.prompt.md`
	- agent-input/topics.md の内容から入力例・コメントなどのノイズを削除し、/plan.admin で利用できるクリーンなトピック定義を出力します。

- `verify.admin.prompt.md`
	- 課題リポジトリの課題内容、CIテストの内容や設定に問題点が無いかを包括的にチェックし、修正します。

### ユーティリティプロンプト (学習用)
学習用プロンプトはユーティリティとして学生が使用出来る状態でリリースします。  
現在リポジトリにユーティリティプロンプトはありません。

## 想定フロー
1. 課題を実装する
	1. リポジトリで取り扱うトピックを決定し、`agent-input/topics.md` に記入する。
	2. `/topics.admin` を実行し、不要な情報を削除する。
	3. `/plan.admin` を実行し、課題実施プランを作成する。
	4. `agent-output/plan.md` を確認し、必要に応じて課題実施プランを修正する。
	5. 必要に応じて `TUTORIAL.md` を作成し、課題の前提知識をインプットするためのチュートリアルを記述する
	6. `release/README.md` に課題内容を記述する
	7. `tests/` 配下にテストを実装する
2. `/verify.admin` で課題の包括的チェックを行う
3. `/release.admin` で課題リポジトリをリリース可能状態とする

## 注意
- フローは各ステップごとに教員が慎重に確認し、修正や続行の判断を下します。エージェントはフローの範囲を超えた作業や提案をしてはいけません。