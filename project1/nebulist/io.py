from typing import List
from .types import Cell


def print_maze(maze: List[List[Cell]]) -> None:
    for row in maze:
        print("".join(f"[{str(cell)}]" for cell in row))
