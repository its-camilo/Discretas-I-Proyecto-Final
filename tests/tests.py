"""
Pruebas unitarias para el juego de Sudoku
"""

import unittest
import sys
import os

# Agregar el directorio padre al path para importar el módulo sudoku
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudoku.board import SudokuBoard
from sudoku.utils import SudokuValidator, SudokuHints

class TestSudokuBoard(unittest.TestCase):
    """Pruebas para la clase SudokuBoard"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.board = SudokuBoard()
    
    def test_board_initialization(self):
        """Prueba la inicialización del tablero"""
        self.assertEqual(self.board.size, 9)
        self.assertEqual(len(self.board.board), 9)
        self.assertEqual(len(self.board.board[0]), 9)
    
    def test_is_valid_basic(self):
        """Prueba la validación básica de números"""
        # Tablero vacío
        empty_board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Todos los números del 1 al 9 deberían ser válidos en una celda vacía
        for num in range(1, 10):
            self.assertTrue(self.board.is_valid(empty_board, 0, 0, num))
    
    def test_is_valid_row_conflict(self):
        """Prueba la detección de conflictos en filas"""
        test_board = [[0 for _ in range(9)] for _ in range(9)]
        test_board[0][0] = 5
        
        # El número 5 no debería ser válido en la misma fila
        self.assertFalse(self.board.is_valid(test_board, 0, 1, 5))
        
        # Otros números deberían ser válidos
        self.assertTrue(self.board.is_valid(test_board, 0, 1, 3))
    
    def test_is_valid_column_conflict(self):
        """Prueba la detección de conflictos en columnas"""
        test_board = [[0 for _ in range(9)] for _ in range(9)]
        test_board[0][0] = 7
        
        # El número 7 no debería ser válido en la misma columna
        self.assertFalse(self.board.is_valid(test_board, 1, 0, 7))
        
        # Otros números deberían ser válidos
        self.assertTrue(self.board.is_valid(test_board, 1, 0, 2))
    
    def test_is_valid_box_conflict(self):
        """Prueba la detección de conflictos en cuadrados 3x3"""
        test_board = [[0 for _ in range(9)] for _ in range(9)]
        test_board[0][0] = 4
        
        # El número 4 no debería ser válido en el mismo cuadrado 3x3
        self.assertFalse(self.board.is_valid(test_board, 1, 1, 4))
        
        # Debería ser válido en un cuadrado diferente
        self.assertTrue(self.board.is_valid(test_board, 3, 3, 4))
    
    def test_generate_puzzle(self):
        """Prueba la generación de puzzles"""
        puzzle, difficulty = self.board.generate_puzzle('medio')
        
        # Verificar que el puzzle es una matriz 9x9
        self.assertEqual(len(puzzle), 9)
        self.assertEqual(len(puzzle[0]), 9)
        
        # Verificar que el nivel de dificultad está en el rango correcto
        self.assertTrue(4 <= difficulty <= 6)
        
        # Verificar que hay exactamente 30 números iniciales
        filled_count = sum(1 for row in puzzle for cell in row if cell != 0)
        self.assertEqual(filled_count, 30)
    
    def test_cell_editability(self):
        """Prueba la funcionalidad de celdas editables"""
        self.board.generate_puzzle('facil')
        
        # Todas las celdas con valor 0 en el tablero inicial deberían ser editables
        for i in range(9):
            for j in range(9):
                if self.board.initial_board[i][j] == 0:
                    self.assertTrue(self.board.is_cell_editable(i, j))
                else:
                    self.assertFalse(self.board.is_cell_editable(i, j))
    
    def test_clear_editable_cells(self):
        """Prueba la función de limpiar celdas editables"""
        self.board.generate_puzzle('facil')
        
        # Agregar algunos números a celdas editables
        for i in range(9):
            for j in range(9):
                if self.board.is_cell_editable(i, j):
                    self.board.set_cell_value(i, j, 5)
                    break
        
        # Limpiar celdas editables
        self.board.clear_editable_cells()
        
        # Verificar que solo se limpiaron las celdas editables
        for i in range(9):
            for j in range(9):
                if self.board.is_cell_editable(i, j):
                    self.assertEqual(self.board.get_cell_value(i, j), 0)


class TestSudokuValidator(unittest.TestCase):
    """Pruebas para la clase SudokuValidator"""
    
    def test_count_filled_cells(self):
        """Prueba el conteo de celdas llenas"""
        # Tablero vacío
        empty_board = [[0 for _ in range(9)] for _ in range(9)]
        self.assertEqual(SudokuValidator.count_filled_cells(empty_board), 0)
        
        # Tablero con algunos números
        test_board = [[0 for _ in range(9)] for _ in range(9)]
        test_board[0][0] = 1
        test_board[0][1] = 2
        test_board[1][0] = 3
        self.assertEqual(SudokuValidator.count_filled_cells(test_board), 3)
    
    def test_is_complete(self):
        """Prueba la verificación de completitud"""
        # Tablero vacío
        empty_board = [[0 for _ in range(9)] for _ in range(9)]
        self.assertFalse(SudokuValidator.is_complete(empty_board))
        
        # Tablero lleno
        full_board = [[1 for _ in range(9)] for _ in range(9)]
        self.assertTrue(SudokuValidator.is_complete(full_board))
    
    def test_completion_percentage(self):
        """Prueba el cálculo del porcentaje de completitud"""
        # Tablero vacío
        empty_board = [[0 for _ in range(9)] for _ in range(9)]
        self.assertEqual(SudokuValidator.calculate_completion_percentage(empty_board), 0.0)
        
        # Tablero lleno
        full_board = [[1 for _ in range(9)] for _ in range(9)]
        self.assertEqual(SudokuValidator.calculate_completion_percentage(full_board), 100.0)
        
        # Tablero medio lleno (41 celdas)
        half_board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(5):
            for j in range(9):
                if i * 9 + j < 41:
                    half_board[i][j] = 1
        
        expected_percentage = (41 / 81) * 100
        self.assertAlmostEqual(
            SudokuValidator.calculate_completion_percentage(half_board), 
            expected_percentage, 
            places=2
        )


class TestSudokuHints(unittest.TestCase):
    """Pruebas para la clase SudokuHints"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.board = SudokuBoard()
        self.board.generate_puzzle('facil')
        self.hints = SudokuHints(self.board)
    
    def test_get_possible_values(self):
        """Prueba la obtención de valores posibles"""
        # Encontrar una celda vacía
        for i in range(9):
            for j in range(9):
                if self.board.get_cell_value(i, j) == 0:
                    possible = self.hints.get_possible_values(i, j)
                    
                    # Debería haber al menos un valor posible
                    self.assertGreater(len(possible), 0)
                    
                    # Todos los valores deberían estar entre 1 y 9
                    for value in possible:
                        self.assertTrue(1 <= value <= 9)
                    
                    return
    
    def test_count_mistakes(self):
        """Prueba el conteo de errores"""
        # Inicialmente no debería haber errores
        mistakes = self.hints.count_mistakes()
        self.assertEqual(mistakes, 0)
        
        # Agregar un error deliberado
        for i in range(9):
            for j in range(9):
                if self.board.is_cell_editable(i, j):
                    # Encontrar un número que cause conflicto
                    for num in range(1, 10):
                        if not self.board.is_valid(self.board.board, i, j, num):
                            self.board.set_cell_value(i, j, num)
                            mistakes = self.hints.count_mistakes()
                            self.assertGreater(mistakes, 0)
                            return


def run_tests():
    """Ejecuta todas las pruebas"""
    unittest.main(verbosity=2)


if __name__ == '__main__':
    run_tests()
