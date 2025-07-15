"""
Clase principal del juego de Sudoku
"""

import pygame
import sys
from .constants import *
from .gui import SudokuGUI

class SudokuGame:
    """Clase principal que maneja el juego de Sudoku"""
    
    def __init__(self):
        """Inicializa el juego"""
        pygame.init()
        
        # Configurar la ventana
        if MAXIMIZED:
            # Obtener el tamaño de la pantalla
            info = pygame.display.Info()
            screen_width = info.current_w - 100  # Dejar espacio para la barra de tareas
            screen_height = info.current_h - 100
            
            # Crear ventana grande pero no pantalla completa
            self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        pygame.display.set_caption("Sudoku - Proyecto Final Matemáticas Discretas")
        
        # Configurar el reloj
        self.clock = pygame.time.Clock()
        
        # Inicializar la GUI
        self.gui = SudokuGUI(self.screen)
        
        # Estado del juego
        self.running = True
    
    def handle_events(self):
        """Maneja los eventos del juego"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                else:
                    self.gui.handle_key(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    action = self.gui.handle_click(event.pos)
                    if action:
                        self.gui.handle_button_action(action)
    
    def update(self):
        """Actualiza el estado del juego"""
        pass  # Por ahora no hay lógica de actualización adicional
    
    def draw(self):
        """Dibuja el juego"""
        self.gui.draw()
        pygame.display.flip()
    
    def run(self):
        """Bucle principal del juego"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
