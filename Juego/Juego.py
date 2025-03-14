from Manada.ManadaCebras import ManadaCebras
from Manada.ManadaHienas import ManadaHienas
from Manada.ManadaLeones import ManadaLeones
from Animal.Cebra import Cebra
from Animal.Hiena import Hiena
from Animal.Leon import Leon
from Juego.Casilla import Casilla
from Juego import Configuracion
from random import randint
import threading
import sys

class Juego:
    def __init__(self):
        self.ganador = None
        self.leones = []
        self.hienas = []
        self.cebras = []
        self.manadas_leones = []
        self.manadas_hienas = []
        self.manadas_cebras = []
        self.lock_leones = threading.Lock()
        self.lock_hienas = threading.Lock()
        self.lock_cebras = threading.Lock()
        self.lock_ganador = threading.Lock()
        self.lock_imprimir = threading.Lock()
        self.obtener_configuracion_usuario()
        self.tablero = [[Casilla(x, y) for y in range(Configuracion.SIZE_TABLERO[1])]
                        for x in range(Configuracion.SIZE_TABLERO[0])]
        self.crear_animales()
        self.imprimir_tablero()

    # Comenzar la simulación
    def comenzar(self):
        # Iniciar hilos de los animales
        for leon in self.leones:
            leon.start()
        for hiena in self.hienas:
            hiena.start()
        for cebra in self.cebras:
            cebra.start()
        print("Todos los hilos comenzados\n")

        # Esperar a que todos los hilos terminen
        for leon in self.leones:
            leon.join()
        for hiena in self.hienas:
            hiena.join()
        for cebra in self.cebras:
            cebra.join()

        # Después de que todos los hilos han finalizado
        print("Todos los hilos han sido finalizados\n")
        print("El juego ha terminado\n")
        self.imprimir_ganador(self.ganador)

    # Función para crear los animales de la simulación
    def crear_animales(self):
        # Establecer el número total de manadas y animales de cada tipo
        num_manadas = Configuracion.NUMERO_MANADAS
        total_leones = Configuracion.NUMERO_LEONES
        total_hienas = total_leones * Configuracion.PROPORCION_LEONES_HIENAS
        total_cebras = total_leones * Configuracion.PROPORCION_LEONES_CEBRAS

        # Se comprueba si el número de animales no excede el tamaño del tablero
        total_animales = total_leones + total_hienas + total_cebras
        if total_animales > Configuracion.SIZE_TABLERO[0] * Configuracion.SIZE_TABLERO[1]:
            raise ValueError("El número total de animales excede el tamaño del tablero")

        # Distribuimos los animales en manadas utilizando Round Robin
        distribucion_leones = self.distribuir_animales_round_robin(total_leones, num_manadas)
        distribucion_hienas = self.distribuir_animales_round_robin(total_hienas, num_manadas)
        distribucion_cebras = self.distribuir_animales_round_robin(total_cebras, num_manadas)

        # Creación de manadas de leones
        for i in range(num_manadas):
            num_leones_manada = distribucion_leones[i]
            manada_leones = ManadaLeones()
            posicion_leon = (
                randint(0, Configuracion.SIZE_TABLERO[0] - 1), randint(0, Configuracion.SIZE_TABLERO[1] - 1))
            for _ in range(num_leones_manada):
                leon = Leon(self, manada_leones, posicion_leon)
                manada_leones.add_animal(leon)
                self.leones.append(leon)
                self.colocar_animal(leon, posicion_leon)
            self.manadas_leones.append(manada_leones)
        print(f"Leones creados: {self.imprimir_manadas(self.manadas_leones)}")

        # Creación de manadas de hienas
        for i in range(num_manadas):
            num_hienas_manada = distribucion_hienas[i]
            manada_hienas = ManadaHienas()
            posicion_hiena = (randint(0, Configuracion.SIZE_TABLERO[0] - 1), randint(0, Configuracion.SIZE_TABLERO[1] - 1))
            for _ in range(num_hienas_manada):
                hiena = Hiena(self, manada_hienas, posicion_hiena)
                manada_hienas.add_animal(hiena)
                self.hienas.append(hiena)
                self.colocar_animal(hiena, posicion_hiena)
            self.manadas_hienas.append(manada_hienas)
        print(f"Hienas creadas: {self.imprimir_manadas(self.manadas_hienas)}")

        # Creación de manadas de cebras
        for i in range(num_manadas):
            num_cebras_manada = distribucion_cebras[i]
            manada_cebras = ManadaCebras()
            posicion_cebra = (randint(0, Configuracion.SIZE_TABLERO[0] - 1), randint(0, Configuracion.SIZE_TABLERO[1] - 1))
            for _ in range(num_cebras_manada):
                cebra = Cebra(self, manada_cebras, posicion_cebra)
                manada_cebras.add_animal(cebra)
                self.cebras.append(cebra)
                self.colocar_animal(cebra, posicion_cebra)
            self.manadas_cebras.append(manada_cebras)
        print(f"Cebras creadas: {self.imprimir_manadas(self.manadas_cebras)}\n")

    # Funcion que intenta colocar un animal en una casilla o en alguna de sus adyacentes
    def colocar_animal(self, animal, posicion):
        x, y = posicion
        casilla = self.tablero[x][y]
        with casilla.lock:
            if casilla.animal is None:
                # La casilla está libre, se coloca el animal aquí
                casilla.animal = animal
                animal.posicion = (x, y)
                return
        # La casilla está ocupada, buscar una casilla vacía cercana
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nuevaX = x + dx
                nuevaY = y + dy
                if animal.es_movimiento_valido(nuevaX, nuevaY):
                    nueva_casilla = self.tablero[nuevaX][nuevaY]
                    if nueva_casilla.lock.acquire(blocking=False):
                        try:
                            if nueva_casilla.animal is None:
                                # Encontró una casilla vacía adyacente
                                nueva_casilla.animal = animal
                                animal.posicion = (nuevaX, nuevaY)
                                return
                        finally:
                            nueva_casilla.lock.release()
        # Si no se encuentra casilla vacía cercana, asignar posición aleatoria
        while True:
            nuevaX = randint(0, Configuracion.SIZE_TABLERO[0] - 1)
            nuevaY = randint(0, Configuracion.SIZE_TABLERO[1] - 1)
            nueva_casilla = self.tablero[nuevaX][nuevaY]
            if nueva_casilla.lock.acquire(blocking=False):
                try:
                    if nueva_casilla.animal is None:
                        nueva_casilla.animal = animal
                        animal.posicion = (nuevaX, nuevaY)
                        return
                finally:
                    nueva_casilla.lock.release()

    # Confirma el ganador del juego
    def confirmar_ganador(self, manada):
        if self.ganador is None:
            print("Ya hay ganador, terminando hilos...")
            self.ganador = manada

    # Anuncia el ganador del juego
    def imprimir_ganador(self, manada):
        with self.lock_imprimir:
            if isinstance(manada, ManadaLeones):
                print(f"¡La manada de Leones número {self.manadas_leones.index(manada)} ha ganado el juego!")
            elif isinstance(manada, ManadaHienas):
                print(f"¡La manada de Hienas número {self.manadas_hienas.index(manada)} ha ganado el juego!")
            else:
                print("¡Ha ocurrido un error al determinar el ganador!")
                exit(-1)

    # Función que imprime el tablero por pantalla
    def imprimir_tablero(self):
        # Imprimir el tablero actual
        tablero = ''
        for fila in self.tablero:
            linea = ''
            for casilla in fila:

                if casilla.animal is None:
                    linea += '[    ] '
                else:
                    if casilla.animal.cazada:
                        linea += '[    ] '
                    else:
                        # Determinar los ID de la manada, del animal y de qué animal se trata
                        indice_manada, tipo_animal, indice_animal = self.obtener_indices(casilla.animal)
                        identificador = f"{indice_manada}{tipo_animal}{indice_animal}"
                        if indice_animal < 10:
                            linea += f"[{identificador} ] "
                        else:
                            linea += f"[{identificador}] "
            tablero += f"{linea}\n"
        print("Estado actual del tablero:\n"
              f"{tablero}")

    # Obtiene los índices que identifican a cada animal (índice de la manada, tipo de animal, índice del animal)
    def obtener_indices(self, animal):
        if isinstance(animal, Leon):
            indice_manada = self.manadas_leones.index(animal.manada)
            with animal.manada.lock:
                indice_animal = animal.manada.animales.index(animal) if animal in animal.manada.animales else -1
            tipo_animal = 'L'
        elif isinstance(animal, Hiena):
            indice_manada = animal.juego.manadas_hienas.index(animal.manada)
            with animal.manada.lock:
                indice_animal = animal.manada.animales.index(animal) if animal in animal.manada.animales else -1
            tipo_animal = 'H'
        elif isinstance(animal, Cebra):
            indice_manada = animal.juego.manadas_cebras.index(animal.manada)
            with animal.manada.lock:
                indice_animal = animal.manada.animales.index(animal) if animal in animal.manada.animales else -1
            tipo_animal = 'C'
        else:
            indice_manada = -1
            indice_animal = -1
            tipo_animal = '?'
        return indice_manada, tipo_animal, indice_animal

    # Se distribuyen los animales en manadas con el metodo Round Robin
    @staticmethod
    def distribuir_animales_round_robin(num_animales, num_manadas):
        distribucion = [0] * num_manadas
        for i in range(num_animales):
            distribucion[i % num_manadas] += 1
        return distribucion

    # Imprimir las manadas de animales a principio de partida
    def imprimir_manadas(self, manadas):
        animales = ""
        for manada in manadas:
            for animal in manada.animales:
                indice_manada, tipo_animal, indice_animal = self.obtener_indices(animal)
                animales += f"{indice_manada}{tipo_animal}{indice_animal} "
            animales += ""
        return animales

    # Configuracion que se solicita al usuario
    @staticmethod
    def obtener_configuracion_usuario():
        # Solicitar tamaño del tablero
        while True:
            try:
                size_x = int(input("Introduce el tamaño X del tablero (máximo 75): "))
                size_y = int(input("Introduce el tamaño Y del tablero (máximo 75): "))

                if size_x <= 0 or size_y <= 0:
                    print("El tamaño del tablero debe ser mayor que 0. Inténtalo de nuevo.")
                    continue
                if size_x > 75 or size_y > 75:
                    print("El tamaño del tablero no puede exceder 75x75. Inténtalo de nuevo.")
                    continue
                break
            except ValueError:
                print("Por favor, introduce números válidos para el tamaño del tablero.")

        # Solicitar número de manadas
        while True:
            try:
                numero_manadas = int(input("Introduce el número de manadas (mínimo 2): "))

                if numero_manadas < 2:
                    print("Debe haber al menos 2 manadas. Inténtalo de nuevo.")
                    continue
                break
            except ValueError:
                print("Por favor, introduce un número válido para el número de manadas.")

        # Solicitar número de leones
        while True:
            try:
                numero_leones = int(input("Introduce el número de leones (habrá 3 hienas y 6 cebras por cada leon): "))

                if numero_leones < 2:
                    print("Deben haber al menos dos leones. Inténtalo de nuevo.")
                    continue
                break
            except ValueError:
                print("Por favor, introduce un número válido para el número de leones.")

        # Asignar valores a la clase Configuracion
        Configuracion.SIZE_TABLERO = (size_x, size_y)
        Configuracion.NUMERO_LEONES = numero_leones
        Configuracion.NUMERO_MANADAS = numero_manadas

        # Calcular total de animales y validar contra el tamaño del tablero
        total_leones = Configuracion.NUMERO_LEONES
        total_hienas = total_leones * Configuracion.PROPORCION_LEONES_HIENAS
        total_cebras = total_leones * Configuracion.PROPORCION_LEONES_CEBRAS
        total_animales = total_leones + total_hienas + total_cebras
        size_tablero = Configuracion.SIZE_TABLERO[0] * Configuracion.SIZE_TABLERO[1]

        if total_animales > size_tablero:
            print(f"El número total de animales ({total_animales}) excede el tamaño del tablero ({size_tablero}).")
            print("Por favor, ajusta los valores e intenta de nuevo.")
            sys.exit(1)

        print("\nConfiguración del juego:")
        print(f"Tamaño del tablero: {Configuracion.SIZE_TABLERO[0]}x{Configuracion.SIZE_TABLERO[1]}")
        print(f"Número de manadas: {Configuracion.NUMERO_MANADAS}")
        print(f"Número de leones: {Configuracion.NUMERO_LEONES}")
        print(f"Número de hienas: {total_hienas}")
        print(f"Número de cebras: {total_cebras}\n")
