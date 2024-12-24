class Graph:
    def __init__(self):
        self.graph = {}
   
    def insert_edge(self, start, end):
        if start not in self.graph:
            self.graph[start] = []
        self.graph[start].append(end)
   
    def display(self):
        for node in self.graph:
            print(f"{node} -> {', '.join(self.graph[node])}")
            