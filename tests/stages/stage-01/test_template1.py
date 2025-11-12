import pytest

@pytest.mark.stage01
def test_1():
    from kadai.script import f

    assert f() == 0