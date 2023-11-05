import heapq
import os

class Movimiento:
    """Conexión entre dos ciudades con su peso máximo admitido y precio."""
    def __init__(self, ciudad_origen, ciudad_destino, peso, precio):
        self.ciudad_origen = ciudad_origen
        self.ciudad_destino = ciudad_destino
        self.peso_mx = peso  # Capacidad máxima de peso admitida en kg
        self.precio = precio  # Precio en unidades de 1000
        self.nombre = ciudad_destino  # Agregar el atributo nombre para comparaciones

    def __lt__(self, otro_movimiento):
        return self.precio < otro_movimiento.precio

class Vertice:
    """Representa nodos que son los nombres de las ciudades, hace un seguimiento sobre el nodo, si este fue visitado o no,
      y guarda los movimientos (rutas) desde un nodo al otro, junto con su peso máximo admitido y precio."""
    def __init__(self, nombre):
        self.nombre = nombre
        self.visitado = False
        self.vecinos = []
        self.distancia = float('inf')
        self.predecesor = None

    def agregar_vecino(self, ciudad_destino, peso, precio):
        movimiento = Movimiento(self.nombre, ciudad_destino, peso, precio)
        self.vecinos.append(movimiento)

    def obtenerConexiones(self):
        return self.vecinos

    def obtenerPonderacion(self, vertice):
        for movimiento in self.vecinos:
            if movimiento.ciudad_destino == vertice.nombre:
                return movimiento.precio
        return float('inf')

    def __lt__(self, otro_vertice):
        return self.distancia < otro_vertice.distancia

class Grafo:
    """Grafo que contiene ciudades y sus conexiones, contiene 2 métodos para agregar vértices al grafo, y agregar movimientos
     para guardar en el grafo el movimiento de la ciudad de origen (CiudadBs.As. en este caso) a una ciudad destino cualquiera
      justo con si peso máximo admitido y precio del recorrido."""
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
        self.claves = {}  # Diccionario para mantener las claves

    def estaVacia(self):
        return len(self.heap) == 0

    def construirMonticulo(self, lista):
        heapq.heapify(lista)
        self.heap = lista
        # Inicializar el diccionario de claves
        self.claves = {vertice: indice for indice, (_, vertice) in enumerate(self.heap)}

    def eliminarMin(self):
        if not self.estaVacia():
            distancia, vertice = heapq.heappop(self.heap)
            del self.claves[vertice]  # Eliminar la clave del diccionario
            return distancia, vertice
        else:
            raise IndexError("La cola de prioridad está vacía")

    def decrementarClave(self, vertice, nuevaDistancia):
        nombre_vertice = vertice.nombre  # Obtener el nombre del vértice
        if nombre_vertice in self.claves:
            indice = self.claves[nombre_vertice]
            self.heap[indice] = (nuevaDistancia, vertice)

def dijkstra(unGrafo, inicio):
    cp = ColaPrioridad()
    inicio.distancia = 0
    cp.construirMonticulo([(v.distancia, v) for v in unGrafo.vertices.values()])
    
    while not cp.estaVacia():
        distancia, verticeActual = cp.eliminarMin()  # Obtener el vértice actual del heap
        for movimiento in verticeActual.obtenerConexiones():  # Iterar sobre los movimientos del vértice
            verticeSiguiente = unGrafo.vertices[movimiento.ciudad_destino]  # Obtener el vértice siguiente
            nuevaDistancia = distancia + movimiento.precio
            if nuevaDistancia < verticeSiguiente.distancia:
                verticeSiguiente.distancia = nuevaDistancia
                verticeSiguiente.predecesor = verticeActual
                cp.decrementarClave(verticeSiguiente, nuevaDistancia)

def encontrar_peso_precio_minimo(unGrafo, ciudad_origen):
    resultados = {}  # Diccionario para almacenar el peso máximo y el precio mínimo para cada ciudad destino

    dijkstra(unGrafo, unGrafo.vertices[ciudad_origen])  # Ejecutar Dijkstra una vez para la ciudad de origen

    for ciudad_destino, vertice_destino in unGrafo.vertices.items():
        if ciudad_destino != ciudad_origen and vertice_destino.distancia != float('inf'):
            # Verificar si es alcanzable desde CiudadBs.As.
            cuello_botella = vertice_destino.predecesor.obtenerPonderacion(vertice_destino)
            precio_min = vertice_destino.distancia
            resultados[ciudad_destino] = (precio_min, cuello_botella)

    return resultados

# Crear el grafo y cargar datos desde el archivo
grafo = Grafo()
ruta_del_archivo = os.path.abspath("/home/dany/Escritorio/Nueva carpeta/algoritmos/TP-AyED/ejerciciosTP2/rutas.txt")  # Obtener la ruta absoluta del archivo de entrada

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

# Verificar si la ciudad de origen está en el grafo
ciudad_origen = "CiudadBs.As."
if ciudad_origen in grafo.vertices:
    resultados = encontrar_peso_precio_minimo(grafo, ciudad_origen)

    print("Ciudades destino desde CiudadBs.As.:")
    for ciudad_destino, cuello_botella in resultados.items():
        if cuello_botella != float('inf'):  # Verificar si es alcanzable desde CiudadBs.As.
            print(f"Para llegar a {ciudad_destino}:")
            print(f"Precio mínimo: {cuello_botella[0]} unidades de 1000.")
            print(f"Peso máximo que se puede transportar: {cuello_botella[1]} kg.")
            print("-----")
else:
    print(f"La ciudad de origen '{ciudad_origen}' no se encuentra en el grafo.")
