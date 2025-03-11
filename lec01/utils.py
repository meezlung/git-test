from dataclasses import dataclass
from typing import TypeVar, Generic
T = TypeVar('T')

@dataclass
class Edge(Generic[T]):
    x: T
    y: T
    weight: int