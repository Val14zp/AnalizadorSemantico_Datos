import Variable
import AnalizadorSemantico

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
        self.variables_sin_declarar = {}
        self.variable_mal_iniciaizada = {}
    @staticmethod
    def esString(s):
        if s == '':
            return False
        return (s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")

    @staticmethod
    def esNumero(n):
        return n.replace('.', '', 1).isdigit()

    @staticmethod
    def es_flotante(variable):
        try:
            float(variable)
            return True
        finally:
            return False

    def es_operador(self, variable):
        """Revisa si la variable es un operador."""
        return variable in self.matematicos or variable in self.comparacion or variable in self.parentesis or variable in self.bloques

    def es_tipo_dato(self, variable):
        """Revisa si la primer palabra de una lista es uno de los tipos de datos con los que se trabaja."""
        return variable in self.tiposDatos

    def es_reservada(self, variable):
        """Revisa si la variable es una palabra reservada."""
        return variable in self.reservada

    def esta_declarada(self, variable):
        """Revisa si la variable esta declarada."""
        return self.variables_sin_declarar.get(hash(variable), None)

    def revisa_declaracion_variables(self, variable):
        """Revisa está declarada."""
        if not self.esta_declarada(variable) and not self.buscar(variable) and not self.es_reservada(variable) and not self.es_operador(variable) and not self.esString(variable) and not self.esNumero(variable) and not self.es_flotante(variable):
            print(f"Error: La variable '{variable}' no se encuentra declarada.")
            self.variables_sin_declarar[hash(variable)] = variable
            return False

    def coincide_tipo_dato_con_valor(self, variable):
        """Revisa si el tipo de dato coincide con el valor."""
        variable = self.buscar(variable)
        if variable.tipo == "int" and not self.esNumero(variable.valor):
            print(f"Error: El tipo de dato '{variable.tipo}' no coincide con el valor '{variable.valor}'.")
            return False
        elif variable.tipo == "float" and not self.es_flotante(variable.valor):
            print(f"Error: El tipo de dato '{variable.tipo}' no coincide con el valor '{variable.valor}'.")
            return False
        elif variable.tipo == "string" and not self.esString(variable.valor):
            print(f"Error: El tipo de dato '{variable.tipo}' no coincide con el valor '{variable.valor}'.")
            return False

    def revisa_inicializacion_variables(self, variable):
        """Revisa si la variable está inicializada."""
        if not self.coincide_tipo_dato_con_valor(variable):
            self.variable_mal_iniciaizada[hash(variable.nombre)] = variable
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
                        if valor is not None:
                            self.revisa_inicializacion_variables(variable)

                        self.insertar(variable)
                    else:
                        """Error de sintaxis."""
                        print("Error: Falta el nombre de la variable después del tipo.")
                        break
                else:
                    """Revisa si ya la palabra se encontraba entre las palabras sin reservar."""


                    #To do: revisar si al retornar se está retornando correctamente la variable
                    if not self.revisa_declaracion_variables(palabra):
                        if self.buscar(palabra):
                            self.revisa_inicializacion_variables(self.buscar(palabra))
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