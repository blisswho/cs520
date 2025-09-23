from typing import List
import heapq, random
from .types import Cell, Action
from .utils import inbounds, pick_random_cell


def generate_grid(d: int) -> List[List[Cell]]:
    return [[Cell.BLOCKED for _ in range(d)] for _ in range(d)]


def set_random_goal_cell(grid: List[List[Cell]]) -> tuple[int, int]:
    open_cells = [
        (r, c)
        for r in range(len(grid))
        for c in range(len(grid[0]))
        if grid[r][c] is Cell.OPEN
    ]
    if not open_cells:
        raise RuntimeError("No open cells available to set as goal.")
    r, c = random.choice(open_cells)
    return (r, c)


def fill_open_with_robot(grid: List[List[Cell]]) -> None:
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] is Cell.OPEN:
                grid[r][c] = Cell.ROBOT


def has_one_open_neighbor(grid: List[List[Cell]], r: int, c: int) -> bool:
    open_count = 0
    for action in Action:
        dy, dx = action.value
        nr, nc = r + dy, c + dx
        if inbounds(grid, nr, nc) and grid[nr][nc] is Cell.OPEN:
            open_count += 1
    return open_count == 1


def generate_ship_layout(grid: List[List[Cell]]) -> List[List[Cell]]:
    pq = []
    sr, sc = pick_random_cell(grid)
    grid[sr][sc] = Cell.OPEN
    heapq.heappush(pq, (random.random(), (sr, sc)))

    while pq:
        _, (r, c) = heapq.heappop(pq)
        neighbors = [(r + dy, c + dx) for dy, dx in (a.value for a in Action)]
        for nr, nc in neighbors:
            if (
                inbounds(grid, nr, nc)
                and grid[nr][nc] is Cell.BLOCKED
                and has_one_open_neighbor(grid, nr, nc)
            ):
                grid[nr][nc] = Cell.OPEN
                heapq.heappush(pq, (random.random(), (nr, nc)))
    return grid
