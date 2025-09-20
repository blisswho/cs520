from typing import List
import random
import sys

import heapq


def pick_random_cell(grid: List[List[int]]):
    rows = len(grid)
    cols = len(grid[0])
    r = random.randrange(rows)
    c = random.randrange(cols)
    return (r, c)


def generate_grid(d: int) -> List[List[int]]:
    grid = [[1 for _ in range(d)] for _ in range(d)]
    return grid


def print_maze(maze: list[list[int]]) -> None:
    width = len(maze[0])
    # Top border
    print("┌" + "─" * (2 * width + 1) + "┐")
    for row in maze:
        # Print each cell with borders
        print("│ " + " ".join(str(cell) for cell in row) + " │")
    # Bottom border
    print("└" + "─" * (2 * width + 1) + "┘")


def has_one_open_neighbor(grid: list[list[int]], r: int, c: int) -> bool:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    zero_count = 0
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            if grid[nr][nc] == 0:
                zero_count += 1
    return zero_count == 1


def generate_ship_layout(grid: List[List[int]]):
    cell_queue = []

    start_row, start_col = pick_random_cell(grid)
    grid[start_row][start_col] = 0

    print(f"Starting at cell ({start_row}, {start_col})")

    heapq.heappush(cell_queue, (random.random(), (start_row, start_col)))

    while cell_queue:
        _, (r, c) = heapq.heappop(cell_queue)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = [(r + dr, c + dc) for dr, dc in directions]

        for nr, nc in neighbors:
            if (
                0 <= nr < len(grid)
                and 0 <= nc < len(grid[0])
                and grid[nr][nc] == 1
                and has_one_open_neighbor(grid, nr, nc)
            ):
                print(f"Opening cell ({nr}, {nc})")
                grid[nr][nc] = 0
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

    # TODO: Add first solution for task 2


if __name__ == "__main__":
    main()
