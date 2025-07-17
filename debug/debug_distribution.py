"""Test de debugging para la distribución difícil"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudoku.advanced_difficulty import AdvancedDifficultySystem
import copy

def debug_difficult_distribution():
    """Debug específico para el método de distribución difícil"""
    print("Debugging Difficult Distribution...")
    
    # Crear sistema avanzado
    advanced_system = AdvancedDifficultySystem()
    
    # Generar tablero completo
    complete_board = advanced_system.board.generate_complete_board()
    
    print("Tablero completo generado")
    print(f"Celdas llenas en tablero completo: {sum(1 for i in range(9) for j in range(9) if complete_board[i][j] != 0)}")
    
    # Probar distribución difícil directamente
    cells_to_remove = 51  # 81 - 30 = 51
    print(f"Celdas a remover: {cells_to_remove}")
    
    difficult_puzzle = advanced_system._create_difficult_distribution(complete_board, cells_to_remove)
    
    # Contar celdas
    filled_cells = sum(1 for i in range(9) for j in range(9) if difficult_puzzle[i][j] != 0)
    empty_cells = 81 - filled_cells
    
    print(f"Celdas llenas después de distribución difícil: {filled_cells}")
    print(f"Celdas vacías después de distribución difícil: {empty_cells}")
    
    # Mostrar distribución
    print("Distribución resultante:")
    for i in range(9):
        row = ""
        for j in range(9):
            if difficult_puzzle[i][j] == 0:
                row += ". "
            else:
                row += "X "
        print(row)
    
    # Probar también distribución fácil
    print("\n" + "="*50)
    print("Probando distribución fácil para comparación:")
    
    easy_puzzle = advanced_system._create_easy_distribution(complete_board, cells_to_remove)
    filled_cells_easy = sum(1 for i in range(9) for j in range(9) if easy_puzzle[i][j] != 0)
    
    print(f"Celdas llenas en distribución fácil: {filled_cells_easy}")
    
    print("Distribución fácil:")
    for i in range(9):
        row = ""
        for j in range(9):
            if easy_puzzle[i][j] == 0:
                row += ". "
            else:
                row += "X "
        print(row)

if __name__ == "__main__":
    debug_difficult_distribution()
