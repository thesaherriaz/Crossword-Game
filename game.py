from linkedlists import LinkedList
from graph import Graph
from trie import Trie
from cw_queue import Queue
from grid import Grid
from player import Player
from timer import Timer
import random
# import cw_queue import Queue

class GameMove:
    def __init__(self, word, row, col, direction, player):
        self.word = word
        self.row = row
        self.col = col
        self.direction = direction
        self.player = player

class GameState:
    def __init__(self, rows, cols, valid_words, game_mode='two_player'):
        self.game_mode = game_mode
        self.players = [Player("Player 1")]
        if game_mode == 'two_player':
            self.players.append(Player("Player 2"))
        self.grid = Grid(rows, cols)
        self.current_player = 0
        self.hint_queue = Queue()
        self.trie = Trie()
        self.timer = Timer() if game_mode == 'single_player' else None
        self.move_history = LinkedList()
        self.word_connection_graph = Graph()
        self.load_valid_words(valid_words)
        self.move_stack = []
        self.redo_stack = []
        self.used_words = set() # Add this to track used words
 

    def load_valid_words(self, words):
        for word in words:
            self.trie.insert(word)
            self.hint_queue.enqueue(word)

    def switch_player(self):
        if self.game_mode == 'two_player':
            self.current_player = (self.current_player + 1) % 2

    def add_word(self, word, row, col, direction):
        # First check if word has already been used
        if word in self.used_words:
            return False, "Word has already been placed on the grid"

        if not self.trie.search(word):
            return False, "Not a valid word"

        # Check if word can be placed
        for i, letter in enumerate(word):
            if direction == 'right':
                if col + i >= self.grid.cols or (self.grid.grid[row][col + i] and self.grid.grid[row][col + i] != letter):
                    return False, "Word doesn't fit in the grid"
            elif direction == 'down':
                if row + i >= self.grid.rows or (self.grid.grid[row + i][col] and self.grid.grid[row + i][col] != letter):
                    return False, "Word doesn't fit in the grid"
   
        # If all checks pass, place the word
        for i, letter in enumerate(word):
            if direction == 'right':
                self.grid.grid[row][col + i] = letter
            elif direction == 'down':
                self.grid.grid[row + i][col] = letter

        # Add word to used_words set
        self.used_words.add(word)

        move = GameMove(word, row, col, direction, self.players[self.current_player])
        self.move_history.insert(move)
        self._update_word_connections(move)
        self.move_stack.append(GameMove(word, row, col, direction, self.players[self.current_player]))
        self.redo_stack.clear()
        self.word_positions.append((word, row, col, direction))
        self.players[self.current_player].increase_score(len(word))
        return True, "Word placed successfully"

    def provide_hint(self):
        if not self.hint_queue.is_empty():
            available_positions = []
            
            # Check current grid state for empty cells
            for row in range(self.grid.rows):
                for col in range(self.grid.cols):
                    if self.grid.grid[row][col] == " ":  # Empty cell
                        available_positions.append((row, col))
            
            if not available_positions:
                return None, None, "No empty positions available for hints"
            
            # Select random empty position
            hint_pos = random.choice(available_positions)
            row, col = hint_pos
            
            # Find valid words that can be placed at this position
            possible_words = []
            for word in self.valid_words:
                if word not in self.used_words:  # Check only unused words
                    # Check if word can fit in the 'right' direction
                    if col + len(word) <= self.grid.cols:
                        can_place_right = True
                        for i, letter in enumerate(word):
                            if self.grid.grid[row][col + i] != " " and self.grid.grid[row][col + i] != letter:
                                can_place_right = False
                                break
                        if can_place_right:
                            possible_words.append((word, "right"))
                    
                    # Check if word can fit in the 'down' direction
                    if row + len(word) <= self.grid.rows:
                        can_place_down = True
                        for i, letter in enumerate(word):
                            if self.grid.grid[row + i][col] != " " and self.grid.grid[row + i][col] != letter:
                                can_place_down = False
                                break
                        if can_place_down:
                            possible_words.append((word, "down"))
            
            if possible_words:
                # Select a random word and direction from possible words
                word, direction = random.choice(possible_words)
                
                # Select a random letter position from the word
                letter_index = random.randint(0, len(word) - 1)
                hint_letter = word[letter_index]
                
                # Determine the hint position based on the selected direction
                if direction == "right":
                    hint_position = (row, col + letter_index)
                else:  # down
                    hint_position = (row + letter_index, col)
                
                # Deduct points for using a hint
                self.players[self.current_player].decrease_score(1)
                
                return hint_letter, hint_position, f"Try letter '{hint_letter}' at position {hint_position}"
            
            return None, None, "No valid words can be placed at available positions"
        
        return None, None, "No more hints available"

    def undo(self):
        if not self.move_stack:
            return False, "No moves to undo"
        last_move = self.move_stack.pop()
        self.redo_stack.append(last_move)
        self.grid.remove_word(last_move.word, last_move.row, last_move.col, last_move.direction)
        self.used_words.remove(last_move.word)
        last_move.player.decrease_score(len(last_move.word))
        return True, "Undo successful"

    def redo(self):
        if not self.redo_stack:
            return False, "No moves to redo"
        move = self.redo_stack.pop()
        self.move_stack.append(move)
        self.grid.place_word(move.word, move.row, move.col, move.direction)
        self.used_words.add(move.word)
        move.player.increase_score(len(move.word))
        return True, "Redo successful"
