
if __name__ == "__main__":
    from nebulist.setup.types import Cell
    from nebulist.setup.io import print_maze
    from nebulist.astar.astar_solver import AStarSolver

    # Manually construct the grid for your test case
    grid = [
        [Cell.OPEN,   Cell.BLOCKED, Cell.BLOCKED, Cell.BLOCKED, Cell.OPEN],
        [Cell.OPEN,   Cell.OPEN,    Cell.BLOCKED, Cell.OPEN,    Cell.OPEN],
        [Cell.OPEN,   Cell.BLOCKED, Cell.OPEN,    Cell.BLOCKED, Cell.OPEN],
        [Cell.OPEN,   Cell.OPEN,    Cell.OPEN,    Cell.OPEN,    Cell.OPEN],
        [Cell.ROBOT,   Cell.BLOCKED, Cell.ROBOT,   Cell.BLOCKED, Cell.OPEN],
    ]

    print("Initial grid:")
    print_maze(grid)

    solver = AStarSolver(grid)
    solver.goal = (4, 2)  # Set a specific goal for testing
    actions = solver.solve()