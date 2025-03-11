# pyright: strict

from lab05a import total_effort

def test_total_effort():
    assert total_effort([(1, 2, 2), (1, 3, 1), (1, 4, 3)], 3) == 24