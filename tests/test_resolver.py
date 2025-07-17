#!/usr/bin/env python3
"""
Prueba simple del botón de resolver
"""

import sys
sys.path.append('.')

from sudoku.board import SudokuBoard
import copy

def test_resolver():
    """Prueba simple del método resolver"""
    print("=== PRUEBA DEL MÉTODO RESOLVER ===")
    
    # Crear un tablero
    board = SudokuBoard()
    
    # Generar un puzzle
    print("Generando puzzle...")
    board.generate_puzzle('dificil')
    
    # Mostrar el puzzle inicial
    print("\nPuzzle inicial:")
    for row in board.board:
        print(row)
    
    # Resolver el puzzle
    print("\nResolviendo puzzle...")
    board.solve_current_board()
    
    # Mostrar el puzzle resuelto
    print("\nPuzzle resuelto:")
    for row in board.board:
        print(row)
    
    # Verificar la solución
    print("\nVerificando solución...")
    verification = board.verify_solution()
    
    all_correct = True
    for i in range(9):
        for j in range(9):
            if not verification[i][j]:
                all_correct = False
                print(f"Error en posición ({i}, {j}): {board.board[i][j]}")
    
    if all_correct:
        print("¡Sudoku resuelto correctamente!")
    else:
        print("El sudoku no está resuelto correctamente.")

if __name__ == "__main__":
    test_resolver()
