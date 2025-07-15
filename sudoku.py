import random
from tkinter import *
from tkinter import messagebox

# --- 1. CLASE SUDOKU MODEL (Lógica del Sudoku) ---
class SudokuModel:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution_board = [[0 for _ in range(9)] for _ in range(9)]
        self.initial_board = [[0 for _ in range(9)] for _ in range(9)]

    def is_valid(self, row, col, num):
        """Verifica si 'num' es válido en la posición (row, col) según las reglas del Sudoku."""
        # Verificar fila
        for x in range(9):
            if self.board[row][x] == num and col != x:
                return False

        # Verificar columna
        for x in range(9):
            if self.board[x][col] == num and row != x:
                return False

        # Verificar caja 3x3
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_col] == num and (i + start_row != row or j + start_col != col):
                    return False
        return True

    def find_empty(self):
        """Encuentra la próxima celda vacía (representada por 0)."""
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return (r, c)
        return None # No hay celdas vacías, el tablero está lleno

    def solve(self):
        """
        Implementa el algoritmo de backtracking para resolver el Sudoku.
        Retorna True si se encuentra una solución, False de lo contrario.
        """
        find = self.find_empty()
        if not find:
            return True # No hay celdas vacías, el Sudoku está resuelto
        else:
            row, col = find

        for num in range(1, 10): # Prueba números del 1 al 9
            if self.is_valid(row, col, num):
                self.board[row][col] = num

                if self.solve(): # Llamada recursiva
                    return True

                self.board[row][col] = 0 # Backtrack: si no funciona, resetear la celda

        return False # No se encontró un número válido para esta celda

    def fill_board_initial(self):
        """
        Genera un Sudoku completamente lleno (válido) para luego quitar números.
        Usa backtracking para asegurar un tablero válido.
        """
        find = self.find_empty()
        if not find:
            return True # Tablero lleno
        else:
            row, col = find

        nums = list(range(1, 10))
        random.shuffle(nums) # Aleatorizar el orden para generar diferentes Sudokus

        for num in nums:
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_board_initial():
                    return True
                self.board[row][col] = 0 # Backtrack
        return False

    def generate_sudoku(self, difficulty="medium"):
        """
        Genera un nuevo Sudoku.
        1. Crea un tablero completo.
        2. Quita números para crear el puzzle.
        3. Almacena la solución.
        """
        self.board = [[0 for _ in range(9)] for _ in range(9)] # Resetear tablero
        self.fill_board_initial() # Llenar completamente el tablero
        
        # Guardar la solución antes de quitar números
        for r in range(9):
            for c in range(9):
                self.solution_board[r][c] = self.board[r][c]

        # Quitar números para crear el puzzle
        cells_to_remove = 0
        if difficulty == "easy":
            cells_to_remove = 35 # Aproximado
        elif difficulty == "medium":
            cells_to_remove = 45
        elif difficulty == "hard":
            cells_to_remove = 55 # Requiere más lógica para asegurar unicidad

        removed_count = 0
        while removed_count < cells_to_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            if self.board[row][col] != 0:
                original_value = self.board[row][col]
                self.board[row][col] = 0 # Intentar quitar el número

                # Opcional pero crucial: Verificar unicidad de la solución
                # Esto es la parte más compleja de la generación de Sudokus de calidad
                # Una forma simple pero no infalible es intentar resolverlo y ver si se encuentra una solución
                # Para un control estricto de la unicidad, se necesitaría un solucionador que cuente soluciones
                temp_board_copy = [row[:] for row in self.board] # Copia del tablero
                temp_model = SudokuModel()
                temp_model.board = temp_board_copy
                
                # Para simplificar, si el Sudoku generado tiene múltiples soluciones,
                # para este proyecto, podrías no preocuparte por la unicidad en esta primera fase.
                # Una forma más robusta sería:
                # count_solutions(temp_model.board) == 1
                
                # Por ahora, simplemente quitamos el número si la resolución es posible
                if temp_model.solve(): # Si es resoluble, lo dejamos quitado
                     removed_count += 1
                else: # Si no es resoluble, restauramos
                    self.board[row][col] = original_value
        
        # Guardar el tablero inicial con los números quitados
        for r in range(9):
            for c in range(9):
                self.initial_board[r][c] = self.board[r][c]


