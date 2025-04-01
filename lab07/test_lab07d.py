# pyright: strict

from lab07d import Investigation

def test_Investigation():
    investigation = Investigation(5, ((1, 2), (2, 4), (1, 3), (3, 4), (2, 3), (4, 5)))

    assert investigation.min_shared_spots(1, 4) == 0
    assert investigation.min_shared_spots(2, 5) == 1

    # TODO add more tests here
