# Sudoku - Proyecto Final Matemáticas Discretas

Un juego de Sudoku implementado en Python con un sistema avanzado de dificultad basado en conceptos de Matemáticas Discretas.

## Overview

Este proyecto implementa un generador y solucionador de puzzles Sudoku utilizando algoritmos avanzados basados en:

- **Permutaciones**: Análisis de grupos simétricos para evaluar la complejidad estructural
- **Teoría de Grafos**: Modelado del puzzle como grafo de restricciones para medir conectividad
- **Combinatoria**: Aplicación del principio de inclusión-exclusión y coeficientes binomiales para calcular complejidad

El sistema genera puzzles con exactamente 30 números iniciales y clasifica automáticamente la dificultad en dos niveles (Fácil, Difícil) usando métricas matemáticas precisas.

## Características

- Generación automática de puzzles con dificultad controlada
- Sistema de dificultad basado en matemáticas discretas
- Interfaz gráfica con Pygame
- Resolución automática por backtracking
- Verificación de soluciones en tiempo real

## Instalación y Uso

```bash
pip install pygame
python main.py
```

## Controles

- **Clic**: Seleccionar celda
- **1-9**: Ingresar número  
- **DELETE**: Borrar número
- **ESC**: Salir
- **Limpiar**: Limpia todas las celdas editables (mantiene los números iniciales)

## Estructura del Proyecto

```
├── main.py              # Punto de entrada de la aplicación
├── sudoku/
│   ├── __init__.py      # Paquete de sudoku
│   ├── constants.py     # Constantes y configuraciones
│   ├── board.py         # Lógica del tablero y algoritmos
│   ├── gui.py           # Interfaz gráfica de usuario
│   └── game.py          # Clase principal del juego
└── README.md           # Este archivo
```

## Algoritmos Implementados

### Generación de Puzzles
1. **Tablero completo**: Se genera un tablero de Sudoku válido completo
2. **Remoción de números**: Se remueven números aleatoriamente hasta dejar exactamente 30
3. **Validación**: Se asegura que el puzzle tenga una solución única

### Resolución por Backtracking
1. **Buscar celda vacía**: Encuentra la primera celda vacía (valor 0)
2. **Probar números**: Prueba números del 1 al 9
3. **Validar**: Verifica si el número es válido según las reglas del Sudoku
4. **Recursión**: Si es válido, continúa con la siguiente celda
5. **Retroceso**: Si no encuentra solución, regresa y prueba otro número

### Validación de Reglas
- **Fila**: No puede haber números repetidos en la misma fila
- **Columna**: No puede haber números repetidos en la misma columna
- **Cuadrado 3x3**: No puede haber números repetidos en el mismo cuadrado 3x3

## Niveles de Dificultad

El sistema asigna automáticamente un nivel de dificultad del 1 al 10:
- **Fácil**: Niveles 1-3
- **Difícil**: Niveles 8-10

## Características Técnicas

- **Ventana maximizada**: La aplicación se ejecuta en ventana grande pero no pantalla completa
- **Interfaz lateral organizada**: Tablero fijo a la izquierda, panel de información estructurado a la derecha
- **Distribución sin superposiciones**: Textos y botones organizados en secciones bien definidas
- **Separadores visuales**: Líneas divisorias que delimitan cada sección de información
- **Etiquetas descriptivas**: Cada grupo de botones tiene su etiqueta correspondiente
- **Colores diferenciados**: Los números iniciales aparecen en gris oscuro y no son editables
- **Feedback visual**: Las celdas se resaltan al seleccionarlas
- **Información de dificultad**: Muestra claramente el nivel actual (1-10) y los rangos por dificultad
- **Validación en tiempo real**: La verificación muestra errores inmediatamente
- **Persistencia de estado**: El tablero mantiene su estado durante toda la sesión
- **Navegación fácil**: Tecla ESC para salir, ventana redimensionable

## Contribuciones

Este proyecto fue desarrollado como parte del curso de Matemáticas Discretas, implementando conceptos de:
- Algoritmos de backtracking
- Validación de restricciones
- Generación de permutaciones
- Estructuras de datos matriciales
