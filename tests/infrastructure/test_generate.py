"""generate.py のテスト"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from generate import build_context, create_env, render_template, TEMPLATES_DIR


@pytest.fixture
def sample_context():
    return build_context({
        "title": "テスト課題",
        "stack": "python",
        "topics": ["変数"],
        "prerequisites": ["基本文法"],
        "learning_goals": ["変数を使えることができる"],
        "stages": [
            {"name": "stage01", "feature": "変数定義", "acceptance_criteria": "変数が定義できる", "score": 60},
            {"name": "stage02", "feature": "変数出力", "acceptance_criteria": "変数を出力できる", "score": 40},
        ],
        "tutorial_required": False,
    })


@pytest.fixture
def env():
    return create_env()


def test_build_context_defaults():
    """空の入力でもデフォルト値が設定されることを確認"""
    ctx = build_context({})
    assert ctx["title"] == ""
    assert ctx["stack"] == "python"
    assert ctx["stages"] == []
    assert ctx["tutorial_required"] is False


def test_build_context_override():
    """入力値がデフォルトを上書きすることを確認"""
    ctx = build_context({"title": "my title", "stack": "java"})
    assert ctx["title"] == "my title"
    assert ctx["stack"] == "java"


def test_classroom_template_renders(env, sample_context):
    """classroom.yml.j2 が正常にレンダリングされることを確認"""
    content = render_template(env, "classroom.yml.j2", sample_context)
    # ステージ名が含まれること
    assert "stage01" in content
    assert "stage02" in content
    # スコアが含まれること
    assert "max-score: 60" in content
    assert "max-score: 40" in content
    # GitHub Actions 式が正しくエスケープされること
    assert "${{steps.stage01.outputs.result}}" in content
    # runners が正しいこと
    assert "runners: stage01,stage02" in content


def test_plan_template_renders(env, sample_context):
    """plan.md.j2 が正常にレンダリングされることを確認"""
    content = render_template(env, "plan.md.j2", sample_context)
    assert "テスト課題" in content
    assert "変数" in content
    assert "変数定義" in content


def test_readme_template_renders(env, sample_context):
    """README.md.j2 が正常にレンダリングされることを確認"""
    content = render_template(env, "README.md.j2", sample_context)
    assert "テスト課題" in content
    assert "stage01" not in content  # マーカー名ではなくステージ番号
    assert "| 1 |" in content


def test_tutorial_template_renders(env, sample_context):
    """TUTORIAL.md.j2 が正常にレンダリングされることを確認"""
    sample_context["tutorial_required"] = True
    content = render_template(env, "TUTORIAL.md.j2", sample_context)
    assert "テスト課題" in content
    assert "基本文法" in content


def test_classroom_template_django_react(env):
    """django-react スタックで classroom.yml.j2 が正しくレンダリングされることを確認"""
    ctx = build_context({
        "title": "Django React 課題",
        "stack": "django-react",
        "stages": [
            {"name": "stage01", "feature": "API実装", "acceptance_criteria": "APIが動作する", "score": 50},
            {"name": "stage02", "feature": "UI実装", "acceptance_criteria": "UIが動作する", "score": 50},
        ],
    })
    content = render_template(env, "classroom.yml.j2", ctx)
    # Python と Node.js のセットアップが含まれること
    assert "setup-python" in content
    assert "setup-node" in content
    # バックエンド・フロントエンドの依存インストールが含まれること
    assert "pip install" in content
    assert "npm ci" in content
    # Jest コマンドが --prefix 付きで正しく構成されていること
    assert "npx --prefix src/kadai/frontend jest tests/stages/stage01/ --passWithNoTests" in content
    # ステージ名とスコアが含まれること
    assert "stage01" in content
    assert "stage02" in content
    assert "max-score: 50" in content


def test_classroom_template_javascript(env):
    """javascript スタックで classroom.yml.j2 が正しくレンダリングされることを確認"""
    ctx = build_context({
        "title": "JavaScript 課題",
        "stack": "javascript",
        "stages": [
            {"name": "stage01", "feature": "関数実装", "acceptance_criteria": "関数が動作する", "score": 100},
        ],
    })
    content = render_template(env, "classroom.yml.j2", ctx)
    assert "setup-node" in content
    assert 'cache: "npm"' in content
    assert 'cache-dependency-path: "src/kadai/package-lock.json"' in content
    assert "cd src/kadai && npx jest --ci ../../tests/stages/stage01/ --passWithNoTests" in content


def test_classroom_template_with_no_stages(env):
    """ステージなしで classroom.yml.j2 がエラーにならないことを確認"""
    ctx = build_context({"stages": []})
    content = render_template(env, "classroom.yml.j2", ctx)
    assert "Autograding Tests" in content
    assert "runners: " in content
