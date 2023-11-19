from Variable import Variable
import ast
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
        self.funcion = {}
        self.estructura = {}
        self.pila = []
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
        if not self.esta_declarada(variable) and not self.buscar(variable) and not self.buscar_funcion(variable) and not self.buscar_Estructura(variable):
            print(f"Error: La variable '{variable}' no se encuentra declarada.")
            self.variables_sin_declarar[hash(variable)] = variable
            return False
        return True

    def coincide_tipo_dato_con_valor(self, variable):
      """Revisa si el tipo de dato coincide con el valor."""
      variable = self.buscar(variable)
      if variable is not None:
        if variable.tipo == "int" and not self.esNumero(variable.valor):
            print(f"Error: En la variable '{variable.nombre}' el tipo de dato '{variable.tipo}' no coincide con el valor '{variable.valor}'.")
            return False
        elif variable.tipo == "float" and not self.es_flotante(variable.valor):
            print(f"Error: En la variable '{variable.nombre}' el tipo de dato '{variable.tipo}' no coincide con el valor '{variable.valor}'.")
            return False
        elif variable.tipo == "string" and not self.esString(variable.valor):
            print(f"Error: En la variable '{variable.nombre}' el tipo de dato '{variable.tipo}' no coincide con el valor '{variable.valor}'.")
            return False

    def revisa_inicializacion_variables(self, variable):
        """Revisa si la variable está inicializada."""
        
        if not self.coincide_tipo_dato_con_valor(variable):
            variable = self.buscar(variable)
            self.variable_mal_iniciaizada[hash(variable.nombre)] = variable
          
    def insertar(self, variable):
        """Inserta el objeto variable a la tabla de simbolos usando una funcion hash."""
        hash_value = hash(variable.nombre)
        self.table[hash_value] = variable

    def insertarFuncion(self, variable):
        """Inserta el objeto variable a la tabla de funciones para tener control de su espacio permitido usando una funcion hash."""
        hash_value = hash(variable.nombre)
        self.funcion[hash_value] = variable

    def insertar_Estructura_Dentro_Funcion(self, variable):
        """Inserta el objeto variable a una tabla para limitar su uso dentro del programa en caso de que este dentro de una funcion usando una funcion hash."""
        hash_value = hash(variable.nombre)
        self.estructura[hash_value] = variable

    def buscar(self, nombre):
        hash_value = hash(nombre)
        variable = self.table.get(hash_value, None)
        return variable

    def buscar_funcion(self, nombre):
        hash_value = hash(nombre)
        variable = self.funcion.get(hash_value, None)
        return variable

    def buscar_Estructura(self, nombre):
        hash_value = hash(nombre)
        variable = self.estructura.get(hash_value, None)
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
        """
        Procesa las listas de palabras de cada una de las líneas leídas del archivo y,
        si son declaraciones o parámetros, las inserta en la tabla de símbolos como Variables.
        """
        for palabras in lista:
            i = 0
            while i < len(palabras):
                palabra = palabras[i]

                if palabra in self.tiposDatos:
                    tipo = self.tiposDatos[palabra]
                    i += 1

                    if i < len(palabras):
                        nombre = palabras[i]
                        i += 1

                        if i < len(palabras) and palabras[i] == "=":
                            i += 1
                            valor = palabras[i]

                            variable_a_asignar = self.buscar(valor)
                            if variable_a_asignar:
                                valor = variable_a_asignar.valor
                            else:
                                print(f"Error: Variable '{valor}' no declarada.")
                                break

                            # Realizar el análisis de la expresión aritmética o concatenación
                            resultado, tipo_resultado = self.analizar_expresion(valor)
                            valor = resultado

                            # Verificar la coincidencia de tipos
                            if tipo != tipo_resultado:
                                print(f"Error: Tipo de dato '{tipo}' no coincide con el valor '{resultado}'.")
                                break

                        else:
                            valor = None

                        variable = Variable(tipo, nombre, valor)

                        if self.pila:
                            if self.pila[-1] == '(' or self.pila[-1] == '{':
                                self.insertarFuncion(variable)
                            elif self.pila[-2] == '{' or self.pila[-1] == '{':
                                self.insertar_Estructura_Dentro_Funcion(variable)
                        else:
                            self.insertar(variable)

                        if valor is not None:
                            self.revisa_inicializacion_variables(palabra)

                    else:
                        print("Error: Falta el nombre de la variable después del tipo.")
                        break

                else:
                    """Revisa si es una llave de función o para poder llamar parámetros"""
                    if palabra in self.bloques.keys() or palabra in self.parentesis.keys():
                        if self.pila:
                            if self.pila[-1] == '{' and palabra == '{':
                                self.pila.append(palabra)
                            if len(self.pila) >= 2:
                                if palabra == '}' and self.pila[-2] == '}':
                                    self.estructura.clear()
                                    self.pila.pop()
                            elif palabra == '}':
                                self.funcion.clear()
                                self.pila.pop()
                            else:
                                self.pila.pop()
                        else:
                            self.pila.append(palabra)
                    else:
                        # Revisa si la palabra ya se encontraba entre las palabras sin reservar.
                        if not self.es_reservada(palabra) and not self.es_operador(palabra) and not self.esString(
                                palabra) and not self.esNumero(palabra) and not self.es_flotante(palabra):
                            if self.revisa_declaracion_variables(palabra):
                                i += 1
                                if i < len(palabras) and palabras[i] == "=":
                                    i += 1
                                    siguientePalabra = self.buscar(palabras[i])
                                    if siguientePalabra:
                                        valor = siguientePalabra.valor
                                    else:
                                        valor = palabras[i]
                                    variable.valor = valor
                                else:
                                    valor = None

                                variable_a_asignar = self.buscar(valor)
                                if variable_a_asignar:
                                    valor = variable_a_asignar.valor
                                elif variable_a_asignar is None and not isinstance(valor, int):
                                    print(f"Error: Variable '{valor}' no declarada.")
                                    break

                                # Realizar el análisis de la expresión aritmética o concatenación
                                resultado, tipo_resultado = self.analizar_expresion(valor)
                                valor = resultado

                                # Verificar la coincidencia de tipos
                                if tipo != tipo_resultado:
                                    print(f"Error: Tipo de dato '{tipo}' no coincide con el valor '{resultado}'.")
                                    break

                            else:
                                valor = None

                            if valor is not None:
                                self.revisa_inicializacion_variables(palabra)

                i += 1

    def analizar_expresion(self, expresion):
        """
        Analiza la expresión aritmética o de concatenación y devuelve el resultado y el tipo.
        """
        try:
            # Utiliza la biblioteca 'ast' para evaluar la expresión
            nodo = ast.parse(expresion, mode='eval')
            resultado = eval(compile(nodo, '<string>', 'eval'))

            # Determina el tipo del resultado
            tipo_resultado = None
            if isinstance(resultado, int):
                tipo_resultado = 'int'
            elif isinstance(resultado, float):
                tipo_resultado = 'float'
            elif isinstance(resultado, str):
                tipo_resultado = 'string'

            return resultado, tipo_resultado

        except (SyntaxError, TypeError, NameError) as e:
            print(f"Error: No se puede evaluar la expresión '{expresion}': {e}")
            return None, None


    def buscar_variable_en_tabla_simbolos(self, nombre_variable):
        """Busca una variable por nombre en la tabla de simbolos creada"""
        variable = self.buscar(nombre_variable)
        if variable:
            print(f"Información de la variable '{nombre_variable}':")
            print(f"Tipo: {variable.tipo}")
            print(f"Valor: {variable.valor}")
        else:
            print(f"La variable '{nombre_variable}' no se encontró en la tabla de símbolos.")