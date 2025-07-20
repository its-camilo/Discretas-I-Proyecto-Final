# Sudoku - Proyecto Final Matemáticas Discretas

Un juego de Sudoku implementado en Python con un sistema avanzado de dificultad basado en conceptos de Matemáticas Discretas.

## Overview

Este proyecto implementa un generador y solucionador de puzzles Sudoku utilizando algoritmos avanzados basados en:

- **Permutaciones**: análisis de grupos simétricos para evaluar la complejidad estructural.
- **Teoría de Grafos**: modelado del puzzle como grafo de restricciones para medir conectividad.
- **Combinatoria**: aplicación del principio de inclusión-exclusión y coeficientes binomiales para calcular complejidad.

El sistema genera puzzles con exactamente 30 números iniciales y clasifica automáticamente la dificultad en dos niveles (Fácil, Difícil) usando métricas matemáticas precisas.

## Características

- Generación automática de puzzles con dificultad controlada.
- Sistema de dificultad basado en matemáticas discretas.
- Interfaz gráfica con Pygame.
- Resolución automática por backtracking.
- Verificación de soluciones en tiempo real.

## Instalación y uso

```bash
pip install pygame
python main.py
```

## Controles

- **Clic**: seleccionar celda.
- **1-9**: ingresar número.
- **DELETE**: borrar número.
- **ESC**: salir.
- **Limpiar**: limpia todas las celdas editables (mantiene los números iniciales).

## Estructura del Proyecto

```
├── main.py                     # Punto de entrada de la aplicación
├── sudoku/
│   ├── __init__.py             # Paquete de sudoku
│   ├── constants.py            # Constantes y configuraciones
│   ├── board.py                # Lógica del tablero y algoritmos
│   ├── gui.py                  # Interfaz gráfica de usuario
│   ├── game.py                 # Clase principal del juego
│   └── README.md               # Archivo con especificaciones de la implementación
└── README.md                   # Este archivo
```

## Niveles de Dificultad

El sistema asigna automáticamente un nivel de dificultad del 1 al 10:
- **Fácil**: niveles 1-5.
- **Difícil**: niveles 6-10.

## Contribuciones

Este proyecto fue desarrollado como parte del curso de Matemáticas Discretas I, implementando conceptos de:
- Algoritmos de backtracking.
- Validación de restricciones.
- Generación de permutaciones.
- Estructuras de datos matriciales.
- Teoria de Grafos.
