from abc import abstractmethod
from Animal.Animal import Animal

class Depredador(Animal):
    @abstractmethod
    def run(self):
        """ Este metodo se queda en blanco, se debe de implementar en las clases hijas """
        raise NotImplementedError("Método `run` debe ser implementado por subclases.")

    @abstractmethod
    def descansar(self):
        """ Este metodo se queda en blanco, se debe de implementar en las clases hijas """
        raise NotImplementedError("Método `run` debe ser implementado por subclases.")

    # Función que hace comprobaciones para ver si es posible cazar, y si se puede, devuelve la presa
    def intentar_cazar(self):
        from Animal.Cebra import Cebra
        from Animal.Hiena import Hiena
        from Animal.Leon import Leon
        posiciones_adyacentes = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if not (dx == 0 and dy == 0):
                    x = self.posicion[0] + dx
                    y = self.posicion[1] + dy
                    posiciones_adyacentes.append((x, y))
        for x, y in posiciones_adyacentes:
            if not self.es_movimiento_valido(x, y):
                continue
            casilla = self.juego.tablero[x][y]
            if casilla.lock.acquire(blocking=False):
                try:
                    if not casilla.animal is None and casilla.animal.cazada == False:
                        presa = casilla.animal
                        with presa.lock_cazada:
                            if isinstance(self, Leon):
                                if isinstance(presa, Cebra):
                                    return presa
                                elif isinstance(presa, Hiena):
                                    num_leones = self.contar_aliados()
                                    num_hienas = presa.contar_aliados()
                                    if num_leones >= num_hienas > 0:
                                        return presa
                            elif isinstance(self, Hiena):
                                if isinstance(presa, Cebra):
                                    num_hienas = self.contar_aliados()
                                    num_cebras = presa.contar_aliados()
                                    if num_hienas > num_cebras > 0:
                                        return presa
                finally:
                    casilla.lock.release()
        return None

    # Se marca la presa como cazada, se notifica terminando los hilos y eliminando el animal del juego
    def cazar(self, presa):
        # Importación dentro de la función para evitar error de importación circular
        from Animal.Cebra import Cebra
        from Animal.Hiena import Hiena
        from Animal.Leon import Leon

        # Si ya ha sido cazada, no intenta cazarla
        if presa.cazada:
            return

        # Se protege cazada para marcar como cazado al animal y que así termine su hilo
        with presa.lock_cazada:
            presa.cazada = True

        casilla_presa = self.juego.tablero[presa.posicion[0]][presa.posicion[1]]

        # Se protege imprimir para que no cambien los datos que se van a imprimir y que así estén actualizados
        with self.juego.lock_imprimir:
            # Se protege la casilla para quitar el animal
            with casilla_presa.lock:
                # Se quita el animal
                casilla_presa.animal = None

                # Se imprime la caza
                indice_manada_cazador, tipo_cazador, indice_animal_cazador = self.juego.obtener_indices(self)
                indice_manada_presa, tipo_presa, indice_animal_presa = self.juego.obtener_indices(presa)
                print(f"{indice_manada_cazador}{tipo_cazador}{indice_animal_cazador} en la posición {self.posicion} "
                      f"ha cazado a {indice_manada_presa}{tipo_presa}{indice_animal_presa} en la posición {presa.posicion}")

                if self.juego.ganador is None:
                    # Actualizar puntuación
                    if isinstance(self, Leon):
                        if isinstance(presa, Cebra):
                            with presa.lock_puntuacion:
                                self.manada.puntuacion += 1
                        elif isinstance(presa, Hiena):
                            with presa.lock_puntuacion:
                                self.manada.puntuacion += 2
                    elif isinstance(self, Hiena):
                        if isinstance(presa, Cebra):
                            with presa.lock_puntuacion:
                                self.manada.puntuacion += 1

            # Imprimir tablero y puntuación actualizada
            if self.juego.ganador is None:
                self.mostrar_puntuaciones()
                self.juego.imprimir_tablero()

        # Esperar a que el hilo de la presa finalice
        presa.join()

        # Después de que el hilo ha terminado, eliminar el animal de las listas
        if isinstance(presa, Hiena):
            with self.juego.lock_hienas:
                presa.juego.hienas.remove(presa)
            with presa.manada.lock:
                presa.manada.eliminar_animal(presa)
        elif isinstance(presa, Cebra):
            with self.juego.lock_cebras:
                presa.juego.cebras.remove(presa)
            with presa.manada.lock:
                presa.manada.eliminar_animal(presa)

        # Verificar si la manada ha ganado y antes de confirmar el ganador comprobar si ya ha ganado alguien antes
        if self.manada.puntuacion >= 20:
            if self.juego.lock_ganador.acquire(blocking=False) and self.juego.ganador is None:
                try:
                    if self.juego.ganador is None:
                        self.juego.confirmar_ganador(self.manada)
                        return
                finally:
                    self.juego.lock_ganador.release()

        # Notificar caza para que se genere una nueva cebra
        if isinstance(presa, Cebra):
            # Se protege imprimir para que se imprima junto la generación de una nueva cebra y el tablero actualizado
            with self.juego.lock_imprimir:
                presa.notificar_caza()
                self.juego.imprimir_tablero()

    # Funcion para mostrar por pantalla las puntuaciones
    def mostrar_puntuaciones(self):
        print("\nPuntuaciones")
        for manada in self.juego.manadas_leones:
            print(f"{self.juego.manadas_leones.index(manada)}L: {manada.puntuacion} ptos")
        for manada in self.juego.manadas_hienas:
            print(f"{self.juego.manadas_hienas.index(manada)}H: {manada.puntuacion} ptos")
        print("")

