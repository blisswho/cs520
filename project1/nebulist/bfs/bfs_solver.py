from typing import List, Optional, Tuple, Set
import heapq
import random
from collections import deque

from nebulist.setup import move
from nebulist.setup.types import Cell, Action
from nebulist.setup.grid import has_one_open_neighbor, reached_single_robot_space
from nebulist.setup.utils import inbounds


class BfsSolver:
    def __init__(self, grid: List[List[Cell]]):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
    
    def get_all_possible_positions(self) -> Set[Tuple[int, int]]:
        """Get all open cells where the bot could be."""
        positions = set()
        for r in range(self.height):
            for c in range(self.width):
                if self.grid[r][c] != Cell.BLOCKED:
                    positions.add((r, c))
        return positions
    
    def simulate_move(self, positions: Set[Tuple[int, int]], action: Action) -> Set[Tuple[int, int]]:
        """Simulate what happens when we attempt a move from all possible positions."""
        new_positions = set()
        dr, dc = action.value
        
        for pos in positions:
            r, c = pos
            new_r, new_c = r + dr, c + dc
            
            # Check if move is valid from this position
            if (inbounds(self.grid, new_r, new_c) and 
                self.grid[new_r][new_c] != Cell.BLOCKED):
                new_positions.add((new_r, new_c))
            else:
                # Move was blocked, bot stays in current position
                new_positions.add((r, c))
        
        return new_positions
    
    def find_optimal_sequence(self) -> List[Action]:
        """Find optimal sequence using BFS over belief states."""
        # Start with all possible positions
        initial_positions = self.get_all_possible_positions()
        
        # BFS queue: (current_positions, actions_so_far)
        queue = deque()
        queue.append((initial_positions, []))
        visited = set()
        visited.add(frozenset(initial_positions))
        
        while queue:
            current_positions, actions = queue.popleft()
            
            # Check if we've localized to a single position
            if len(current_positions) == 1:
                return actions
            
            # Try all possible actions
            for action in Action:
                new_positions = self.simulate_move(current_positions, action)
                frozen_new = frozenset(new_positions)
                
                if frozen_new not in visited:
                    visited.add(frozen_new)
                    queue.append((new_positions, actions + [action]))
        
        return []  # Should not happen for valid maps
    
    def solve(self) -> List[Action]:
        """Main solve method."""
        return self.find_optimal_sequence()
