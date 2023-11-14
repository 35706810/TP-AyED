import heapq
import os

class Movimiento:
    def __init__(self, ciudad_origen, ciudad_destino, peso, precio):
        self.ciudad_origen = ciudad_origen
        self.ciudad_destino = ciudad_destino
        self.peso_max = peso
        self.precio = precio

    def __lt__(self, otro_movimiento):
        return self.peso_max > otro_movimiento.peso_max  # Modificado para ordenar por peso máximo descendente

class Vertice:
    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = []
        self.distancia = float('inf')  # Iniciar con distancia infinita
        self.predecesor = None

    def agregar_vecino(self, ciudad_destino, peso, precio):
        movimiento = Movimiento(self.nombre, ciudad_destino, peso, precio)
        self.vecinos.append(movimiento)

    def obtener_conexiones(self):
        return self.vecinos

    def obtener_ponderacion(self, vertice):
        for movimiento in self.vecinos:
            if movimiento.ciudad_destino == vertice.nombre:
                return movimiento.peso_max
        return float('-inf')  # Modificado para retornar la ponderación mínima

    def __lt__(self, otro_vertice):
        return self.distancia > otro_vertice.distancia  # Modificado para ordenar por distancia máxima

class Grafo:
    def __init__(self):
        self.vertices = {}

    def agregar_vertice(self, nombre):
        vertice = Vertice(nombre)
        self.vertices[nombre] = vertice

    def agregar_movimiento(self, ciudad_origen, ciudad_destino, peso, precio):
        self.vertices[ciudad_origen].agregar_vecino(ciudad_destino, peso, precio)

class ColaPrioridad:
    def __init__(self):
        self.heap = []

    def esta_vacia(self):
        return len(self.heap) == 0

    def insertar(self, item):
        heapq.heappush(self.heap, item)

    def eliminar_min(self):
        if not self.esta_vacia():
            return heapq.heappop(self.heap)
        else:
            raise IndexError("La cola de prioridad está vacía")

def dijkstra(un_grafo, inicio):
    cp = ColaPrioridad()
    inicio.distancia = 0
    cp.insertar((0, inicio.nombre, inicio))
    
    while not cp.esta_vacia():
        distancia, _, vertice_actual = cp.eliminar_min()
        for movimiento in vertice_actual.obtener_conexiones():
            vertice_siguiente = un_grafo.vertices[movimiento.ciudad_destino]
            nueva_distancia = distancia + movimiento.precio  # Modificado para obtener el precio acumulado
            if nueva_distancia < vertice_siguiente.distancia:
                vertice_siguiente.distancia = nueva_distancia
                vertice_siguiente.predecesor = vertice_actual
                cp.insertar((nueva_distancia, vertice_siguiente.nombre, vertice_siguiente))

def encontrar_precio_peso_minimo(un_grafo, ciudad_origen):
    resultados = {}

    dijkstra(un_grafo, un_grafo.vertices[ciudad_origen])

    for ciudad_destino, vertice_destino in un_grafo.vertices.items():
        if ciudad_destino != ciudad_origen and vertice_destino.distancia != float('inf') and vertice_destino.predecesor is not None:
            cuello_botella = vertice_destino.predecesor.obtener_ponderacion(vertice_destino)
            precio_min = vertice_destino.distancia
            resultados[ciudad_destino] = (precio_min, cuello_botella)

    return resultados

# Crear el grafo y cargar datos desde el archivo
grafo = Grafo()
ruta_del_archivo = os.path.abspath("/home/dany/Escritorio/Nueva carpeta/ejerciciosTP2/ejercicio3/rutas.txt")

try:
    with open(ruta_del_archivo, 'r') as arch_ruta:
        for linea in arch_ruta:
            datos = linea.strip().split(',')
            ciudad_origen = datos[0]
            ciudad_destino = datos[1]
            peso = int(datos[2])
            precio = int(datos[3])
            if ciudad_origen not in grafo.vertices:
                grafo.agregar_vertice(ciudad_origen)
            if ciudad_destino not in grafo.vertices:
                grafo.agregar_vertice(ciudad_destino)
            grafo.agregar_movimiento(ciudad_origen, ciudad_destino, peso, precio)

except FileNotFoundError:
    print("El archivo no se encuentra.")
except Exception as error:
    print(f"Error: {error}")

if "CiudadBs.As." in grafo.vertices:
    ciudad_origen = "CiudadBs.As."
    resultados = encontrar_precio_peso_minimo(grafo, ciudad_origen)

    for ciudad_destino, valores in resultados.items():
        print(f"Desde {ciudad_origen} a {ciudad_destino}:")
        print(f"  Precio mínimo: ${valores[0]}")
        print(f"  Cuello de botella (peso máximo): {valores[1]} kg")
else:
    print(f"La ciudad de origen 'CiudadBs.As.' no se encuentra en el grafo.")
