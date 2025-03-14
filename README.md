# 🦁 Simulación de la Sabana Africana 🌿
## 📌 Descripción
Este proyecto es una simulación de un ecosistema de la Sabana Africana, donde diferentes especies de animales (leones, hienas y cebras) interactúan en un entorno con un tablero de tamaño configurable.

El programa utiliza hilos (threads) en Python para simular el comportamiento independiente de cada animal, incluyendo su movimiento, descanso y comportamiento de caza.

La simulación se desarrolla siguiendo las siguientes reglas:
- Los leones cazan cebras y pueden cazar hienas si hay suficientes aliados cercanos.
- Las hienas cazan cebras en grupo.
- Las cebras solo se mueven por el tablero y pueden ser cazadas.
- La simulación termina cuando una de las manadas alcanza la puntuación requerida.

## 🛠️ Tecnologías utilizadas
- Python 3.x (Lenguaje principal).
- Programación Orientada a Objetos (POO).
- Hilos (threading) en Python para concurrencia.
- Bloqueos (Locks) para evitar condiciones de carrera y garantizar la integridad de los datos.
- Modelo basado en agentes para simular las interacciones entre animales.
- Sistema de configuración dinámica para definir el tamaño del tablero y el número de animales.

## 📥 Instalación
### 1️⃣ Requisitos previos
Asegúrate de tener Python 3.8 o superior instalado en tu sistema. Puedes comprobar tu versión con:
```bash
python --version
```

### 2️⃣ Clonar el repositorio
Clona el repositorio en tu máquina local con:
```bash
git clone https://github.com/alexbercom/Simulacion-Sabana-Africana.git
cd Simulacion-Sabana-Africana
```

## ▶️ Ejecución del programa
Para ejecutar la simulación, simplemente ejecuta el archivo main.py

El programa solicitará la configuración del juego:
  - Ingrese el tamaño del tablero (máx. 75x75): (Ejemplo: 20x20)
  - Ingrese el número de manadas (mínimo 2): (Ejemplo: 4)
  - Ingrese el número de leones por manada: (Ejemplo: 10)

Luego, la simulación comenzará mostrando el estado inicial del tablero y los movimientos de los animales hasta que una manada gane.

## 🏗️ Estructura del Proyecto
Animal/: Clases base y específicas para cada tipo de animal:
  - Animal: Clase base para que todos los tipos de animales hereden de ella.
  - Depredador: Clase base para que Leon y Hiena hereden de ella.
  - León: Clase para el comportamiento de los leones.
  - Hiena: Clase para el comportamiento de las hienas.
  - Cebra: Clase para el comportamiento de las cebras.

Manada/: Manejo de los diferentes tipos de manadas:
  - Manada: Clase base para que las diferentes manadas hereden de ella.
  - ManadaLeones
  - ManadaHienas
  - ManadaCebras

Juego/: Clases relacionadas con el funcionamiento del juego:
  - Casilla: Representación del tablero con bloqueos para evitar movimientos inválidos.
  - Configuracion: Configuración del juego.
  - Juego: Lógica principal del juego, manejo del tablero y flujo de la simulación.

main: Archivo principal que inicia la simulación.

## ⚙️ Funcionamiento del Programa
1. Configuración Inicial:
   - El usuario introduce el tamaño del tablero y el número de manadas.
   - Se distribuyen los animales en el tablero siguiendo el algoritmo Round Robin.

2. Inicio de la simulación:
   - Cada animal se ejecuta en su propio hilo (thread).
   - Los leones y hienas buscan presas y cazan si es posible.
   - Las cebras se mueven aleatoriamente para evitar ser cazadas.
   - Cada ciclo representa una unidad de tiempo en la simulación.

3. Caza y Eliminación:
   - Los depredadores verifican si hay presas cerca antes de moverse.
   - Si una cebra es cazada, se genera una nueva en el mismo lugar.
   - Se suman puntos por caza hasta que una manada alcanza la puntuación requerida.

4. Finalización:
   - El programa muestra la manada ganadora y detiene todos los hilos.

## 📝 Reglas del Juego
- Un león puede cazar una cebra si está adyacente.
- Un león puede cazar una hiena solo si hay más leones que hienas cerca.
- Una hiena puede cazar una cebra si hay más hienas que cebras en la zona.
- Si una cebra es cazada, se genera una nueva en la misma posición.
- El juego finaliza cuando una manada alcanza la puntuación requerida.

## 👨‍💻 Autor
Alex Bermejo Compán
