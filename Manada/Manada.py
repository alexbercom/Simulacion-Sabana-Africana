import threading

class Manada:
    def __init__(self):
        self.animales = []
        self.lock = threading.Lock()

    def add_animal(self, animal):
        with self.lock:
            self.animales.append(animal)
