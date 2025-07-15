"""
Lógica principal del tablero de Sudoku con sistema avanzado de dificultad
"""

import random
import copy
from typing import List, Tuple, Optional, Dict

class SudokuBoard:
    """Maneja la lógica del tablero de Sudoku"""
    
    def __init__(self):
        self.size = 9
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.initial_board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.solution = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.difficulty_level = 1
        self.difficulty_metrics = {}
        self.use_advanced_difficulty = True
        
    def is_valid(self, board: List[List[int]], row: int, col: int, num: int) -> bool:
        """Verifica si un número es válido en una posición específica"""
        
        # Verificar fila
        for j in range(self.size):
            if board[row][j] == num:
                return False
        
        # Verificar columna
        for i in range(self.size):
            if board[i][col] == num:
                return False
        
        # Verificar cuadrado 3x3
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def solve_backtracking(self, board: List[List[int]]) -> bool:
        """Resuelve el Sudoku usando backtracking"""
        
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, i, j, num):
                            board[i][j] = num
                            
                            if self.solve_backtracking(board):
                                return True
                            
                            board[i][j] = 0
                    
                    return False
        
        return True
    
    def generate_complete_board(self) -> List[List[int]]:
        """Genera un tablero completo de Sudoku válido"""
        board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        
        # Llenar diagonal de cuadrados 3x3 primero
        for i in range(0, self.size, 3):
            self.fill_box(board, i, i)
        
        # Completar el resto del tablero
        self.solve_backtracking(board)
        
        return board
    
    def fill_box(self, board: List[List[int]], row: int, col: int):
        """Llena un cuadrado 3x3"""
        nums = list(range(1, 10))
        random.shuffle(nums)
        
        for i in range(3):
            for j in range(3):
                board[row + i][col + j] = nums[i * 3 + j]
    
    def generate_puzzle(self, difficulty: str = 'medio') -> Tuple[List[List[int]], int]:
        """Genera un puzzle usando el sistema avanzado o básico"""
        
        if self.use_advanced_difficulty:
            return self.generate_advanced_puzzle(difficulty)
        else:
            return self.generate_basic_puzzle(difficulty)
    
    def generate_advanced_puzzle(self, difficulty: str = 'medio') -> Tuple[List[List[int]], int]:
        """Genera un puzzle con sistema avanzado de dificultad"""
        
        from .advanced_difficulty import AdvancedDifficultySystem
        
        advanced_system = AdvancedDifficultySystem()
        puzzle, final_difficulty, metrics = advanced_system.generate_advanced_puzzle(difficulty)
        
        # Actualizar el tablero
        self.board = copy.deepcopy(puzzle)
        self.initial_board = copy.deepcopy(puzzle)
        self.solution = copy.deepcopy(advanced_system.board.solution)
        self.difficulty_level = final_difficulty
        self.difficulty_metrics = metrics
        
        # Guardar información detallada de dificultad
        self.last_difficulty_info = {
            'permutations': metrics['permutation_difficulty'],
            'density': metrics['density_difficulty'],
            'average': final_difficulty,
            'system': 'advanced'
        }
        
        return puzzle, final_difficulty
    
    def generate_basic_puzzle(self, difficulty: str = 'medio') -> Tuple[List[List[int]], int]:
        """Genera un puzzle con sistema básico de dificultad"""
        
        # Generar tablero completo
        complete_board = self.generate_complete_board()
        self.solution = copy.deepcopy(complete_board)
        
        # Crear puzzle removiendo números
        puzzle = copy.deepcopy(complete_board)
        
        # Determinar número de celdas a remover basado en dificultad
        if difficulty == 'facil':
            cells_to_remove = random.randint(46, 50)
            self.difficulty_level = random.randint(1, 3)
        elif difficulty == 'medio':
            cells_to_remove = random.randint(51, 55)
            self.difficulty_level = random.randint(4, 6)
        else:  # dificil
            cells_to_remove = random.randint(56, 60)
            self.difficulty_level = random.randint(7, 10)
        
        # Ajustar para que siempre queden exactamente 30 números iniciales
        cells_to_remove = 81 - 30
        
        # Remover números aleatoriamente
        positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(positions)
        
        for i in range(cells_to_remove):
            row, col = positions[i]
            puzzle[row][col] = 0
        
        self.board = copy.deepcopy(puzzle)
        self.initial_board = copy.deepcopy(puzzle)
        
        return puzzle, self.difficulty_level
    
    def get_cell_value(self, row: int, col: int) -> int:
        """Obtiene el valor de una celda"""
        return self.board[row][col]
    
    def set_cell_value(self, row: int, col: int, value: int) -> bool:
        """Establece el valor de una celda si es editable"""
        if self.is_cell_editable(row, col):
            self.board[row][col] = value
            return True
        return False
    
    def is_cell_editable(self, row: int, col: int) -> bool:
        """Verifica si una celda es editable (no es parte del puzzle inicial)"""
        return self.initial_board[row][col] == 0
    
    def clear_editable_cells(self):
        """Limpia todas las celdas editables"""
        for i in range(self.size):
            for j in range(self.size):
                if self.is_cell_editable(i, j):
                    self.board[i][j] = 0
    
    def verify_solution(self) -> List[List[bool]]:
        """Verifica la solución actual y retorna una matriz de validez"""
        validity = [[True for _ in range(self.size)] for _ in range(self.size)]
        
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    # Crear una copia temporal sin el número actual
                    temp_board = copy.deepcopy(self.board)
                    temp_board[i][j] = 0
                    
                    # Verificar si el número es válido en esta posición
                    if not self.is_valid(temp_board, i, j, self.board[i][j]):
                        validity[i][j] = False
                elif self.board[i][j] == 0:
                    # Las celdas vacías no son válidas en una verificación completa
                    validity[i][j] = False
        
        return validity
    
    def solve_current_board(self):
        """Resuelve el tablero actual manteniendo los números iniciales"""
        temp_board = copy.deepcopy(self.board)
        if self.solve_backtracking(temp_board):
            # Solo actualizar celdas editables
            for i in range(self.size):
                for j in range(self.size):
                    if self.is_cell_editable(i, j):
                        self.board[i][j] = temp_board[i][j]
    
    def get_difficulty_level(self) -> int:
        """Retorna el nivel de dificultad actual"""
        return int(self.difficulty_level)
    
    def get_difficulty_metrics(self) -> Dict:
        """Retorna las métricas detalladas de dificultad"""
        if hasattr(self, 'difficulty_metrics') and self.difficulty_metrics:
            # Añadir breakdown si tenemos last_difficulty_info
            if hasattr(self, 'last_difficulty_info') and self.last_difficulty_info:
                self.difficulty_metrics['difficulty_breakdown'] = {
                    'permutations': self.last_difficulty_info['permutations'],
                    'density': self.last_difficulty_info['density'],
                    'average': self.last_difficulty_info['average']
                }
            return self.difficulty_metrics
        else:
            return {
                'permutation_difficulty': self.difficulty_level,
                'density_difficulty': self.difficulty_level,
                'final_difficulty': self.difficulty_level,
                'difficulty_breakdown': {
                    'permutations': self.difficulty_level,
                    'density': self.difficulty_level,
                    'average': self.difficulty_level
                }
            }

    def toggle_difficulty_system(self) -> bool:
        """Alterna entre sistema básico y avanzado"""
        self.use_advanced_difficulty = not self.use_advanced_difficulty
        return self.use_advanced_difficulty
        """Alterna entre sistema básico y avanzado"""
        self.use_advanced_difficulty = not self.use_advanced_difficulty
        return self.use_advanced_difficulty
