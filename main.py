import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QColor
from game import GameState
from game import GameMove
from player import Player

class CrosswordGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Crossword Game")
        self.setWindowState(Qt.WindowMaximized) 
        self.setStyleSheet("background-color: #f0f0f0;") 

        self.game = GameState(rows=7, cols=7, valid_words=[
            "HIS", "TOP", "HOW", "STRANGE", "WAR", "USE", "TOO", "TOURISM", "WIN", "INK", "SHE", "KEY", "GAS", "MAY", "WAS", "PIE"
        ], game_mode='two_player')

        self.grid_labels = []
        self.used_words = set() 

        self.players = [Player("Player 1"), Player("Player 2")]
        self.current_player_index = 0 
        self.move_stack = []
        self.redo_stack = []

        self.init_ui()
        self.show_start_image()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)


    def show_start_image(self):
        self.image_label = QLabel(self)
        pixmap = QPixmap("startpage2.jpg")
        pixmap = pixmap.scaled(1400, 800, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.layout.addWidget(self.image_label)
        QTimer.singleShot(3000, self.show_button_page)

    def show_button_page(self):
        if self.image_label:
            self.layout.removeWidget(self.image_label)
            self.image_label.deleteLater()
            self.image_label = None

        # Create a frame to hold buttons
        button_frame = QFrame(self)
        button_layout = QHBoxLayout(button_frame)

        # Load images
        start_img = QPixmap("img-2.jpg").scaled(200, 200, Qt.KeepAspectRatio)
        two_player_img = QPixmap("img-3.jpg").scaled(200, 200, Qt.KeepAspectRatio)

        # Create buttons
        single_player_button = QPushButton("Single Player", self)
        single_player_button.setIcon(start_img)
        single_player_button.setIconSize(start_img.size())
        single_player_button.clicked.connect(self.start_single_player)
        two_player_button = QPushButton("Two Players", self)
        two_player_button.setIcon(two_player_img)
        two_player_button.setIconSize(two_player_img.size())
        two_player_button.clicked.connect(self.start_two_player_game)

        # Add buttons to layout
        button_layout.addWidget(single_player_button)
        button_layout.addWidget(two_player_button)

        # Add frame to main layout
        self.layout.addWidget(button_frame)


    def start_single_player(self):
        self.game.game_mode = 'single_player'
        self.start_game()

    def start_two_player_game(self):
        self.game.game_mode = 'two_player'
        self.start_game()

    def start_game(self):
        # Clear the button page
        for i in reversed(range(self.layout.count())): 
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create main game frame
        self.main_frame = QWidget(self)
        self.main_layout = QVBoxLayout(self.main_frame)

        # Create player information frame
        self.create_player_info()

        # Create input and controls
        self.create_game_controls()

        # Create grid display
        self.create_grid_display()

        # Load the predefined grid
        self.load_predefined_grid()

        # Add main frame to layout
        self.layout.addWidget(self.main_frame)

    def create_player_info(self):
        player_frame = QFrame(self.main_frame)
        player_layout = QHBoxLayout(player_frame)

        self.current_player_label = QLabel(f"Current Player: {self.players[self.current_player_index].name}", self)
        player_layout.addWidget(self.current_player_label)

        self.scores_label = QLabel(self.get_scores_text(), self)
        player_layout.addWidget(self.scores_label)

        self.main_layout.addWidget(player_frame)

    def create_game_controls(self):
        controls_frame = QFrame(self.main_frame)
        controls_layout = QHBoxLayout(controls_frame)

        self.word_entry = QLineEdit(self)
        self.word_entry.setPlaceholderText("Enter word here")
        controls_layout.addWidget(self.word_entry)

        place_word_button = QPushButton("Place Word", self)
        place_word_button.clicked.connect(self.place_word)
        controls_layout.addWidget(place_word_button)

        hint_button = QPushButton("Hint", self)

        hint_button = QPushButton("Hint", self)
        hint_button.clicked.connect(self.get_hint)
        controls_layout.addWidget(hint_button)

        undo_button = QPushButton("Undo", self)
        undo_button.clicked.connect(self.undo_move)
        controls_layout.addWidget(undo_button)

        redo_button = QPushButton("Redo", self)
        redo_button.clicked.connect(self.redo_move)
        controls_layout.addWidget(redo_button)

        self.status_label = QLabel("Game Started!", self)
        self.status_label.setStyleSheet("color: red;")
        controls_layout.addWidget(self.status_label)

        self.main_layout.addWidget(controls_frame)

    def create_grid_display(self):
        grid_frame = QFrame(self.main_frame)
        grid_layout = QGridLayout(grid_frame)

        self.grid_labels = []
        for i in range(self.game.grid.rows):
            row_labels = []
            for j in range(self.game.grid.cols):
                label = QLabel("", self)
                label.setStyleSheet("border: 1px solid black;")
                label.setFixedSize(40, 40)
                grid_layout.addWidget(label, i, j)
                row_labels.append(label)
            self.grid_labels.append(row_labels)

        self.main_layout.addWidget(grid_frame)

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
        self.hidden_grid = self.hidden_grid
        self.words_with_positions = words_with_positions

        # Initialize the visible grid with empty cells
        for row in range(len(self.hidden_grid)):
            for col in range(len(self.hidden_grid[row])):
                self.grid_labels[row][col].setText("")

    def place_word(self):
        word = self.word_entry.text().strip().upper()
        # Get the entered word
        if not word:
            self.status_label.setText("Please enter a word.")
            return
        if word in self.used_words:
            self.status_label.setText("This word has already been used!")
            return

        # Store the current state of affected cells before placing the word
        affected_cells = []
        word_position = self.words_with_positions.get(word)
        if word_position:
            (row, col), direction = word_position
            # Store the current state of cells
            if direction == "right":
                for i, letter in enumerate(word):
                    affected_cells.append((row, col + i, self.grid_labels[row][col + i].text()))
            else:
                # down
                for i, letter in enumerate(word):
                    affected_cells.append((row + i, col, self.grid_labels[row + i][col].text()))

            # Place the word
            for row, col, _ in affected_cells:
                cell_index = affected_cells.index((row, col, _))
                self.grid_labels[row][col].setText(word[cell_index])
                self.grid_labels[row][col].setStyleSheet("background-color: green;")

            # Record the move
            move = GameMove(word, row, col, direction, affected_cells)
            self.move_stack.append(move)
            self.redo_stack.clear()
            # Clear redo stack when new move is made


    def update_game(self):
        self.used_words.add(word)
        self.game.players[self.game.current_player].score += len(word)
        self.update_scores()
        self.status_label.setText(f"'{word}' placed successfully!")
        self.game.switch_player()
        self.update_current_player()
        self.word_entry.clear()

    def update_scores(self):
        self.scores_label.setText(self.get_scores_text())

    def update_current_player(self):
        self.current_player_label.setText(f"Current Player: {self.game.players[self.game.current_player].name}")

    def get_scores_text(self):
        return " | ".join([f"{player.name}: {player.score}" for player in self.game.players])

    def get_hint(self):
        result = self.game.provide_hint()
        # Assuming this returns 3 values: hint_letter, cell_position, message
        hint_letter, cell_position, message = result
        # Unpack all 3 values
        if hint_letter and cell_position:
            # If a valid hint is returned
            row, col = cell_position
            self.grid_labels[row][col].setText(hint_letter)
            self.grid_labels[row][col].setStyleSheet("background-color: yellow;")
        else:
            self.status_label.setText(message)

    def undo_move(self):
        if not self.move_stack:
            self.status_label.setText("No moves to undo!")
            return
        # Get the last move
        move = self.move_stack.pop()
        # Restore previous state
        for row, col, prev_letter in move.cells:
            self.grid_labels[row][col].setText(prev_letter if prev_letter else "")
            self.grid_labels[row][col].setStyleSheet("")
        # Remove word from used words
        self.used_words.remove(move.word)
        # Update player score
        self.game.players[self.game.current_player].score -= len(move.word)
        # Add to redo stack
        self.redo_stack.append(move)
        # Update UI
        self.update_scores()
        self.status_label.setText(f"Undid placement of '{move.word}'")

    def redo_move(self):
        if not self.redo_stack:
            self.status_label.setText("No moves to redo!")
            return
        # Get the last undone move
        move = self.redo_stack.pop()
        # Reapply the move
        for i, (row, col, _) in enumerate(move.cells):
            self.grid_labels[row][col].setText(move.word[i])
            self.grid_labels[row][col].setStyleSheet("background-color: green;")
        # Add word back to used words
        self.used_words.add(move.word)
        # Update player score
        self.game.players[self.game.current_player].score += len(move.word)
        # Add back to undo stack
        self.move_stack.append(move)
        # Update UI
        self.update_scores()
        self.status_label.setText(f"Redid placement of '{move.word}'")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = CrosswordGame()
    game.show()
    sys.exit(app.exec_())
