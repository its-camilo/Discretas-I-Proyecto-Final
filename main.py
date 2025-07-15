#!/usr/bin/env python3
"""
Punto de entrada principal para el juego de Sudoku
"""

import pygame
import sys
from sudoku.game import SudokuGame

def main():
    """Función principal que inicializa y ejecuta el juego"""
    pygame.init()
    
    try:
        game = SudokuGame()
        game.run()
    except Exception as e:
        print(f"Error al ejecutar el juego: {e}")
        sys.exit(1)
    finally:
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()
