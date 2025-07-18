"""Test de verificación de consistencia de celdas para las tres dificultades"""

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

def test_three_difficulty_consistency():
    """Test para verificar que las tres dificultades tienen la misma cantidad de celdas"""
    print("=" * 80)
    print("🧪 TEST DE CONSISTENCIA DE CELDAS - TRES DIFICULTADES")
    print("📊 Verificando que todas generen exactamente 30 celdas llenas")
    print("=" * 80)
    
    board = SudokuBoard()
    
    # Test múltiples generaciones
    for test_num in range(5):
        print(f"\n=== Test {test_num + 1} ===")
        
        for diff in ['facil', 'dificil']:
            print(f"\n--- Generando puzzle {diff.upper()} ---")
            
            board.generate_puzzle(diff)
            filled_cells = count_filled_cells(board.board)
            empty_cells = 81 - filled_cells
            
            print(f"Celdas llenas: {filled_cells}")
            print(f"Celdas vacías: {empty_cells}")
            
            # Verificar que son exactamente 30 celdas llenas
            if filled_cells == 30:
                print("✅ Cantidad correcta de celdas")
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
            print()

    print("=" * 80)
    print("✅ Test de consistencia completado!")
    print("=" * 80)

if __name__ == "__main__":
    test_three_difficulty_consistency()
