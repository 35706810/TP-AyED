from datetime import datetime

class NodoAVL:
    def __init__(self, fecha, temperatura):
        self.fecha = fecha
        self.temperatura = temperatura
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self.altura(nodo.izquierda), self.altura(nodo.derecha))

    def balance(self, nodo):
        if not nodo:
            return 0
        return self.altura(nodo.izquierda) - self.altura(nodo.derecha)

    def rotar_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda

        y.izquierda = x
        x.derecha = T2

        x.altura = 1 + max(self.altura(x.izquierda), self.altura(x.derecha))
        y.altura = 1 + max(self.altura(y.izquierda), self.altura(y.derecha))

        return y

    def rotar_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha

        x.derecha = y
        y.izquierda = T2

        y.altura = 1 + max(self.altura(y.izquierda), self.altura(y.derecha))
        x.altura = 1 + max(self.altura(x.izquierda), self.altura(x.derecha))

        return x

    def insertar(self, nodo, fecha, temperatura):
        if not nodo:
            return NodoAVL(fecha, temperatura)
        if fecha < nodo.fecha:
            nodo.izquierda = self.insertar(nodo.izquierda, fecha, temperatura)
        elif fecha > nodo.fecha:
            nodo.derecha = self.insertar(nodo.derecha, fecha, temperatura)
        else:
            return nodo

        self.actualizar_altura(nodo)

        balance = self.balance(nodo)

        if balance > 1:
            if fecha < nodo.izquierda.fecha:
                return self.rotar_derecha(nodo)
            else:
                nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
                return self.rotar_derecha(nodo)

        if balance < -1:
            if fecha > nodo.derecha.fecha:
                return self.rotar_izquierda(nodo)
            else:
                nodo.derecha = self.rotar_derecha(nodo.derecha)
                return self.rotar_izquierda(nodo)

        return nodo
    
