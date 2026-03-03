"""Dynamic pytest configuration from topics.yaml."""
from pathlib import Path

import pytest
import yaml

TOPICS_PATH = Path(__file__).resolve().parent.parent / "agent-input" / "topics.yaml"


def _load_topics():
    """Load topics.yaml and return its contents."""
    if not TOPICS_PATH.exists():
        return {}
    with open(TOPICS_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def pytest_configure(config):
    """Register stage markers dynamically from topics.yaml."""
    topics = _load_topics()
    for stage in topics.get("stages", []):
        name = stage.get("name", "")
        feature = stage.get("feature", "")
        if name:
            config.addinivalue_line(
                "markers",
                f"{name}: {feature or f'{name} tests'}",
            )

    # django-react スタックの場合、Django 設定を自動構成
    stack = topics.get("stack", "python")
    if stack == "django-react":
        import os
        settings = topics.get("scenario", {}).get(
            "django_settings", "config.settings"
        )
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)


@pytest.fixture
def kadai():
    """Provide the kadai package for tests.

    Override in stage-specific conftest.py for custom imports.
    """
    try:
        import kadai
        return kadai
    except ImportError:
        pytest.skip("kadai package not yet implemented")
