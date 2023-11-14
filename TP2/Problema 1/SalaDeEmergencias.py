# -*- coding: utf-8 -*-
"""
Sala de emergencias
"""

import time
import datetime
import random

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, item):
        entry = (item.get_riesgo(), item.get_contador(), item)
        self.heap.append(entry)
        self.heap.sort()  # Ordenamos la lista después de agregar un elemento

    def pop(self):
        if self.heap:
            _, _, item = self.heap.pop(0)
            return item
        else:
            raise IndexError("pop from an empty priority queue")

class Paciente:
    def __init__(self, contador):
        self.__nombre = random.choice(['Leandro', 'Mariela', 'Gastón', 'Andrea', 'Antonio', 'Estela', 'Jorge', 'Agustina'])
        self.__apellido = random.choice(['Perez', 'Colman', 'Rodriguez', 'Juarez', 'García', 'Belgrano', 'Mendez', 'Lopez'])
        self.__riesgo = random.choice([1, 2, 3])
        self.__descripcion = ['crítico', 'moderado', 'bajo'][self.__riesgo - 1]
        self.__contador = contador

    def get_nombre(self):
        return self.__nombre

    def get_apellido(self):
        return self.__apellido

    def get_riesgo(self):
        return self.__riesgo

    def get_descripcion_riesgo(self):
        return self.__descripcion

    def get_contador(self):
        return self.__contador

    def __lt__(self, other):
        # Define the less than comparison for Paciente objects
        return (self.__riesgo, self.__contador) < (other.__riesgo, other.__contador)

    def __str__(self):
        cad = f"{self.__nombre} {self.__apellido}".ljust(25) + f" -> {self.__riesgo}-{self.__descripcion}"
        return cad

n = 20  # cantidad de ciclos de simulación

cola_de_espera = PriorityQueue()

# Ciclo que gestiona la simulación
for i in range(n):
    ahora = datetime.datetime.now()
    fecha_y_hora = ahora.strftime('%d/%m/%Y %H:%M:%S')
    print('-*-' * 15)
    print('\n', fecha_y_hora, '\n')

    paciente = Paciente(i)
    cola_de_espera.push(paciente)

    if random.random() < 0.5:
        paciente_atendido = cola_de_espera.pop()
        print('*' * 40)
        print('Se atiende el paciente:', paciente_atendido)
        print('*' * 40)
    else:
        pass

    print()

    print('Pacientes que faltan atenderse:', len(cola_de_espera.heap))
    for (_, _, paciente) in cola_de_espera.heap:
        print('\t', paciente)

    print()
    print('-*-' * 15)

    time.sleep(1)

# Atender a los pacientes restantes en la cola de espera
print('\nTerminando de atender a los pacientes restantes:')
while len(cola_de_espera.heap) > 0:
    paciente_atendido = cola_de_espera.pop()
    print('*' * 40)
    print('Se atiende el paciente:', paciente_atendido)
    print('*' * 40)
    time.sleep(1)  # Agregamos un breve intervalo entre pacientes

print('\nTodos los pacientes han sido atendidos.')
