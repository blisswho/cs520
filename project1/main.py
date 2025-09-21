from typing import List
import random
import sys

import heapq
from enum import Enum


class Cell(Enum):
    OPEN = 0
    BLOCKED = 1
    ROBOT = 2
    GOAL = 3


def pick_random_cell(grid: List[List[int]]):
    rows = len(grid)
    cols = len(grid[0])
    r = random.randrange(rows)
    c = random.randrange(cols)
    return (r, c)


def generate_grid(d: int) -> List[List[int]]:
    grid = [[Cell.BLOCKED for _ in range(d)] for _ in range(d)]
    return grid


def print_maze(maze: list[list[Cell]]) -> None:
    width = len(maze[0])
    # Top border
    print("┌" + "─" * (2 * width + 1) + "┐")
    for row in maze:
        # Print each cell with borders
        print("│ " + " ".join(str(cell.value) for cell in row) + " │")
    # Bottom border
    print("└" + "─" * (2 * width + 1) + "┘")


def has_one_open_neighbor(grid: list[list[Cell]], r: int, c: int) -> bool:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    open_count = 0
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            if grid[nr][nc] == Cell.OPEN:
                open_count += 1
    return open_count == 1


def set_random_goal_cell(grid: list[list[Cell]]) -> None:
    open_cells = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == Cell.OPEN:
                open_cells.append((r, c))
    
    if len(open_cells) == 0:
        raise RuntimeError("No open cells available to set as goal.")
    
    goal_row, goal_col = random.choice(open_cells)
    grid[goal_row][goal_col] = Cell.GOAL
    print(f"Goal set at cell ({goal_row}, {goal_col})")


def fill_open_with_robot(grid: list[list[Cell]]) -> None:
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == Cell.OPEN:
                grid[r][c] = Cell.ROBOT


def generate_ship_layout(grid: List[List[int]]):
    cell_queue = []

    start_row, start_col = pick_random_cell(grid)
    grid[start_row][start_col] = Cell.OPEN

    print(f"Starting at cell ({start_row}, {start_col})")

    heapq.heappush(cell_queue, (random.random(), (start_row, start_col)))

    while cell_queue:
        _, (r, c) = heapq.heappop(cell_queue)

        actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = [(r + act_y, c + act_x) for act_y, act_x in actions]

        for nr, nc in neighbors:
            if (
                0 <= nr < len(grid)
                and 0 <= nc < len(grid[0])
                and grid[nr][nc] == Cell.BLOCKED
                and has_one_open_neighbor(grid, nr, nc)
            ):
                print(f"Opening cell ({nr}, {nc})")
                grid[nr][nc] = Cell.OPEN
                heapq.heappush(cell_queue, (random.random(), (nr, nc)))
            else:
                print(f"Skipping cell ({nr}, {nc})")

    return grid


def main():
    maze_size = 10
    if len(sys.argv) > 1:
        try:
            maze_size = int(sys.argv[1])
        except ValueError:
            print("Invalid maze size argument, using default.")

    grid = generate_grid(maze_size)
    ship_layout = generate_ship_layout(grid)
    print_maze(ship_layout)
    print("Setting random goal cell...")
    set_random_goal_cell(ship_layout)
    fill_open_with_robot(ship_layout)
    print_maze(ship_layout)


if __name__ == "__main__":
    main()
