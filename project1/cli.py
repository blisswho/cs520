import sys, random
from nebulist.setup.types import Action
from nebulist.setup.grid import (
    generate_grid,
    fill_open_with_robot,
    generate_ship_layout,
)
from nebulist.setup.move import move, do_moves
from nebulist.setup.io import print_maze
from nebulist.astar.astar_solver import AStarSolver
from nebulist.bfs.bfs_solver import BfsSolver
import argparse
import copy


def main() -> None:
    parser = argparse.ArgumentParser(description="Maze solver CLI")
    parser.add_argument("--size", type=int, nargs="?", default=5, help="Maze size")
    parser.add_argument("--solver", type=str, default="", help="Solver to use")
    args = parser.parse_args()

    random.seed()  # or fixed seed for reproducibility

    maze_size = args.size
    solver_type = args.solver

    grid = generate_grid(maze_size)
    generate_ship_layout(grid)
    print_maze(grid)

    print("Filling open cells with robot...")
    fill_open_with_robot(grid)
    print_maze(grid)


    original_grid = copy.deepcopy(grid)
    if solver_type == "astar":
        astar = AStarSolver(grid)
        result = astar.solve()

        print("Path of actions:", [action.name for action in result])
        do_moves(original_grid, result)
        print("Final grid after A* moves:")
        print_maze(original_grid)
    elif solver_type == "bfs":
        bfs = BfsSolver(grid)
        result = bfs.solve()
        print("Result:", [action.name for action in result])

    else:
        print(f"Unknown solver type: `{solver_type}`")
        return


if __name__ == "__main__":
    main()
