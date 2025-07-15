"""
Configuraciones personalizables para el juego de Sudoku
"""

# Configuración del juego
GAME_CONFIG = {
    'initial_cells': 30,  # Número de celdas iniciales
    'auto_save': True,    # Guardar automáticamente el progreso
    'show_hints': True,   # Mostrar pistas
    'show_timer': True,   # Mostrar cronómetro
    'show_mistakes': True, # Mostrar contador de errores
    'sound_effects': False, # Efectos de sonido (requiere archivos de audio)
    'animations': True,    # Animaciones
}

# Configuración de dificultad personalizada
CUSTOM_DIFFICULTY = {
    'muy_facil': {
        'cells_to_remove': 40,  # Dejar 41 números
        'level_range': (1, 2),
        'label': 'Muy Fácil'
    },
    'personalizado': {
        'cells_to_remove': 55,  # Dejar 26 números
        'level_range': (5, 7),
        'label': 'Personalizado'
    }
}

# Configuración de colores personalizada
CUSTOM_COLORS = {
    'background': (245, 245, 245),
    'board_background': (255, 255, 255),
    'grid_lines': (200, 200, 200),
    'thick_lines': (100, 100, 100),
    'selected_cell': (180, 220, 255),
    'correct_cell': (220, 255, 220),
    'incorrect_cell': (255, 220, 220),
    'initial_numbers': (80, 80, 80),
    'user_numbers': (20, 20, 20),
    'button_normal': (230, 230, 230),
    'button_hover': (220, 220, 220),
    'button_active': (200, 230, 255),
}

# Configuración de fuentes
FONT_CONFIG = {
    'main_font': 'Arial',
    'number_size': 32,
    'button_size': 18,
    'title_size': 40,
    'info_size': 16,
}

# Configuración de la ventana
WINDOW_CONFIG = {
    'resizable': False,
    'fullscreen': False,
    'icon_path': None,  # Ruta al icono de la ventana
    'min_width': 800,
    'min_height': 600,
}

# Configuración de debugging
DEBUG_CONFIG = {
    'show_fps': False,
    'show_coordinates': False,
    'verbose_logging': False,
    'performance_monitor': False,
}
