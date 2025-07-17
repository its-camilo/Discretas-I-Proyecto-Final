#!/usr/bin/env python3

from sudoku.advanced_difficulty import AdvancedDifficultySystem
from sudoku.board import SudokuBoard

# Test advanced system
print("=== TESTING ADVANCED DIFFICULTY SYSTEM ===")
ads = AdvancedDifficultySystem()

puzzle_facil, diff_facil, metrics_facil = ads.generate_advanced_puzzle('facil')
print(f"Fácil: dificultad={diff_facil}, target_range={metrics_facil.get('target_range')}, clasificación={metrics_facil.get('classification')}")

puzzle_dificil, diff_dificil, metrics_dificil = ads.generate_advanced_puzzle('dificil')
print(f"Difícil: dificultad={diff_dificil}, target_range={metrics_dificil.get('target_range')}, clasificación={metrics_dificil.get('classification')}")

# Test board system
print("\n=== TESTING BOARD SYSTEM ===")
board = SudokuBoard()

puzzle_f, diff_f = board.generate_puzzle('facil')
print(f"Board fácil: dificultad={diff_f}")

puzzle_d, diff_d = board.generate_puzzle('dificil')
print(f"Board difícil: dificultad={diff_d}")

# Show constants
from sudoku.constants import DIFFICULTY_LEVELS
print(f"\nConstants: {DIFFICULTY_LEVELS}")
