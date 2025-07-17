#!/usr/bin/env python3

from sudoku.advanced_difficulty import AdvancedDifficultySystem
import copy

# Test with more detailed debugging
print("=== DETAILED DEBUGGING ADVANCED DIFFICULTY SYSTEM ===")
ads = AdvancedDifficultySystem()

# Generate complete board first
complete_board = ads.board.generate_complete_board()

# Test individual components
puzzle_facil = ads._create_puzzle_variation(complete_board, 'facil')
puzzle_dificil = ads._create_puzzle_variation(complete_board, 'dificil')

print(f"Puzzle fácil tiene {sum(row.count(0) for row in puzzle_facil)} celdas vacías")
print(f"Puzzle difícil tiene {sum(row.count(0) for row in puzzle_dificil)} celdas vacías")

# Let's debug the calculation step by step
def debug_calculate_difficulty(ads, puzzle, label):
    print(f"\n=== {label} ===")
    
    # Check individual components
    number_perms = ads._analyze_number_permutations(puzzle)
    row_perms = ads._analyze_row_permutations(puzzle)
    col_perms = ads._analyze_column_permutations_perm(puzzle)
    block_perms = ads._analyze_block_permutations(puzzle)
    graph_complexity = ads._analyze_constraint_graph(puzzle)
    combinatorial_complexity = ads._analyze_combinatorial_complexity(puzzle)
    
    print(f"Number permutations: {number_perms:.3f}")
    print(f"Row permutations: {row_perms:.3f}")
    print(f"Col permutations: {col_perms:.3f}")
    print(f"Block permutations: {block_perms:.3f}")
    print(f"Graph complexity: {graph_complexity:.3f}")
    print(f"Combinatorial complexity: {combinatorial_complexity:.3f}")
    
    # Calculate total complexity manually
    total_complexity = (
        number_perms * 0.25 +
        row_perms * 0.17 +
        col_perms * 0.17 +
        block_perms * 0.11 +
        graph_complexity * 0.15 +
        combinatorial_complexity * 0.15
    )
    
    print(f"Total complexity: {total_complexity:.3f}")
    print(f"Scaled (x10): {total_complexity * 10:.3f}")
    print(f"Final difficulty: {max(1, min(10, round(total_complexity * 10, 1)))}")

debug_calculate_difficulty(ads, puzzle_facil, "PUZZLE FÁCIL")
debug_calculate_difficulty(ads, puzzle_dificil, "PUZZLE DIFÍCIL")
