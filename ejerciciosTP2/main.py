import datetime
import time
import random

class Nodo:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class ABB:
    def __init__(self):
        self.raiz = None
        self.tamano = 0

    def agregar(self, clave, valor):
        self.raiz = self._agregar_recursivamente(self.raiz, clave, valor)
        self.tamano += 1

    def _agregar_recursivamente(self, nodo, clave, valor):
        if nodo is None:
            return Nodo(clave, valor)
        if clave < nodo.clave:
            nodo.izquierda = self._agregar_recursivamente(nodo.izquierda, clave, valor)
        else:
            nodo.derecha = self._agregar_recursivamente(nodo.derecha, clave, valor)
        return nodo

    def eliminar(self, clave):
        if self.raiz is not None:
            self.raiz = self._eliminar_recursivamente(self.raiz, clave)
            self.tamano -= 1

    def _eliminar_recursivamente(self, nodo, clave):
        if nodo is None:
            raise ValueError(f"La clave {clave} no existe en el árbol")

        if clave < nodo.clave:
            nodo.izquierda = self._eliminar_recursivamente(nodo.izquierda, clave)
        elif clave > nodo.clave:
            nodo.derecha = self._eliminar_recursivamente(nodo.derecha, clave)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda

            nodo.clave = self._encontrar_minimo(nodo.derecha).clave
            nodo.derecha = self._eliminar_minimo(nodo.derecha)

        return nodo

    def _encontrar_minimo(self, nodo):
        while nodo.izquierda is not None:
            nodo = nodo.izquierda
        return nodo

    def _eliminar_minimo(self, nodo):
        if nodo.izquierda is None:
            return nodo.derecha
        nodo.izquierda = self._eliminar_minimo(nodo.izquierda)
        return nodo

    def obtener_max_prioridad(self):
        if self.raiz is not None:
            return self._encontrar_max_prioridad(self.raiz).valor
        return None

    def _encontrar_max_prioridad(self, nodo):
        while nodo.derecha is not None:
            nodo = nodo.derecha
        return nodo

    def __iter__(self):
        return self._inorden(self.raiz)

    def _inorden(self, nodo):
        if nodo is not None:
            yield from self._inorden(nodo.izquierda)
            yield (nodo.clave, nodo.valor)
            yield from self._inorden(nodo.derecha)

    def __len__(self):
        return self.tamano

    def __contains__(self, clave):
        return self._contiene_recursivamente(self.raiz, clave)

    def _contiene_recursivamente(self, nodo, clave):
        if nodo is None:
            return False

        if clave == nodo.clave:
            return True

        if clave < nodo.clave:
            return self._contiene_recursivamente(nodo.izquierda, clave)
        else:
            return self._contiene_recursivamente(nodo.derecha, clave)

    def obtener(self, clave):
        return self._obtener_recursivamente(self.raiz, clave)

    def _obtener_recursivamente(self, nodo, clave):
        if nodo is None:
            return None

        if clave == nodo.clave:
            return nodo.valor

    def __getitem__(self, clave):
        return self.obtener(clave)

    def __setitem__(self, clave, valor):
        self.agregar(clave, valor)

    def __delitem__(self, clave):
        self.eliminar(clave)

class Paciente:
    def __init__(self):
        self.nombre = self.generar_nombre()
        self.riesgo = self.generar_riesgo()
        self.izquierda = None
        self.derecha = None

    def generar_nombre(self):
        nombres = ['Andrea', 'Antonio', 'Estela', 'Gastón', 'Jorge', 'Leandro', 'Mariela', 'Agustina']
        apellidos = ['Lopez', 'Juarez', 'Rodriguez', 'García', 'Belgrano', 'Perez', 'Colman', 'Mendez']
        nombre_completo = random.choice(nombres) + ' ' + random.choice(apellidos)
        return nombre_completo

    def generar_riesgo(self):
        return random.randint(1, 3)

    def get_riesgo(self):
        return self.riesgo

    def __str__(self):
        riesgo_str = '1-crítico' if self.riesgo == 1 else '2-moderado' if self.riesgo == 2 else '3-bajo'
        return f"{self.nombre} -> {riesgo_str}"

if __name__ == "__main__":
    n = 10  # Número de pacientes a simular

    cola_de_espera = ABB()

    for i in range(n):
        ahora = datetime.datetime.now()
        fecha_y_hora = ahora.strftime('%d/%m/%Y %H:%M:%S')
        print('*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-\n')
        print(f"{fecha_y_hora}\n")

        paciente = Paciente()
        # Agregar paciente usando la notación de corchetes
        cola_de_espera[paciente.riesgo] = paciente

        print("Pacientes en espera:")
        for clave, valor in cola_de_espera:
            print(valor)

    while len(cola_de_espera) > 0:
        paciente_atendido = cola_de_espera.obtener_max_prioridad()
        if paciente_atendido:
            ahora = datetime.datetime.now()
            fecha_y_hora = ahora.strftime('%d/%m/%Y %H:%M:%S')
            print('*' * 40)
            print(f"{fecha_y_hora}\nSe atiende al paciente:\n{paciente_atendido}")
            print('*' * 40)
            # Eliminar paciente usando la notación de corchetes
            del cola_de_espera[paciente_atendido.riesgo]

        print("Pacientes en espera:")
        for clave, valor in cola_de_espera:
            print(valor)

        print('Pacientes que faltan por atenderse:', len(cola_de_espera))
        print()
        print('*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-')
        time.sleep(1)  # Espera 1 segundo antes de continuar
