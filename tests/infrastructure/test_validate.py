"""validate.py のテスト"""
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from validate import validate_schema, validate_business_rules, load_yaml


SCHEMA_PATH = Path(__file__).parent.parent.parent / "schema" / "topics.schema.yaml"


@pytest.fixture
def schema():
    return load_yaml(SCHEMA_PATH)


@pytest.fixture
def valid_topics():
    return {
        "title": "テスト課題",
        "language": "python",
        "topics": ["変数"],
        "prerequisites": ["基本文法"],
        "learning_goals": ["変数を使えるようになれることができる"],
        "difficulty": "初級",
        "estimated_time": {
            "tutorial_minutes": 0,
            "implementation_minutes": 30,
            "total_minutes": 30,
        },
        "tutorial_required": False,
        "tutorial_reason": "",
        "tutorial_topics": [],
        "stages": [
            {
                "name": "stage01",
                "feature": "変数の定義",
                "acceptance_criteria": "変数が定義できる",
                "score": 100,
            }
        ],
    }


def test_valid_topics_pass_schema(schema, valid_topics):
    """正しい topics がスキーマバリデーションを通ることを確認"""
    errors = validate_schema(valid_topics, schema)
    assert errors == []


def test_empty_title_fails(schema, valid_topics):
    """空のタイトルでバリデーションが失敗することを確認"""
    valid_topics["title"] = ""
    errors = validate_schema(valid_topics, schema)
    assert any("title" in e for e in errors)


def test_invalid_difficulty_fails(schema, valid_topics):
    """不正な難易度でバリデーションが失敗することを確認"""
    valid_topics["difficulty"] = "超上級"
    errors = validate_schema(valid_topics, schema)
    assert any("difficulty" in e for e in errors)


def test_learning_goal_pattern_fails(schema, valid_topics):
    """学習目標が「できる」で終わらない場合に失敗することを確認"""
    valid_topics["learning_goals"] = ["変数を学ぶ"]
    errors = validate_schema(valid_topics, schema)
    assert any("learning_goals" in e for e in errors)


def test_scores_must_sum_to_100(valid_topics):
    """スコアの合計が100でない場合にビジネスルールが失敗することを確認"""
    valid_topics["stages"][0]["score"] = 50
    errors = validate_business_rules(valid_topics)
    assert any("100" in e for e in errors)


def test_sequential_stage_names(valid_topics):
    """ステージ名が連番でない場合にビジネスルールが失敗することを確認"""
    valid_topics["stages"] = [
        {"name": "stage02", "feature": "f", "acceptance_criteria": "a", "score": 100}
    ]
    errors = validate_business_rules(valid_topics)
    assert any("stage01" in e for e in errors)


def test_tutorial_minutes_required_when_tutorial(valid_topics):
    """チュートリアル必須時に tutorial_minutes が 0 だと失敗することを確認"""
    valid_topics["tutorial_required"] = True
    valid_topics["estimated_time"]["tutorial_minutes"] = 0
    errors = validate_business_rules(valid_topics)
    assert any("tutorial_minutes" in e for e in errors)
