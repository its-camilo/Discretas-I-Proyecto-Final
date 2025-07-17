"""Test específico para verificar que ambas dificultades generan 30 celdas llenas"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudoku.board import SudokuBoard

def count_filled_cells(board):
    """Cuenta las celdas llenas en un tablero"""
    count = 0
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                count += 1
    return count

def test_cell_count_consistency():
    """Test para verificar que ambas dificultades tienen la misma cantidad de celdas"""
    print("Testing Cell Count Consistency...")
    
    board = SudokuBoard()
    board.use_advanced_difficulty = True
    
    # Test múltiples generaciones
    for test_num in range(3):
        print(f"\n=== Test {test_num + 1} ===")
        
        for diff in ['facil', 'dificil']:
            print(f"\n--- Generando puzzle {diff} ---")
            
            board.generate_puzzle(diff)
            filled_cells = count_filled_cells(board.board)
            empty_cells = 81 - filled_cells
            
            print(f"Celdas llenas: {filled_cells}")
            print(f"Celdas vacías: {empty_cells}")
            
            # Verificar que son exactamente 30 celdas llenas
            if filled_cells == 30:
                print("✓ Cantidad correcta de celdas")
            else:
                print(f"✗ ERROR: Se esperaban 30 celdas, pero hay {filled_cells}")
            
            # Verificar distribución visual
            print("Distribución del tablero:")
            for i in range(9):
                row = ""
                for j in range(9):
                    if board.board[i][j] == 0:
                        row += ". "
                    else:
                        row += "X "
                print(row)

if __name__ == "__main__":
    test_cell_count_consistency()
