import time
from Juego import Configuracion
from random import randint
from Animal.Animal import Animal

class Cebra(Animal):
    def __init__(self, juego, manada, posicion_inicial):
        super().__init__(juego, manada, posicion_inicial)
        self.velocidad = randint(Configuracion.VELOCIDAD_CEBRA[0], Configuracion.VELOCIDAD_CEBRA[1])

    # Se mueve y descansa ciclicamente hasta que es cazada o termina el juego
    def run(self):
        while self.juego.ganador is None and not self.cazada:
            time.sleep(self.velocidad)
            self.mover()
            self.descansar()

    # Generación de una nueva cebra al notificar que otra ha sido cazada
    def notificar_caza(self):
        # Crear nueva cebra en la misma manada y posición
        posicion = (randint(0, Configuracion.SIZE_TABLERO[0] - 1),
                    randint(0, Configuracion.SIZE_TABLERO[1] - 1))
        nueva_cebra = Cebra(self.juego, self.manada, posicion)
        self.manada.add_animal(nueva_cebra)
        with self.juego.lock_cebras:
            self.juego.cebras.append(nueva_cebra)
        self.juego.colocar_animal(nueva_cebra, posicion)
        nueva_cebra.start()
        print(f"Cebra nueva generada")

    # 10% de descansar
    def descansar(self):
        if randint(0, 100) < Configuracion.DESCANSO_HIENA:
            time.sleep(randint(*Configuracion.TIEMPO_DESCANSO))