class Temperaturas_DB:
    def __init__(self):
        self.arbol = ArbolAVL()
        self.muestras = 0  # Inicializo el contador de muestras en 0
   
    def guardar_temperatura(self, fecha, temperatura):
        """ Método para guardar una nueva temperatura en la base de datos"""
        try:
            fecha = datetime.strptime(fecha, "%d/%m/%Y")
            self.arbol.raiz = self.arbol.insertar(self.arbol.raiz, fecha, temperatura)
            self.muestras += 1
        except ValueError:
            raise ValueError("Formato de fecha incorrecto. Utilice el formato dd/mm/yyyy.")
    
    def devolver_temperatura(self, fecha):
        """Método para buscar y devolver la temperatura asociada a una fecha específica"""
        try:
            fecha = datetime.strptime(fecha, "%d/%m/%Y")
            return self._buscar_temperatura(self.arbol.raiz, fecha)
        except ValueError:
            raise ValueError("Formato de fecha incorrecto. Utilice el formato dd/mm/yyyy.")


    def _buscar_temperatura(self, nodo, fecha):
        """Método auxiliar para buscar la temperatura en el árbol AVL"""
        
        if not nodo:
            return None
        if fecha < nodo.fecha:
            return self._buscar_temperatura(nodo.izquierda, fecha)
        elif fecha > nodo.fecha:
            return self._buscar_temperatura(nodo.derecha, fecha)
        else:
            return nodo.temperatura

    
    def _buscar_muestras_rango(self, nodo, fecha1, fecha2, resultados):
        """Método para buscar y almacenar las temperaturas en un rango de fechas"""
        if not nodo:
            return 
        if fecha1 < nodo.fecha:
            self._buscar_muestras_rango(nodo.izquierda, fecha1, fecha2, resultados)
        if fecha1 <= nodo.fecha and nodo.fecha <= fecha2:
            # Convertir la cadena de fecha en un objeto datetime
            fecha_datetime = nodo.fecha
            # Formatear la fecha y almacenar la temperatura en los resultados
            resultados.append(f"{fecha_datetime}: {nodo.temperatura} ºC")
            
        if fecha2 > nodo.fecha:
            self._buscar_muestras_rango(nodo.derecha, fecha1, fecha2, resultados)
    
    def devolver_temperaturas(self, fecha1, fecha2):
        """Método para devolver las temperaturas en un rango de fechas"""
        resultados = []
        fecha1 = datetime.strptime(fecha1, "%d/%m/%Y")
        fecha2 = datetime.strptime(fecha2, "%d/%m/%Y")
        self._buscar_muestras_rango(self.arbol.raiz, fecha1, fecha2, resultados)
        return resultados

    
    def max_temp_rango(self, fecha1, fecha2):
        """ Método para encontrar la temperatura máxima en un rango de fechas"""
        temperaturas=[] 
        fecha1 = datetime.strptime(fecha1, "%d/%m/%Y")
        fecha2 = datetime.strptime(fecha2, "%d/%m/%Y")
        self._buscar_muestras_rango(self.arbol.raiz, fecha1, fecha2, temperaturas)
        
        if temperaturas:
            return max(float(temp.split(': ')[1][:-3]) for temp in temperaturas)
        return None

    
    def min_temp_rango(self, fecha1, fecha2):
        """Método para encontrar la temperatura mínima en un rango de fechas"""
        temperaturas =[]
        fecha1 = datetime.strptime(fecha1, "%d/%m/%Y")
        fecha2 = datetime.strptime(fecha2, "%d/%m/%Y")
        self._buscar_muestras_rango(self.arbol.raiz, fecha1, fecha2, temperaturas)
        if temperaturas:
            return min(float(temp.split(': ')[1][:-3]) for temp in temperaturas)
        return None

    
    def temp_extremos_rango(self, fecha1, fecha2):
        """Método para encontrar las temperaturas máxima y mínima en un rango de fechas"""
        temperaturas=[] 
        fecha1 = datetime.strptime(fecha1, "%d/%m/%Y")
        fecha2 = datetime.strptime(fecha2, "%d/%m/%Y")
        self._buscar_muestras_rango(self.arbol.raiz, fecha1, fecha2,temperaturas )
        
        if temperaturas:
            temperaturas = [float(temp.split(': ')[1][:-2]) for temp in temperaturas]
            #print(temperaturas)
            min_temp = min(temperaturas)
            max_temp = max(temperaturas)
            return min_temp, max_temp
        return None

    
    def borrar_temperatura(self, fecha):
        """Método para borrar una temperatura en una fecha específica"""
        try:
            fecha = datetime.strptime(fecha, "%d/%m/%Y")
            if self._buscar_temperatura(self.arbol.raiz, fecha) is not None:
                self.muestras -= 1
            self.raiz = self._borrar_temperatura(self.arbol.raiz, fecha)
        except ValueError:
            raise ValueError("Formato de fecha incorrecto. Utilice el formato dd/mm/yyyy.")

    
    def _encontrar_minimo(self, nodo):
        """Método auxiliar para encontrar el nodo con el fecha mínima en un árbol"""
        while nodo.izquierda:
            nodo = nodo.izquierda
        return nodo

    
    def _borrar_temperatura(self, raiz, fecha):
        """Método para borrar una temperatura en el árbol AVL y balancearlo"""
        if not raiz:
            return raiz

        if fecha < raiz.fecha:
            raiz.izquierda = self._borrar_temperatura(raiz.izquierda, fecha)
        elif fecha > raiz.fecha:
            raiz.derecha = self._borrar_temperatura(raiz.derecha, fecha)
        else:
            if not raiz.izquierda:
                temp = raiz.derecha
                raiz = None
                return temp
            elif not raiz.derecha:
                temp = raiz.izquierda
                raiz = None
                return temp

            temp = self.arbol._encontrar_minimo(raiz.derecha)
            raiz.fecha = temp.fecha
            raiz.temperatura = temp.temperatura
            raiz.derecha = self._borrar_temperatura(raiz.derecha, temp.fecha)

        if not raiz:
            return raiz

        raiz.altura = 1 + max(self.arbol.altura(raiz.izquierda), self.arbol.altura(raiz.derecha))

        balance = self.arbol.balance(raiz)

        # rotaciones para balancear el árbol después de borrar un nodo
        if balance > 1 and self.arbol.balance(raiz.izquierda) >= 0:
            return self.arbol.rotar_derecha(raiz)

        if balance < -1 and self.arbol.balance(raiz.derecha) <= 0:
            return self.arbol.rotar_izquierda(raiz)

        if balance > 1 and self.arbol.balance(raiz.izquierda) < 0:
            raiz.izquierda = self.arbol.rotar_izquierda(raiz.izquierda)
            return self.arbol.rotar_derecha(raiz)

        if balance < -1 and self.arbol.balance(raiz.derecha) > 0:
            raiz.derecha = self.arbol.rotar_derecha(raiz.derecha)
            return self.arbol.rotar_izquierda(raiz)

        return raiz

    
    def cantidad_muestras(self):
        """Método para obtener la cantidad de muestras en la base de datos"""
        return self.muestras

# Testeo del código
temperaturas_db = Temperaturas_DB()

# para guardar temperaturas
temperaturas_db.guardar_temperatura("01/11/2023", 9.5) #se debe guardar la temperatura 25.5 junto con la fecha "01/11/2023" en la base de datos de temperaturas representada por el objeto temperaturas_db. 
temperaturas_db.guardar_temperatura("02/01/2023", 26.2)
temperaturas_db.guardar_temperatura("03/10/2023", 24.8)
temperaturas_db.guardar_temperatura("04/01/2023", 27.0)

# para consultar temperaturas
print("Temperatura el 12/05/2023:", temperaturas_db.devolver_temperatura("12/05/2023"))

# consultar temperaturas en un rango
print("Temperaturas entre el 01/11/2023 y el 03/10/2023:")
print(temperaturas_db.devolver_temperaturas("06/01/2020", "01/11/2023"))

# consultar temperatura máxima y mínima en un rango
print("Temperatura máxima entre el 02/01/2023 y el 01/11/2023:", temperaturas_db.max_temp_rango("02/01/2023", "01/11/2023"))
print("Temperatura mínima entre el 02/01/2023 y el 01/11/2023:", temperaturas_db.min_temp_rango("02/01/2023", "01/11/2023"))

# consultar temperaturas extremas en un rango
print("Temperaturas extremas entre el 04/01/2023 y el 03/10/2023:", temperaturas_db.temp_extremos_rango("04/01/2023", "03/10/2023"))

# para borrar una temperatura
temperaturas_db.borrar_temperatura("02/01/2023")
print("Temperatura el 02/01/2023 después de borrarla:", temperaturas_db.devolver_temperatura("02/01/2023"))

# para consultar la cantidad de muestras
print("Cantidad de muestras:", temperaturas_db.cantidad_muestras())