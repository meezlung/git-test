# pyright: strict

from lab05b import num_trips 

def test_num_trips():
    assert num_trips([(1, 2), (2, 3), (3, 4)], 2) == [3, 5, 5, 3]