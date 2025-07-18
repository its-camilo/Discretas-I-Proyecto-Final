"""
Sistema avanzado de dificultad para Sudoku basado en conceptos de Matemáticas Discretas:
1. Permutaciones (análisis de grupos simétricos)
2. Teoría de Grafos (grafo de restricciones)
3. Combinatoria (principio de inclusión-exclusión y coeficientes binomiales)
"""

import random
import copy
import math
from typing import List, Tuple, Dict, Set
from collections import defaultdict
from .board import SudokuBoard
from itertools import permutations

HIGH_DIFFICULTY_THRESHOLD = 5.7

CELLS_TO_REMOVE_LOW_DIFFICULTY = 51
CELLS_TO_REMOVE_HIGH_DIFFICULTY = 51

class AdvancedDifficultySystem:
    """Sistema avanzado de dificultad con múltiples conceptos de matemáticas discretas"""
    
    def __init__(self):
        self.board = SudokuBoard()
        self.permutation_difficulty = 1
        self.graph_difficulty = 1
        self.combinatorial_difficulty = 1
        self.final_difficulty = 1
        
    def calculate_difficulty(self, board_matrix: List[List[int]]) -> int:
        """Calcula la dificultad usando múltiples conceptos de matemáticas discretas"""
        
        # 1. DISTRIBUCIÓN DE NÚMEROS (1-9)
        number_distribution = self._measure_number_distribution_uniformity(board_matrix)
        
        # 2. PERMUTACIONES DE FILAS DENTRO DE BLOQUES
        row_permutations = self._analyze_row_permutations(board_matrix)
        
        # 3. PERMUTACIONES DE COLUMNAS DENTRO DE BLOQUES  
        col_permutations = self._analyze_column_permutations_perm(board_matrix)
        
        # 4. PERMUTACIONES DE BLOQUES 3x3
        block_permutations = self._analyze_block_permutations(board_matrix)
        
        # 5. TEORÍA DE GRAFOS - Análisis del grafo de restricciones
        graph_complexity = self._analyze_constraint_graph(board_matrix)
        
        # 6. COMBINATORIA - Inclusión-exclusión y coeficientes binomiales
        combinatorial_complexity = self._analyze_combinatorial_complexity(board_matrix)
        
        # 7. CÁLCULO COMBINATORIO DE SOLUCIONES POSIBLES
        solution_space = self._calculate_solution_space_complexity(board_matrix)
        
        # Combinar todas las métricas con pesos matemáticamente justificados
        total_complexity = (
            number_distribution * 0.15 +      # 15% - Permutaciones de números
            row_permutations * 0.15 +         # 15% - Permutaciones de filas
            col_permutations * 0.15 +         # 15% - Permutaciones de columnas
            block_permutations * 0.11 +       # 11% -  Permutaciones de bloques
            graph_complexity * 0.15 +         # 15% - Teoría de grafos
            combinatorial_complexity * 0.15 + # 15% - Combinatoria avanzada
            solution_space * 0.14             # 14% - Espacio de solución
        )

        # Convertir a escala 1-10 con rounding apropiado
        difficulty = max(1, min(10, round(total_complexity * 10, 1)))
        
        # Almacenar métricas individuales
        self.permutation_difficulty = (number_distribution + row_permutations + col_permutations + block_permutations) / 4
        self.graph_difficulty = graph_complexity
        self.combinatorial_difficulty = combinatorial_complexity
        
        return difficulty
    
    def _measure_number_distribution_uniformity(self, board_matrix: List[List[int]]) -> float:
        """Evalúa la uniformidad en la frecuencia de los números del 1 al 9 en el tablero"""
        
        # Contar frecuencia de cada número
        number_counts = [0] * 10  # índice 0 no se usa
        for row in board_matrix:
            for num in row:
                if num != 0:
                    number_counts[num] += 1
        
        # Calcular distribución de números
        total_numbers = sum(number_counts[1:])
        if total_numbers == 0:
            return 0.0
        
        # Calcular varianza de distribución para medir uniformidad
        avg_count = total_numbers / 9.0
        variance = sum((count - avg_count) ** 2 for count in number_counts[1:]) / 9.0
        
        # Normalizar varianza (máximo teórico cuando todos están en una posición)
        max_variance = ((total_numbers - 0) ** 2 + 8 * (0 - avg_count) ** 2) / 9.0

        return min(1.0, variance / max_variance if max_variance > 0 else 0.0)
    
    def _analyze_row_permutations(self, board_matrix: List[List[int]]) -> float:
        """Analiza permutaciones válidas de filas dentro de bloques"""
        complexity_sum = 0.0
        
        # Para cada bloque de 3 filas
        for block_row in range(3):
            start_row = block_row * 3
            rows = [board_matrix[start_row + i] for i in range(3)]
            
            # Calcular cuántas permutaciones de estas 3 filas son válidas
            valid_perms = self._count_valid_row_permutations(rows, board_matrix, start_row)
            
            # Normalizar por 3! = 6 (total de permutaciones posibles)
            complexity_sum += valid_perms / 6.0
        
        return complexity_sum / 3.0  # Promedio de los 3 bloques
    
    def _analyze_column_permutations_perm(self, board_matrix: List[List[int]]) -> float:
        """Analiza permutaciones válidas de columnas dentro de bloques"""
        complexity_sum = 0.0
        
        # Para cada bloque de 3 columnas
        for block_col in range(3):
            start_col = block_col * 3
            cols = []
            for col_offset in range(3):
                col = [board_matrix[row][start_col + col_offset] for row in range(9)]
                cols.append(col)
            
            # Calcular cuántas permutaciones de estas 3 columnas son válidas
            valid_perms = self._count_valid_column_permutations(cols, board_matrix, start_col)
            
            # Normalizar por 3! = 6 (total de permutaciones posibles)
            complexity_sum += valid_perms / 6.0
        
        return complexity_sum / 3.0  # Promedio de los 3 bloques
    
    def _analyze_block_permutations(self, board_matrix: List[List[int]]) -> float:
        """Analiza permutaciones válidas de bloques 3x3"""
        
        # Extraer los 9 bloques 3x3
        blocks = []
        for block_row in range(3):
            for block_col in range(3):
                block = []
                for r in range(block_row * 3, (block_row + 1) * 3):
                    for c in range(block_col * 3, (block_col + 1) * 3):
                        block.append(board_matrix[r][c])
                blocks.append(block)
        
        # Contar permutaciones válidas de bloques por fila y columna
        valid_row_perms = 0
        valid_col_perms = 0
        
        # Permutaciones de bloques por fila (3 bloques por fila)
        for row_group in range(3):
            block_indices = [row_group * 3 + i for i in range(3)]
            row_blocks = [blocks[i] for i in block_indices]
            valid_row_perms += self._count_valid_block_permutations(row_blocks, 'row')
        
        # Permutaciones de bloques por columna (3 bloques por columna)
        for col_group in range(3):
            block_indices = [col_group + i * 3 for i in range(3)]
            col_blocks = [blocks[i] for i in block_indices]
            valid_col_perms += self._count_valid_block_permutations(col_blocks, 'col')
        
        # Normalizar por 3! = 6 para cada grupo
        row_complexity = (valid_row_perms / 3) / 6.0
        col_complexity = (valid_col_perms / 3) / 6.0
        
        return (row_complexity + col_complexity) / 2.0
    
    def _analyze_constraint_graph(self, board_matrix: List[List[int]]) -> float:
        """TEORÍA DE GRAFOS: Analiza el grafo de restricciones del Sudoku"""
        
        # Construir grafo donde cada celda es un vértice
        # Las aristas conectan celdas que no pueden tener el mismo valor
        graph = self._build_constraint_graph()
        
        # 1. Calcular coeficiente de clustering (conectividad local)
        clustering_coefficient = self._calculate_clustering_coefficient(graph, board_matrix)
        
        # 2. Densidad del grafo de celdas vacías
        empty_cells = sum(row.count(0) for row in board_matrix)
        if empty_cells <= 1:
            graph_density = 0
        else:
            max_edges = empty_cells * (empty_cells - 1) / 2
            actual_edges = sum(len([n for n in graph[cell] if board_matrix[n[0]][n[1]] == 0]) 
                             for i in range(9) for j in range(9) 
                             if board_matrix[i][j] == 0 for cell in [(i, j)]) / 2
            graph_density = actual_edges / max_edges if max_edges > 0 else 0

        # Combinar métricas del grafo
        graph_complexity = (
            clustering_coefficient * 0.6 +         # Coeficiente de clustering
            graph_density * 0.4                    # Densidad del grafo
        )
        
        return min(1.0, graph_complexity)
    
    def _build_constraint_graph(self) -> Dict[Tuple[int, int], Set[Tuple[int, int]]]:
        """Construye el grafo de restricciones del Sudoku"""
        graph = defaultdict(set)
        
        for i in range(9):
            for j in range(9):
                cell = (i, j)
                
                # Conexiones por fila
                for k in range(9):
                    if k != j:
                        graph[cell].add((i, k))
                
                # Conexiones por columna
                for k in range(9):
                    if k != i:
                        graph[cell].add((k, j))
                
                # Conexiones por caja 3x3
                box_start_row, box_start_col = 3 * (i // 3), 3 * (j // 3)
                for r in range(box_start_row, box_start_row + 3):
                    for c in range(box_start_col, box_start_col + 3):
                        if (r, c) != cell:
                            graph[cell].add((r, c))
        
        return graph
    
    def _calculate_clustering_coefficient(self, graph: Dict, board_matrix: List[List[int]]) -> float:
        """Calcula el coeficiente de clustering del grafo"""
        clustering_sum = 0
        empty_cells = []
        
        for i in range(9):
            for j in range(9):
                if board_matrix[i][j] == 0:
                    empty_cells.append((i, j))
        
        if len(empty_cells) < 2:
            return 0.0
        
        for cell in empty_cells:
            neighbors = [n for n in graph[cell] if board_matrix[n[0]][n[1]] == 0]
            
            if len(neighbors) < 2:
                continue
            
            # Contar triángulos (conexiones entre vecinos)
            triangles = 0
            for i, n1 in enumerate(neighbors):
                for n2 in neighbors[i+1:]:
                    if n2 in graph[n1]:
                        triangles += 1
            
            # Calcular clustering local
            possible_triangles = len(neighbors) * (len(neighbors) - 1) / 2
            local_clustering = triangles / possible_triangles if possible_triangles > 0 else 0
            clustering_sum += local_clustering
        
        return clustering_sum / len(empty_cells) if empty_cells else 0.0
    
    def _analyze_combinatorial_complexity(self, board_matrix: List[List[int]]) -> float:
        """COMBINATORIA: Análisis usando inclusión-exclusión y coeficientes binomiales"""
        
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if board_matrix[i][j] == 0:
                    candidates = self._get_possible_values(board_matrix, i, j)
                    empty_cells.append((i, j, len(candidates)))
        
        if not empty_cells:
            return 0.0
        
        # 1. Aplicar Principio de Inclusión-Exclusión
        inclusion_exclusion_score = self._calculate_inclusion_exclusion(empty_cells, board_matrix)
        
        # 2. Calcular Coeficientes Binomiales para elecciones
        binomial_complexity = self._calculate_binomial_complexity(empty_cells)
        
        # 3. Entropía combinatorial
        entropy = 0
        for _, _, candidates in empty_cells:
            if candidates > 1:
                entropy += math.log2(candidates)
        
        max_entropy = len(empty_cells) * math.log2(9)  # Máximo teórico
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        # Combinar métricas combinatoriales
        combinatorial_score = (
            inclusion_exclusion_score * 0.4 +    # 40% - Inclusión-exclusión
            binomial_complexity * 0.4 +          # 40% - Coeficientes binomiales
            normalized_entropy * 0.2              # 20% - Entropía
        )
        
        return min(1.0, combinatorial_score)
    
    def _calculate_inclusion_exclusion(self, empty_cells: List[Tuple], board_matrix: List[List[int]]) -> float:
        """Aplica el Principio de Inclusión-Exclusión para calcular restricciones"""
        
        if len(empty_cells) < 2:
            return 0.0
        
        # Agrupar celdas por región (fila, columna, caja)
        regions = {'rows': defaultdict(list), 'cols': defaultdict(list), 'boxes': defaultdict(list)}
        
        for i, (row, col, candidates) in enumerate(empty_cells):
            regions['rows'][row].append(i)
            regions['cols'][col].append(i)
            box_id = (row // 3, col // 3)
            regions['boxes'][box_id].append(i)
        
        # Calcular intersecciones usando inclusión-exclusión
        total_restrictions = 0
        
        for region_type, region_dict in regions.items():
            for region_id, cell_indices in region_dict.items():
                if len(cell_indices) > 1:
                    # Aplicar inclusión-exclusión para pares de celdas
                    for i in range(len(cell_indices)):
                        for j in range(i + 1, len(cell_indices)):
                            idx1, idx2 = cell_indices[i], cell_indices[j]
                            cell1 = empty_cells[idx1]
                            cell2 = empty_cells[idx2]
                            
                            # Calcular intersección de candidatos
                            candidates1 = self._get_possible_values(board_matrix, cell1[0], cell1[1])
                            candidates2 = self._get_possible_values(board_matrix, cell2[0], cell2[1])
                            
                            intersection = len(candidates1 & candidates2)

                            # Aplicar inclusión-exclusión: |A ∪ B| = |A| + |B| - |A ∩ B|
                            union = (len(candidates1) + len(candidates2) - intersection)
                            
                            ie_value = intersection / union

                            total_restrictions += ie_value
        
        # Normalizar por número máximo de restricciones posibles
        max_restrictions = len(empty_cells) * (len(empty_cells) - 1) / 2
        return total_restrictions / max_restrictions if max_restrictions > 0 else 0
    
    def _calculate_binomial_complexity(self, empty_cells: List[Tuple]) -> float:
        """Calcula complejidad usando coeficientes binomiales"""
        
        if not empty_cells:
            return 0.0
        
        # Calcular coeficientes binomiales para elecciones de candidatos
        binomial_sum = 0
        
        for _, _, candidates in empty_cells:
            if candidates > 1:
                # C(n,k) para diferentes valores de k (elecciones posibles)
                for k in range(1, min(candidates + 1, 4)):  # Limitar para eficiencia
                    try:
                        # Coeficiente binomial C(candidates, k)
                        binomial_coeff = math.comb(candidates, k)
                        binomial_sum += binomial_coeff
                    except (ValueError, OverflowError):
                        continue
        
        # Normalizar por máximo teórico
        max_binomial = len(empty_cells) * sum(math.comb(9, k) for k in range(1, 4))

        return binomial_sum / max_binomial if max_binomial > 0 else 0
    
    def _calculate_solution_space_complexity(self, board_matrix: List[List[int]]) -> float:
        """Calcula complejidad del espacio de soluciones usando backtracking"""
        
        # Contar celdas vacías
        empty_cells = sum(row.count(0) for row in board_matrix)
        
        if empty_cells == 0:
            return 1.0
        
        # Estimar factor de ramificación promedio
        branching_factors = []
        for row in range(9):
            for col in range(9):
                if board_matrix[row][col] == 0:
                    possible_values = self._get_possible_values(board_matrix, row, col)
                    branching_factors.append(len(possible_values))
        
        if not branching_factors:
            return 0.0
        
        avg_branching = sum(branching_factors) / len(branching_factors)
        
        # Calcular complejidad logarítmica del espacio de búsqueda
        search_space_log = empty_cells * math.log(avg_branching) if avg_branching > 1 else 0
        
        # Normalizar (máximo teórico: 81 celdas * log(9) ≈ 178)
        return min(1.0, search_space_log / 178.0)
    
    def _count_valid_row_permutations(self, rows: List[List[int]], board: List[List[int]], start_row: int) -> int:
        """Cuenta permutaciones válidas de filas que mantienen validez del Sudoku"""
        
        valid_count = 0
        for perm in permutations(range(3)):
            # Crear tablero temporal con filas permutadas
            temp_board = copy.deepcopy(board)
            for i, new_pos in enumerate(perm):
                temp_board[start_row + i] = rows[new_pos]
            
            # Verificar si sigue siendo válido
            if self._is_valid_sudoku_state(temp_board):
                valid_count += 1
        
        return valid_count
    
    def _count_valid_column_permutations(self, cols: List[List[int]], board: List[List[int]], start_col: int) -> int:
        """Cuenta permutaciones válidas de columnas que mantienen validez del Sudoku"""
        
        valid_count = 0
        for perm in permutations(range(3)):
            # Crear tablero temporal con columnas permutadas
            temp_board = copy.deepcopy(board)
            for row in range(9):
                for i, new_pos in enumerate(perm):
                    temp_board[row][start_col + i] = cols[new_pos][row]
            
            # Verificar si sigue siendo válido
            if self._is_valid_sudoku_state(temp_board):
                valid_count += 1
        
        return valid_count
    
    def _count_valid_block_permutations(self, blocks: List[List[int]], direction: str) -> int:
        """Cuenta permutaciones válidas de bloques 3x3"""
        
        valid_count = 0
        for perm in permutations(range(3)):
            # Las permutaciones de bloques siempre son válidas en Sudoku
            # ya que no afectan las restricciones internas
            # Solo verificamos que los bloques mantengan su estructura
            permuted_blocks = [blocks[new_pos] for new_pos in perm]
            
            # Verificar que cada bloque tenga estructura válida internamente
            all_valid = True
            for block in permuted_blocks:
                if not self._is_valid_block_structure(block):
                    all_valid = False
                    break
            
            if all_valid:
                valid_count += 1
        
        return valid_count
    
    def _get_possible_values(self, board: List[List[int]], row: int, col: int) -> Set[int]:
        """Obtiene valores posibles para una celda"""
        used_values = set()
        
        # Valores en fila
        used_values.update(board[row])
        
        # Valores en columna
        for r in range(9):
            used_values.add(board[r][col])
        
        # Valores en caja 3x3
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                used_values.add(board[r][c])
        
        # Remover 0 y devolver valores posibles
        used_values.discard(0)
        return set(range(1, 10)) - used_values
    
    def _is_valid_sudoku_state(self, board: List[List[int]]) -> bool:
        """Verifica si el estado del Sudoku es válido"""
        # Verificar filas, columnas y cajas
        for i in range(9):
            if not self._is_valid_group([board[i][j] for j in range(9) if board[i][j] != 0]):
                return False
            if not self._is_valid_group([board[j][i] for j in range(9) if board[j][i] != 0]):
                return False
        
        # Verificar cajas 3x3
        for box_row in range(3):
            for box_col in range(3):
                box_values = []
                for r in range(box_row * 3, (box_row + 1) * 3):
                    for c in range(box_col * 3, (box_col + 1) * 3):
                        if board[r][c] != 0:
                            box_values.append(board[r][c])
                if not self._is_valid_group(box_values):
                    return False
        
        return True
    
    def _is_valid_group(self, values: List[int]) -> bool:
        """Verifica si un grupo no tiene duplicados"""
        return len(values) == len(set(values))
    
    def _is_valid_block_structure(self, block: List[int]) -> bool:
        """Verifica si un bloque 3x3 tiene estructura válida"""
        filled_values = [x for x in block if x != 0]
        return self._is_valid_group(filled_values)
    
    def generate_advanced_puzzle(self, target_difficulty: str = 'facil') -> Tuple[List[List[int]], int, Dict]:
        """Genera un puzzle con sistema avanzado de dificultad"""
        
        # Generar tablero base
        complete_board = self.board.generate_complete_board()
        
        # Determinar rangos objetivo según la clasificación
        # Ajustados para crear mayor contraste
        if target_difficulty == 'facil':
            target_range = (1, 6.5)  # Puzzles fáciles
        elif target_difficulty == 'dificil':
            target_range = (6.6, 10)  # Puzzles difíciles
        else:  # Default a facil
            target_range = (1, 3.5)
        
        best_puzzle = None
        best_metrics = None
        best_final_difficulty = 0
        
        # Intentar múltiples variaciones
        for attempt in range(100):  # Aumentado de 30 a 100 para mejor cobertura
            puzzle = self._create_puzzle_variation(complete_board, target_difficulty)
            
            # Calcular métricas de cada aspecto (1-10)
            total_diff = self.calculate_difficulty(puzzle)
            
            # Clasificar según rangos ajustados para sistema de 2 niveles con mayor contraste
            if total_diff <= HIGH_DIFFICULTY_THRESHOLD:
                classification = 'Fácil'
            else:
                classification = 'Difícil'
            
            metrics = {
                'permutation_difficulty': round(self.permutation_difficulty, 2),
                'graph_difficulty': round(self.graph_difficulty, 2),
                'combinatorial_difficulty': round(self.combinatorial_difficulty, 2),
                'final_difficulty': float(total_diff),
                'target_range': target_range,
                'classification': classification,
                'difficulty_breakdown': {
                    'permutations': round(self.permutation_difficulty, 2),
                    'graph_theory': round(self.graph_difficulty, 2),
                    'combinatorics': round(self.combinatorial_difficulty, 2),
                    'final': float(total_diff)
                }
            }
            
            # Verificar si está en el rango objetivo
            if target_range[0] <= total_diff <= target_range[1]:
                # Preferir puzzles más extremos dentro del rango
                if target_difficulty == 'facil':
                    score = 6.5 - total_diff  # Mientras menor, mejor para fácil
                else:  # dificil
                    score = total_diff - 6.6  # Mientras mayor, mejor para difícil
                    
                if score > best_final_difficulty:
                    best_puzzle = puzzle
                    best_metrics = metrics
                    best_final_difficulty = score
        
        # Si no encontramos uno perfecto, usar el mejor
        if best_puzzle is None:
            puzzle = self._create_puzzle_variation(complete_board, target_difficulty)
            total_diff = self.calculate_difficulty(puzzle)
            
            # Clasificar según rangos ajustados para sistema de 2 niveles con mayor contraste
            if total_diff <= HIGH_DIFFICULTY_THRESHOLD:
                classification = 'Fácil'
            else:
                classification = 'Difícil'
            
            best_metrics = {
                'permutation_difficulty': round(self.permutation_difficulty, 2),
                'graph_difficulty': round(self.graph_difficulty, 2),
                'combinatorial_difficulty': round(self.combinatorial_difficulty, 2),
                'final_difficulty': float(total_diff),
                'target_range': target_range,
                'classification': classification,
                'difficulty_breakdown': {
                    'permutations': round(self.permutation_difficulty, 2),
                    'graph_theory': round(self.graph_difficulty, 2),
                    'combinatorics': round(self.combinatorial_difficulty, 2),
                    'final': float(total_diff)
                }
            }
            best_puzzle = puzzle
        
        # Actualizar el tablero principal
        self.board.board = copy.deepcopy(best_puzzle)
        self.board.initial_board = copy.deepcopy(best_puzzle)
        self.board.solution = copy.deepcopy(complete_board)
        
        self.permutation_difficulty = best_metrics['permutation_difficulty']
        self.graph_difficulty = best_metrics['graph_difficulty']
        self.combinatorial_difficulty = best_metrics['combinatorial_difficulty']
        self.final_difficulty = best_metrics['final_difficulty']
        
        return best_puzzle, int(round(best_metrics['final_difficulty'])), best_metrics
    
    def _create_puzzle_variation(self, complete_board: List[List[int]], target_difficulty: str) -> List[List[int]]:
        """Crea una variación del puzzle usando remoción inteligente"""
        
        puzzle = copy.deepcopy(complete_board)
        
        # Determinar cuántas celdas remover - MISMO NÚMERO para ambas dificultades
        # La dificultad vendrá de la DISTRIBUCIÓN, no de la cantidad
        
        # Diferentes estrategias de remoción según dificultad
        if target_difficulty == 'facil':
            puzzle = self._create_easy_distribution(complete_board, CELLS_TO_REMOVE_LOW_DIFFICULTY)
        else:  # dificil
            puzzle = self._create_difficult_distribution(complete_board, CELLS_TO_REMOVE_HIGH_DIFFICULTY)
            
        return puzzle
    
    def _create_easy_distribution(self, complete_board: List[List[int]], cells_to_remove: int) -> List[List[int]]:
        """Crea distribución fácil: celdas conectadas y agrupadas"""
        puzzle = copy.deepcopy(complete_board)
        
        # ESTRATEGIA FÁCIL: Crear clusters conectados de celdas llenas
        # Esto permite técnicas de resolución secuencial y lógica simple
        
        # 1. Mantener bloques 3x3 relativamente completos
        positions_to_remove = []
        
        # Priorizar remoción que mantenga conectividad
        for block_row in range(3):
            for block_col in range(3):
                block_positions = []
                for r in range(block_row * 3, (block_row + 1) * 3):
                    for c in range(block_col * 3, (block_col + 1) * 3):
                        block_positions.append((r, c))
                
                # En cada bloque, quitar aproximadamente 5-6 celdas (dejar 3-4)
                # pero mantener las que quedan conectadas
                random.shuffle(block_positions)
                
                # Quitar las primeras 5-6 posiciones de cada bloque
                cells_per_block = cells_to_remove // 9
                remainder = cells_to_remove % 9
                
                cells_this_block = cells_per_block
                if block_row * 3 + block_col < remainder:
                    cells_this_block += 1
                    
                positions_to_remove.extend(block_positions[:cells_this_block])
        
        # 2. Aplicar la remoción manteniendo conectividad
        for row, col in positions_to_remove:
            puzzle[row][col] = 0
            
        return puzzle
    
    def _create_difficult_distribution(self, complete_board: List[List[int]], cells_to_remove: int) -> List[List[int]]:
        """Crea distribución difícil: celdas dispersas y desconectadas"""
        puzzle = copy.deepcopy(complete_board)
        
        # ESTRATEGIA SIMPLIFICADA PERO EFECTIVA: 
        # Remover celdas maximizando dispersión de forma más robusta
        
        all_positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(all_positions)  # Añadir aleatoriedad inicial
        
        removed_positions = []
        
        for _ in range(cells_to_remove):
            if len(removed_positions) >= cells_to_remove:
                break
                
            # Encontrar la posición que maximiza la dispersión
            best_pos = None
            best_score = -1
            
            for pos in all_positions:
                if pos in removed_positions:
                    continue
                    
                row, col = pos
                
                # Calcular score de dispersión simple pero efectivo
                dispersión_score = 0
                
                # Penalizar posiciones cerca de celdas ya removidas
                for removed_row, removed_col in removed_positions:
                    distance = abs(row - removed_row) + abs(col - removed_col)
                    if distance <= 2:  # Muy cerca
                        dispersión_score -= 3
                    elif distance <= 4:  # Moderadamente cerca
                        dispersión_score -= 1
                
                # Bonus por estar en bordes (incrementa dificultad)
                if row == 0 or row == 8 or col == 0 or col == 8:
                    dispersión_score += 2
                
                # Bonus por dispersión en bloques 3x3
                block_r, block_c = row // 3, col // 3
                block_removals = sum(1 for r, c in removed_positions 
                                   if r // 3 == block_r and c // 3 == block_c)
                if block_removals < 2:  # Preferir dispersar entre bloques
                    dispersión_score += 1
                
                # Añadir componente aleatorio para variabilidad
                dispersión_score += random.uniform(0, 0.5)
                
                if dispersión_score > best_score:
                    best_score = dispersión_score
                    best_pos = pos
            
            if best_pos:
                removed_positions.append(best_pos)
            else:
                # Fallback: tomar cualquier posición disponible
                available = [pos for pos in all_positions if pos not in removed_positions]
                if available:
                    removed_positions.append(random.choice(available))
        
        # Aplicar la remoción
        for row, col in removed_positions:
            puzzle[row][col] = 0
            
        return puzzle
    
    def get_difficulty_metrics(self) -> Dict:
        """Obtiene las métricas de dificultad actuales"""
        # Clasificar según rangos ajustados para sistema de 2 niveles con mayor contraste
        if self.final_difficulty <= HIGH_DIFFICULTY_THRESHOLD:
            classification = 'Fácil'
        else:
            classification = 'Difícil'
        
        return {
            'permutation_difficulty': round(self.permutation_difficulty, 2),
            'graph_difficulty': round(self.graph_difficulty, 2),
            'combinatorial_difficulty': round(self.combinatorial_difficulty, 2),
            'final_difficulty': self.final_difficulty,
            'classification': classification,
            'difficulty_breakdown': {
                'permutations': round(self.permutation_difficulty, 2),
                'graph_theory': round(self.graph_difficulty, 2),
                'combinatorics': round(self.combinatorial_difficulty, 2),
                'final': self.final_difficulty
            }
        }
