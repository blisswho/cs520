from typing import List, Tuple
import random
from .types import Cell


def inbounds(grid: List[List[Cell]], r: int, c: int) -> bool:
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def pick_random_cell(grid: List[List[Cell]]) -> Tuple[int, int]:
    rows, cols = len(grid), len(grid[0])
    return random.randrange(rows), random.randrange(cols)
