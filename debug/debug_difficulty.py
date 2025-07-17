#!/usr/bin/env python3

from sudoku.advanced_difficulty import AdvancedDifficultySystem
import copy

# Test with debugging
print("=== DEBUGGING ADVANCED DIFFICULTY SYSTEM ===")
ads = AdvancedDifficultySystem()

# Generate complete board first
complete_board = ads.board.generate_complete_board()

# Test puzzle variations
print("\nTesting different puzzle variations:")
for i in range(10):
    puzzle_facil = ads._create_puzzle_variation(complete_board, 'facil')
    diff_facil = ads.calculate_permutation_difficulty(puzzle_facil)
    print(f"Fácil {i+1}: {diff_facil:.2f}")

print()
for i in range(10):
    puzzle_dificil = ads._create_puzzle_variation(complete_board, 'dificil')
    diff_dificil = ads.calculate_permutation_difficulty(puzzle_dificil)
    print(f"Difícil {i+1}: {diff_dificil:.2f}")
