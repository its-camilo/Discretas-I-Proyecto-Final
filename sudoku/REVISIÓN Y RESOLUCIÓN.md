# REVISIÓN Y RESOLUCIÓN

## Sistema Avanzado de Verificación y Resolución de Sudoku

**Basado en Permutaciones y Teoría de Grafos**

Este módulo implementa la verificación de soluciones propuestas por el usuario y la resolución automática de tableros incompletos, utilizando principios de Matemáticas Discretas. Las principales herramientas teóricas aplicadas son Permutaciones y Coloreo de Grafos.

---

### 🧠 Fundamento Matemático

#### 1. Permutaciones (Grupos Simétricos)
Cada fila, columna y región 3×3 en un tablero de Sudoku debe contener una permutación del conjunto {1, 2, ..., 9}, es decir, todos los números sin repeticiones. Esta propiedad se verifica en la resolución y validación.

- **Verificación de usuario:** Se analiza si las filas, columnas y regiones son permutaciones válidas.
- **Resolución automática:** El algoritmo explora el espacio de permutaciones posibles bajo restricciones locales (vecinos), usando backtracking optimizado.

#### 2. Coloreo de Grafos (Teoría de Grafos)
El tablero de Sudoku se modela como un grafo de restricciones, donde:
- Cada casilla es un nodo.
- Se traza una arista entre dos nodos si están en la misma fila, columna o región.
- La asignación de un número a una casilla equivale a colorear un nodo con un color (valor numérico).
- El objetivo es lograr una coloración propia: ningún nodo tiene el mismo color que sus vecinos.

---

### 🛠️ Funcionalidades Implementadas

#### ✅ Verificación de Soluciones (Entrada del Usuario)
- Verifica que no se repitan valores en las filas, columnas ni regiones 3×3.
- Utiliza la estructura de grafo para comprobar que cada nodo tiene un color distinto a sus vecinos (coloración propia).
- La función `verificar_coloracion_propia(i, j)` evalúa si un valor asignado a la casilla (i, j) cumple con las restricciones del grafo de Sudoku.

#### 🤖 Resolución Automática
- Emplea backtracking con heurísticas de reducción del espacio de búsqueda basado en vecinos.
- En cada paso se asegura que la asignación cumple con la regla de coloración del grafo.
- Explora las permutaciones válidas en las subestructuras del tablero para hallar una solución coherente.

---

### 📂 Estructura del Código

```python
class SudokuBoard:
    def get_neighbors(self, row, col) -> Set[Tuple[int, int]]:
        # Retorna los vecinos según el grafo de restricciones del Sudoku

    def verificar_coloracion_propia(self, row, col, value) -> bool:
        # Verifica si el valor en la posición (row, col) es válido según sus vecinos

    def solve(self) -> bool:
        # Algoritmo de resolución automática basado en DFS y validación por coloración
```

---

### 📚 Conclusión

Este proyecto trasciende una implementación básica de Sudoku al incorporar herramientas fundamentales de Matemáticas Discretas:

- **Permutaciones:** para validar conjuntos sin repeticiones.
- **Teoría de grafos:** para modelar restricciones y aplicar una coloración propia eficiente.

La integración de estos conceptos permite validar de forma rigurosa soluciones propuestas por el usuario y generar soluciones automáticamente, asegurando coherencia matemática en todo momento.
