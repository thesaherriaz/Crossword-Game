# main.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from game import GameState
from game import GameMove
from player import Player


class CrosswordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Crossword Game")
        self.root.state('zoomed')  # Fullscreen window
        self.root.config(bg='SystemButtonFace')

        # Initialize the game with a predefined grid
        self.game = GameState(rows=7, cols=7, valid_words=[
            "HIS", "TOP", "HOW", "STRANGE", "WAR", "USE", "TOO",
            "TOURISM", "WIN", "INK", "SHE", "KEY", "GAS", "MAY", "WAS", "PIE"
        ], game_mode='two_player')

        self.grid_labels = []
        self.used_words = set()  # Keep track of used words

        # Create a list of players
        self.players = [Player("Player 1"), Player("Player 2")]
        self.current_player_index = 0  # Track the current player
        self.move_stack = []
        self.redo_stack = []
        self.show_start_image()
    
    def load_predefined_grid(self):
        
        # Define the hidden grid with the predefined words
        self.hidden_grid = [
            ['H', 'I', 'S', ' ', 'T', 'O', 'P'],
            ['O', ' ', 'T', 'O', 'O', ' ', 'I'],
            ['W', 'A', 'R', ' ', 'U', 'S', 'E'],
            [' ', ' ', 'A', ' ', 'R', ' ', ' '],
            ['W', 'I', 'N', ' ', 'I', 'N', 'K'],
            ['A', ' ', 'G', 'A', 'S', ' ', 'E'],
            ['S', 'H', 'E', ' ', 'M', 'A', 'Y'],
        ]

        words_with_positions = {
            "HIS": ((0, 0), "right"),
            "TOP": ((0, 4), "right"),
            "HOW": ((0, 0), "down"),
            "STRANGE": ((0, 2), "down"),
            "WAR": ((2, 0), "right"),
            "USE": ((2, 4), "right"),
            "TOO": ((1, 4), "right"),
            "TOURISM": ((0, 4), "down"),
            "WIN": ((4, 0), "right"),
            "INK": ((4, 4), "right"),
            "KEY": ((4, 6), "right"),
            "GAS": ((5, 0), "right"),
            "MAY": ((6, 4), "right"),
            "SHE": ((6, 0), "right"),
            "WAS": ((4, 0), "down"),
            "PIE": ((0, 6), "down"),
        }
        # Store the grid and word positions
        # self.hidden_grid = hidden_grid
        self.words_with_positions = words_with_positions
        # Initialize the visible grid with empty cells
        for row in range(len(self.hidden_grid)):
            for col in range(len(self.hidden_grid[row])):
                self.grid_labels[row][col].config(text="", bg="white")


    def show_start_image(self):
        img = Image.open("startpage2.jpg")
        img = img.resize((1400, 800), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)

        self.image_label = tk.Label(self.root, image=self.photo)
        self.image_label.pack(expand=True, fill=tk.BOTH)
        self.root.after(3000, self.show_button_page)

    def create_gradient(self, canvas, width, height, start_color, end_color):
        # Convert HEX colors to RGB
        start_rgb = canvas.winfo_rgb(start_color)
        end_rgb = canvas.winfo_rgb(end_color)
        
        # Compute RGB difference per step
        r_diff = (end_rgb[0] - start_rgb[0]) / height
        g_diff = (end_rgb[1] - start_rgb[1]) / height
        b_diff = (end_rgb[2] - start_rgb[2]) / height

        # Draw the gradient
        for i in range(height):
            r = int(start_rgb[0] / 256 + (r_diff * i) / 256)
            g = int(start_rgb[1] / 256 + (g_diff * i) / 256)
            b = int(start_rgb[2] / 256 + (b_diff * i) / 256)
            # Clamp RGB values to 0-255
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, width, i, fill=color)

    def show_button_page(self):
        # Remove any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a canvas for the gradient background
        width, height = self.root.winfo_width(), self.root.winfo_height()
        canvas = tk.Canvas(self.root, width=width, height=height)
        canvas.pack(fill=tk.BOTH, expand=True)
        self.create_gradient(canvas, width, height, "#191970", "#9400D3")  # Midnight Blue to Dark Violet

        # Create a frame to hold buttons over the gradient
        button_frame = tk.Frame(canvas, bg="#0E0330")
        button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Load images
        start_img = Image.open("img-2.jpg").resize((200, 200), Image.LANCZOS)
        two_player_img = Image.open("img-3.jpg").resize((200, 200), Image.LANCZOS)
        start_photo = ImageTk.PhotoImage(start_img)
        two_player_photo = ImageTk.PhotoImage(two_player_img)

        # Add buttons
        tk.Button(button_frame, image=start_photo, text="Single Player", compound=tk.TOP,
                command=self.start_single_player).pack(side=tk.LEFT, padx=20, pady=20)
        tk.Button(button_frame, image=two_player_photo, text="Two Players", compound=tk.TOP,
                command=self.start_two_player_game).pack(side=tk.LEFT, padx=20, pady=20)

        # Keep references to images to prevent garbage collection
        button_frame.start_photo = start_photo
        button_frame.two_player_photo = two_player_photo



    def start_single_player(self):
        self.game.game_mode='single_player'
        self.start_1player_game()

    def start_two_player_game(self):
        self.game.game_mode='two_player'
        self.start_2player_game()
    
    def update_current_player(self):
        # Update the current player label
        self.current_player_label.config(
            text=f"Current Player: {self.game.players[self.game.current_player].name}"
        )
        
        # Change the background color based on the current player
        if self.game.current_player == 0:  # Player 1
            self.main_frame.config(bg="#0FB667")
        else:  # Player 2
            self.main_frame.config(bg="#F4B000")


    def show_rules(self):
        # Display rules in a message box (You can customize this)
        rules_text = "Game Rules:\n1. Players take turns.\n2. A word can only be placed once.\n3. Use the grid wisely!"
        messagebox.showinfo("Rules", rules_text)

    def start_2player_game(self):
        # Clear the button page
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create main game frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        # Create player information frame
        self.create_player_info()

        # Create input and controls
        self.create_game_controls()

        # Create grid display
        self.create_grid_display()

        # Load the predefined grid
        self.load_predefined_grid()

    def start_1player_game(self):
        # Clear the button page
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create main game frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        # Create player information frame
        # self.create_player_info()

        # Create input and controls
        self.create_game_controls()

        # Create grid display
        self.create_grid_display()

        # Load the predefined grid
        self.load_predefined_grid()



    def create_grid_display(self):
        grid_frame = tk.Frame(self.main_frame)
        grid_frame.pack(expand=True)

        self.grid_labels = []
        for i in range(self.game.grid.rows):
            row_labels = []
            for j in range(self.game.grid.cols):
                cell_value = self.game.grid.grid[i][j]
                if cell_value!=" ":  # Only create a label for non-empty cells
                    # if cell_value!=" ":
                    label = tk.Label(grid_frame,
                                    text="",  # Initially blank
                                    width=4,
                                    height=2,
                                    borderwidth=1,
                                    relief="solid",
                                    font=("Helvetica", 16),
                                    bg="white",
                                    fg="black")
                    label.grid(row=i, column=j, padx=2, pady=2)
                    row_labels.append(label)
                else:
                    row_labels.append(" ")
            self.grid_labels.append(row_labels)

    def create_player_info(self):
        player_frame = tk.Frame(self.main_frame)
        player_frame.pack(fill=tk.X, pady=10)

        self.current_player_label = tk.Label(
            player_frame,
            text=f"Current Player: {self.game.players[self.game.current_player].name}",
            font=("Helvetica", 16),
            bg="SystemButtonFace",activebackground="SystemButtonFace"
        )
        self.current_player_label.pack(side=tk.LEFT, padx=10)

        self.scores_label = tk.Label(
            player_frame,
            text=self.get_scores_text(),
            font=("Helvetica", 16), bg="SystemButtonFace",activebackground="SystemButtonFace"
        )
        self.scores_label.pack(side=tk.RIGHT, padx=10)

    def place_word(self):
        word = self.word_entry.get().strip().upper()  # Get the entered word
        if not word:
            self.status_label.config(text="Please enter a word.")
            return
        if word in self.used_words:
            self.status_label.config(text="This word has already been used!")
            return

        # Store the current state of affected cells before placing the word
        affected_cells = []
        word_position = self.words_with_positions.get(word)

        if word_position:
            (row, col), direction = word_position
            
            # Store the current state of cells
            if direction == "right":
                for i, letter in enumerate(word):
                    affected_cells.append((row, col + i, 
                                        self.grid_labels[row][col + i].cget("text")))
            else:  # down
                for i, letter in enumerate(word):
                    affected_cells.append((row + i, col, 
                                        self.grid_labels[row + i][col].cget("text")))

            # Place the word
            for row, col, _ in affected_cells:
                cell_index = affected_cells.index((row, col, _))
                self.grid_labels[row][col].config(text=word[cell_index], bg="green")

            # Record the move for undo/redo
            move = GameMove(word, row, col, direction, affected_cells)
            self.move_stack.append(move)
            self.redo_stack.clear()  # Clear redo stack when new move is made
            
            # Update game state
            self.used_words.add(word)
            self.game.players[self.game.current_player].score += len(word)
            self.update_scores()
            self.status_label.config(text=f"'{word}' placed successfully!")
            
        else:
            self.status_label.config(text=f"'{word}' not found in the grid!")
            self.game.switch_player()

        self.update_current_player()
        self.word_entry.delete(0, tk.END)

        found = False  # Flag to indicate if the word is found
        # Check rows for the word
        for row in range(len(self.hidden_grid)):
            row_data = ''.join(self.hidden_grid[row])  # Combine row into a string
            if word in row_data:  # Check if the word exists in the row
                found = True
                start_index = row_data.find(word)  # Find the starting index of the word
                for i, char in enumerate(word):
                    # Update the visible grid
                    cell = self.grid_labels[row][start_index + i]
                    cell.config(text=char, bg="green")  # Reveal the word in the grid
                break

        # Check columns for the word if not found in rows
        if not found:
            for col in range(len(self.hidden_grid[0])):
                col_data = ''.join(self.hidden_grid[row][col] for row in range(len(self.hidden_grid)))  # Get the column as a string
                if word in col_data:
                    found = True
                    start_index = col_data.find(word)  # Find the starting index in the column
                    for i, char in enumerate(word):
                        # Update the visible grid
                        cell = self.grid_labels[start_index + i][col]
                        cell.config(text=char, bg="green")  # Reveal the word in the grid
                    break

        if found:
            self.status_label.config(text=f"'{word}' placed successfully!")
            self.used_words.add(word)  # Add the word to the set of used words
            self.game.players[self.game.current_player].score += 1  # Update score
            self.update_scores()
        else:
            self.status_label.config(text=f"'{word}' not found. Switching player.")
            self.game.switch_player()

        self.update_current_player()
        self.word_entry.delete(0, tk.END)
    
    def undo_move(self):
        if not self.move_stack:
            self.status_label.config(text="No moves to undo!")
            return

        # Get the last move
        move = self.move_stack.pop()
        
        # Restore previous state
        for row, col, prev_letter in move.cells:
            self.grid_labels[row][col].config(text=prev_letter if prev_letter else "", 
                                            bg="white")

        # Remove word from used words
        self.used_words.remove(move.word)
        
        # Update player score
        self.game.players[self.game.current_player].score -= len(move.word)
        
        # Add to redo stack
        self.redo_stack.append(move)
        
        # Update UI
        self.update_scores()
        self.status_label.config(text=f"Undid placement of '{move.word}'")

    def redo_move(self):
        if not self.redo_stack:
            self.status_label.config(text="No moves to redo!")
            return

        # Get the last undone move
        move = self.redo_stack.pop()
        
        # Reapply the move
        for i, (row, col, _) in enumerate(move.cells):
            self.grid_labels[row][col].config(text=move.word[i], bg="green")

        # Add word back to used words
        self.used_words.add(move.word)
        
        # Update player score
        self.game.players[self.game.current_player].score += len(move.word)
        
        # Add back to undo stack
        self.move_stack.append(move)
        
        # Update UI
        self.update_scores()
        self.status_label.config(text=f"Redid placement of '{move.word}'")

    def update_grid_with_word(self, word, index, is_row):
        print("n")
        if is_row:
            print("o")
            row_data = ''.join(self.game.grid.grid[index])  # Extract the row as a string
            start_positions = [
                i for i in range(len(row_data)) if row_data[i:i + len(word)] == " " * len(word)
            ]
            print("p")
            if not start_positions:
                # No valid position to place the word
                print("q")
                self.status_label.config(text=f"'{word}' cannot be placed in row {index}.")
                print(f"'{word}' cannot be placed in row {index}.")
                return  # Exit the function early

            start = start_positions[0]
            print(f"Placing '{word}' at row {index}, starting at index {start}")

            for i, char in enumerate(word):
                cell = self.grid_labels[index][start + i]
                cell.config(text=char, bg="green")  # Update GUI
                self.game.grid.grid[index][start + i] = char  # Update the grid internally
            self.next_index = start + len(word)
        else:
            print("u")
            column_data = ''.join(self.game.grid.grid[i][index] for i in range(len(self.game.grid.grid)))
            start_positions = [
                i for i in range(len(column_data)) if column_data[i:i + len(word)] == " " * len(word)
            ]
            if not start_positions:
                # No valid position to place the word
                print("v")
                self.status_label.config(text=f"'{word}' cannot be placed in column {index}.")
                return  # Exit the function early

            start = start_positions[0]
            print(f"Placing '{word}' at column {index}, starting at index {start}")

            for i, char in enumerate(word):
                cell = self.grid_labels[start + i][index]
                cell.config(text=char, bg="green")  # Update GUI
                self.game.grid.grid[start + i][index] = char  # Update the grid internally

            self.next_index = start + len(word)



    def update_scores(self):
        self.scores_label.config(text=self.get_scores_text())

    # def update_current_player(self):
    #     self.current_player_label.config(
    #         text=f"Current Player: {self.game.players[self.game.current_player].name}"
    #     )

    def get_scores_text(self):
        return " | ".join([f"{player.name}: {player.score}" for player in self.game.players])

    def get_hint(self):
        result = self.game.provide_hint()  # Assuming this returns 3 values: hint_letter, cell_position, message
        hint_letter, cell_position, message = result  # Unpack all 3 values

        if hint_letter and cell_position:  # If a valid hint is returned
            row, col = cell_position
            self.grid_labels[row][col].config(text=hint_letter, bg="yellow")
        else:
            self.status_label.config(text=message)  # Display the message from provide_hint



    def redo_move(self):
        current_player = self.players[self.current_player_index]
        move = current_player.redo_lastmove()
        
        if move:
            self.update_grid_with_redone_move(move)
            self.update_scores()
            self.status_label.config(text=f"Redo move: {move}")
        else:
            self.status_label.config(text="No moves to redo.")

    def create_game_controls(self):
        controls_frame = tk.Frame(self.main_frame)
        controls_frame.pack(fill=tk.X, pady=10)

        self.word_entry = tk.Entry(controls_frame, font=("Helvetica", 16), width=20)
        self.word_entry.pack(side=tk.LEFT, padx=10)

        place_word_button = tk.Button(controls_frame, text="Place Word", font=("Helvetica", 16), bg="SystemButtonFace",activebackground="SystemButtonFace", command=self.place_word)
        place_word_button.pack(side=tk.LEFT, padx=10)

        hint_button = tk.Button(controls_frame, text="Hint", font=("Helvetica", 16), bg="SystemButtonFace",activebackground="SystemButtonFace", command=self.get_hint)
        hint_button.pack(side=tk.LEFT, padx=10)

        self.status_label = tk.Label(self.main_frame, text="Game Started!", font=("Helvetica", 14), fg="red", bg="SystemButtonFace",activebackground="SystemButtonFace")
        self.status_label.pack(pady=10)

        undo_button = tk.Button(controls_frame, text="Undo", 
                              font=("Helvetica", 16), bg="SystemButtonFace",
                              activebackground="SystemButtonFace", command=self.undo_move)
        undo_button.pack(side=tk.LEFT, padx=10)

        redo_button = tk.Button(controls_frame, text="Redo", 
                              font=("Helvetica", 16), bg="SystemButtonFace",
                              activebackground="SystemButtonFace", command=self.redo_move)
        redo_button.pack(side=tk.LEFT, padx=10)


if __name__ == "__main__":
    root = tk.Tk()
    game = CrosswordGame(root)
    root.mainloop()