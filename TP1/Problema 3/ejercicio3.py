from random import randint

class ArchivoNumeros:
    """Genera un archivo con un tamaño mayor o igual a 100 megabytes. En cada línea del archivo debe haber un único número entero. 
    Los números deben estar desordenados en este archivo."""
    def __init__(self, datos_desordenados, cant_lineas, cant_cifras):
        self.datos_desordenados = datos_desordenados
        self.cant_lineas = cant_lineas
        self.cant_cifras = cant_cifras

    def generar_numeros(self):
        
        try:
            with open(self.datos_desordenados, 'w') as arch_d:
                for i in range(self.cant_lineas):
                    numero = randint(10 ** (self.cant_cifras - 1), (10 ** self.cant_cifras) - 1)
                    arch_d.write(f"{numero}\n")    
            print(f"Se generaron {self.cant_lineas} números aleatorios y se guardaron en '{self.datos_desordenados}'.")
        except Exception as error:
            print(f"Error al crear el archivo: {str(error)}")

class Mezcla_Directa:
    """algoritmo de ordenamiento externo 'mezcla directa' tomando bloques de B claves en cada lectura. B es un número 
    entero positivo menor al número de datos a ordenar que representa la cantidad de claves por bloque leído"""
    def __init__(self, archivo_escrito, archivo_ordenado, B):
        self.archivo_escrito = archivo_escrito
        self.archivo_ordenado = archivo_ordenado
        self.B = B
    def mezclar(self):
        """la primera línea del archivo resultante contenga el menor número entero y la última el mayor"""
        try:
            with open(self.archivo_escrito, 'r') as entrada, open(self.archivo_ordenado, 'w') as salida:
                bloques = []
                while True:
                    bloque = []
                    for i in range(self.B):
                        linea = entrada.readline()
                        if not linea:
                            break
                        bloque.append(int(linea))
                    if not bloque:
                        break
                    bloque.sort()
                    bloques.append(bloque)

                while bloques:
                    bloques.sort(key=lambda b: b[0])
                    minimo = bloques[0].pop(0)
                    salida.write(f"{minimo}\n")
                    if not bloques[0]:
                        bloques.pop(0)

            print(f"Se ordenó el archivo '{self.archivo_escrito}' y se guardó en '{self.archivo_ordenado}'.")
        
        except Exception as error:
            print(f"Error al mezclar el archivo: {error}")

def obtener_tamano_archivo_mb(archivo):
    with open(archivo, 'r') as f:
        return len(f.read()) / (1024 * 1024)  # Convierte a megabytes

def verificar_funcionamiento(archivo_original, archivo_ordenado):
    """prueba que verifica el funcionamiento del algoritmo: el archivo resultante posea el mismo tamaño (en bytes) 
    que el archivo original y que los datos en su interior están realmente ordenados de menor a mayor luego de aplicar 
    el algoritmo."""
    try:
        tam_original = obtener_tamano_archivo_mb(archivo_original)
        tam_ordenado = obtener_tamano_archivo_mb(archivo_ordenado)
        
        if tam_original != tam_ordenado:
            return False, "Los tamaños de los archivos no coinciden"

        with open(archivo_ordenado, 'r') as archivo_ordenado:
            lineas_ordenadas = []
            for linea in archivo_ordenado.readlines():
                lineas_ordenadas.append(int(linea.strip()))

            if lineas_ordenadas == sorted(lineas_ordenadas):
                return True, "El archivo ordenado está correctamente ordenado"
            else:
                return False, "El archivo ordenado no está correctamente ordenado"
    except Exception as error:
        return False, f"Error al verificar el archivo: {str(error)}"


if __name__ == "__main__":
    num_lineas = 5000000  # 5 millones de líneas
    cantidad_cifras = 20  # 20 cifras
    datos_desordenados = "datos_desordenados.txt"

    generador = ArchivoNumeros(datos_desordenados, num_lineas, cantidad_cifras)
    generador.generar_numeros()

    datos_ordenados = "datos_ordenados.txt"
    B = 1000  # Tamaño escogido para el bloque
    mezcla = Mezcla_Directa(datos_desordenados, datos_ordenados, B)
    mezcla.mezclar()

    exito, mensaje = verificar_funcionamiento(datos_desordenados, datos_ordenados)

    if exito:
        print("Éxito, el archivo está correctamente ordenado.")
    else:
        print("No funcionó, no se ordenó correctamente:", mensaje)
