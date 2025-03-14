import time
from Juego import Configuracion
from random import randint
from Animal.Depredador import Depredador

class Leon(Depredador):
    def __init__(self, juego, manada, posicion_inicial):
        super().__init__(juego, manada, posicion_inicial)
        self.velocidad = randint(Configuracion.VELOCIDAD_LEON[0], Configuracion.VELOCIDAD_LEON[1])

    # Si puede cazar caza y si no se mueve, si tiene que descansar descansa y hace un sleep de su respectiva velocidad
    def run(self):
        while self.juego.ganador is None:
            time.sleep(self.velocidad)
            presa = self.intentar_cazar()
            if presa and presa.cazada is False:
                self.cazar(presa)
            else:
                self.mover()
            self.descansar()

    # 20% de descansar (más propenso que las hienas y las cebras)
    def descansar(self):
        if randint(0, 100) < Configuracion.DESCANSO_LEON:
            time.sleep(randint(*Configuracion.TIEMPO_DESCANSO))
