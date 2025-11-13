
## 目的
このリポジトリは、学生のプログラミング課題および課題採点用のCIを作成するための複数のプロンプトファイルを含むテンプレート・ツールキットです。  
エージェントは、本`AGENTS.md` を基に、初学者の学生が最先端のコーディング技術を身に着けることが出来るような課題リポジトリ作成を支援してください。

## リポジトリ構成
```
.
├─ .devcontainer
├─ .github
│   ├─ prompts
│   └─ workflows
├─ release
│   ├─ README.md
│   └─ evac.AGENTS.md
├─ src
│   ├─ kadai
│   └─ tutorial
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

- `release.admin.prompt.md`
	- 課題リポジトリをリリース可能な状態とするために、不要なファイルを削除し、必要なファイルを整理します。

- `verify.admin.prompt.md`
	- 課題リポジトリの課題内容、CIテストの内容や設定に問題点が無いかを包括的にチェックし、修正します。

### ユーティリティプロンプト (学習用)
学習用プロンプトはユーティリティとして学生が使用出来る状態でリリースします。  
現在リポジトリにユーティリティプロンプトはありません。

## 想定フロー
1. 課題を実装する
	1. リポジトリで取り扱うトピックを決定する
	2. 大まかな課題内容をドラフトする
	3. 必要に応じて `TUTORIAL.md` を作成し、課題の前提知識をインプットするためのチュートリアルを記述する
	4. `release/README.md` に課題内容を記述する
	5. `tests/` 配下にテストを実装する
2. `/verify.admin` で課題の包括的チェックを行う
3. `/release.admin` で課題リポジトリをリリース可能状態とする

## 注意
- フローは各ステップごとに教員が慎重に確認し、修正や続行の判断を下します。エージェントはフローの範囲を超えた作業や提案をしてはいけません。