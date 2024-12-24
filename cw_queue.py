class Queue:
 def __init__(self, capacity=100):
   self.capacity = capacity  
   self.queue = [None] * self.capacity 
   self.front = 0  
   self.rear = -1  
   self.count = 0 
   
 def enqueue(self, item):
    if self.size() == self.capacity:
        print("Queue is full. Cannot enqueue.")
        return
 
    self.rear = (self.rear + 1) % self.capacity
    self.queue[self.rear] = item
    self.count += 1
   
 def dequeue(self):
    if self.is_empty():
        print("Queue is empty. Cannot dequeue.")
        return None
    item = self.queue[self.front]
    self.queue[self.front] = None 
    self.front = (self.front + 1) % self.capacity
    self.count -= 1
    return item
   
 def peek(self):
    if self.is_empty():
        print("Queue is empty. Nothing to peek.")
        return None
    return self.queue[self.front]
   
 def is_empty(self):
    return self.count == 0
   
 def size(self):
    return self.count
 
 def display(self):
    if self.is_empty():
        print("Queue is empty.")
        return
    print("Queue elements: ", end="")
    for i in range(self.count):
        index = (self.front + i) % self.capacity
        print(self.queue[index], end=" ")
    print()