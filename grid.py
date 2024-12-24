
from trie import Trie
from hashtable import HashTable


class Grid:
     def __init__(self, rows, cols):
         self.rows = rows
         self.cols = cols
         self.grid = [[" " for _ in range(cols)] for _ in range(rows)]  # Initialize empty grid

         self.word_positions = HashTable() 
         self.valid_words = Trie() 
         self.load_predefined_grid() 
         self.load_valid_words() 

     def place_word(self, word, row, start, is_row):
        # Place word in the grid
         if is_row:
             for i in range(len(word)):
                 self.grid[row][start + i] = word[i]
         else:
             for i in range(len(word)):
                 self.grid[start + i][row] = word[i]


     def load_predefined_grid(self): 
         predefined_grid = [ ['H', 'I', 'S', ' ', 'T', 'O', 'P'],
                             ['O', ' ', 'T', 'O', 'O', ' ', 'I'],
                             ['W', 'A', 'R', ' ', 'U', 'S', 'E'], 
                             [' ', ' ', 'A', ' ', 'R', ' ', ' '],
                             ['W', 'I', 'N', ' ', 'I', 'N', 'K'],
                             ['A', ' ', 'G', 'A', 'S', ' ', 'E'],
                             ['S', 'H', 'E', ' ', 'M', 'A', 'Y'], ] 
         
         words_with_positions = { "HIS": ((0, 0), "right"), 
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
                                 "PIE": ((0, 6), "down"),  }
          
         for i in range(self.rows): 
             for j in range(self.cols): 
                self.grid[i][j] = predefined_grid[i][j]

                 
         for word, position in words_with_positions.items():
             self.word_positions.insert(word, position)
        
     def load_valid_words(self): 
         words = ["HIS", "TOP", "HOW", "STRANGE", "WAR", "USE", "TOO","TOURISM", "WIN", "INK", "SHE", "KEY", "GAS", "MAY","WAS","PIE"] 
         for word in words: self.valid_words.insert(word) 

     def validate_word(self, word): 
         return self.valid_words.search(word) 
     
     def get_word_position(self, word): 
         return self.word_positions.search(word)
     
     def remove_word(self, word, row, col, direction):
        for i, letter in enumerate(word):
            if direction == 'right':
                self.grid[row][col + i] = " "
            elif direction == 'down':
                self.grid[row + i][col] = " "