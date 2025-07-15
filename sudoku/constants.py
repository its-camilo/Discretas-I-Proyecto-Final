"""
Constantes y configuraciones para el juego de Sudoku
"""

import pygame

# Configuración de la ventana
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60
MAXIMIZED = True
FULLSCREEN = False

# Configuración del tablero
BOARD_SIZE = 9
CELL_SIZE = 60
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE
BOARD_X = 100  # Posición fija más a la izquierda
BOARD_Y = 100

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_RED = (255, 200, 200)
LIGHT_GREEN = (200, 255, 200)

# Configuración de fuentes
FONT_SIZE = 36
BUTTON_FONT_SIZE = 24
TITLE_FONT_SIZE = 48
INFO_FONT_SIZE = 20

# Configuración de botones
BUTTON_WIDTH = 140
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 15

# Configuración de la interfaz lateral
SIDEBAR_X = BOARD_X + BOARD_WIDTH + 50  # Posición del panel lateral
SIDEBAR_WIDTH = 450  # Aumentado para dar más espacio
BUTTON_SPACING = 20

# Número de celdas iniciales
INITIAL_CELLS = 30

# Configuración de dificultad
DIFFICULTY_LEVELS = {
    'facil': {'range': (1, 3), 'label': 'Fácil'},
    'medio': {'range': (4, 6), 'label': 'Medio'},
    'dificil': {'range': (7, 10), 'label': 'Difícil'}
}
