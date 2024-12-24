class HashTable:
    def __init__(self):
        self.size = 100
        self.table = [[] for _ in range(self.size)]
   
    def _hash_function(self, key):
        return hash(key) % self.size
   
    def insert(self, word,position):
        index = self._hash_function(word)
        if word not in self.table[index]:
            self.table[index].append((word,position))
   
    def search(self, word):
        index = self._hash_function(word)
        for entry in self.table[index]:
            if entry[0]==word:
                return entry[1]
        return None
