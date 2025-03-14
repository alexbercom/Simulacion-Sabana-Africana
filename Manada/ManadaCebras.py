from Manada.Manada import Manada

class ManadaCebras(Manada):
    def __init__(self):
        super().__init__()

    def eliminar_animal(self, animal):
        if animal in self.animales:
            self.animales.remove(animal)