"""
Interfaz gráfica de usuario para el juego de Sudoku
"""

import pygame
from typing import List, Tuple, Optional
from .constants import *
from .board import SudokuBoard

class SudokuGUI:
    """Maneja la interfaz gráfica del juego"""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.board = SudokuBoard()
        self.selected_cell = None
        self.verification_results = None
        self.current_difficulty = 'medio'
        
        # Inicializar fuentes
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.info_font = pygame.font.Font(None, INFO_FONT_SIZE)
        
        # Crear botones
        self.buttons = self.create_buttons()
        
        # Generar puzzle inicial
        self.board.generate_puzzle(self.current_difficulty)
    
    def create_buttons(self) -> List[dict]:
        """Crea los botones de la interfaz en el panel lateral"""
        buttons = []
        
        # Calcular posición inicial centrada respecto al tablero
        start_y = BOARD_Y + (BOARD_HEIGHT - 7 * (BUTTON_HEIGHT + 10)) // 2
        x_pos = SIDEBAR_X
        
        # Botones de dificultad
        difficulties = [('facil', 'Fácil'), ('medio', 'Medio'), ('dificil', 'Difícil')]
        
        for i, (diff, label) in enumerate(difficulties):
            button = {
                'rect': pygame.Rect(x_pos, start_y + i * (BUTTON_HEIGHT + 15), 
                                  BUTTON_WIDTH, BUTTON_HEIGHT),
                'text': label,
                'action': f'difficulty_{diff}',
                'color': LIGHT_BLUE if diff == self.current_difficulty else LIGHT_GRAY
            }
            buttons.append(button)
        
        # Botón de nuevo juego
        nuevo_button = {
            'rect': pygame.Rect(x_pos, start_y + 3 * (BUTTON_HEIGHT + 15) + 20, 
                              BUTTON_WIDTH, BUTTON_HEIGHT),
            'text': 'Nuevo Juego',
            'action': 'nuevo',
            'color': LIGHT_GRAY
        }
        buttons.append(nuevo_button)
        
        # Botones de acción
        actions_start_y = start_y + 4 * (BUTTON_HEIGHT + 15) + 40
        actions = [('resolver', 'Resolver'), ('verificar', 'Verificar'), ('limpiar', 'Limpiar')]
        
        for i, (action, label) in enumerate(actions):
            button = {
                'rect': pygame.Rect(x_pos, actions_start_y + i * (BUTTON_HEIGHT + 15), 
                                  BUTTON_WIDTH, BUTTON_HEIGHT),
                'text': label,
                'action': action,
                'color': LIGHT_GRAY
            }
            buttons.append(button)
        
        return buttons
    
    def handle_click(self, pos: Tuple[int, int]) -> Optional[str]:
        """Maneja los clics del mouse"""
        
        # Verificar clics en botones
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                return button['action']
        
        # Verificar clics en el tablero (posición fija)
        board_click_x, board_click_y = pos[0] - BOARD_X, pos[1] - BOARD_Y
        
        if 0 <= board_click_x < BOARD_WIDTH and 0 <= board_click_y < BOARD_HEIGHT:
            col = board_click_x // CELL_SIZE
            row = board_click_y // CELL_SIZE
            
            if 0 <= row < 9 and 0 <= col < 9:
                if self.board.is_cell_editable(row, col):
                    self.selected_cell = (row, col)
                else:
                    self.selected_cell = None
        
        return None
    
    def handle_key(self, key: int) -> bool:
        """Maneja las teclas presionadas"""
        if self.selected_cell is None:
            return False
        
        row, col = self.selected_cell
        
        # Números del 1 al 9
        if pygame.K_1 <= key <= pygame.K_9:
            number = key - pygame.K_0
            self.board.set_cell_value(row, col, number)
            self.verification_results = None  # Limpiar resultados de verificación
            return True
        
        # Tecla de borrar (Delete o Backspace)
        elif key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
            self.board.set_cell_value(row, col, 0)
            self.verification_results = None  # Limpiar resultados de verificación
            return True
        
        return False
    
    def handle_button_action(self, action: str):
        """Maneja las acciones de los botones"""
        if action.startswith('difficulty_'):
            difficulty = action.split('_')[1]
            self.current_difficulty = difficulty
            self.board.generate_puzzle(difficulty)
            self.verification_results = None
            self.selected_cell = None
            
            # Recrear botones para actualizar colores
            self.buttons = self.create_buttons()
            
            # Actualizar colores de botones
            for button in self.buttons:
                if button['action'].startswith('difficulty_'):
                    diff = button['action'].split('_')[1]
                    button['color'] = LIGHT_BLUE if diff == difficulty else LIGHT_GRAY
        
        elif action == 'nuevo':
            self.board.generate_puzzle(self.current_difficulty)
            self.verification_results = None
            self.selected_cell = None
        
        elif action == 'resolver':
            self.board.solve_current_board()
            self.verification_results = None
            self.selected_cell = None
        
        elif action == 'verificar':
            self.verification_results = self.board.verify_solution()
            self.selected_cell = None
        
        elif action == 'limpiar':
            self.board.clear_editable_cells()
            self.verification_results = None
            self.selected_cell = None
    
    def draw_board(self):
        """Dibuja el tablero de Sudoku en posición fija"""
        
        # Fondo del tablero
        board_rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, board_rect)
        pygame.draw.rect(self.screen, BLACK, board_rect, 2)
        
        # Dibujar celdas
        for row in range(9):
            for col in range(9):
                x = BOARD_X + col * CELL_SIZE
                y = BOARD_Y + row * CELL_SIZE
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                # Color de fondo de la celda
                cell_color = WHITE
                
                # Verificar si la celda está seleccionada
                if self.selected_cell == (row, col):
                    cell_color = LIGHT_BLUE
                
                # Verificar resultados de verificación
                if self.verification_results is not None:
                    if self.verification_results[row][col]:
                        cell_color = LIGHT_GREEN
                    else:
                        cell_color = LIGHT_RED
                
                pygame.draw.rect(self.screen, cell_color, cell_rect)
                
                # Bordes de la celda
                border_width = 1
                if row % 3 == 0:
                    pygame.draw.line(self.screen, BLACK, (x, y), (x + CELL_SIZE, y), 2)
                if col % 3 == 0:
                    pygame.draw.line(self.screen, BLACK, (x, y), (x, y + CELL_SIZE), 2)
                if row == 8:
                    pygame.draw.line(self.screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
                if col == 8:
                    pygame.draw.line(self.screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
                
                pygame.draw.rect(self.screen, GRAY, cell_rect, border_width)
                
                # Número en la celda
                value = self.board.get_cell_value(row, col)
                if value != 0:
                    # Color del texto
                    text_color = BLACK
                    if not self.board.is_cell_editable(row, col):
                        text_color = DARK_GRAY  # Números iniciales en gris oscuro
                    
                    text = self.font.render(str(value), True, text_color)
                    text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    self.screen.blit(text, text_rect)
        
        # Líneas gruesas para separar los cuadrados 3x3
        for i in range(1, 3):
            # Líneas verticales
            x = BOARD_X + i * 3 * CELL_SIZE
            pygame.draw.line(self.screen, BLACK, (x, BOARD_Y), (x, BOARD_Y + BOARD_HEIGHT), 3)
            
            # Líneas horizontales
            y = BOARD_Y + i * 3 * CELL_SIZE
            pygame.draw.line(self.screen, BLACK, (BOARD_X, y), (BOARD_X + BOARD_WIDTH, y), 3)
    
    def draw_buttons(self):
        """Dibuja los botones de la interfaz"""
        for button in self.buttons:
            pygame.draw.rect(self.screen, button['color'], button['rect'])
            pygame.draw.rect(self.screen, BLACK, button['rect'], 2)
            
            text = self.button_font.render(button['text'], True, BLACK)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
    
    def draw_info(self):
        """Dibuja información en el panel lateral"""
        
        # Título principal - centrado respecto a toda la ventana
        title = self.title_font.render("SUDOKU", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 40))
        self.screen.blit(title, title_rect)
    
    def draw(self):
        """Dibuja toda la interfaz"""
        self.screen.fill(WHITE)
        
        self.draw_board()
        self.draw_buttons()
        self.draw_info()
