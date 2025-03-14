from abc import abstractmethod
from threading import Thread
import threading
import random
from Juego import Configuracion


class Animal(Thread):
    def __init__(self, juego, manada, posicion_inicial):
        super().__init__()
        self.juego = juego
        self.manada = manada
        self.posicion = posicion_inicial
        self.cazada = False
        self.lock_cazada = threading.Lock()
        self.lock_puntuacion = threading.Lock()

    @abstractmethod
    def run(self):
        """ Depende de la clase """
        raise NotImplementedError("Método `run` debe ser implementado por subclases.")

    @abstractmethod
    def descansar(self):
        """ Depende de la clase """
        raise NotImplementedError("Método `descansar` debe ser implementado por subclases.")

    # Función que determina el sistema de movimiento
    def mover(self):
        origenX, origenY = self.posicion
        casilla_origen = self.juego.tablero[origenX][origenY]

        # Generar lista de movimientos posibles (casillas adyacentes)
        movimientos = [(-1, -1),(-1, 0),(-1, 1),
                       (0, -1), (0, 0), (0, 1),
                       (1, -1), (1, 0), (1, 1)]

        # Mezclar la lista de movimientos para aleatoriedad
        random.shuffle(movimientos)

        for movimientoX, movimientoY in movimientos:
            destinoX = origenX + movimientoX
            destinoY = origenY + movimientoY
            # Se comprueba si el movimiento es válido
            if self.es_movimiento_valido(destinoX, destinoY):
                casilla_destino = self.juego.tablero[destinoX][destinoY]
                # Comprobar si el movimiento es (0, 0)
                if casilla_origen == casilla_destino:
                    break
                # Determinar el orden de adquisición de locks basado en las coordenadas
                if (origenX, origenY) <= (destinoX, destinoY):
                    primera_casilla = casilla_origen
                    segunda_casilla = casilla_destino
                else:
                    primera_casilla = casilla_destino
                    segunda_casilla = casilla_origen
                # Intentar moverse
                if primera_casilla.lock.acquire(blocking=False):
                    try:
                        if segunda_casilla.lock.acquire(blocking=False):
                            try:
                                if casilla_destino.animal is None:
                                    with self.juego.lock_imprimir:
                                        # Se mueve al animal
                                        casilla_origen.animal = None
                                        casilla_destino.animal = self
                                        self.posicion = (destinoX, destinoY)
                                        # Se imprime tablero actualizado
                                        indice_manada, tipo_animal, indice_animal = self.juego.obtener_indices(self)
                                        print(f"{indice_manada}{tipo_animal}{indice_animal} se mueve a la posición {self.posicion}")
                                        self.juego.imprimir_tablero()
                                        return
                            finally:
                                segunda_casilla.lock.release()
                    finally:
                        primera_casilla.lock.release()

        # No se ha movido
        with self.juego.lock_imprimir:
            indice_manada, tipo_animal, indice_animal = self.juego.obtener_indices(self)
            print(f"{indice_manada}{tipo_animal}{indice_animal} no se ha movido")
            self.juego.imprimir_tablero()

    # Función que comprueba si un movimiento es válido
    @staticmethod
    def es_movimiento_valido(x, y):
        max_x = Configuracion.SIZE_TABLERO[0]
        max_y = Configuracion.SIZE_TABLERO[1]
        return 0 <= x < max_x and 0 <= y < max_y

    # Función para contabilizar los animales aliados
    def contar_aliados(self):
        visitados = set()
        aliados_pendientes = set()
        aliados_pendientes.add(self.posicion)
        contador = 0

        while aliados_pendientes:
            posicion_actual = aliados_pendientes.pop()

            # Si la posicion actual ya ha sido visitada, la ignora
            if posicion_actual in visitados:
                continue

            # Si no, la visita y la añade a visitados
            visitados.add(posicion_actual)

            # Se declara la casilla que se va a comprobar
            actualX, actualY = posicion_actual
            casilla = self.juego.tablero[actualX][actualY]

            # Si hay un animal en la casilla y es del mismo tipo, lo cuenta como aliado
            if casilla.animal and isinstance(casilla.animal, type(self)):
                contador += 1
                # Agregar adyacentes a aliados_pendientes
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nuevaX = actualX + dx
                        nuevaY = actualY + dy
                        if self.es_movimiento_valido(nuevaX, nuevaY):
                            if (nuevaX, nuevaY) not in visitados:
                                aliados_pendientes.add((nuevaX, nuevaY))

        return contador