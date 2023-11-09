import Variable

class TablaSimbolos:
    """Tabla de simbolos que almacena los nombres de las variables como key utilizando una funcion hash."""

    def __init__(self):
        self.tiposDatos = {'void': "void", 'int': "int", 'float': "float", 'string': "string"}
        self.reservada = {'if': "if", 'while': "while", 'return': "return"}
        self.matematicos = {'+': "+", '-': "-", ';': ";", '*': "*", ',': ",", '/': "/", '=': "="}
        self.comparacion = {'==': "==", '!=': "!=",'<': "<", '>': ">"}
        self.parentesis = {'(': "(", ')': ")"}
        self.bloques = {'{': "{", '}': "}"}
        self.table = {}

    def insertar(self, variable):
        """Inserta el objeto variable a la tabla de simbolos usando una funcion hash."""
        hash_value = hash(variable.nombre)
        self.table[hash_value] = variable

    def buscar(self, nombre):
        """Busca un objeto utilizando su nombre como key."""
        hash_value = hash(nombre)
        variable = self.table.get(hash_value, None)
        return variable

    def eliminar(self, nombre):
        """Elimina un objeto utilizando su nombre como key."""
        hash_value = hash(nombre)
        if hash_value in self.table:
            del self.table[hash_value]

    def revisar_tipo_dato(self, palabra):
        """Revisa si la primer palabra de una lista es uno de los tipos de datos con los que se trabaja."""
        return palabra in self.tiposDatos

    def procesar_lineas(self, lista):
        """Procesa las listas de palabras de cada una de las lineas leidas del archivo y si son declaraciones o parametros las inserta en la tabla de simbolos como Variables."""
        for palabras in lista:
            i = 0
            while i < len(palabras):
                palabra = palabras[i]
                """Revisa si la palabra es un tipo de dato."""
                if palabra in self.tiposDatos:
                    tipo = self.tiposDatos[palabra]
                    i += 1  
                    """Revisa en la proxima posicion para asignar el nombre de la variable."""
                    if i < len(palabras):
                        nombre = palabras[i]
                        i += 1  
                        """Revisa si es una declaracion para asignar el valor."""
                        if palabras[i] == "=":
                            i += 1
                            valor = palabras[i]
                        else:
                            valor = None
                            """Inserta la variable en la tabla de simbolos."""
                        variable = Variable.Variable(tipo, nombre, valor)
                        self.insertar(variable)
                    else:
                        """Error de sintaxis."""
                        print("Error: Falta el nombre de la variable después del tipo.")
                        break
                else:
                    """Se mueve a la proxima palabra."""
                    i += 1

    def buscar_variable_en_tabla_simbolos(self, nombre_variable):
        """Busca una variable por nombre en la tabla de simbolos creada"""
        variable = self.buscar(nombre_variable)
        if variable:
            print(f"Información de la variable '{nombre_variable}':")
            print(f"Tipo: {variable.tipo}")
            print(f"Valor: {variable.valor}")
        else:
            print(f"La variable '{nombre_variable}' no se encontró en la tabla de símbolos.")