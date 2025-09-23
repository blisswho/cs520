import sys, random
from nebulist.setup.types import Action
from nebulist.setup.grid import (
    generate_grid,
    fill_open_with_robot,
    generate_ship_layout,
)
from nebulist.setup.move import move
from nebulist.setup.io import print_maze


def main() -> None:
    random.seed()  # or fixed seed for reproducibility
    maze_size = 5
    if len(sys.argv) > 1:
        try:
            maze_size = int(sys.argv[1])
        except ValueError:
            print("Invalid maze size argument, using default.")

    grid = generate_grid(maze_size)
    generate_ship_layout(grid)
    print_maze(grid)

    print("Filling open cells with robot...")
    fill_open_with_robot(grid)
    print_maze(grid)


if __name__ == "__main__":
    main()
