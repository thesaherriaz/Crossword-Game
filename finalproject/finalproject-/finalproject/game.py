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
        self.players = [Player("Player 1"), Player("Player 2")]
        self.grid = Grid(rows, cols)
        self.current_player = 0
        self.hint_queue = Queue()
        self.trie = Trie()
        self.timer = Timer() if game_mode == 'single_player' else None
        self.move_history = LinkedList() 
        self.word_connection_graph = Graph() 
        self.load_valid_words(valid_words)
        self.word_positions = []
        self.valid_words = valid_words 

    def load_valid_words(self, words):
        for word in words:
            self.trie.insert(word)
            self.hint_queue.enqueue(word)

    def add_word(self, word, row, col, direction):
        if not self.trie.search(word):
            return False 

        for i, letter in enumerate(word):
            if direction == 'right':
                if col + i >= self.grid.cols or (self.grid.grid[row][col + i] and self.grid.grid[row][col + i] != letter):
                    return False  
            elif direction == 'down':
                if row + i >= self.grid.rows or (self.grid.grid[row + i][col] and self.grid.grid[row + i][col] != letter):
                    return False  
   
        for i, letter in enumerate(word):
            if direction == 'right':
                self.grid.grid[row][col + i] = letter
            elif direction == 'down':
                self.grid.grid[row + i][col] = letter

        move = GameMove(word, row, col, direction, self.players[self.current_player])
        
        self.move_history.insert(move)
     
        self._update_word_connections(move)

        self.word_positions.append((word, row, col, direction))
      
        self.players[self.current_player].increase_score(len(word))
        return True

    def _update_word_connections(self, move):
        self.word_connection_graph.insert_edge(move.word, move.word)
 
        current_move_cells = self._get_word_cells(move)
      
        current = self.move_history.head
        while current:
            if current.data != move:
                prev_move_cells = self._get_word_cells(current.data)
                
                intersections = set(current_move_cells) & set(prev_move_cells)
              
                if intersections:
                    self.word_connection_graph.insert_edge(move.word, current.data.word)
            
            current = current.next

    def _get_word_cells(self, move):
        cells = []
        for i in range(len(move.word)):
            if move.direction == 'horizontal':
                cells.append((move.row, move.col + i))
            else:
                cells.append((move.row + i, move.col))
        return cells

    def get_move_stats(self):
        total_moves = 0
        current = self.move_history.head
        while current:
            total_moves += 1
            current = current.next
        
        total_score = self.move_history.total_score()
        
        return {
            'total_moves': total_moves,
            'total_score_from_moves': total_score
        }

    def get_word_connections(self):
        print("Word Connections:")
        self.word_connection_graph.display()

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def start_game(self):
        if self.game_mode == 'single_player':
            self.timer.start()
        
    def end_game(self):
        if self.game_mode == 'single_player':
            self.timer.stop()
        winner = max(self.players, key=lambda player: player.score)
        move_stats = self.get_move_stats()
        
        return {
            'winner': winner,
            'move_stats': move_stats
        }
    
    def search(self, word):
        for entry in self.word_positions:
            if entry[0] == word:  # Assuming entry[0] is the word
                return entry[1:]  # Return the row, col, and direction
        return None  # Return None if the word is not found


    def provide_hint(self):
        if not self.hint_queue.is_empty():  # Check if the queue is not empty
            hint_word = self.hint_queue.dequeue()  # Get the word from the queue
            if len(hint_word) > 0:  # Ensure the hint_word is not empty
                letter_index = random.randint(0, len(hint_word) - 1)  # Randomly select an index
                hint_letter = hint_word[letter_index]  # Get the letter from the word
                
                # Get the position of the hint word
                position = self.search(hint_word)
                
                if position:  # If the position is found
                    row, col, direction = position  # Unpack position
                    # Determine the specific cell based on the direction
                    if direction == "horizontal":
                        cell_position = (row, col + letter_index)
                    else:  # Assuming direction can only be 'vertical'
                        cell_position = (row + letter_index, col)
                    
                    self.players[self.current_player].decrease_score(2)  # Decrease the score
                    # Update the grid cell with the hint letter
                    self.grid.grid[cell_position[0]][cell_position[1]] = hint_letter  # Update grid
                    return hint_letter, cell_position  # Return the letter and its cell position
                
                # If position is not found, log an error or handle it
                print(f"Error: Position for '{hint_word}' not found.")
                
        return None, None  # Return None if there are no words left for hints

