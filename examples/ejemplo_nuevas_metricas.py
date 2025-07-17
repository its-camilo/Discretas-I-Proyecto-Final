#!/usr/bin/env python3
"""
Ejemplo de las nuevas métricas de matemáticas discretas implementadas
en el sistema de dificultad avanzado del Sudoku.
"""

from sudoku.advanced_difficulty import AdvancedDifficultySystem
import json

def mostrar_analisis_detallado():
    """Muestra un análisis detallado de las nuevas métricas implementadas"""
    
    print("=" * 80)
    print("DEMOSTRACIÓN DE NUEVAS MÉTRICAS DE MATEMÁTICAS DISCRETAS")
    print("=" * 80)
    
    # Crear sistema de dificultad
    system = AdvancedDifficultySystem()
    
    # Generar diferentes tipos de puzzles
    niveles = ['facil', 'medio', 'dificil']
    
    for nivel in niveles:
        print(f"\n{'='*20} ANÁLISIS NIVEL: {nivel.upper()} {'='*20}")
        
        # Generar puzzle
        puzzle, dificultad, metricas = system.generate_advanced_puzzle(nivel)
        
        # Mostrar análisis detallado
        print(f"\n📊 RESUMEN GENERAL:")
        print(f"   Dificultad Final: {dificultad}/10")
        print(f"   Clasificación: {metricas['classification']}")
        print(f"   Celdas vacías: {sum(row.count(0) for row in puzzle)}/81")
        
        # Desglose por áreas matemáticas
        breakdown = metricas['difficulty_breakdown']
        
        print(f"\n🧮 DESGLOSE POR ÁREAS DE MATEMÁTICAS DISCRETAS:")
        print(f"   ├─ Permutaciones: {breakdown['permutations']:.2f}/10")
        print(f"   │  └─ Análisis de grupos simétricos S₃")
        print(f"   ├─ Teoría de Grafos: {breakdown['graph_theory']:.2f}/10")
        print(f"   │  └─ Grafo de restricciones, clustering, componentes")
        print(f"   ├─ Combinatoria: {breakdown['combinatorics']:.2f}/10")
        print(f"   │  └─ Inclusión-exclusión, coeficientes binomiales")
        print(f"   └─ Teoría de Conjuntos: {breakdown['set_theory']:.2f}/10")
        print(f"      └─ Intersecciones, uniones, cardinalidad")
        
        # Análisis específico de conceptos implementados
        print(f"\n🔍 CONCEPTOS MATEMÁTICOS APLICADOS:")
        
        # 1. Teoría de Grafos
        print(f"   📈 TEORÍA DE GRAFOS:")
        print(f"      • Construcción del grafo de restricciones G=(V,E)")
        print(f"      • Cálculo de grados de vértices (máx. 20 por celda)")
        print(f"      • Coeficiente de clustering local")
        print(f"      • Análisis de componentes conexas")
        print(f"      • Densidad del grafo de celdas vacías")
        
        # 2. Combinatoria Avanzada  
        print(f"   🔢 COMBINATORIA AVANZADA:")
        print(f"      • Principio de Inclusión-Exclusión: |A∪B| = |A|+|B|-|A∩B|")
        print(f"      • Coeficientes Binomiales: C(n,k) = n!/(k!(n-k)!)")
        print(f"      • Entropía combinatorial: Σ log₂(candidatos)")
        print(f"      • Análisis de restricciones entre regiones")
        
        # 3. Teoría de Conjuntos
        print(f"   🎯 TEORÍA DE CONJUNTOS:")
        print(f"      • Índice de Jaccard: |A∩B|/|A∪B|")
        print(f"      • Análisis de intersecciones entre candidatos")
        print(f"      • Diversidad por uniones regionales")
        print(f"      • Cardinalidad promedio de conjuntos")
        print(f"      • Detección de conjuntos singleton")
        
        # Mostrar algunos datos específicos del puzzle generado
        print(f"\n📋 DATOS ESPECÍFICOS DE ESTE PUZZLE:")
        empty_count = sum(row.count(0) for row in puzzle)
        print(f"      • Vértices en grafo: {empty_count} (celdas vacías)")
        print(f"      • Aristas máximas: {empty_count * 20} (restricciones)")
        print(f"      • Grupos simétricos: 9 bloques × S₃ = 54 permutaciones")
        print(f"      • Operaciones de conjunto: {empty_count * (empty_count-1)//2} pares analizados")
        
        print(f"\n" + "-" * 60)

def mostrar_formulas_matematicas():
    """Muestra las fórmulas matemáticas implementadas"""
    
    print(f"\n{'='*60}")
    print("FÓRMULAS MATEMÁTICAS IMPLEMENTADAS")
    print(f"{'='*60}")
    
    formulas = {
        "Dificultad Final": """
        D = 0.20×P + 0.15×G + 0.15×C + 0.10×S
        donde:
        P = Permutaciones (números + filas + columnas + bloques)
        G = Teoría de Grafos (grado + clustering + componentes + densidad)
        C = Combinatoria (inclusión-exclusión + binomiales + entropía)
        S = Teoría de Conjuntos (intersecciones + uniones + cardinalidad)
        """,
        
        "Teoría de Grafos": """
        Clustering(v) = triángulos_locales / triángulos_posibles
        Densidad = |E| / (|V| × (|V|-1) / 2)
        Grado(v) = |{u ∈ V : (v,u) ∈ E}|
        """,
        
        "Inclusión-Exclusión": """
        |A ∪ B| = |A| + |B| - |A ∩ B|
        Para n conjuntos: |⋃Aᵢ| = Σ|Aᵢ| - Σ|Aᵢ∩Aⱼ| + Σ|Aᵢ∩Aⱼ∩Aₖ| - ...
        """,
        
        "Coeficientes Binomiales": """
        C(n,k) = n! / (k!(n-k)!)
        Complejidad = Σᵢ Σₖ C(candidatos_i, k) para k=1,2,3
        """,
        
        "Índice de Jaccard": """
        J(A,B) = |A ∩ B| / |A ∪ B|
        Mide similitud entre conjuntos de candidatos
        """
    }
    
    for concepto, formula in formulas.items():
        print(f"\n📐 {concepto}:")
        print(formula)

if __name__ == "__main__":
    mostrar_analisis_detallado()
    mostrar_formulas_matematicas()
    
    print(f"\n{'='*80}")
    print("✅ NUEVAS FUNCIONALIDADES IMPLEMENTADAS:")
    print("   • Teoría de Grafos - Análisis de grafo de restricciones")
    print("   • Combinatoria - Inclusión-exclusión y coeficientes binomiales")  
    print("   • Teoría de Conjuntos - Operaciones y análisis de candidatos")
    print("   • Sistema integrado con pesos matemáticamente justificados")
    print(f"{'='*80}")
