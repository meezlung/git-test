from dataclasses import dataclass

Route = tuple[tuple[str, str], int]

@dataclass(frozen=True)
class Result:
    shortest_time: int
    num_ways: int
    min_routes: int
    max_routes: int