from stack import Stack 

class Player:
    def __init__(self,name):
        self.name=name
        self.max_undo=3
        self.score=0
        self.undo=Stack()
        self.redo=Stack()

    def undo_move(self):
        return not self.undo.is_empty() and self.max_undo>0
    
    def redo_move(self):
        return not self.redo.is_empty()

    def undo_lastmove(self):
     if self.undo_move():
        move = self.undo.pop()
        self.redo.push(move)
        self.max_undo -= 1
        return move
     return None

    def redo_lastmove(self):
     if self.redo_move():
        move = self.redo.pop()
        self.undo.push(move)
        return move
     return None

    
    def increase_score(self, points):
        self.score += points

    def decrease_score(self, points):
        self.score = max(0, self.score - points)