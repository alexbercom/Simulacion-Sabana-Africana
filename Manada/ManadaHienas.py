from Manada.Manada import Manada

class ManadaHienas(Manada):
    def __init__(self):
        super().__init__()
        self.puntuacion = 0

    def eliminar_animal(self, animal):
        if animal in self.animales:
            self.animales.remove(animal)