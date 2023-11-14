import os

class Movimiento:
    def __init__(self, ciudad_origen, ciudad_destino, peso, precio):
        self.ciudad_origen = ciudad_origen
        self.ciudad_destino = ciudad_destino
        self.peso_mx = peso
        self.precio = precio
        self.nombre = ciudad_destino

    def __lt__(self, otro_movimiento):
        return self.precio < otro_movimiento.precio

class Vertice:
    def __init__(self, clave):
        self.id = clave
        self.visitado = False
        self.vecinos = {}
        self.distancia_precio = float('inf')
        self.distancia_peso = float('inf')
        self.predecesor_precio = None
        self.predecesor_peso = None

    def agregar_vecino(self, ciudad_destino, peso, precio):
        movimiento = Movimiento(self.id, ciudad_destino, peso, precio)
        self.vecinos[ciudad_destino] = movimiento

    def __str__(self):
        return str(self.id) + ' conectadoA: ' + str([x for x in self.vecinos.keys()])

    def obtener_conexiones(self):
        return self.vecinos.keys()

    def obtener_id(self):
        return self.id

    def obtener_ponderacion(self, ciudad_destino, tipo='precio'):
        if ciudad_destino in self.vecinos:
            movimiento = self.vecinos[ciudad_destino]
            return movimiento.precio if tipo == 'precio' else movimiento.peso_mx
        return float('inf') if tipo == 'precio' else float('inf')  # Cambiado de float('-inf')

    def __lt__(self, otro_vertice):
        return self.distancia_precio < otro_vertice.distancia_precio

class Grafo:
    def __init__(self):
        self.vertices = {}

    def agregar_vertice(self, clave):
        vertice = Vertice(clave)
        self.vertices[clave] = vertice

    def agregar_movimiento(self, ciudad_origen, ciudad_destino, peso, precio):
        self.vertices[ciudad_origen].agregar_vecino(ciudad_destino, peso, precio)

class ColaPrioridad:
    def __init__(self):
        self.lista = []

    def esta_vacia(self):
        return len(self.lista) == 0

    def insertar(self, elemento):
        self.lista.append(elemento)
        self.lista.sort(key=lambda x: x[0])

    def eliminar_min(self):
        if not self.esta_vacia():
            minimo = self.lista.pop(0)
            return minimo
        else:
            raise IndexError("La cola de prioridad está vacía")

    def decrementar_clave(self, vertice, nueva_distancia):
        for i, (distancia, v) in enumerate(self.lista):
            if v.id == vertice.id:
                if nueva_distancia < distancia:
                    self.lista[i] = (nueva_distancia, vertice)
                    self.lista.sort(key=lambda x: x[0])

def dijkstra(un_grafo, inicio, tipo='precio', destino=None):
    cp = ColaPrioridad()

    if tipo == 'precio':
        inicio.distancia_precio = 0
        cp.insertar((inicio.distancia_precio, inicio))
    elif tipo == 'peso':
        inicio.distancia_peso = 0
        cp.insertar((inicio.distancia_peso, inicio))

    while not cp.esta_vacia():
        if tipo == 'precio':
            distancia, vertice_actual = cp.eliminar_min()
        elif tipo == 'peso':
            distancia, vertice_actual = cp.eliminar_min()
        for ciudad_destino in vertice_actual.obtener_conexiones():
            vertice_siguiente = un_grafo.vertices[ciudad_destino]
            if tipo == 'precio':
                nueva_distancia = distancia + vertice_actual.obtener_ponderacion(ciudad_destino, 'precio')
                if nueva_distancia < vertice_siguiente.distancia_precio:
                    vertice_siguiente.distancia_precio = nueva_distancia
                    vertice_siguiente.predecesor_precio = vertice_actual
                    cp.decrementar_clave(vertice_siguiente, nueva_distancia)
            elif tipo == 'peso':
                nueva_distancia = distancia + vertice_actual.obtener_ponderacion(ciudad_destino, 'peso')
                if nueva_distancia < vertice_siguiente.distancia_peso:
                    vertice_siguiente.distancia_peso = nueva_distancia
                    vertice_siguiente.predecesor_peso = vertice_actual
                    cp.decrementar_clave(vertice_siguiente, nueva_distancia)

def encontrar_peso_precio_minimo(un_grafo, ciudad_origen, ciudad_destino=None):
    resultados = {}

    dijkstra(un_grafo, un_grafo.vertices[ciudad_origen], 'precio', ciudad_destino)
    dijkstra(un_grafo, un_grafo.vertices[ciudad_origen], 'peso', ciudad_destino)

    for ciudad_dest, vertice_dest in un_grafo.vertices.items():
        if ciudad_dest != ciudad_origen:
            predecesor_precio = vertice_dest.predecesor_precio
            cuello_botella_precio = vertice_dest.obtener_ponderacion(predecesor_precio, 'precio') if predecesor_precio else None
            precio_min = vertice_dest.distancia_precio
            predecesor_peso = vertice_dest.predecesor_peso
            cuello_botella_peso = vertice_dest.obtener_ponderacion(predecesor_peso, 'peso') if predecesor_peso else None
            peso_max = vertice_dest.distancia_peso

            resultados[ciudad_dest] = {'precio_min': precio_min, 'cuello_botella_precio': cuello_botella_precio,
                                       'peso_max': peso_max, 'cuello_botella_peso': cuello_botella_peso}

    return resultados

# Crear el grafo y cargar datos desde el archivo
grafo = Grafo()
ruta_del_archivo = os.path.abspath("C:\Users\Fernando\Desktop\Problema 3/rutas.txt")  # Ruta relativa

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

    for ciudad_destino, valores in resultados.items():
        print(f"Desde {ciudad_origen} a {ciudad_destino}:")
        print(f"  Precio mínimo: ${valores['precio_min']}")
        print(f"  Cuello de botella (precio): {valores['cuello_botella_precio']} kg")
        print(f"  Peso máximo: {valores['peso_max']} kg")
        print(f"  Cuello de botella (peso): {valores['cuello_botella_peso']} unidades de 1000")
else:
    print(f"La ciudad de origen '{ciudad_origen}' no se encuentra en el grafo.")
