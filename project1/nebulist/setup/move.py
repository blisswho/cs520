from typing import List
from nebulist.setup.types import Cell, Action


def move(grid: List[List[Cell]], direction: Action) -> None:
    orig = [row.copy() for row in grid]
    rows, cols = len(grid), len(grid[0])
    dy, dx = direction.value

    def inb(r: int, c: int) -> bool:
        return 0 <= r < rows and 0 <= c < cols

    for r in range(rows):
        for c in range(cols):
            cell = orig[r][c]
            if cell == Cell.BLOCKED:
                continue

            pr, pc = r - dy, c - dx
            nr, nc = r + dy, c + dx

            robot_incoming = inb(pr, pc) and orig[pr][pc] is Cell.ROBOT
            robot_hit_wall = (cell is Cell.ROBOT) and (
                not inb(nr, nc) or orig[nr][nc] is Cell.BLOCKED
            )

            grid[r][c] = Cell.ROBOT if (robot_incoming or robot_hit_wall) else Cell.OPEN


def do_moves(grid: List[List[Cell]], moves: List[Action]) -> None:
    for move_action in moves:
        move(grid, move_action)