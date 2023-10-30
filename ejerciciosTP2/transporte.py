class Movimiento:
    """Conexión entre dos ciudades con su peso máximo admitido y precio."""
    def __init__(self, ciudad_origen, ciudad_destino, peso, precio):
        self.ciudad_origen = ciudad_origen
        self.ciudad_destino = ciudad_destino
        self.peso_mx = peso  # Capacidad máxima de peso admitida en kg
        self.precio = precio  # Precio en unidades de 1000

class Vertice:
    """Representa nodos que son los nombres de las ciudades, hace un seguimiento sobre el nodo, si este fue visitado o no,
      y guarda los movimientos (rutas) desde un nodo al otro, junto con su peso máximo admitido y precio."""
    def __init__(self, nombre):
        self.nombre = nombre
        self.visitado = False
        self.vecinos = []

    def agregar_vecino(self, ciudad_destino, peso, precio):
        movimiento = Movimiento(self.nombre, ciudad_destino, peso, precio)
        self.vecinos.append(movimiento)

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

def buscar_precio_minimo(vertice, max_cuello_botella):
    """Función auxiliar para buscar el precio mínimo recursivamente."""
    if not vertice.vecinos:
        # Si no hay rutas disponibles, el precio mínimo es 0
        return 0
    vertice.visitado = True
    precio_min = float('inf')
    for movimiento in vertice.vecinos:
        ciudad_destino_objeto = grafo.vertices[movimiento.ciudad_destino]
        if not ciudad_destino_objeto.visitado and movimiento.peso_mx <= max_cuello_botella:
            precio_ruta_actual = movimiento.precio
            precio_min = min(precio_min, precio_ruta_actual)
    return precio_min

def encontrar_cuello_botella(grafo, ciudad_origen, ciudad_destino):
    """Determina el cuello de botella desde la ciudad de origen a la destino en el grafo."""
    max_cuello_botella = float('inf')
    for movimiento in grafo.vertices[ciudad_origen].vecinos:
        if movimiento.ciudad_destino == ciudad_destino:
            max_cuello_botella = min(max_cuello_botella, movimiento.peso_mx)
    return max_cuello_botella

def encontrar_destinos_diferentes(grafo, ciudad_origen):
    """Encuentra todos los destinos diferentes desde la ciudad de origen."""
    destinos = set()
    for movimiento in grafo.vertices[ciudad_origen].vecinos:
        destinos.add(movimiento.ciudad_destino)
    return list(destinos)

def calcular_precio_y_cuello_botella(grafo, ciudad_origen, ciudad_destino):
    """Calcula el precio mínimo y el cuello de botella para un destino específico."""
    max_cuello_botella = encontrar_cuello_botella(grafo, ciudad_origen, ciudad_destino)
    precio_min = buscar_precio_minimo(grafo.vertices[ciudad_origen], max_cuello_botella)
    return precio_min, max_cuello_botella

# Crear el grafo y cargar datos desde el archivo
grafo = Grafo()
ruta_del_archivo = '/home/dany/Escritorio/Nueva carpeta/algoritmos/TP-AyED/ejerciciosTP2/rutas.txt'

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

ciudad_origen = "CiudadBs.As."
destinos = encontrar_destinos_diferentes(grafo, ciudad_origen)

for destino in destinos:
    precio_min, cuello_botella = calcular_precio_y_cuello_botella(grafo, ciudad_origen, destino)
    print(f"Para llegar a {destino}:")
    print(f"Precio mínimo: {precio_min} unidades de 1000.")
    print(f"Peso máximo que se puede transportar: {cuello_botella} kg.")
    print("-----")
