
from lab06e import packet_flood

def test_packet_flood():
    assert packet_flood([10**12, 4, 10**12], [
        (1, 2, 5),
        (2, 3, 5),
        (1, 3, 7),
    ]) == (
            11,
            [4, 4, 7],
            [11, 4, 11],
        )