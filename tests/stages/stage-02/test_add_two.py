import pytest

@pytest.mark.stage02
def test_add_two_exists():
    from kadai import add_two

    assert add_two(3) == 5, "add_two(3) は 5 を返すべきです"

@pytest.mark.stage02  
def test_add_two_negative():
    from kadai import add_two

    assert add_two(-1) == 1, "add_two(-1) は 1 を返すべきです"
