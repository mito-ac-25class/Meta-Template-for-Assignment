"""Dynamic pytest configuration from topics.yaml."""
from pathlib import Path

import pytest
import yaml

TOPICS_PATH = Path(__file__).resolve().parent.parent / "agent-input" / "topics.yaml"


def pytest_configure(config):
    """Register stage markers dynamically from topics.yaml."""
    if not TOPICS_PATH.exists():
        return
    with open(TOPICS_PATH, encoding="utf-8") as f:
        topics = yaml.safe_load(f) or {}
    for stage in topics.get("stages", []):
        name = stage.get("name", "")
        feature = stage.get("feature", "")
        if name:
            config.addinivalue_line(
                "markers",
                f"{name}: {feature or f'{name} tests'}",
            )


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