# --- 2. CLASE SUDOKU GUI (Interfaz Gráfica) ---
class SudokuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku")

        self.model = SudokuModel()
        self.cells = {} # Para almacenar los objetos Entry de Tkinter

        self.create_widgets()
        self.generate_new_sudoku()

    def create_widgets(self):
        # Frame principal para el tablero
        self.board_frame = Frame(self.master, bg="grey", bd=5, relief=RIDGE)
        self.board_frame.pack(pady=10)

        # Crear las celdas del tablero
        for r in range(9):
            for c in range(9):
                cell_color = "light grey" if (r // 3 + c // 3) % 2 == 0 else "white"
                
                entry = Entry(self.board_frame, width=3, font=("Arial", 24),
                              justify="center", bd=1, relief=SOLID,
                              bg=cell_color)
                entry.grid(row=r, column=c, padx=1, pady=1)
                self.cells[(r, c)] = entry
                # Validar la entrada del usuario a solo números del 1-9 o vacío
                vcmd = (self.master.register(self.validate_input), '%P')
                entry.config(validate="key", validatecommand=vcmd)
                entry.bind("<FocusOut>", lambda event, r=r, c=c: self.check_cell_on_focus_out(r, c))

        # Frame para los botones
        self.button_frame = Frame(self.master)
        self.button_frame.pack(pady=10)

        self.solve_btn = Button(self.button_frame, text="Resolver", command=self.solve_sudoku)
        self.solve_btn.pack(side=LEFT, padx=5)

        self.new_game_btn = Button(self.button_frame, text="Nuevo Juego (Fácil)", command=lambda: self.generate_new_sudoku("easy"))
        self.new_game_btn.pack(side=LEFT, padx=5)
        
        self.new_game_medium_btn = Button(self.button_frame, text="Nuevo Juego (Medio)", command=lambda: self.generate_new_sudoku("medium"))
        self.new_game_medium_btn.pack(side=LEFT, padx=5)
        
        self.new_game_hard_btn = Button(self.button_frame, text="Nuevo Juego (Difícil)", command=lambda: self.generate_new_sudoku("hard"))
        self.new_game_hard_btn.pack(side=LEFT, padx=5)


        self.reset_btn = Button(self.button_frame, text="Reiniciar", command=self.reset_board)
        self.reset_btn.pack(side=LEFT, padx=5)

        self.check_btn = Button(self.button_frame, text="Verificar", command=self.check_solution)
        self.check_btn.pack(side=LEFT, padx=5)

    def validate_input(self, new_value):
        """Valida que la entrada sea un número del 1 al 9 o una cadena vacía."""
        if new_value == "":
            return True
        try:
            val = int(new_value)
            if 1 <= val <= 9:
                return True
            else:
                return False
        except ValueError:
            return False

    def update_board_gui(self):
        """Actualiza la interfaz gráfica con el estado actual del tablero del modelo."""
        for r in range(9):
            for c in range(9):
                value = self.model.board[r][c]
                entry = self.cells[(r, c)]
                entry.delete(0, END)
                if value != 0:
                    entry.insert(0, str(value))
                    # Si es un número inicial, hacerlo de solo lectura
                    if self.model.initial_board[r][c] != 0:
                        entry.config(state='readonly', fg='blue')
                    else:
                        entry.config(state='normal', fg='black')
                else:
                    entry.config(state='normal', fg='black') # Asegurarse de que las celdas vacías sean editables

    def get_board_from_gui(self):
        """Carga el estado actual del tablero de la GUI al modelo."""
        for r in range(9):
            for c in range(9):
                value = self.cells[(r, c)].get()
                if value == "":
                    self.model.board[r][c] = 0
                else:
                    try:
                        self.model.board[r][c] = int(value)
                    except ValueError:
                        # Si el usuario ingresó algo inválido, lo tratamos como 0 para la lógica.
                        # La validación de entrada debería prevenir esto.
                        self.model.board[r][c] = 0

    def generate_new_sudoku(self, difficulty="medium"):
        """Genera un nuevo Sudoku y lo muestra en la GUI."""
        self.model.generate_sudoku(difficulty)
        self.update_board_gui()
        messagebox.showinfo("Sudoku", f"¡Nuevo Sudoku Generado ({difficulty.capitalize()})!")

    def solve_sudoku(self):
        """Resuelve el Sudoku actual en la GUI y muestra la solución."""
        self.get_board_from_gui() # Asegurarse de que el modelo tenga el estado actual de la GUI
        
        # Para resolver, usamos una copia del initial_board para que los números originales queden fijos
        # y solo se llenen los vacíos.
        # Una forma más robusta es pasar el initial_board al solucionador.
        # Por simplicidad, si el usuario ha modificado el tablero, el solucionador intentará resolverlo
        # desde el estado actual. Si solo quiere la solución del generado, debe usar "Reiniciar" primero.
        
        # Para este proyecto, usaremos la solution_board que ya se generó para la solución.
        for r in range(9):
            for c in range(9):
                if self.model.initial_board[r][c] == 0: # Solo llenamos celdas que estaban vacías inicialmente
                    self.cells[(r, c)].delete(0, END)
                    self.cells[(r, c)].insert(0, str(self.model.solution_board[r][c]))
                    self.cells[(r,c)].config(fg='green') # Colorear la solución
                else:
                    self.cells[(r,c)].config(fg='blue') # Asegurar que los números iniciales sigan siendo azules


    def reset_board(self):
        """Reinicia el tablero a su estado inicial (después de la generación)."""
        for r in range(9):
            for c in range(9):
                self.model.board[r][c] = self.model.initial_board[r][c]
        self.update_board_gui()
        messagebox.showinfo("Sudoku", "Tablero Reiniciado.")
        
    def check_solution(self):
        """Verifica si la solución ingresada por el usuario es correcta."""
        self.get_board_from_gui() # Obtener el estado actual del usuario
        
        is_correct = True
        
        # Verificar cada celda contra la solución conocida
        for r in range(9):
            for c in range(9):
                user_val = self.model.board[r][c]
                correct_val = self.model.solution_board[r][c]
                
                if user_val != correct_val:
                    is_correct = False
                    # Opcional: Resaltar celdas incorrectas
                    self.cells[(r,c)].config(bg="red")
                elif self.model.initial_board[r][c] == 0: # Si la celda fue llenada por el usuario y es correcta
                    self.cells[(r,c)].config(bg="light green")
                else: # Si es una celda inicial, volver a su color original
                    cell_color = "light grey" if (r // 3 + c // 3) % 2 == 0 else "white"
                    self.cells[(r,c)].config(bg=cell_color)

        if is_correct:
            messagebox.showinfo("Sudoku", "¡Felicidades! La solución es correcta.")
        else:
            messagebox.showerror("Sudoku", "La solución es incorrecta. Las celdas erróneas están resaltadas en rojo.")
            
    def check_cell_on_focus_out(self, r, c):
        """Verifica una celda individual cuando el usuario sale de ella."""
        user_val_str = self.cells[(r,c)].get()
        if user_val_str == "":
            user_val = 0
        else:
            try:
                user_val = int(user_val_str)
            except ValueError:
                user_val = 0 # Valor inválido, se trata como 0
        
        # Actualizar el modelo temporalmente para la verificación
        original_model_val = self.model.board[r][c]
        self.model.board[r][c] = user_val
        
        # Solo verificar si la celda es editable (no es un número inicial)
        if self.model.initial_board[r][c] == 0:
            if user_val != 0 and not self.model.is_valid(r, c, user_val):
                self.cells[(r,c)].config(fg='red') # Marcar en rojo si es inválido
            else:
                self.cells[(r,c)].config(fg='black') # Volver a negro si es válido o vacío
        
        # Restaurar el valor original en el modelo (si esta verificación no es para el 'check_solution' completo)
        # O podrías optar por mantener el valor para que el 'check_solution' luego opere sobre él.
        # Para este esquema, el 'check_solution' leerá directamente de la GUI.

# --- 3. INICIO DE LA APLICACIÓN ---
if __name__ == "__main__":
    root = Tk()
    app = SudokuGUI(root)
    root.mainloop()
