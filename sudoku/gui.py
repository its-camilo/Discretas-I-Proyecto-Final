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
        
        # Botones de dificultad en el panel lateral
        y_pos = BOARD_Y + 80  # Ajustado para más espacio
        x_pos = SIDEBAR_X
        
        difficulties = [('facil', 'Fácil'), ('medio', 'Medio'), ('dificil', 'Difícil')]
        
        for i, (diff, label) in enumerate(difficulties):
            button = {
                'rect': pygame.Rect(x_pos, y_pos + i * (BUTTON_HEIGHT + 10), 
                                  BUTTON_WIDTH, BUTTON_HEIGHT),
                'text': label,
                'action': f'difficulty_{diff}',
                'color': LIGHT_BLUE if diff == self.current_difficulty else LIGHT_GRAY
            }
            buttons.append(button)
        
        # Botón para alternar sistema de dificultad
        toggle_button = {
            'rect': pygame.Rect(x_pos, y_pos + 3 * (BUTTON_HEIGHT + 10) + 10, 
                              BUTTON_WIDTH, BUTTON_HEIGHT),
            'text': 'Sist. Avanzado' if self.board.use_advanced_difficulty else 'Sist. Básico',
            'action': 'toggle_difficulty_system',
            'color': LIGHT_GREEN if self.board.use_advanced_difficulty else LIGHT_GRAY
        }
        buttons.append(toggle_button)
        
        # Botones de acción en el panel lateral
        y_pos = BOARD_Y + 300  # Ajustado para más espacio
        actions = [('nuevo', 'Nuevo Juego'), ('resolver', 'Resolver'), 
                  ('verificar', 'Verificar'), ('limpiar', 'Limpiar')]
        
        for i, (action, label) in enumerate(actions):
            button = {
                'rect': pygame.Rect(x_pos, y_pos + i * (BUTTON_HEIGHT + 10), 
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
        
        elif action == 'toggle_difficulty_system':
            # Alternar sistema de dificultad
            is_advanced = self.board.toggle_difficulty_system()
            
            # Generar nuevo puzzle con el sistema actualizado
            self.board.generate_puzzle(self.current_difficulty)
            self.verification_results = None
            self.selected_cell = None
            
            # Recrear botones para actualizar el texto del botón toggle
            self.buttons = self.create_buttons()
        
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
        
        # Título principal
        title = self.title_font.render("SUDOKU", True, BLACK)
        title_rect = title.get_rect(center=(SIDEBAR_X + SIDEBAR_WIDTH // 2, 40))
        self.screen.blit(title, title_rect)
        
        # Información de dificultad actual con métricas avanzadas
        current_level = self.board.get_difficulty_level()
        metrics = self.board.get_difficulty_metrics()
        
        if self.board.use_advanced_difficulty and 'difficulty_breakdown' in metrics:
            difficulty_text = f"Dificultad Final: {current_level}/10"
            breakdown = metrics['difficulty_breakdown']
            perm_text = f"Permutaciones: {breakdown['permutations']}"
            density_text = f"Densidad: {breakdown['density']}"
        else:
            difficulty_text = f"Dificultad: {current_level}/10"
            perm_text = "Sistema básico activo"
            density_text = ""
        
        # Mostrar dificultad principal
        difficulty_surface = self.info_font.render(difficulty_text, True, BLACK)
        difficulty_rect = difficulty_surface.get_rect(x=SIDEBAR_X, y=BOARD_Y + 10)
        self.screen.blit(difficulty_surface, difficulty_rect)
        
        # Mostrar métricas detalladas si está el sistema avanzado
        if self.board.use_advanced_difficulty:
            perm_surface = pygame.font.Font(None, 16).render(perm_text, True, DARK_GRAY)
            perm_rect = perm_surface.get_rect(x=SIDEBAR_X, y=BOARD_Y + 30)
            self.screen.blit(perm_surface, perm_rect)
            
            if density_text:
                density_surface = pygame.font.Font(None, 16).render(density_text, True, DARK_GRAY)
                density_rect = density_surface.get_rect(x=SIDEBAR_X, y=BOARD_Y + 45)
                self.screen.blit(density_surface, density_rect)
        else:
            basic_surface = pygame.font.Font(None, 16).render(perm_text, True, DARK_GRAY)
            basic_rect = basic_surface.get_rect(x=SIDEBAR_X, y=BOARD_Y + 30)
            self.screen.blit(basic_surface, basic_rect)
        
        # Etiqueta para botones de dificultad
        diff_label = self.info_font.render("Seleccionar Dificultad:", True, DARK_GRAY)
        diff_label_rect = diff_label.get_rect(x=SIDEBAR_X, y=BOARD_Y + 60)
        self.screen.blit(diff_label, diff_label_rect)
        
        # Explicación de rangos de dificultad (a la derecha de los botones)
        ranges_x = SIDEBAR_X + BUTTON_WIDTH + 15
        ranges_y = BOARD_Y + 80
        ranges_info = [
            "Rangos:",
            "Fácil: 1-3",
            "Medio: 4-6", 
            "Difícil: 7-10"
        ]
        
        for i, info in enumerate(ranges_info):
            color = DARK_GRAY if i == 0 else BLACK
            font_size = INFO_FONT_SIZE - 2 if i == 0 else INFO_FONT_SIZE - 4
            font = pygame.font.Font(None, font_size)
            text = font.render(info, True, color)
            text_rect = text.get_rect(x=ranges_x, y=ranges_y + i * 18)
            self.screen.blit(text, text_rect)
        
        # Información del sistema de dificultad
        if self.board.use_advanced_difficulty:
            system_info = [
                "Sistema Avanzado:",
                "• Analiza permutaciones",
                "• Evalúa densidad de celdas",
                "• Celdas disjuntas = más difícil"
            ]
        else:
            system_info = [
                "Sistema Básico:",
                "• Remoción aleatoria",
                "• Dificultad por cantidad"
            ]
        
        system_y = ranges_y + len(ranges_info) * 18 + 10
        for i, info in enumerate(system_info):
            color = DARK_GRAY if i == 0 else BLACK
            font_size = INFO_FONT_SIZE - 4 if i == 0 else 12
            font = pygame.font.Font(None, font_size)
            text = font.render(info, True, color)
            text_rect = text.get_rect(x=ranges_x, y=system_y + i * 16)
            self.screen.blit(text, text_rect)
        
        # Etiqueta para botones de acción
        actions_label_y = BOARD_Y + 280
        actions_label = self.info_font.render("Controles del Juego:", True, DARK_GRAY)
        actions_label_rect = actions_label.get_rect(x=SIDEBAR_X, y=actions_label_y)
        self.screen.blit(actions_label, actions_label_rect)
        
        # Instrucciones de uso (debajo de los botones de acción)
        instructions_y = BOARD_Y + 520
        instructions = [
            "Instrucciones de Uso:",
            "• Clic en celda vacía para seleccionar",
            "• Teclas 1-9 para ingresar números",
            "• DELETE/BACKSPACE para borrar",
            "• ESC para salir del juego"
        ]
        
        for i, instruction in enumerate(instructions):
            color = DARK_GRAY if i == 0 else BLACK
            font_size = INFO_FONT_SIZE if i == 0 else 14
            font = pygame.font.Font(None, font_size)
            text = font.render(instruction, True, color)
            text_rect = text.get_rect(x=SIDEBAR_X, y=instructions_y + i * 20)
            self.screen.blit(text, text_rect)
        
        # Información de reglas del juego
        rules_y = instructions_y + len(instructions) * 20 + 25
        rules_info = [
            "Reglas del Sudoku:",
            "• Números grises son fijos (no editables)",
            "• No repetir números en la misma fila",
            "• No repetir números en la misma columna",
            "• No repetir números en cuadrado 3x3",
            "• Verificar: Verde=Correcto, Rojo=Error"
        ]
        
        for i, rule in enumerate(rules_info):
            color = DARK_GRAY if i == 0 else BLACK
            font_size = INFO_FONT_SIZE if i == 0 else 12
            font = pygame.font.Font(None, font_size)
            text = font.render(rule, True, color)
            text_rect = text.get_rect(x=SIDEBAR_X, y=rules_y + i * 16)
            self.screen.blit(text, text_rect)
    
    def draw(self):
        """Dibuja toda la interfaz"""
        self.screen.fill(WHITE)
        
        # Dibujar línea separadora entre tablero y panel lateral
        separator_x = BOARD_X + BOARD_WIDTH + 25
        pygame.draw.line(self.screen, LIGHT_GRAY, 
                        (separator_x, 20), 
                        (separator_x, self.screen.get_height() - 20), 2)
        
        # Dibujar fondo del panel lateral
        sidebar_rect = pygame.Rect(SIDEBAR_X - 20, 20, 
                                  SIDEBAR_WIDTH + 40, 
                                  self.screen.get_height() - 40)
        pygame.draw.rect(self.screen, (250, 250, 250), sidebar_rect)
        pygame.draw.rect(self.screen, LIGHT_GRAY, sidebar_rect, 1)
        
        # Líneas divisorias horizontales en el panel lateral
        line_y_positions = [
            BOARD_Y + 185,  # Después de los botones de dificultad
            BOARD_Y + 405,  # Después de los botones de acción
            BOARD_Y + 530   # Después de las instrucciones
        ]
        
        for y_pos in line_y_positions:
            pygame.draw.line(self.screen, LIGHT_GRAY, 
                           (SIDEBAR_X, y_pos), 
                           (SIDEBAR_X + SIDEBAR_WIDTH - 20, y_pos), 1)
        
        self.draw_board()
        self.draw_buttons()
        self.draw_info()
