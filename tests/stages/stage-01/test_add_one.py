import pytest

@pytest.mark.stage01
def test_add_one_exists():
    from kadai import add_one

    assert add_one(1) == 2, "add_one(1) は 2 を返すべきです"

@pytest.mark.stage01
def test_add_one_negative():
    from kadai import add_one

    assert add_one(-1) == 0, "add_one(-1) は 0 を返すべきです"