
from lab07b import max_production

def test_max_production():
    assert max_production(((1, 2), (2, 3), (1, 3), (1, 4)), (1, 2, 3, 1)) == (6, [(1, 2), (2, 3), (3, 1), (4, 1)])
