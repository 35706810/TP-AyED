class Nodo_DobleEnlazado:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None
        
    def __str__(self):
        return str(self.dato)
    
    def __repr__(self):
        return str(self.dato)
    
    def __gt__(self, o):
        return self.dato > o.dato
    
class ListaDobleEnlazada:

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self._tamanio = 0

    def __getitem__(self, indice):
        auxiliar = self.cabeza
        for _ in range(indice):
            auxiliar = auxiliar.siguiente
        return auxiliar.dato

    def __iter__(self):
        nodo_nuevo = self.cabeza
        while nodo_nuevo:
            yield nodo_nuevo.dato
            nodo_nuevo = nodo_nuevo.siguiente
            
    def __str__(self):
        lista = [nodo for nodo in self]
        return str(lista)

    def esta_vacia(self):
        return self.cabeza is None
    
    def __len__(self):
        return self._tamanio
        
    @property
    def tamanio(self):
        return self._tamanio

    def extraer(self, posicion=None):
        
        if posicion == None or posicion== -1:
            posicion = self._tamanio-1
        
        if posicion < 0 or posicion> self._tamanio-1:
            raise IndexError("Esta fuera de rango")
        else:
            nodo = None
            if self.cabeza.siguiente  is None:
                nodo = self.cabeza
                self.cabeza = None
                self.cola = None
            elif posicion == self._tamanio-1:
                nodo = self.cola
                nodo.anterior.siguiente = None
                self.cola = nodo.anterior
            elif posicion == 0:
                nodo = self.cabeza
                self.cabeza = self.cabeza.siguiente
                self.cabeza.anterior = None
            else:
                aux = self.cabeza
                for _ in range(posicion):
                    aux = aux.siguiente
                    nodo = aux
                aux.anterior.siguiente = aux.siguiente
                aux.siguiente.anterior = aux.anterior
            
            self._tamanio -= 1
            return nodo.dato
    
    def insertar(self, dato, posicion):
        
        if posicion < 0 or posicion >=self._tamanio+1:
            raise IndexError("Esta fuera de rango")
        else:
            if posicion == 0:
                self.agregar_al_inicio(dato)
            elif posicion == self._tamanio:
                self.agregar_al_final(dato)     
            elif posicion == self._tamanio:
                nuevo = Nodo_DobleEnlazado(dato)
                self.cola.anterior.siguiente = nuevo
                nuevo.anterior = self.cola.anterior
                nuevo.siguiente = self.cola
                self.cola.anterior = nuevo
                self._tamanio += 1
            else: 
                nuevo = Nodo_DobleEnlazado(dato)
                aux = self.cabeza
                for _ in range(posicion):
                    aux = aux.siguiente
                aux.anterior.siguiente = nuevo    
                nuevo.anterior = aux.anterior
                nuevo.siguiente = aux
                aux.anterior = nuevo
                self._tamanio += 1

    def agregar_al_inicio(self, dato):
        
        nuevo_nodo = Nodo_DobleEnlazado(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
            
        self._tamanio += 1

    def agregar_al_final(self, dato):
        
        nuevo_nodo = Nodo_DobleEnlazado(dato)
        if self._tamanio == 0:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo
        self._tamanio += 1

    def copiar(self):
        
        nueva_lista = ListaDobleEnlazada()
        nodo_aux = self.cabeza
        while nodo_aux is not None:
            nueva_lista.agregar_al_final(nodo_aux.dato)
            nodo_aux = nodo_aux.siguiente
        return nueva_lista

    def invertir(self):
        
        actual = self.cabeza
        while actual is not None:
            siguiente_temp = actual.siguiente
            actual.siguiente = actual.anterior
            actual.anterior = siguiente_temp
            if siguiente_temp is None:
                self.cabeza, self.cola = self.cola, self.cabeza
            actual = siguiente_temp

    def ordenar(self):
        
        if self._tamanio < 2:
            return
        nodo_actual = self.cabeza.siguiente
        while nodo_actual is not None:
            nodo_orde = self.cabeza
            while nodo_orde is not nodo_actual and nodo_actual > nodo_orde:
                nodo_orde = nodo_orde.siguiente
    
            if nodo_orde is not nodo_actual:
                nodo_anterior = nodo_actual.anterior

                nodo_anterior.siguiente = nodo_actual.siguiente
                if nodo_actual.siguiente is not None:
                    nodo_actual.siguiente.anterior = nodo_anterior
    
                nodo_actual.anterior = nodo_orde.anterior
                nodo_actual.siguiente = nodo_orde
                nodo_orde.anterior = nodo_actual
                if nodo_actual.anterior is not None:
                    nodo_actual.anterior.siguiente = nodo_actual
                else:
                    self.cabeza = nodo_actual

                nodo_actual = nodo_anterior.siguiente
            else:
                nodo_actual = nodo_actual.siguiente

        self.cola = nodo_anterior

    def _ordenar_recursivo(self, inicio, fin):
        
        if inicio is not None and fin is not None and inicio != fin and inicio.anterior != fin:
            pivote = self._particionar(inicio, fin)
            self._ordenar_recursivo(inicio, pivote.anterior)
            self._ordenar_recursivo(pivote.siguiente, fin)

    def _particionar(self, inicio, fin):
        
        pivote = inicio.dato
        izquierda = inicio
        derecha = fin

        while izquierda != derecha:
            while izquierda != derecha and derecha.dato >= pivote:
                derecha = derecha.anterior
            while izquierda != derecha and izquierda.dato <= pivote:
                izquierda = izquierda.siguiente
            if izquierda != derecha:
                izquierda.dato, derecha.dato = derecha.dato, izquierda.dato

        izquierda.dato, inicio.dato = inicio.dato, izquierda.dato

        return izquierda

    def concatenar(self, otra_lista):
        
        for i in otra_lista:
            self.agregar_al_final(i)
        return self

    def _concatenar(self, otra_lista):
        
        nueva_lista = self.copiar()
        for i in otra_lista:
            nueva_lista.agregar_al_final(i)
        return nueva_lista

    def __add__(self, otra_lista):
        return self._concatenar(otra_lista)
