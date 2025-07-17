"""Test avanzado del cronómetro de resolución - 50 sudokus por dificultad"""

import sys
import os
import time
import statistics
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudoku.board import SudokuBoard

def test_timing_comprehensive():
    """Test exhaustivo del cronómetro con 50 sudokus por dificultad"""
    print("=" * 80)
    print("🧪 TEST EXHAUSTIVO DEL CRONÓMETRO DE RESOLUCIÓN")
    print("📊 Resolviendo 50 sudokus por cada dificultad")
    print("=" * 80)
    
    board = SudokuBoard()
    
    # Configuración de test
    difficulties = ['facil', 'medio', 'dificil']
    num_tests = 50
    
    # Resultados globales
    all_results = {}
    
    for difficulty in difficulties:
        print(f"\n🎯 INICIANDO TEST PARA DIFICULTAD: {difficulty.upper()}")
        print("-" * 60)
        
        times = []
        success_count = 0
        
        # Progress indicator setup
        progress_interval = 10
        
        for i in range(num_tests):
            # Mostrar progreso cada 10 sudokus
            if (i + 1) % 10 == 0:
                print(f"  📈 Progreso: {i + 1}/{num_tests} sudokus completados...")
            
            # Generar nuevo puzzle
            board.generate_puzzle(difficulty)
            
            # Medir tiempo de resolución (sin prints)
            start_time = time.time()
            temp_board = board.board.copy()
            solved = board.solve_backtracking([row[:] for row in temp_board])
            end_time = time.time()
            
            resolution_time = end_time - start_time
            times.append(resolution_time)
            
            if solved:
                success_count += 1
        
        # Calcular estadísticas
        if times:
            min_time = min(times)
            max_time = max(times)
            avg_time = statistics.mean(times)
            median_time = statistics.median(times)
            std_dev = statistics.stdev(times) if len(times) > 1 else 0
            success_rate = (success_count / num_tests) * 100
            
            # Guardar resultados
            all_results[difficulty] = {
                'times': times,
                'min': min_time,
                'max': max_time,
                'avg': avg_time,
                'median': median_time,
                'std_dev': std_dev,
                'success_rate': success_rate,
                'total_time': sum(times)
            }
            
            # Mostrar resultados para esta dificultad
            print(f"\n✅ RESULTADOS PARA {difficulty.upper()}:")
            print(f"   📊 Sudokus resueltos: {success_count}/{num_tests} ({success_rate:.1f}%)")
            print(f"   ⚡ Tiempo mínimo: {min_time:.4f}s ({min_time*1000:.2f}ms)")
            print(f"   🐌 Tiempo máximo: {max_time:.4f}s ({max_time*1000:.2f}ms)")
            print(f"   📈 Tiempo promedio: {avg_time:.4f}s ({avg_time*1000:.2f}ms)")
            print(f"   📊 Tiempo mediano: {median_time:.4f}s ({median_time*1000:.2f}ms)")
            print(f"   📏 Desviación estándar: {std_dev:.4f}s ({std_dev*1000:.2f}ms)")
            print(f"   🕒 Tiempo total: {sum(times):.4f}s")
            
            # Categorización de velocidad
            if avg_time < 0.001:
                speed_category = "⚡ ULTRA RÁPIDO"
            elif avg_time < 0.01:
                speed_category = "🏃 MUY RÁPIDO"
            elif avg_time < 0.1:
                speed_category = "🚶 RÁPIDO"
            elif avg_time < 1.0:
                speed_category = "🐢 NORMAL"
            else:
                speed_category = "🐌 LENTO"
            
            print(f"   🏆 Categoría de velocidad: {speed_category}")
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN COMPARATIVO FINAL")
    print("=" * 80)
    
    print(f"{'DIFICULTAD':<12} {'PROMEDIO':<12} {'MIN':<10} {'MAX':<10} {'ÉXITO':<8}")
    print("-" * 60)
    
    for difficulty in difficulties:
        if difficulty in all_results:
            r = all_results[difficulty]
            print(f"{difficulty.upper():<12} {r['avg']*1000:>8.2f}ms {r['min']*1000:>7.2f}ms {r['max']*1000:>7.2f}ms {r['success_rate']:>6.1f}%")
    
    # Análisis de rendimiento
    print(f"\n🔍 ANÁLISIS DE RENDIMIENTO:")
    
    if len(all_results) >= 2:
        # Comparar fácil vs difícil
        if 'facil' in all_results and 'dificil' in all_results:
            easy_avg = all_results['facil']['avg']
            hard_avg = all_results['dificil']['avg']
            difference = hard_avg - easy_avg
            percentage_diff = (difference / easy_avg) * 100 if easy_avg > 0 else 0
            
            print(f"   📈 Diferencia Fácil → Difícil: +{difference:.4f}s (+{percentage_diff:.1f}%)")
        
        # Comparar medio vs extremos
        if 'medio' in all_results:
            medium_avg = all_results['medio']['avg']
            if 'facil' in all_results:
                easy_medium_diff = medium_avg - all_results['facil']['avg']
                print(f"   📊 Diferencia Fácil → Medio: +{easy_medium_diff:.4f}s")
            if 'dificil' in all_results:
                medium_hard_diff = all_results['dificil']['avg'] - medium_avg
                print(f"   📊 Diferencia Medio → Difícil: +{medium_hard_diff:.4f}s")
    
    # Estadísticas globales
    total_sudokus = sum(len(r['times']) for r in all_results.values())
    total_time = sum(r['total_time'] for r in all_results.values())
    
    print(f"\n🌟 ESTADÍSTICAS GLOBALES:")
    print(f"   🧩 Total de sudokus resueltos: {total_sudokus}")
    print(f"   ⏰ Tiempo total de procesamiento: {total_time:.4f}s")
    print(f"   🚀 Velocidad promedio global: {total_time/total_sudokus:.4f}s por sudoku")
    print(f"   💾 Sudokus por segundo: {total_sudokus/total_time:.1f}")
    
    print("\n✅ Test exhaustivo completado!")
    print("=" * 80)

if __name__ == "__main__":
    test_timing_comprehensive()
