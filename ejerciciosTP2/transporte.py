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

# Variable grafo contiene los datos del archivo ruta, usa la clase Grafo
grafo = Grafo()
ruta_del_archivo = '/home/dany/Escritorio/Nueva carpeta/algoritmos/TP-AyED/ejerciciosTP2/rutas.txt'

try:
    # Leo el archivo y guardo cada variable
    with open(ruta_del_archivo, 'r') as arch_ruta:
        for linea in arch_ruta:
            datos = linea.strip().split(',')
            ciudad_origen = datos[0]
            ciudad_destino = datos[1]
            peso = int(datos[2])
            precio = int(datos[3])
            # Me aseguro de que todas las rutas hayan sido agregadas, por si alguna no se agregó al inicio
            if ciudad_origen not in grafo.vertices:
                grafo.agregar_vertice(ciudad_origen)
            if ciudad_destino not in grafo.vertices:
                grafo.agregar_vertice(ciudad_destino)

            grafo.agregar_movimiento(ciudad_origen, ciudad_destino, peso, precio)

except FileNotFoundError:
    print("El archivo no se encuentra.")
except Exception as error:
    print(f"Error: {error}")

def buscar_precio_minimo(vertice, max_cuello_botella):
    """Función auxiliar para buscar el precio mínimo recursivamente."""
    if not vertice.vecinos:
        # Si no hay rutas disponibles, el precio mínimo es 0
        return 0
    vertice.visitado = True
    precio_min = float('inf')
    for movimiento in vertice.vecinos:
        ciudad_destino_objeto = grafo.vertices[movimiento.ciudad_destino]  # Obtén el objeto Vertice correspondiente a la ciudad de destino
        if not ciudad_destino_objeto.visitado and movimiento.peso_mx <= max_cuello_botella:
            precio_ruta_actual = movimiento.precio
            precio_min = min(precio_min, precio_ruta_actual)
    return precio_min

def encontrar_cuello_botella(grafo, ciudad_origen):
    """Determina el cuello de botella desde la ciudad de origen a la destino en el grafo."""
    max_cuello_botella = float('inf')
    for movimiento in grafo.vertices[ciudad_origen].vecinos:
        max_cuello_botella = min(max_cuello_botella, movimiento.peso_mx)
    return max_cuello_botella

def precio_minimo(grafo, ciudad_origen):
    """Determina el precio mínimo para transportar bienes desde la ciudad de origen hasta cualquier destino."""
    max_cuello_botella = encontrar_cuello_botella(grafo, ciudad_origen)
    return buscar_precio_minimo(grafo.vertices[ciudad_origen], max_cuello_botella)

# Prueba de que anda lo solicitado
ciudad_origen = "CiudadBs.As."
precio_min = precio_minimo(grafo, ciudad_origen)
cuello_botella = encontrar_cuello_botella(grafo, ciudad_origen)
print(f"Precio mínimo para transportar desde {ciudad_origen} hasta cualquier destino: {precio_min} unidades de 1000.")
print(f"Peso máximo que se puede transportar desde {ciudad_origen} a cualquier otra ciudad de destino: {cuello_botella} kg.")
