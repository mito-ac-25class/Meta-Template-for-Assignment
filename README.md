# Python 課題テンプレート

本リポジトリは、Github Classroom で配布する Python 用課題テンプレートリポジトリを作成するためのテンプレートです。

## 教員向け: GitHub Classroom 課題作成手順

### 1. 課題テンプレートリポジトリの作成
1. GitHub 上の本リポジトリから Use this template > Create a new repository を選択
2. Repository name に課題名、Description にリポジトリの説明を記述
3. visibility で Private が選択されていることを確認し、Create repository を選択
4. 作成したリポジトリの Settings > General から Template repository に✅を入れる

### 2. 課題作成
1. `src/kadai/` に Python プログラムの雛形を配置
2. `tests/stages/` に段階的なテストを配置
3. `pytest.ini` の `markers` にテストに合わせたマーカーを定義
4. `.github/workflows/classroom.yml` にステージ毎のテストを設定
5. README の [課題内容](#課題内容) を記述し、課題作成手順を削除

### 3. 課題割り当て
1. [Github Classroom](https://classroom.github.com/classrooms) のクラスから + New assignment を選択
2. Assignment title, Deadline をそれぞれ設定し、Individual assignmenet が選択されていることを確認して Continue
3. Find a Github repository から [2.課題作成](#2-課題作成) で作成したリポジトリを検索して選択
4. visibility が Private、Copy the default branch only にのみ✅が付いていることを確認
5. Add a supported editor で Github Codespaces を選択して Continue
6. Add autograding tests に表示される YAML にテストが設定されていることを確認し Create assignment

### 4. 課題を開く
1. 課題の Copy invite link を生徒に共有
2. 招待を Accept 後、Open in Github Codespaces ボタンから課題実施

---

## 課題内容

<!-- ここに具体的な課題内容を記載してください -->

**例: 四則演算関数の実装**

`src/kadai/` 内に以下の関数を実装してください：
1. `add_one(x)`: 引数に1を加算する関数
2. その他、段階的に要求される関数

## 実行方法

### 段階別テスト実行
```bash
# 初回のみ実行が必要
chmod +x ./scripts/test
```

```bash
# Stage 1 のテストのみ実行
./scripts/test 1

# Stage 2 のテストのみ実行  
./scripts/test 2
```

### 全ステージ一括テスト実行
```bash
pytest
```

## プログラム作成ガイド

1. `src/kadai/` ディレクトリ内にPythonファイルを作成
2. `src/kadai/__init__.py` で適切にインポートしているか確認
3. テストを実行して動作確認
4. 先のテスト結果が変わらないようにしながら、次の段階のテストに通るよう修正

## 提出方法

1. 変更を行ったファイルを全て `Ctrl + S` で保存しておく
2. 左側の「ソース管理」タブ > コミットの下の「変更」にカーソルを合わせ、「すべての変更をステージ」を選択
3. コミットの上に変更内容を簡単に記述する(空欄はエラーになる)
4. コミット後、変更を同期を押下すると提出されます

## 自動採点の確認方法

課題リポジトリでは、課題の提出と同時に自動採点が行なわれます。

1. Github で自身の課題リポジトリを開く(`https://classroom.github.com/mito-ac-25class/[課題名]-[Githubアカウント名]`)
2. Actions タブ内で最新の workflow runs を選択
3. run-autograding-test > Autograding Reporter に、テストの通過状況と得点が記載されています。