from typing import List
import random
import sys

import heapq
from enum import Enum


class Action(Enum):
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)


class Cell(Enum):
    OPEN = 0
    ROBOT = 1
    BLOCKED = 2
    GOAL = 3


def pick_random_cell(grid: List[List[Cell]]) -> tuple[int, int]:
    rows = len(grid)
    cols = len(grid[0])
    r = random.randrange(rows)
    c = random.randrange(cols)
    return (r, c)


def generate_grid(d: int) -> List[List[Cell]]:
    grid = [[Cell.BLOCKED for _ in range(d)] for _ in range(d)]
    return grid


def inbounds(grid: List[List[Cell]], r: int, c: int) -> bool:
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


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
    open_count = 0
    for direction in Action:
        dir_y, dir_x = direction.value
        nr, nc = r + dir_y, c + dir_x
        if inbounds(grid, nr, nc):
            if grid[nr][nc] is Cell.OPEN:
                open_count += 1
    return open_count == 1


def set_random_goal_cell(grid: list[list[Cell]]) -> None:
    open_cells = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] is Cell.OPEN:
                open_cells.append((r, c))

    if len(open_cells) == 0:
        raise RuntimeError("No open cells available to set as goal.")

    goal_row, goal_col = random.choice(open_cells)
    grid[goal_row][goal_col] = Cell.GOAL
    print(f"Goal set at cell ({goal_row}, {goal_col})")


def fill_open_with_robot(grid: list[list[Cell]]) -> None:
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] is Cell.OPEN:
                grid[r][c] = Cell.ROBOT


def generate_ship_layout(grid: List[List[Cell]]) -> List[List[Cell]]:
    cell_queue = []

    start_row, start_col = pick_random_cell(grid)
    grid[start_row][start_col] = Cell.OPEN

    print(f"Starting at cell ({start_row}, {start_col})")

    heapq.heappush(cell_queue, (random.random(), (start_row, start_col)))

    while cell_queue:
        _, (r, c) = heapq.heappop(cell_queue)

        neighbors = [
            (r + act_y, c + act_x) for act_y, act_x in (act.value for act in Action)
        ]

        for nr, nc in neighbors:
            if (
                inbounds(grid, nr, nc)
                and grid[nr][nc] is Cell.BLOCKED
                and has_one_open_neighbor(grid, nr, nc)
            ):
                print(f"Opening cell ({nr}, {nc})")
                grid[nr][nc] = Cell.OPEN
                heapq.heappush(cell_queue, (random.random(), (nr, nc)))
            else:
                print(f"Skipping cell ({nr}, {nc})")

    return grid


def move(grid: list[list[Cell]], direction: Action) -> None:
    orig = [row.copy() for row in grid]

    rows, columns = len(grid), len(grid[0])
    move_y, move_x = direction.value

    # this function captures rows/columns from the outer scope
    def inbounds(r: int, c: int) -> bool:
        return 0 <= r < rows and 0 <= c < columns

    # Write results directly into `grid`
    for r in range(rows):
        for c in range(columns):
            cell = orig[r][c]
            if cell in (Cell.BLOCKED, Cell.GOAL):
                continue

            prev_y, prev_x = r - move_y, c - move_x
            next_y, next_x = r + move_y, c + move_x

            robot_incoming = (
                inbounds(prev_y, prev_x) and orig[prev_y][prev_x] is Cell.ROBOT
            )
            robot_hit_wall = cell is Cell.ROBOT and (
                not inbounds(next_y, next_x) or orig[next_y][next_x] is Cell.BLOCKED
            )

            if robot_incoming or robot_hit_wall:
                grid[r][c] = Cell.ROBOT
            else:
                grid[r][c] = Cell.OPEN


def main():
    maze_size = 5
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

    # Example movement:
    for _ in range(10):
        move(ship_layout, Action.UP)
        print("Moving robot UP")
        print_maze(ship_layout)


if __name__ == "__main__":
    main()
