"""
Sistema avanzado de dificultad para Sudoku basado en:
1. Permutaciones (1-10)
2. Densidad de celdas disjuntas (1-10)
El promedio de ambos determina la dificultad final
"""

import random
import copy
from typing import List, Tuple, Dict, Set
from .board import SudokuBoard

class CellDensity:
    """Clase para manejar la densidad de celdas"""
    
    def __init__(self, row: int, col: int, value: int = 0):
        self.row = row
        self.col = col
        self.value = value
        self.box = (row // 3) * 3 + (col // 3)
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def __hash__(self):
        return hash((self.row, self.col))

class AdvancedDifficultySystem:
    """Sistema avanzado de dificultad con permutaciones y densidad"""
    
    def __init__(self):
        self.board = SudokuBoard()
        self.cells = []
        self.rows = [[] for _ in range(9)]
        self.columns = [[] for _ in range(9)]
        self.boxes = [[] for _ in range(9)]
        self.permutation_difficulty = 1
        self.density_difficulty = 1
        self.final_difficulty = 1
        
    def initialize_cell_structure(self, board_matrix: List[List[int]]):
        """Inicializa la estructura de celdas con densidad"""
        self.cells = []
        self.rows = [[] for _ in range(9)]
        self.columns = [[] for _ in range(9)]
        self.boxes = [[] for _ in range(9)]
        
        for row in range(9):
            for col in range(9):
                cell = CellDensity(row, col, board_matrix[row][col])
                self.cells.append(cell)
                self.rows[row].append(cell)
                self.columns[col].append(cell)
                self.boxes[cell.box].append(cell)
    
    def get_density(self, cell: CellDensity) -> float:
        """Calcula la densidad de contexto de una celda"""
        possibilities = self.rows[cell.row] + self.columns[cell.col] + self.boxes[cell.box]
        
        # Remover la celda actual si está en las posibilidades
        if cell in possibilities:
            possibilities.remove(cell)
        
        # Contar celdas con valor != 0
        filled_count = len([x for x in set(possibilities) if x.value != 0])
        
        # Normalizar por 20.0 (máximo teórico: 8+8+4 = 20 celdas relacionadas)
        return filled_count / 20.0
    
    def get_used_cells(self) -> List[CellDensity]:
        """Obtiene todas las celdas que tienen valor != 0"""
        return [cell for cell in self.cells if cell.value != 0]
    
    def calculate_permutation_difficulty(self, board_matrix: List[List[int]]) -> int:
        """Calcula la dificultad basada en permutaciones"""
        
        # Analizar patrones de números en filas, columnas y cajas
        row_patterns = self._analyze_row_patterns(board_matrix)
        col_patterns = self._analyze_column_patterns(board_matrix)
        box_patterns = self._analyze_box_patterns(board_matrix)
        
        # Calcular complejidad de permutaciones
        row_complexity = self._calculate_pattern_complexity(row_patterns)
        col_complexity = self._calculate_pattern_complexity(col_patterns)
        box_complexity = self._calculate_pattern_complexity(box_patterns)
        
        # Promedio de complejidades
        avg_complexity = (row_complexity + col_complexity + box_complexity) / 3
        
        # Convertir a escala 1-10
        difficulty = max(1, min(10, int(avg_complexity * 10)))
        
        return difficulty
    
    def _analyze_row_patterns(self, board_matrix: List[List[int]]) -> List[Dict]:
        """Analiza patrones en filas"""
        patterns = []
        for row in board_matrix:
            filled = [x for x in row if x != 0]
            patterns.append({
                'filled_count': len(filled),
                'unique_count': len(set(filled)),
                'distribution': self._calculate_distribution(filled, row)
            })
        return patterns
    
    def _analyze_column_patterns(self, board_matrix: List[List[int]]) -> List[Dict]:
        """Analiza patrones en columnas"""
        patterns = []
        for col in range(9):
            column = [board_matrix[row][col] for row in range(9)]
            filled = [x for x in column if x != 0]
            patterns.append({
                'filled_count': len(filled),
                'unique_count': len(set(filled)),
                'distribution': self._calculate_distribution(filled, column)
            })
        return patterns
    
    def _analyze_box_patterns(self, board_matrix: List[List[int]]) -> List[Dict]:
        """Analiza patrones en cajas 3x3"""
        patterns = []
        for box_row in range(3):
            for box_col in range(3):
                box = []
                for row in range(box_row * 3, (box_row + 1) * 3):
                    for col in range(box_col * 3, (box_col + 1) * 3):
                        box.append(board_matrix[row][col])
                
                filled = [x for x in box if x != 0]
                patterns.append({
                    'filled_count': len(filled),
                    'unique_count': len(set(filled)),
                    'distribution': self._calculate_distribution(filled, box)
                })
        return patterns
    
    def _calculate_distribution(self, filled: List[int], total: List[int]) -> float:
        """Calcula qué tan distribuidos están los números"""
        if len(filled) == 0:
            return 0.0
        
        # Calcular espacios entre números
        positions = [i for i, x in enumerate(total) if x != 0]
        if len(positions) <= 1:
            return 0.0
        
        # Calcular varianza de posiciones
        avg_pos = sum(positions) / len(positions)
        variance = sum((pos - avg_pos) ** 2 for pos in positions) / len(positions)
        
        # Normalizar (máximo teórico de varianza para 9 posiciones)
        return min(1.0, variance / 18.0)
    
    def _calculate_pattern_complexity(self, patterns: List[Dict]) -> float:
        """Calcula la complejidad de los patrones"""
        if not patterns:
            return 0.0
        
        complexities = []
        for pattern in patterns:
            # Factores de complejidad
            fill_factor = pattern['filled_count'] / 9.0
            unique_factor = pattern['unique_count'] / min(9, pattern['filled_count']) if pattern['filled_count'] > 0 else 0
            dist_factor = pattern['distribution']
            
            # Combinar factores (más lleno y más distribuido = más complejo)
            complexity = (fill_factor * 0.4) + (unique_factor * 0.3) + (dist_factor * 0.3)
            complexities.append(complexity)
        
        return sum(complexities) / len(complexities)
    
    def calculate_density_difficulty(self, board_matrix: List[List[int]]) -> int:
        """Calcula la dificultad basada en densidad de celdas disjuntas"""
        
        self.initialize_cell_structure(board_matrix)
        
        # Obtener celdas usadas
        used_cells = self.get_used_cells()
        
        if len(used_cells) == 0:
            return 1
        
        # Calcular densidad para cada celda
        densities = []
        for cell in used_cells:
            density = self.get_density(cell)
            densities.append(density)
        
        # Analizar distribución de densidades
        avg_density = sum(densities) / len(densities)
        density_variance = sum((d - avg_density) ** 2 for d in densities) / len(densities)
        
        # Calcular factores de dificultad
        disjoint_factor = 1.0 - avg_density  # Menos densidad = más disjuntas = más difícil
        variance_factor = density_variance  # Más varianza = más irregular = más difícil
        
        # Combinar factores
        difficulty_score = (disjoint_factor * 0.7) + (variance_factor * 0.3)
        
        # Convertir a escala 1-10
        difficulty = max(1, min(10, int(difficulty_score * 10) + 1))
        
        return difficulty
    
    def generate_advanced_puzzle(self, target_difficulty: str = 'medio') -> Tuple[List[List[int]], int, Dict]:
        """Genera un puzzle con sistema avanzado de dificultad"""
        
        # Generar tablero base
        complete_board = self.board.generate_complete_board()
        
        # Determinar rangos objetivo según la clasificación
        if target_difficulty == 'facil':
            target_range = (1, 3)
        elif target_difficulty == 'medio':
            target_range = (4, 6)
        else:  # dificil
            target_range = (7, 10)
        
        best_puzzle = None
        best_metrics = None
        best_final_difficulty = 0
        
        # Intentar múltiples variaciones
        for attempt in range(30):
            puzzle = self._create_puzzle_variation(complete_board, target_difficulty)
            
            # Calcular métricas de cada aspecto (1-10)
            perm_diff = self.calculate_permutation_difficulty(puzzle)
            density_diff = self.calculate_density_difficulty(puzzle)
            
            # Calcular dificultad final como promedio
            final_diff = (perm_diff + density_diff) / 2.0
            
            # Clasificar según rangos ajustados
            if final_diff <= 4.0:
                classification = 'Fácil'
            elif final_diff <= 4.5:
                classification = 'Medio'
            else:
                classification = 'Difícil'
            
            metrics = {
                'permutation_difficulty': perm_diff,
                'density_difficulty': density_diff,
                'final_difficulty': final_diff,
                'target_range': target_range,
                'classification': classification,
                'difficulty_breakdown': {
                    'permutations': perm_diff,
                    'density': density_diff,
                    'final': final_diff
                }
            }
            
            # Verificar si está en el rango objetivo
            if target_range[0] <= final_diff <= target_range[1]:
                if final_diff > best_final_difficulty:
                    best_puzzle = puzzle
                    best_metrics = metrics
                    best_final_difficulty = final_diff
        
        # Si no encontramos uno perfecto, usar el mejor
        if best_puzzle is None:
            puzzle = self._create_puzzle_variation(complete_board, target_difficulty)
            perm_diff = self.calculate_permutation_difficulty(puzzle)
            density_diff = self.calculate_density_difficulty(puzzle)
            final_diff = (perm_diff + density_diff) / 2.0
            
            # Clasificar según rangos ajustados
            if final_diff <= 4.0:
                classification = 'Fácil'
            elif final_diff <= 4.5:
                classification = 'Medio'
            else:
                classification = 'Difícil'
            
            best_metrics = {
                'permutation_difficulty': perm_diff,
                'density_difficulty': density_diff,
                'final_difficulty': final_diff,
                'target_range': target_range,
                'classification': classification,
                'difficulty_breakdown': {
                    'permutations': perm_diff,
                    'density': density_diff,
                    'final': final_diff
                }
            }
            best_puzzle = puzzle
        
        # Actualizar el tablero principal
        self.board.board = copy.deepcopy(best_puzzle)
        self.board.initial_board = copy.deepcopy(best_puzzle)
        self.board.solution = copy.deepcopy(complete_board)
        
        self.permutation_difficulty = best_metrics['permutation_difficulty']
        self.density_difficulty = best_metrics['density_difficulty']
        self.final_difficulty = best_metrics['final_difficulty']
        
        return best_puzzle, int(round(best_metrics['final_difficulty'])), best_metrics
    
    def _create_puzzle_variation(self, complete_board: List[List[int]], target_difficulty: str) -> List[List[int]]:
        """Crea una variación del puzzle usando remoción inteligente"""
        
        puzzle = copy.deepcopy(complete_board)
        self.initialize_cell_structure(puzzle)
        
        # Determinar cuántas celdas remover
        if target_difficulty == 'facil':
            cells_to_remove = random.randint(46, 50)
        elif target_difficulty == 'medio':
            cells_to_remove = random.randint(51, 55)
        else:  # dificil
            cells_to_remove = random.randint(56, 60)
        
        # Ajustar para mantener 30 celdas iniciales
        cells_to_remove = 81 - 30
        
        # Remover celdas usando estrategia de densidad
        for _ in range(cells_to_remove):
            used_cells = self.get_used_cells()
            if len(used_cells) <= 30:
                break
            
            # Calcular densidad y ordenar
            density_pairs = [(cell, self.get_density(cell)) for cell in used_cells]
            
            # Para dificultad alta, remover celdas con mayor densidad primero
            if target_difficulty == 'dificil':
                sorted_cells = sorted(density_pairs, key=lambda x: x[1], reverse=True)
            else:
                # Para dificultad baja/media, usar estrategia mixta
                sorted_cells = sorted(density_pairs, key=lambda x: x[1], reverse=random.choice([True, False]))
            
            # Remover la celda seleccionada
            if sorted_cells:
                cell_to_remove = sorted_cells[0][0]
                puzzle[cell_to_remove.row][cell_to_remove.col] = 0
                cell_to_remove.value = 0
        
        return puzzle
    
    def get_difficulty_metrics(self) -> Dict:
        """Obtiene las métricas de dificultad actuales"""
        # Clasificar según rangos ajustados
        if self.final_difficulty <= 4.0:
            classification = 'Fácil'
        elif self.final_difficulty <= 4.5:
            classification = 'Medio'
        else:
            classification = 'Difícil'
        
        return {
            'permutation_difficulty': self.permutation_difficulty,
            'density_difficulty': self.density_difficulty,
            'final_difficulty': self.final_difficulty,
            'classification': classification,
            'difficulty_breakdown': {
                'permutations': self.permutation_difficulty,
                'density': self.density_difficulty,
                'final': self.final_difficulty
            }
        }
