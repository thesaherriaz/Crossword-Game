import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from game import GameState # Ensure this file exists with required functionality
from player import Player  # Ensure this file exists with required functionality


class CrosswordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Crossword Game")
        self.root.state('zoomed')  # Fullscreen window

        # Initialize the game with a predefined grid
        self.game = GameState(rows=7, cols=7, valid_words=[
            "HIS", "TOP", "HOW", "STRANGE", "WAR", "USE", "TOO",
            "TOURISM", "WIN", "INK", "SHE", "KEY", "GAS", "MAY", "WAS", "PIE"
        ], game_mode='two_player')

        self.grid_labels = None
        self.used_words = set()  # Keep track of used words

        # Create a list of players
        self.players = [Player("Player 1"), Player("Player 2")]
        self.current_player_index = 0  # Track the current player

        # Load and display the start image
        self.show_start_image()

    def redo_move(self):
        """Handle the redo move for the current player."""
        current_player = self.players[self.current_player_index]
        move = current_player.redo_lastmove()
        
        if move:
            self.update_grid_with_redone_move(move)  # Define this method
            self.update_scores()
            self.status_label.config(text=f"Redo move: {move}")
        else:
            self.status_label.config(text="No moves to redo.")

    def create_game_controls(self):
        controls_frame = tk.Frame(self.main_frame)
        controls_frame.pack(fill=tk.X, pady=10)

        self.word_entry = tk.Entry(controls_frame, font=("Helvetica", 16))
        self.word_entry.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        self.submit_btn = tk.Button(
            controls_frame,
            text="Submit Word",
            command=self.place_word
        )
        self.submit_btn.pack(side=tk.LEFT, padx=10)

        # Add Hint Button
        self.hint_btn = tk.Button(
            controls_frame,
            text="Hint",
            command=self.get_hint
        )
        self.hint_btn.pack(side=tk.LEFT, padx=10)

        # Add Undo Button
        self.undo_btn = tk.Button(
            controls_frame,
            text="Undo",
            command=self.undo_move
        )
        self.undo_btn.pack(side=tk.LEFT, padx=10)

        # Add Redo Button
        self.redo_btn = tk.Button(
            controls_frame,
            text="Redo",
            command=self.redo_move
        )
        self.redo_btn.pack(side=tk.LEFT, padx=10)

        self.status_label = tk.Label(self.main_frame, text="", font=("Helvetica", 14), fg="red")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

    def undo_move(self):
        """Handle the undo move for the current player."""
        current_player = self.players[self.current_player_index]
        move = current_player.undo_lastmove()
        
        if move:
            # Update the grid and scores based on the undone move
            # You need to define how a move is structured and how to handle it
            self.update_grid_with_undone_move(move)  # Define this method
            self.update_scores()
            self.status_label.config(text=f"Undo move: {move}")
        else:
            self.status_label.config(text="No moves to undo.")

    # Define methods to handle updating the grid for undo/redo
    def update_grid_with_redone_move(self, move):
        # Logic to update the grid based on the redone move
        pass

    def update_grid_with_undone_move(self, move):
        # Logic to update the grid based on the undone move
        pass


    def show_start_image(self):
        img = Image.open("main-img.png")
        img = img.resize((800, 800), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)

        self.image_label = tk.Label(self.root, image=self.photo)
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # Start the game after 3 seconds
        self.root.after(3000, self.start_game)

    def start_game(self):
        # Clear the start image
        self.image_label.pack_forget()

        # Create main game frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Create grid display
        self.create_grid_display()

        # Create player information frame
        self.create_player_info()

        # Create input and controls
        self.create_game_controls()

    def create_grid_display(self):
        # Create a frame for the grid
        grid_frame = tk.Frame(self.main_frame)
        grid_frame.pack(expand=True)

        # Create labels for grid
        self.grid_labels = []
        for i in range(self.game.grid.rows):
            row_labels = []
            for j in range(self.game.grid.cols):
                cell_value = self.game.grid.grid[i][j]
                if cell_value:  # Only create a label for non-empty cells
                    label = tk.Label(grid_frame,
                                    text="",
                                    width=4,
                                    height=2,
                                    borderwidth=1,
                                    relief="solid",
                                    font=("Helvetica", 16))
                    label.grid(row=i, column=j, padx=2, pady=2)
                    row_labels.append(label)
                else:
                    row_labels.append(None)  # Placeholder for consistency
            self.grid_labels.append(row_labels)

    def update_grid_with_word(self, word, start, is_row=True):
        for i, char in enumerate(word):
            if is_row:
                index = start  # Use the same row for horizontal words
                col = start + i
            else:
                index = start + i  # Use different rows for vertical words
                col = start

            if 0 <= index < len(self.grid_labels) and 0 <= col < len(self.grid_labels[0]):
                self.grid_labels[index][col].config(text=char, bg="green")
            else:
                print(f"Attempting to access out-of-bounds indices: ({index}, {col})")


    def create_player_info(self):
        player_frame = tk.Frame(self.main_frame)
        player_frame.pack(fill=tk.X, pady=10)

        self.current_player_label = tk.Label(
            player_frame,
            text=f"Current Player: {self.game.players[self.game.current_player].name}",
            font=("Helvetica", 16)
        )
        self.current_player_label.pack(side=tk.LEFT, padx=10)

        self.scores_label = tk.Label(
            player_frame,
            text=self.get_scores_text(),
            font=("Helvetica", 16)
        )
        self.scores_label.pack(side=tk.RIGHT, padx=10)

    def create_game_controls(self):
        controls_frame = tk.Frame(self.main_frame)
        controls_frame.pack(fill=tk.X, pady=10)

        self.word_entry = tk.Entry(controls_frame, font=("Helvetica", 16))
        self.word_entry.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        self.submit_btn = tk.Button(
            controls_frame,
            text="Submit Word",
            command=self.place_word
        )
        self.submit_btn.pack(side=tk.LEFT, padx=10)

        # Add Hint Button
        self.hint_btn = tk.Button(
            controls_frame,
            text="Hint",
            command=self.get_hint
        )
        self.hint_btn.pack(side=tk.LEFT, padx=10)

        self.status_label = tk.Label(self.main_frame, text="", font=("Helvetica", 14), fg="red")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

    def place_word(self):
        word = self.word_entry.get().strip().upper()
        if not word:
            self.status_label.config(text="Please enter a word.")
            return

        found = False
        for row in range(self.game.grid.rows):
            if word in ''.join(self.game.grid.grid[row]):  # Check rows
                found = True
                self.update_grid_with_word(word, row, is_row=True)
                break

        if not found:
            for col in range(self.game.grid.cols):
                col_data = ''.join(self.game.grid.grid[row][col] for row in range(self.game.grid.rows))
                if word in col_data:  # Check columns
                    found = True
                    self.update_grid_with_word(word, col, is_row=False)
                    break

        if found:
            self.game.players[self.game.current_player].score += 1
            self.used_words.add(word)
            self.status_label.config(text=f"'{word}' placed successfully!")
            self.update_scores()
        else:
            self.status_label.config(text=f"'{word}' not found. Switching player.")
            self.game.switch_player()

        self.update_current_player()
        self.word_entry.delete(0, tk.END)

    def get_hint(self):
        # Provide a hint with an unused word
        unused_words = [word for word in self.game.valid_words if word not in self.used_words]
        if unused_words:
            hint = unused_words[0]  # Take the first unused word as a hint
            messagebox.showinfo("Hint", f"Try this word: {hint}")
        else:
            messagebox.showinfo("Hint", "No more hints available!")

    def update_grid_with_word(self, word, index, is_row):
        if is_row:
            start = ''.join(self.game.grid.grid[index]).index(word)
            for i, char in enumerate(word):
                self.grid_labels[index][start + i].config(text=char, bg="green")
        else:
            col_data = ''.join(self.game.grid.grid[row][index] for row in range(self.game.grid.rows))
            start = col_data.index(word)
            for i, char in enumerate(word):
                self.grid_labels[start + i][index].config(text=char, bg="green")

    def update_scores(self):
        self.scores_label.config(text=self.get_scores_text())

    def update_current_player(self):
        self.current_player_label.config(
            text=f"Current Player: {self.game.players[self.game.current_player].name}"
        )

    def get_scores_text(self):
        return " | ".join([f"{player.name}: {player.score}" for player in self.game.players])
    def get_hint(self):
        hint = self.game.provide_hint()
        tk.messagebox.showinfo("Hint", f"Hint: {hint}")

def main():
    root = tk.Tk()
    game = CrosswordGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
