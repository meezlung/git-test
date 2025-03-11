# pyright: strict

from lab05d import PancakeTowers

def test_PancakeTowers():
    pancake_towers = PancakeTowers([1, 2, 3], [3, 2, 1], [2, 2, 2])

    assert pancake_towers.sum_radii(1, 2, 3) == 3
    assert pancake_towers.sum_radii(3, 2, 4) == 5
    assert pancake_towers.sum_radii(4, 2, 4) == 6
    assert pancake_towers.sum_radii(5, 2, 4) == 6
    assert pancake_towers.sum_radii(7, 2, 7) == 11
    assert pancake_towers.sum_radii(5, 1, 5) == 9

    # TODO add more tests here
