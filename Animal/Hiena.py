import time
from Juego import Configuracion
from random import randint
from Animal.Depredador import Depredador

class Hiena(Depredador):
    def __init__(self, juego, manada, posicion_inicial):
        super().__init__(juego, manada, posicion_inicial)
        self.velocidad = randint(Configuracion.VELOCIDAD_HIENA[0], Configuracion.VELOCIDAD_HIENA[1])

    # Si puede cazar caza y si no se mueve, si tiene que descansar descansa y hace un sleep de su respectiva velocidad
    def run(self):
        while self.juego.ganador is None and self.cazada is False:
            time.sleep(self.velocidad)
            presa = self.intentar_cazar()
            if presa and presa.cazada is False:
                self.cazar(presa)
            else:
                self.mover()
            self.descansar()

    # 10% de descansar
    def descansar(self):
        if randint(0, 100) < Configuracion.DESCANSO_HIENA:
            time.sleep(randint(*Configuracion.TIEMPO_DESCANSO))