import random

class Carta:
    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo

    def __str__(self):
        return f"{self.valor}{self.palo}"

class Nodo:
    def __init__(self, dato=None):
        self.dato = dato
        self.siguiente = None

class Mazo:
    def __init__(self):
        self.lista_cartas = None

    def poner_arriba(self, carta):
        nuevo_nodo = Nodo(carta)
        nuevo_nodo.siguiente = self.lista_cartas
        self.lista_cartas = nuevo_nodo

    def sacar_arriba(self):
        if self.lista_cartas is None:
            return None
        carta = self.lista_cartas.dato
        self.lista_cartas = self.lista_cartas.siguiente
        return carta

    def poner_abajo(self, carta):
        nuevo_nodo = Nodo(carta)
        if self.lista_cartas is None:
            self.lista_cartas = nuevo_nodo
        else:
            current = self.lista_cartas
            while current.siguiente is not None:
                current = current.siguiente
            current.siguiente = nuevo_nodo

    def obtener_cabeza(self):
        if self.lista_cartas:
            return self.lista_cartas.dato
        else:
            return None

    def obtener_cola(self):
        if self.lista_cartas is None:
            return None
        current = self.lista_cartas
        while current.siguiente is not None:
            current = current.siguiente
        return current.dato

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self._mano = Mazo()

    def agregar_cartas_al_final(self, cartas):
        for carta in cartas:
            self._mano.poner_abajo(carta)

    def tamano_mano(self):
        current = self._mano.lista_cartas
        count = 0
        while current is not None:
            count += 1
            current = current.siguiente
        return count

    def tirar_carta(self):
        return self._mano.sacar_arriba()

class JuegoGuerra:
    def __init__(self, jugador1, jugador2):
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.lista_cartas = Mazo()

        self.crear_y_mezclar_mazo()

        self.turno = 0

    def crear_y_mezclar_mazo(self):
        try:
            valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            palos = ['\u2660', '\u2663', '\u2665', '\u2666']
            mazo_cartas = [Carta(valor, palo) for valor in valores for palo in palos]

            random.shuffle(mazo_cartas)

            for carta in mazo_cartas:
                self.lista_cartas.poner_abajo(carta)

        except Exception as e:
            print("Error al crear el mazo:", str(e))

    def imprimir_mano(self, carta1, carta2):
        print("=" * 80)
        print(f"Turno: {self.turno}")
        print("Jugador 1:")
        for _ in range(self.jugador1.tamano_mano()):
            print("-X", end=' ')
        print("\nJugador 2:")
        for _ in range(self.jugador2.tamano_mano()):
            print("-X", end=' ')
        print(f"\nCartas comparadas: {str(carta1)} vs {str(carta2)}")

    def comparar_cartas(self, carta1, carta2):
        valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        try:
            valor1 = valores.index(carta1.valor)
            valor2 = valores.index(carta2.valor)
            return valor1 - valor2
        except ValueError:
            print("Error al comparar cartas. Valor no encontrado.")
            return 0

    def mostrar_cartas_enfrentadas(self, carta1, carta2, tributo):
        espacio = " " * 6
        if tributo:  
            linea_jugador1 = f"{str(carta1)} vs {str(carta2)}"
            cartas_enfrentadas = ' '.join(map(lambda x: "-X", tributo))
            print("\n" + espacio + linea_jugador1 + " " + cartas_enfrentadas)

    def jugar_ronda(self):
        try:
            self.turno += 1

            if self.jugador1.tamano_mano() == 0:
                print("¡Jugador 1 se ha quedado sin cartas!")
                print("¡Jugador 2 gana la partida!")
                return
            elif self.jugador2.tamano_mano() == 0:
                print("¡Jugador 2 se ha quedado sin cartas!")
                print("¡Jugador 1 gana la partida!")
                return

            carta1 = self.jugador1.tirar_carta()
            carta2 = self.jugador2.tirar_carta()

            resultado = self.comparar_cartas(carta1, carta2)

            self.imprimir_mano(carta1, carta2)

            if resultado > 0:
                self.jugador1.agregar_cartas_al_final([carta1, carta2])
                print(f"Jugador 1 gana la ronda.")
            elif resultado < 0:
                self.jugador2.agregar_cartas_al_final([carta2, carta1])
                print(f"Jugador 2 gana la ronda.")
            else:
                print("\n" + " " * 8 + "***GUERRA***")
                tributo = []

                for _ in range(3):
                    if self.jugador1.tamano_mano() > 0:
                        tributo.append(self.jugador1.tirar_carta())
                    if self.jugador2.tamano_mano() > 0:
                        tributo.append(self.jugador2.tirar_carta())

                mesa = [carta1, carta2] + tributo
                self.mostrar_cartas_enfrentadas(carta1, carta2, tributo)

                carta1_volteada = self.jugador1.tirar_carta() if self.jugador1.tamano_mano() > 0 else None
                carta2_volteada = self.jugador2.tirar_carta() if self.jugador2.tamano_mano() > 0 else None

                if carta1_volteada and carta2_volteada:
                    resultado = self.comparar_cartas(carta1_volteada, carta2_volteada)
                    self.imprimir_mano(carta1_volteada, carta2_volteada)

                    if resultado > 0:
                        guerra_resultado = [carta1, carta2] + tributo + [carta1_volteada, carta2_volteada]
                        self.jugador1.agregar_cartas_al_final(guerra_resultado)
                        print(f"Jugador 1 gana la guerra.")
                    else:
                        guerra_resultado = [carta2, carta1] + tributo + [carta2_volteada, carta1_volteada]
                        self.jugador2.agregar_cartas_al_final(guerra_resultado)
                        print(f"Jugador 2 gana la guerra.")
                else:
                    tributo.extend(mesa)
                    self.jugador1.agregar_cartas_al_final([carta1] + tributo + [carta2])
                    print(f"Jugador 1 gana la guerra por falta de cartas.")
        except Exception as e:
            print("Error al jugar la ronda:", str(e))

    def obtener_mazo(self):
        return self.lista_cartas.obtener_cabeza()

    def jugar(self, max_turnos):
        try:
            while self.jugador1.tamano_mano() > 0 and self.jugador2.tamano_mano() > 0 and self.turno < max_turnos:
                self.jugar_ronda()

            print("=" * 80)
            if self.turno == max_turnos:
                print("¡Empate! Se ha alcanzado el máximo de turnos.")
            elif self.jugador1.tamano_mano() > 0:
                print("¡Jugador 1 gana la partida!")
            else:
                print("¡Jugador 2 gana la partida!")
        except Exception as e:
            print("Error al jugar la partida:", str(e))

# Crear dos jugadores
try:
    jugador1 = Jugador("Jugador 1")
    jugador2 = Jugador("Jugador 2")
except Exception as e:
    print("Error al crear los jugadores:", str(e))
    exit(1)

# Crear el juego de Guerra
try:
    juego = JuegoGuerra(jugador1, jugador2)
except Exception as e:
    print("Error al crear el juego:", str(e))
    exit(1)

# Repartir las cartas a cada jugador
try:
    for i in range(0, 26):  
        carta1 = juego.lista_cartas.sacar_arriba()
        jugador1.agregar_cartas_al_final([carta1])

        carta2 = juego.lista_cartas.sacar_arriba()
        jugador2.agregar_cartas_al_final([carta2])
except Exception as e:
    print("Error al repartir las cartas:", str(e))
    exit(1)

# Jugar la partida con un máximo de 1000 turnos.
try:
    juego.jugar(max_turnos=1000)
except Exception as e:
    print("Error al jugar la partida:", str(e))
