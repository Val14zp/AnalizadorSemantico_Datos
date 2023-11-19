import Variable

class TablaSimbolos:
    """Un diccionario que almacena los nombres de las variables como key utilizando una funcion hash."""

    def __init__(self):
        self.tiposDatos = {'void': "void", 'int': "int", 'float': "float", 'string': "string"}
        self.reservada = {'if': "if", 'while': "while", 'return': "return"}
        self.matematicos = {'+': "+", '-': "-", '*': "*", '/': "/", '=': "="}
        self.comparacion = {'==': "==", '!=': "!=",'<': "<", '>': ">"}
        self.parentesis = {'(': "(", ')': ")"}
        self.bloques = {'{': "{", '}': "}"}
        self.ignorar = {';': ";", ',': ","}
        self.table = {}

        #Debe lanzar un error si trata de insertar una variable que ya esta

    def insertar(self, variable):
        """
        Inserta el objeto variable a la tabla de simbolos usando una funcion hash.
        Recibe como argumento un objeto Variable.
        """
        hash_value = hash(variable.nombre)
        #Lanza error si ya se inserto la variable
        if hash_value not in self.table:
            self.table[hash_value] = variable
        else:
            raise ValueError(f"La variable ya fue declarada.")

    def buscar(self, nombre):
        """
        Busca un objeto utilizando su nombre como key.
        Recibe como argumento un string que se utiliza como key.
        Retorna un objeto Variable
        """
        hash_value = hash(nombre)
        variable = self.table.get(hash_value, None)
        return variable
    
    def modificar(self, nombre, nuevo_valor):
        """
        Modifica el valor de una variable en la tabla de símbolos, para eso utiliza la funcion buscar.
        Recibe como argumento un string que se utiliza como key y el nuevo valor para modificar.
        Retorna true en caso de que se haga la modificacion y False en caso contrario.
        """
        variable = self.buscar(nombre)
        if variable:
            variable.valor = nuevo_valor
            return True
        else:
            return False
        
        #Corregir los obtener x si no existe la palabra en la tabla

    def obtener_valor(self, nombre):
        """
        Obtiene el valor de una variable en la tabla de símbolos.
        Recibe como argumento un string que se utiliza como key.
        Retorna el valor de la variable y None en caso contrario.
        """
        variable = self.buscar(nombre)
        if variable:
            return variable.valor
        else:
            return None

    def obtener_tipo(self, nombre):
        """
        Obtiene el tipo de una variable en la tabla de símbolos.
        Recibe como argumento un string y el nuevo valor para modificar.
        Retorna el tipo de la variable y None en caso contrario.
        """
        variable = self.buscar(nombre)
        if variable:
            return variable.tipo
        else:
            return None

    def eliminar(self, nombre):
        """Elimina un objeto utilizando su nombre como key."""
        hash_value = hash(nombre)
        if hash_value in self.table:
            del self.table[hash_value]

    def revisar_tipo_dato(self, palabra):
        """
        Revisa si la primer palabra de una lista es uno de los tipos de datos con los que se trabaja.
        Recibe como argumento la palabra a buscar.
        """
        return palabra in self.tiposDatos

    def procesar_lineas(self, lista):
        """
        Procesa las listas de palabras de cada una de las lineas leidas del archivo y 
        si son declaraciones o parametros las inserta en la tabla de simbolos como Variables.
        Recibe como argumento la lista de palabras.
        """
        for palabras in lista:
            i = 0
            while i < len(palabras):
                palabra = palabras[i]
                #Revisa si la palabra es un tipo de dato.
                if palabra in self.tiposDatos:
                    tipo = self.tiposDatos[palabra]
                    i += 1  
                    #Revisa en la proxima posicion para asignar el nombre de la variable.
                    if i < len(palabras):
                        nombre = palabras[i]
                        i += 1  
                        #Revisa si es una declaracion para asignar el valor.
                        if palabras[i] == "=":
                            i += 1
                            valor = palabras[i]
                        else:
                            valor = None
                            #Inserta la variable en la tabla de simbolos.
                        variable = Variable.Variable(tipo, nombre, valor)
                        self.insertar(variable)
                    else:
                        #Error de sintaxis.
                        print("Error: Falta el nombre de la variable después del tipo.")
                        break

                else:
                    #Se mueve a la proxima palabra.
                    i += 1

    def buscar_variable_en_tabla_simbolos(self, nombre_variable):
        """
        Busca una variable por nombre en la tabla de simbolos creada.
        Recibe como argumento un string nombre_variable.
        """
        variable = self.buscar(nombre_variable)
        if variable:
            print(f"Información de la variable '{nombre_variable}':")
            print(f"Tipo: {variable.tipo}")
            print(f"Valor: {variable.valor}")
        else:
            print(f"La variable '{nombre_variable}' no se encontró en la tabla de símbolos.")

    def imprimir(self, nombre_variable):
        """Busca una variable por nombre en la tabla de simbolos creada"""
        print(f"Valor: {self.obtener_valor(nombre_variable)}")