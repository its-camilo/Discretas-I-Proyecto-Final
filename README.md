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
- **Fácil**: niveles 1-3.
- **Difícil**: niveles 8-10.

## Características Técnicas

- **Ventana maximizada**: la aplicación se ejecuta en ventana grande pero no pantalla completa.
- **Interfaz lateral organizada**: tablero fijo a la izquierda, panel de información estructurado a la derecha.
- **Distribución sin superposiciones**: textos y botones organizados en secciones bien definidas.
- **Separadores visuales**: líneas divisorias que delimitan cada sección de información.
- **Etiquetas descriptivas**: cada grupo de botones tiene su etiqueta correspondiente.
- **Colores diferenciados**: los números iniciales aparecen en gris oscuro y no son editables.
- **Feedback visual**: las celdas se resaltan al seleccionarlas.
- **Información de dificultad**: muestra claramente el nivel actual (1-10) y los rangos por dificultad.
- **Validación en tiempo real**: la verificación muestra errores inmediatamente.
- **Persistencia de estado**: el tablero mantiene su estado durante toda la sesión.
- **Navegación fácil**: tecla ESC para salir, ventana redimensionable.

## Contribuciones

Este proyecto fue desarrollado como parte del curso de Matemáticas Discretas I, implementando conceptos de:
- Algoritmos de backtracking.
- Validación de restricciones.
- Generación de permutaciones.
- Estructuras de datos matriciales.
- Teoria de Grafos.
