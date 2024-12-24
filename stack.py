class Stack:
    def __init__(self):
        self.stack = [] 

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, item):
        self.stack += [item] 

    def pop(self):
        if not self.is_empty():
            item = self.stack[-1] 
            self.stack = self.stack[:-1]  
            return item
        else:
            return "Stack is empty"

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            return "Stack is empty"

    def peek_top(self, n):    
        if n <= len(self.stack):
            return self.stack[-n:]  
        else:
            return self.stack[:]    
