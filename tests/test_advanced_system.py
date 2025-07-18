"""Test script para verificar el sistema de dificultad avanzado"""

import sys
sys.path.append('.')

from sudoku.board import SudokuBoard
from sudoku.advanced_difficulty import AdvancedDifficultySystem

def test_advanced_difficulty_system():
    """Test del sistema de dificultad avanzado"""
    print("Testing Advanced Difficulty System...")
    
    # Crear board
    board = SudokuBoard()
    
    # Alternar a sistema avanzado
    board.use_advanced_difficulty = True
    
    # Probar diferentes niveles de dificultad
    difficulties = ['facil', 'dificil']
    
    for diff in difficulties:
        print(f"\n--- Probando dificultad: {diff} ---")
        
        # Generar puzzle
        board.generate_puzzle(diff)
        
        # Obtener métricas
        metrics = board.get_difficulty_metrics()
        level = board.get_difficulty_level()
        
        print(f"Nivel final: {level}/10")
        print(f"Métricas completas: {metrics}")
        
        if 'difficulty_breakdown' in metrics:
            breakdown = metrics['difficulty_breakdown']
            print(f"Permutaciones: {breakdown['permutations']}/10")
            print(f"Teoría de Grafos: {breakdown['graph_theory']}/10")
            print(f"Combinatoria: {breakdown['combinatorics']}/10")
            print(f"Final: {breakdown['final']}/10")
        
        # Verificar si tenemos last_difficulty_info
        if hasattr(board, 'last_difficulty_info'):
            info = board.last_difficulty_info
            print(f"Info guardada: {info}")
        else:
            print("No hay last_difficulty_info disponible")
        
        print(f"Celdas vacías: {sum(row.count(0) for row in board.board)}/81")
        
        # Verificar que la solución es única
        if board.verify_solution():
            print("✓ Solución válida")
        else:
            print("✗ Solución inválida")

if __name__ == "__main__":
    test_advanced_difficulty_system()
