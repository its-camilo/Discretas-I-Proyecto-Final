"""
Lógica principal del tablero de Sudoku con sistema avanzado de dificultad
"""

import random
import copy
import time
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
        self.use_advanced_difficulty = True  # Siempre usar sistema avanzado


    def get_neighbors(self, row: int, col: int) -> set[tuple[int]]:
        """Genera un conjunto con todas las celdas que estan en la misma fila, la misma columna o la misma cuadricula 3x3 que la celda indicada"""
        neighbors = set()
        # Mismos fila y columna
        for i in range(self.size):
            if i != col:
                neighbors.add((row, i))
            if i != row:
                neighbors.add((i, col))
        # Misma región 3x3
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if (i, j) != (row, col):
                    neighbors.add((i, j))
        return neighbors
    
    def is_proper_coloring_at(self, board: List[List[int]], row: int, col: int, num: int) -> bool:
        """Verifica si una celda (vertice) esta coloreada adecuadamente"""
        for n_row, n_col in self.get_neighbors(row, col):
            if board[n_row][n_col] == num:
                return False
            
        return True
    
    def solve_backtracking(self, board: List[List[int]]) -> bool:
        """Resuelve el Sudoku usando backtracking"""
        
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_proper_coloring_at(board, i, j, num):
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
    
    def generate_puzzle(self, difficulty: str = 'facil') -> Tuple[List[List[int]], int]:
        """Genera un puzzle usando el sistema avanzado o básico"""
        
        return self.generate_advanced_puzzle(difficulty)
    
    def generate_advanced_puzzle(self, difficulty: str = 'facil') -> Tuple[List[List[int]], int]:
        """Genera un puzzle con sistema avanzado de dificultad"""
        
        from .advanced_difficulty import AdvancedDifficultySystem
        
        advanced_system = AdvancedDifficultySystem()
        puzzle, final_difficulty, metrics = advanced_system.generate_advanced_puzzle(difficulty)
        
        # Actualizar el tablero
        self.board = copy.deepcopy(puzzle)
        self.initial_board = copy.deepcopy(puzzle)
        self.solution = copy.deepcopy(advanced_system.board.solution)
        self.difficulty_level = metrics['final_difficulty']  # Usar el valor float directamente
        self.difficulty_metrics = metrics
        
        # Guardar información detallada de dificultad
        self.last_difficulty_info = {
            'permutations': metrics['permutation_difficulty'],
            'average': metrics['final_difficulty'],  # Usar el valor float directamente
            'system': 'advanced'
        }
        
        return puzzle, final_difficulty
    
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
                    
                    # Verificar si el número es válido en esta posición
                    validity[i][j] = self.is_proper_coloring_at(self.board, i, j, self.board[i][j])
                else:
                    # Las celdas vacías no son válidas en una verificación completa
                    validity[i][j] = False
        
        return validity
    
    def solve_current_board(self):
        """Resuelve el tablero actual manteniendo los números iniciales"""
        print("=" * 50)
        print("🚀 INICIANDO RESOLUCIÓN DEL SUDOKU")
        print("=" * 50)
        start_time = time.time()

        self.clear_editable_cells()
        
        temp_board = copy.deepcopy(self.board)
        solved = self.solve_backtracking(temp_board)
        
        end_time = time.time()
        resolution_time = end_time - start_time
        
        if solved:
            # Solo actualizar celdas editables
            for i in range(self.size):
                for j in range(self.size):
                    if self.is_cell_editable(i, j):
                        self.board[i][j] = temp_board[i][j]
            
            print("✅ RESULTADO: Sudoku resuelto exitosamente")
            print(f"⏱️  TIEMPO DE RESOLUCIÓN: {resolution_time:.4f} segundos ({resolution_time * 1000:.2f} ms)")
            
            # Categorizar velocidad
            if resolution_time < 0.001:
                speed_category = "⚡ ULTRA RÁPIDO"
            elif resolution_time < 0.01:
                speed_category = "🏃 MUY RÁPIDO"
            elif resolution_time < 0.1:
                speed_category = "🚶 RÁPIDO"
            elif resolution_time < 1.0:
                speed_category = "🐢 NORMAL"
            else:
                speed_category = "🐌 LENTO"
            
            print(f"📊 VELOCIDAD: {speed_category}")
        else:
            print("❌ RESULTADO: No se pudo resolver el Sudoku")
            print(f"⏱️  TIEMPO TRANSCURRIDO: {resolution_time:.4f} segundos")
            print("🔍 CAUSA: El puzzle podría no tener solución o estar mal configurado")
        
        print("=" * 50)
    
    def get_difficulty_level(self) -> float:
        """Retorna el nivel de dificultad actual"""
        if hasattr(self, 'difficulty_metrics') and self.difficulty_metrics:
            return self.difficulty_metrics.get('final_difficulty', self.difficulty_level)
        return self.difficulty_level
    
    def get_difficulty_metrics(self) -> Dict:
        """Retorna las métricas detalladas de dificultad"""
        if hasattr(self, 'difficulty_metrics') and self.difficulty_metrics:
            return self.difficulty_metrics
        else:
            return {
                'permutation_difficulty': self.difficulty_level,
                'final_difficulty': self.difficulty_level,
                'difficulty_breakdown': {
                    'permutations': self.difficulty_level,
                    'final': self.difficulty_level
                }
            }
    
    def _create_connected_distribution(self, puzzle, cells_to_remove):
        """Crear distribución conectada para puzzles fáciles"""
        import copy
        result = copy.deepcopy(puzzle)
        
        # Estrategia: mantener clusters conectados en bloques 3x3
        blocks = [(r, c) for r in range(0, 9, 3) for c in range(0, 9, 3)]
        random.shuffle(blocks)
        
        removed = 0
        for block_r, block_c in blocks:
            if removed >= cells_to_remove:
                break
                
            # En cada bloque, remover celdas manteniendo conectividad
            block_positions = [(block_r + i, block_c + j) 
                             for i in range(3) for j in range(3)]
            
            # Mantener al menos 3-4 celdas por bloque conectadas
            to_remove_in_block = min(6, cells_to_remove - removed)
            random.shuffle(block_positions)
            
            for i in range(to_remove_in_block):
                if removed < cells_to_remove:
                    row, col = block_positions[i]
                    result[row][col] = 0
                    removed += 1
        
        # Completar remoción si es necesario
        if removed < cells_to_remove:
            remaining_positions = [(i, j) for i in range(9) for j in range(9) 
                                 if result[i][j] != 0]
            random.shuffle(remaining_positions)
            
            for i in range(cells_to_remove - removed):
                if i < len(remaining_positions):
                    row, col = remaining_positions[i]
                    result[row][col] = 0
        
        return result
    
    def _create_dispersed_distribution(self, puzzle, cells_to_remove):
        """Crear distribución dispersa para puzzles difíciles"""
        import copy
        result = copy.deepcopy(puzzle)
        
        # Estrategia: maximizar dispersión usando algoritmo de separación
        positions = [(i, j) for i in range(9) for j in range(9)]
        
        # Calcular scores de desconexión para cada posición
        def calculate_disconnection_score(pos, current_empty):
            row, col = pos
            score = 0
            
            # Bonus por aislar filas/columnas
            row_empty = sum(1 for c in range(9) if (row, c) in current_empty)
            col_empty = sum(1 for r in range(9) if (r, col) in current_empty)
            score += row_empty * 2 + col_empty * 2
            
            # Bonus por aislar bloques 3x3
            block_r, block_c = 3 * (row // 3), 3 * (col // 3)
            block_empty = sum(1 for r in range(block_r, block_r + 3)
                            for c in range(block_c, block_c + 3)
                            if (r, c) in current_empty)
            score += block_empty * 3
            
            return score
        
        # Remover celdas maximizando dispersión
        removed_positions = set()
        
        for _ in range(cells_to_remove):
            if len(positions) == 0:
                break
                
            # Calcular scores para posiciones restantes
            scores = [(pos, calculate_disconnection_score(pos, removed_positions)) 
                     for pos in positions if pos not in removed_positions]
            
            if not scores:
                break
                
            # Elegir posición con mayor score de desconexión
            best_pos = max(scores, key=lambda x: x[1])[0]
            row, col = best_pos
            result[row][col] = 0
            removed_positions.add(best_pos)
        
        return result