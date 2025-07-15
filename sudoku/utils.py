"""
Utilidades adicionales para el juego de Sudoku
"""

import pygame
import time
from typing import List, Tuple

class SudokuValidator:
    """Clase para validar puzzles de Sudoku"""
    
    @staticmethod
    def count_filled_cells(board: List[List[int]]) -> int:
        """Cuenta el número de celdas llenas en el tablero"""
        count = 0
        for row in board:
            for cell in row:
                if cell != 0:
                    count += 1
        return count
    
    @staticmethod
    def is_complete(board: List[List[int]]) -> bool:
        """Verifica si el tablero está completamente lleno"""
        for row in board:
            for cell in row:
                if cell == 0:
                    return False
        return True
    
    @staticmethod
    def calculate_completion_percentage(board: List[List[int]]) -> float:
        """Calcula el porcentaje de completitud del tablero"""
        filled = SudokuValidator.count_filled_cells(board)
        total = 81
        return (filled / total) * 100

class SudokuStatistics:
    """Clase para manejar estadísticas del juego"""
    
    def __init__(self):
        self.games_played = 0
        self.games_solved = 0
        self.total_time = 0
        self.start_time = None
        self.current_game_time = 0
        
    def start_game(self):
        """Inicia el cronómetro para un nuevo juego"""
        self.start_time = time.time()
        self.games_played += 1
        
    def end_game(self, solved: bool = False):
        """Termina el juego actual y actualiza estadísticas"""
        if self.start_time:
            game_time = time.time() - self.start_time
            self.total_time += game_time
            self.current_game_time = game_time
            
            if solved:
                self.games_solved += 1
            
            self.start_time = None
    
    def get_average_time(self) -> float:
        """Obtiene el tiempo promedio por juego"""
        if self.games_played == 0:
            return 0
        return self.total_time / self.games_played
    
    def get_success_rate(self) -> float:
        """Obtiene la tasa de éxito"""
        if self.games_played == 0:
            return 0
        return (self.games_solved / self.games_played) * 100
    
    def get_current_time(self) -> float:
        """Obtiene el tiempo actual del juego en progreso"""
        if self.start_time:
            return time.time() - self.start_time
        return self.current_game_time

class SudokuAnimations:
    """Clase para manejar animaciones del juego"""
    
    @staticmethod
    def create_fade_effect(surface: pygame.Surface, alpha: int) -> pygame.Surface:
        """Crea un efecto de desvanecimiento"""
        fade_surface = surface.copy()
        fade_surface.set_alpha(alpha)
        return fade_surface
    
    @staticmethod
    def create_pulse_effect(base_size: int, time_factor: float) -> int:
        """Crea un efecto de pulso para elementos"""
        import math
        pulse = math.sin(time_factor * 5) * 0.1 + 1
        return int(base_size * pulse)

class SudokuHints:
    """Clase para proporcionar pistas al jugador"""
    
    def __init__(self, board):
        self.board = board
    
    def get_hint(self) -> Tuple[int, int, int]:
        """Obtiene una pista para el jugador"""
        # Buscar la primera celda vacía que tenga una solución única
        for row in range(9):
            for col in range(9):
                if self.board.get_cell_value(row, col) == 0:
                    possible_values = self.get_possible_values(row, col)
                    if len(possible_values) == 1:
                        return row, col, possible_values[0]
        
        # Si no hay soluciones únicas, devolver cualquier celda vacía con su valor correcto
        for row in range(9):
            for col in range(9):
                if self.board.get_cell_value(row, col) == 0:
                    if hasattr(self.board, 'solution'):
                        return row, col, self.board.solution[row][col]
        
        return None, None, None
    
    def get_possible_values(self, row: int, col: int) -> List[int]:
        """Obtiene los valores posibles para una celda"""
        possible = []
        for num in range(1, 10):
            if self.board.is_valid(self.board.board, row, col, num):
                possible.append(num)
        return possible
    
    def count_mistakes(self) -> int:
        """Cuenta el número de errores en el tablero actual"""
        mistakes = 0
        validity = self.board.verify_solution()
        
        for row in range(9):
            for col in range(9):
                if self.board.get_cell_value(row, col) != 0 and not validity[row][col]:
                    mistakes += 1
        
        return mistakes
