from typing import List, Optional, Tuple

from nebulist.setup import move
from nebulist.setup.types import Cell, Action
from nebulist.setup.grid import has_one_open_neighbor, reached_single_robot_space
import random

import heapq

from nebulist.setup.utils import inbounds


class AStarSolver:
    def __init__(self, grid: List[List[Cell]]):
        self.grid: List[List[Cell]] = grid
        self.goal: Optional[Tuple[int, int]] = None
        self.current: Optional[Tuple[int, int]] = None

    def search(self) -> Optional[List[Action]]:
        r, c = self.get_random_robot()

        fringe = []
        prev = {(r, c): None}
        dist_from_start = {(r, c): 0}

        heapq.heappush(
            fringe, (self.manhattan_distance((r, c), self.goal), (r, c), None)
        )

        while fringe:
            _, (r, c), curr_action = heapq.heappop(fringe)
            location = (r, c)
            curr = (r, c, curr_action)

            # Avoid action on first pop
            if curr_action:
                move(self.grid, curr_action)

            # Check for goal state
            if location == self.goal:
                path = []
                node = curr
                while node is not None:
                    _, _, action = node
                    if action is not None:
                        path.append(action)
                    node = prev[node]
                return list(reversed(path))

            # Process fringe for all child actions
            actions = [a for a in Action]
            for action in actions:
                dy, dx = action.value
                next_row, next_col = r + dy, c + dx
                if not self.valid_move(next_row, next_col):
                    continue

                child = (next_row, next_col)
                cost_to_child = dist_from_start[child] + 1
                if (
                    child not in dist_from_start
                    or dist_from_start[child] > cost_to_child
                ):
                    dist_from_start[child] = cost_to_child
                    prev[child] = curr
                    heuristic = cost_to_child + self.manhattan_distance(
                        child, self.goal
                    )
                    heapq.heappush(fringe, (heuristic, child, action))

        return None  # Replace with actual path if found

    def solve(self) -> Optional[List[Action]]:
        # Placeholder for A* algorithm implementation
        # This should return a list of coordinates from start to goal if a path exists
        self.set_random_dead_end_goal()

        # Continue to A* search until only one robot space remains
        all_actions = []
        while not reached_single_robot_space(self.grid):
            list_of_actions = self.search()
            if list_of_actions:
                all_actions.extend(list_of_actions)

        return all_actions

    def valid_move(self, next_row: int, next_col: int) -> bool:
        return (
            inbounds(self.grid, next_row, next_col)
            and self.grid[next_row][next_col] is not Cell.BLOCKED
        )

    def set_random_dead_end_goal(self) -> None:
        dead_ends = [
            (r, c)
            for r in range(len(self.grid))
            for c in range(len(self.grid[0]))
            if self.grid[r][c] is Cell.OPEN and has_one_open_neighbor(self.grid, r, c)
        ]
        if not dead_ends:
            raise RuntimeError("No dead end cells available to set as goal.")
        r, c = random.choice(dead_ends)
        self.goal = (r, c)

    def get_random_robot(self) -> Tuple[int, int]:
        robot_cells = [
            (r, c)
            for r in range(len(self.grid))
            for c in range(len(self.grid[0]))
            if self.grid[r][c] is Cell.ROBOT
        ]
        if not robot_cells:
            raise RuntimeError("No robot cells available to select.")
        return random.choice(robot_cells)

    def manhattan_distance(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
