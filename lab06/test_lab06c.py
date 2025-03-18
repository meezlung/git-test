
from lab06c import max_plushies

def test_packet_flood():
    assert max_plushies([2, 0, 0, 0], [
        (1, 2),
        (1, 3),
        (2, 3),
        (2, 4),
        (3, 4),
    ], [4]) == 2