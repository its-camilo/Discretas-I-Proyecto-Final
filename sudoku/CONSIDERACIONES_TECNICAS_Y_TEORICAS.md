
# CONSIDERACIONES TÉCNICAS Y TEÓRICAS


## Índice

1. [Sistema de Dificultad - Sudoku](#sistema-de-dificultad---sudoku)
2. [Revisión y Resolución](#revisión-y-resolución)
3. [Implementación Avanzada de Permutaciones en Sudoku](#implementación-avanzada-de-permutaciones-en-sudoku-creación-del-tablero)

---

# Sistema de Dificultad - Sudoku

## ¿Cómo influyen las Matemáticas Discretas en la dificultad del Sudoku?

### Introducción para Jugadores de Sudoku

Si juegas Sudoku regularmente, sabes que algunos puzzles son más difíciles que otros; pero **¿qué hace exactamente que un Sudoku sea más difícil?** Este sistema usa conceptos matemáticos avanzados para medir objetivamente la dificultad, analizando aspectos del puzzle que afectan directamente tu experiencia como jugador.

### ¿Por qué usar Matemáticas Discretas para medir la dificultad?

Cuando resuelves un Sudoku, tu cerebro está haciendo inconscientemente:
- **Análisis de patrones** (permutaciones)
- **Evaluación de conexiones** entre celdas (teoría de grafos)
- **Cálculo de posibilidades** (combinatoria)
- **Manejo de opciones** por región (combinatoria)

Este sistema **matematiza** estos procesos mentales para predecir qué tan difícil será un puzzle para el jugador promedio.

## Métricas de Dificultad: ¿Qué miden y cómo afectan tu experiencia?

### 🎯 1. Análisis de Permutaciones (56% del peso total)
*"¿Qué tan predecibles son los patrones del puzzle?"*

#### 📊 Distribución de números (15% del peso)
**¿Qué mide?** La distribución de los números 1-9 en el tablero inicial.

**¿Cómo afecta la dificultad?**
- **MAYOR dificultad** cuando los números están distribuidos de forma **irregular**.
  - Ejemplo: si tienes muchos 7s pero pocos 3s, tu cerebro tiene menos patrones consistentes para seguir.
  - Es como intentar resolver un rompecabezas donde algunas piezas son más abundantes que otras.
- **MENOR dificultad** cuando los números aparecen de forma **equilibrada**.
  - Cada número del 1-9 aparece aproximadamente la misma cantidad de veces.
  - Tu cerebro puede desarrollar estrategias consistentes para cada número.

**En la práctica:** un Sudoku con distribución irregular te hará sentir que "algunos números son imposibles de encontrar" mientras que otros "aparecen por todas partes".

#### 🔄 Permutaciones de filas y columnas (15% cada uno)
**¿Qué mide?** Cuántas formas válidas hay de reorganizar filas/columnas dentro de cada bloque 3×3.

**¿Cómo afecta la dificultad?**
- **MAYOR dificultad** cuando hay **pocas** reorganizaciones válidas.
  - El puzzle tiene una estructura muy rígida.
  - Cada fila/columna debe estar exactamente donde está.
  - No hay "flexibilidad" para errores o aproximaciones.
- **MENOR dificultad** cuando hay **muchas** reorganizaciones válidas.
  - Múltiples patrones funcionales.
  - Más tolerancia a enfoques diferentes.
  - Varias "rutas" para llegar a la solución.

**En la práctica:** si el puzzle tiene alta rigidez estructural, sentirás que "solo hay una forma correcta" de proceder en cada paso.

#### 📦 Permutaciones de bloques (11% del peso)
**¿Qué mide?** La flexibilidad para reorganizar bloques 3×3 completos.

**¿Cómo afecta la dificultad?**
- **MAYOR dificultad** cuando los bloques están **fuertemente interconectados**.
  - Cambiar algo en un bloque afecta inmediatamente a otros.
  - Requiere pensamiento global constante.
- **MENOR dificultad** cuando los bloques son más **independientes**.
  - Puedes enfocarte en un área sin preocuparte tanto por el resto.
  - Estrategia de "divide y vencerás" más efectiva.

**En la práctica:** alta interconexión significa que "tocar una celda aquí arruina todo lo que hice allá".

### 🕸️ 2. Teoría de grafos (15% del peso total)
*"¿Qué tan conectado está el puzzle?"*

**¿Qué mide?** Las conexiones y relaciones entre todas las celdas del Sudoku.

**¿Cómo afecta la dificultad?**
- **MAYOR dificultad** cuando las celdas vacías están **altamente conectadas**.
  - Muchas celdas vacías se afectan mutuamente.
  - Cada decisión tiene consecuencias en cascada.
  - Difícil encontrar un "punto de entrada" seguro.
- **MENOR dificultad** cuando hay **grupos aislados** de celdas vacías.
  - Puedes resolver secciones independientemente.
  - Menos "efecto dominó" entre decisiones.
  - Múltiples puntos de entrada al puzzle

**En la práctica:** 
- Alta conectividad = "Cada número que pongo cambia todo el puzzle"
- Baja conectividad = "Puedo resolver esta esquina sin afectar el resto"

### 🧮 3. Combinatoria avanzada (15% del peso total)
*"¿Cuántas opciones tienes que considerar?"*

#### 🎲 Principio de inclusión-exclusión
**¿Qué mide?** Cuántos candidatos comparten las celdas relacionadas.

**¿Cómo afecta la dificultad?**
- **MAYOR dificultad** cuando hay **muchos candidatos compartidos**.
  - Múltiples celdas pueden tener los mismos números posibles.
  - Difícil decidir dónde va cada número.
  - Requiere análisis profundo de eliminación.
- **MENOR dificultad** cuando los candidatos son **únicos por área**.
  - Cada celda tiene opciones diferentes y claras.
  - Decisiones más directas y evidentes.

**En la práctica:** muchos candidatos compartidos = "Este 5 puede ir en tres lugares diferentes y no sé cuál elegir".

#### 🔢 Coeficientes binomiales
**¿Qué mide?** La complejidad de elegir entre múltiples candidatos por celda.

**¿Cómo afecta la dificultad?**
- **MAYOR dificultad** cuando las celdas tienen **muchas opciones** (4-9 candidatos).
  - Cada celda requiere análisis extenso.
  - Alto potencial para errores de elección.
  - Necesitas técnicas avanzadas (naked pairs, hidden singles, etc.).
- **MENOR dificultad** cuando las celdas tienen **pocas opciones** (1-3 candidatos).
  - Decisiones más obvias y directas.
  - Menos posibilidad de error.
  - Estrategias básicas son suficientes.

**En la práctica:** muchas opciones = "Esta celda puede ser 2, 4, 6, 7 u 8... ¿por dónde empiezo?"

#### 📈 Entropía combinatorial
**¿Qué mide?** La cantidad de incertidumbre o desorden en la distribución de candidatos por celda en el tablero.

**¿Cómo afecta la dificultad?**
- **MAYOR dificultad** cuando la entropía es **alta**.
  - Los candidatos están distribuidos de forma muy desigual y caótica.
  - El jugador debe analizar muchas combinaciones posibles y el tablero se siente impredecible.
- **MENOR dificultad** cuando la entropía es **baja**.
  - Los candidatos están organizados y el tablero tiene patrones claros.
  - El jugador puede seguir estrategias más directas y predecibles.

**En la práctica:** alta entropía significa que "cada celda parece tener opciones muy diferentes y no hay un patrón claro para avanzar", mientras que baja entropía facilita la resolución por patrones y agrupaciones.

#### 🧩 Espacio de solución (14% del peso)
**¿Qué mide?** El número total de soluciones posibles para el tablero dado.

**¿Cómo afecta la dificultad?**
- **MAYOR dificultad** cuando el espacio de solución es **muy grande**.
  - Hay muchas formas de completar el tablero, lo que puede generar ambigüedad y requerir técnicas avanzadas para descartar soluciones incorrectas.
  - El jugador puede sentirse perdido ante tantas posibilidades.
- **MENOR dificultad** cuando el espacio de solución es **muy pequeño** (idealmente, solo una solución).
  - El camino hacia la solución es más claro y directo.
  - El jugador puede avanzar con mayor seguridad, sabiendo que cada decisión lo acerca a la única solución posible.

**En la práctica:** un espacio de solución grande puede hacer que el puzzle se sienta "abierto" y requiera más análisis, mientras que un espacio pequeño da una sensación de control y progresión lógica.

### ⚖️ Fórmula Final: ¿Cómo se combina todo?

```
total_complexity = (
    number_distribution * 0.15 +      # 15% - Distribución de numeros
    row_permutations * 0.15 +         # 15% - Permutaciones de filas
    col_permutations * 0.15 +         # 15% - Permutaciones de columnas
    block_permutations * 0.11 +       # 11% - Permutaciones de bloques
    graph_complexity * 0.15 +         # 15% - Teoría de grafos
    combinatorial_complexity * 0.15 + # 15% - Combinatoria avanzada
    solution_space * 0.14             # 14% - Espacio de solución
)
```

**¿Por qué estos pesos?**
- **Distribución de números (15%)**: es el primer patrón que percibes y condiciona tu estrategia inicial.
- **Permutaciones de filas (15%) y columnas (15%)**: reflejan la flexibilidad estructural del tablero y la dificultad para reorganizar regiones.
- **Permutaciones de bloques (11%)**: indican el grado de interconexión global y la necesidad de pensar en el tablero como un todo.
- **Teoría de grafos (15%)**: mide la complejidad de las relaciones entre celdas y el efecto dominó de cada decisión.
- **Combinatoria avanzada (15%)**: agrupa la dificultad por candidatos compartidos, coeficientes binomiales y entropía combinatorial, reflejando la cantidad y calidad de opciones por celda.
- **Espacio de solución (14%)**: determina cuán abierto o restringido es el camino hacia la solución, afectando la claridad y el control del jugador.

## Escala de dificultad: ¿Qué significa cada nivel?

### 🟢 Fácil (1-4 puntos)
**Características del puzzle:**
- Números bien distribuidos (cada uno aparece 3-4 veces).
- Clusters agrupados y baja entropía combinatorial.
- Exactamente 30 celdas llenas (51 vacías).
- Patrones que permiten resolución secuencial.
- Baja conectividad y espacio de solución reducido.

**Tu experiencia como jugador:**
- Progreso constante y predecible.
- Decisiones mayormente obvias.
- Raramente te sientes "atascado".
- Técnicas básicas (naked singles, hidden singles) son suficientes.
- Sensación de flujo continuo.

### 🔴 Difícil (5-10 puntos)
**Características del puzzle:**
- Distribución maximizada en dispersión y desconexión.
- Alta entropía combinatorial y candidatos caóticos.
- Celdas llenas estratégicamente aisladas unas de otras.
- Exactamente 30 celdas llenas (51 vacías).
- Patrones que requieren análisis global y pensamiento sistémico.
- Alta conectividad y espacio de solución amplio.

**Tu experiencia como jugador:**
- Requiere análisis profundo y sistemático.
- Muchas decisiones no son obvias.
- Necesitas técnicas avanzadas.
- Frecuentes "callejones sin salida" que requieren backtracking.
- Sensación de resolver un rompecabezas complejo, no solo rellenar números.

---

# REVISIÓN Y RESOLUCIÓN

## Sistema avanzado de verificación y resolución de Sudoku

**Basado en permutaciones y teoría de grafos**

Este módulo implementa la verificación de soluciones propuestas por el usuario y la resolución automática de tableros incompletos, utilizando principios de Matemáticas Discretas. Las principales herramientas teóricas aplicadas son Permutaciones y Coloreo de Grafos.

---

### 🧠 Fundamento Matemático

#### 1. Permutaciones
Cada fila, columna y región 3×3 en un tablero de Sudoku debe contener una permutación del conjunto {1, 2, ..., 9}, es decir, todos los números sin repeticiones. Esta propiedad se verifica en la resolución y validación.

- **Verificación de la solución:** se analiza si las filas, columnas y regiones son permutaciones válidas.
- **Resolución automática:** el algoritmo explora el espacio de permutaciones posibles bajo restricciones locales (vecinos), usando backtracking optimizado.

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
- La función `is_proper_coloring_at(board, row, col, num)` evalúa si un valor asignado a la casilla (row, col) cumple con las restricciones del grafo de Sudoku.

#### 🤖 Resolución Automática
- Emplea backtracking con heurísticas de reducción del espacio de búsqueda basado en vecinos.
- En cada paso se asegura que la asignación cumple con la regla de coloración del grafo.
- Explora las permutaciones válidas en las subestructuras del tablero para hallar una solución coherente.

---

### 📂 Estructura del Código

```python
class SudokuBoard:

    """Otras funciones"""

    def get_neighbors(self, row, col) -> Set[Tuple[int, int]]:
        # Retorna los vecinos según el grafo de restricciones del Sudoku

    def is_proper_coloring_at(self, board, row, col, num) -> bool:
        # Verifica si el valor en la posición (row, col) es válido según sus vecinos

    def solve_backtracking(self) -> bool:
        # Algoritmo de resolución automática y validación por coloración

    def verify_solution(self) -> List[List[bool]]:
        # Verifica que la solución del Sudoku sea correcta

    def solve_current_board(self):
        # Resuelve el Sudoku
        
    """Otras funciones"""
```

---

# Implementación avanzada de permutaciones en el Sudoku: Creación del tablero

## ¿Por qué las permutaciones son clave en la creación de un tablero de Sudoku?

La esencia matemática de un tablero de Sudoku resuelto es la existencia de permutaciones válidas en cada fila, columna y bloque 3x3. Para construir un tablero inicial, el sistema explora el espacio de todas las posibles disposiciones (permutaciones) de los números del 1 al 9, asegurando que se cumplan las restricciones del juego.

## Algoritmo Backtracking y permutaciones

El método más utilizado para crear un tablero válido es el **backtracking**, que explora sistemáticamente las permutaciones posibles:

1. **Selección de celdas vacías:** el algoritmo recorre el tablero buscando la siguiente celda vacía.
2. **Cálculo de candidatos:** para cada celda, se calcula el conjunto de números que pueden ser colocados sin violar las reglas de permutación en su fila, columna y bloque.
3. **Permutación aleatoria:** antes de probar los candidatos, se barajan aleatoriamente para generar variedad en los tableros resultantes.
4. **Colocación y recursión:** se coloca un candidato y se avanza recursivamente a la siguiente celda. Si no hay candidatos válidos, se retrocede (backtrack) y se prueba otra permutación.

Este proceso se repite hasta que el tablero esté completamente lleno y todas las filas, columnas y bloques sean permutaciones válidas del conjunto {1,2,...,9}.

## Variedad y aleatorización

La aleatorización de las permutaciones permite que cada tablero generado sea único. El uso de `random.shuffle()` en los candidatos de cada celda asegura que el proceso de generación no siga siempre el mismo patrón, aumentando la diversidad de puzzles posibles.


### Referencias

[1] R. Saavedra Hernandez, "Sudoku, aspectos matemáticos," TFG, Universidad de La Laguna, 2018. [Online]. Available: https://riull.ull.es/xmlui/bitstream/handle/915/13479/Sudoku,+aspectos+matematicos.pdf?sequence=1