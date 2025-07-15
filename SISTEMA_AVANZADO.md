# Sistema de Dificultad Avanzado - Sudoku

## Funcionalidades Implementadas

### 1. Sistema Dual de Dificultad
- **Sistema Básico**: Basado en remoción aleatoria de celdas
- **Sistema Avanzado**: Basado en análisis de permutaciones y densidad de celdas

### 2. Métricas de Dificultad Avanzada

#### Análisis de Permutaciones (1-10)
- Analiza patrones de números en filas, columnas y cajas 3x3
- Calcula la complejidad basada en:
  - Distribución de números
  - Varianza de posiciones
  - Factores de complejidad combinados

#### Análisis de Densidad de Celdas (1-10)
- Implementa el concepto de "celdas disjuntas"
- Calcula la densidad de contexto de cada celda
- Considera la relación con celdas vecinas en filas, columnas y cajas
- Menos densidad = más disjuntas = más difícil

#### Dificultad Final
- Promedio de dificultad de permutaciones y densidad
- Escala de 1-10 donde:
  - Fácil: 1-3
  - Medio: 4-6
  - Difícil: 7-10

### 3. Interfaz de Usuario

#### Botones de Control
- **Fácil/Medio/Difícil**: Genera puzzle con dificultad específica
- **Alternar Sistema**: Cambia entre sistema básico y avanzado
- **Nuevo**: Genera nuevo puzzle con misma dificultad
- **Resolver**: Resuelve automáticamente el puzzle
- **Verificar**: Valida la solución actual
- **Limpiar**: Borra celdas editables

#### Información Mostrada
- **Sistema Activo**: Básico o Avanzado
- **Métricas Detalladas**: (Solo sistema avanzado)
  - Permutaciones: X/10
  - Densidad: X/10
  - Promedio: X/10
- **Rangos de Dificultad**: Explicación de niveles
- **Instrucciones**: Guía de uso

### 4. Características Técnicas

#### Generación de Puzzles
- Garantiza 30 celdas iniciales
- Solución única verificada
- Cumple reglas estándar de Sudoku

#### Algoritmos Implementados
- **Backtracking**: Para resolver puzzles
- **Análisis de Patrones**: Para calcular permutaciones
- **Análisis de Densidad**: Para evaluar celdas disjuntas
- **Validación**: Verificación de soluciones

#### Estructura del Código
- **Modular**: Separación clara de responsabilidades
- **Escalable**: Fácil adición de nuevas funcionalidades
- **Documentado**: Comentarios y docstrings completos

### 5. Uso del Sistema

#### Controles
- **Clic**: Seleccionar celda
- **Teclas 1-9**: Ingresar números
- **DELETE/BACKSPACE**: Borrar número
- **Botones**: Controlar juego y dificultad

#### Flujo Típico
1. Seleccionar dificultad (Fácil/Medio/Difícil)
2. Optionally alternar sistema (Básico/Avanzado)
3. Resolver puzzle manualmente
4. Verificar solución
5. Generar nuevo puzzle o usar controles

### 6. Ejemplo de Salida

```
Sistema: Avanzado
Dificultad Final: 5/10
Permutaciones: 4/10
Densidad: 6/10
Promedio: 5/10
Celdas vacías: 51/81
```

## Archivos Principales

- `main.py`: Punto de entrada
- `sudoku/board.py`: Lógica del tablero y generación
- `sudoku/gui.py`: Interfaz gráfica
- `sudoku/advanced_difficulty.py`: Sistema avanzado de dificultad
- `sudoku/game.py`: Bucle principal del juego
- `sudoku/constants.py`: Constantes y configuración

## Pruebas

- `tests.py`: Suite de pruebas completa
- `test_advanced_system.py`: Pruebas específicas del sistema avanzado
- `examples.py`: Ejemplos de uso
