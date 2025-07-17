"""
Ejemplos de uso y documentación técnica del juego de Sudoku
"""

# Ejemplo de uso básico
from sudoku.board import SudokuBoard
from sudoku.utils import SudokuValidator, SudokuHints

def ejemplo_basico():
    """Ejemplo básico de uso del módulo de Sudoku"""
    
    # Crear un nuevo tablero
    board = SudokuBoard()
    
    # Generar un puzzle fácil
    puzzle, difficulty = board.generate_puzzle('facil')
    
    print(f"Puzzle generado con dificultad: {difficulty}/10")
    print(f"Número de celdas llenas: {SudokuValidator.count_filled_cells(puzzle)}")
    
    # Imprimir el tablero
    for row in puzzle:
        print(' '.join(str(cell) if cell != 0 else '.' for cell in row))
    
    return board

def ejemplo_resolucion():
    """Ejemplo de resolución de puzzle"""
    
    board = SudokuBoard()
    board.generate_puzzle('dificil')
    
    print("Tablero inicial:")
    for row in board.board:
        print(' '.join(str(cell) if cell != 0 else '.' for cell in row))
    
    # Resolver el puzzle
    board.solve_current_board()
    
    print("\nTablero resuelto:")
    for row in board.board:
        print(' '.join(str(cell) for cell in row))

def ejemplo_validacion():
    """Ejemplo de validación de solución"""
    
    board = SudokuBoard()
    board.generate_puzzle('facil')
    
    # Agregar algunos números incorrectos
    for i in range(9):
        for j in range(9):
            if board.is_cell_editable(i, j):
                board.set_cell_value(i, j, 5)  # Número que probablemente cause conflicto
                break
    
    # Verificar la solución
    validity = board.verify_solution()
    
    print("Resultados de validación:")
    for i, row in enumerate(validity):
        for j, is_valid in enumerate(row):
            if board.get_cell_value(i, j) != 0:
                status = "✓" if is_valid else "✗"
                print(f"Celda ({i},{j}): {board.get_cell_value(i, j)} {status}")

def ejemplo_hints():
    """Ejemplo de uso del sistema de pistas"""
    
    board = SudokuBoard()
    board.generate_puzzle('facil')
    
    hints = SudokuHints(board)
    
    # Obtener una pista
    row, col, value = hints.get_hint()
    
    if row is not None:
        print(f"Pista: La celda ({row},{col}) debería tener el valor {value}")
        
        # Obtener valores posibles para una celda
        possible = hints.get_possible_values(row, col)
        print(f"Valores posibles para ({row},{col}): {possible}")
    
    # Contar errores
    mistakes = hints.count_mistakes()
    print(f"Número de errores actuales: {mistakes}")

def ejemplo_estadisticas():
    """Ejemplo de uso de estadísticas"""
    
    from sudoku.utils import SudokuStatistics
    
    stats = SudokuStatistics()
    
    # Simular algunos juegos
    for i in range(5):
        stats.start_game()
        # Simular tiempo de juego
        import time
        time.sleep(0.1)  # Simular 100ms de juego
        stats.end_game(solved=(i % 2 == 0))  # Resolver juegos alternos
    
    print(f"Juegos jugados: {stats.games_played}")
    print(f"Juegos resueltos: {stats.games_solved}")
    print(f"Tasa de éxito: {stats.get_success_rate():.1f}%")
    print(f"Tiempo promedio: {stats.get_average_time():.2f}s")

def ejemplo_personalizacion():
    """Ejemplo de personalización del juego"""
    
    from sudoku.config import CUSTOM_COLORS, GAME_CONFIG
    
    # Mostrar configuración actual
    print("Configuración del juego:")
    for key, value in GAME_CONFIG.items():
        print(f"  {key}: {value}")
    
    print("\nColores personalizados:")
    for key, value in CUSTOM_COLORS.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    print("=== Ejemplos de uso del juego de Sudoku ===\n")
    
    print("1. Ejemplo básico:")
    ejemplo_basico()
    
    print("\n2. Ejemplo de resolución:")
    ejemplo_resolucion()
    
    print("\n3. Ejemplo de validación:")
    ejemplo_validacion()
    
    print("\n4. Ejemplo de pistas:")
    ejemplo_hints()
    
    print("\n5. Ejemplo de estadísticas:")
    ejemplo_estadisticas()
    
    print("\n6. Ejemplo de personalización:")
    ejemplo_personalizacion()
