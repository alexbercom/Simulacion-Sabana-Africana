import threading

class Casilla:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lock = threading.Lock()
        self.animal = None