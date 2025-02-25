# pyright: strict

from dataclasses import dataclass

@dataclass(frozen=True)
class ItemCount:
    item: str
    count: int

@dataclass(frozen=True)
class Recipe:
    item: str
    ingredients: list[ItemCount]
