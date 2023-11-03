import random
import timeit
import matplotlib.pyplot as plt
from modulos_ListaDobleEnlazada import ListaDobleEnlazada

"""La función genera y devuelve una lista de tamaño n con valores aleatorios entre 1 y 1000."""
def generar_lista_aleatoria(n):
    return [random.randint(1, 1000) for _ in range(n)]

"""La función genera una lista de valores aleatorios de tamaño n utilizando la función generar_lista_aleatoria y 
luego agrega esos valores a la lista doblemente enlazada lista utilizando el método agregar_al_final."""
def llenar_lista(lista, n):
    valores = generar_lista_aleatoria(n)
    for valor in valores:
        lista.agregar_al_final(valor)

"""para medir el tiempo que toma ejecutar el método ordenar de la lista y devuelve ese tiempo en segundos."""
def medir_tiempo_ordenamiento(lista):
    tiempo = timeit.timeit(lambda: lista.ordenar(), number=1)
    return tiempo

"""Esta línea crea una lista llamada tamanios que contiene los tamaños de las listas que se 
utilizarán para medir el rendimiento del algoritmo de ordenamiento."""
tamanios = [10, 100, 500, 1000, 2000]

# Mide el tiempo para cada tamaño de entrada y guarda los tiempos en una lista
tiempos = []

for n in tamanios:
    lista = ListaDobleEnlazada()
    llenar_lista(lista, n)
    tiempo = medir_tiempo_ordenamiento(lista)
    tiempos.append(tiempo)

# Grafica los resultados
plt.plot(tamanios, tiempos, marker='o')
plt.xlabel('Número de Elementos')
plt.ylabel('Tiempo de Ejecución (segundos)')
plt.title('orden de complejidad del algoritmo de ordenamiento Burbuja')
plt.show()
