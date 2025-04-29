from dataclasses import dataclass

@dataclass(frozen=True)
class Vec2D:
    x: int | float
    y: int | float

