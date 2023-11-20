import ast
import Variable


class TablaSimbolos:
    """Un diccionario que almacena los nombres de las variables como key utilizando una funcion hash."""

    def __init__(self):
        self.tiposDatos = {'void': "void", 'int': "int", 'float': "float", 'string': "string"}
        self.reservada = {'if': "if", 'while': "while", 'return': "return"}
        self.matematicos = {'+': "+", '-': "-", '*': "*", '/': "/", '=': "="}
        self.comparacion = {'==': "==", '!=': "!=", '<': "<", '>': ">"}
        self.parentesis = {'(': "(", ')': ")"}
        self.bloques = {'{': "{", '}': "}"}
        self.ignorar = {';': ";", ',': ","}
        self.table = {}
        self.funcion = {}
        self.estructura = {}
        self.pila = []

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

    def insertar(self, variable):
        """
        Inserta el objeto variable a la tabla de simbolos usando una funcion hash.
        Recibe como argumento un objeto Variable.
        Retorna True si logro insertar y False en caso de que ya este declarada.
        """
        hash_value = hash(variable.nombre)
        # Lanza error si ya se inserto la variable
        if hash_value not in self.table:
            self.table[hash_value] = variable
            return True
        else:
            return False

    # NUEVA
    def insertarFuncion(self, variable):
        """Inserta el objeto variable a la tabla de funciones para tener control de su espacio permitido usando una funcion hash."""
        hash_value = hash(variable.nombre)
        self.funcion[hash_value] = variable

    # NUEVA
    def insertar_Estructura_Dentro_Funcion(self, variable):
        """Inserta el objeto variable a una tabla para limitar su uso dentro del programa en caso de que este dentro de una funcion usando una funcion hash."""
        hash_value = hash(variable.nombre)
        self.estructura[hash_value] = variable

    def buscar(self, nombre):
        """
        Busca un objeto utilizando su nombre como key.
        Recibe como argumento un string nombre que se utiliza como key.
        Retorna un objeto Variable
        """
        hash_value = hash(nombre)
        variable = self.table.get(hash_value, None)
        return variable

    def modificar(self, nombre, nuevo_valor):
        """
        Modifica el valor de una variable en la tabla de símbolos, para eso utiliza la funcion buscar.
        Recibe como argumento un string nombre que se utiliza como key y el nuevo valor para modificar.
        Retorna True en caso de que se haga la modificacion y False en caso contrario.
        """
        variable = self.buscar(nombre)
        if variable:
            if variable.tipo == "int" and isinstance(int(nuevo_valor), int):
                variable.valor = nuevo_valor
            elif variable.tipo == "float" and isinstance(float(nuevo_valor), float):
                variable.valor = nuevo_valor
            elif variable.tipo == "string" and isinstance(str(nuevo_valor), str):
                variable.valor = nuevo_valor
            return True
        else:
            return False

    def validar_declaracion(self, nombre):
        """
        Revisa la tabla de símbolos buscando una variable.
        Recibe como argumento un string nombre que se utiliza como key.
        Retorna True en caso de que la encunetre y False en caso contrario.
        """
        variable = self.buscar(nombre)
        if variable:
            return True
        else:
            return False

    def obtener_valor(self, nombre):
        """
        Obtiene el valor de una variable en la tabla de símbolos.
        Recibe como argumento un string nombre que se utiliza como key.
        Retorna el valor de la variable y None en caso contrario.
        """
        variable = self.buscar(nombre)
        if variable:
            return variable.valor
        else:
            print(f"Error: La variable '{variable}' no está declarada.")

    def obtener_tipo(self, nombre):
        """
        Obtiene el tipo de una variable en la tabla de símbolos.
        Recibe como argumento un string nombre que se utiliza como key.
        Retorna el tipo de la variable y None en caso contrario.
        """
        variable = self.buscar(nombre)
        if variable:
            return variable.tipo

    def eliminar(self, nombre):
        """Elimina un objeto utilizando su nombre como key."""
        hash_value = hash(nombre)
        if hash_value in self.table:
            del self.table[hash_value]

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
                # Revisa si la palabra es un tipo de dato.
                if palabra in self.tiposDatos:
                    tipo = self.tiposDatos[palabra]
                    i += 1
                    # Revisa en la proxima posicion para asignar el nombre de la variable.
                    if i < len(palabras):
                        nombre = palabras[i]
                        i += 1
                        # Revisa si es una declaracion para asignar el valor.
                        if i < len(palabras) and palabras[i] == "=":
                            i += 1
                            valor = palabras[i]
                        else:
                            valor = None
                        # Inserta la variable en la tabla de simbolos.
                        variable = Variable.Variable(tipo, nombre, valor)

                        if variable.valor == None:
                            self.insertar(variable)
                            self.procesar_variables(variable)
                        elif variable.tipo == "int" and isinstance(int(variable.valor), int):
                            self.insertar(variable)
                            self.procesar_variables(variable)
                        elif variable.tipo == "float" and isinstance(float(variable.valor), float):
                            self.insertar(variable)
                            self.procesar_variables(variable)
                        elif variable.tipo == "string" and isinstance(str(variable.valor), str):
                            self.insertar(variable)
                            self.procesar_variables(variable)
                    else:
                        # Error de sintaxis.
                        print("Error: Falta el nombre de la variable después del tipo.")
                        break
                else:
                    variable = self.buscar(palabra)
                    i += 1
                    if variable is not None:
                        if i < len(palabras) and palabras[i] == "=":
                            i += 1
                            siguientePalabra = self.buscar(palabras[i])
                            if siguientePalabra:
                                valor = siguientePalabra.valor
                            else:
                                # Verifica si hay una expresión matemática después del "="
                                # expresion_matematica = []
                                # while i < len(palabras) - 1 and palabras[i] in self.matematicos:
                                #    expresion_matematica.append(palabras[i])
                                #    i += 1
                                # valor = self.analizar_expresion(expresion_matematica)
                                valor = palabras[i]
                            self.modificar(palabra, valor)
                        else:
                            valor = None

    def encontrar_errores(self, lista):
        """
        Procesa las listas de palabras de cada una de las lineas leidas del archivo y
        determina si hay errores.
        Recibe como argumento la lista de palabras.
        """
        for palabras in lista:
            i = 0
            while i < len(palabras):
                palabra = palabras[i]

                if i < len(palabras):
                    nombre = palabras[i]
                    i += 1

                    if i < len(
                            palabras) and nombre not in self.tiposDatos and nombre not in self.matematicos and nombre not in self.reservada and nombre not in self.comparacion and nombre not in self.parentesis and nombre not in self.bloques and nombre not in self.ignorar:

                        # revisar si la variable esta declarada
                        if not self.validar_declaracion(nombre) and not self.es_flotante(nombre) and not self.esNumero(
                                nombre):
                            print(f"Error: Variable '{nombre}' no declarada.")

                        # Revisar tipos de datos

                    # Revisa si es una llave de función o para poder llamar parámetros
                    elif palabra in self.bloques.keys() or palabra in self.parentesis.keys():
                        if self.pila:
                            if (self.pila[-1] == '{' and palabra == '{') or (self.pila[-1] == '{' and palabra == '('):
                                self.pila.append(palabra)
                            elif len(self.pila) >= 2:
                                if palabra == '}' and self.pila[-2] == '}':
                                    self.eliminar_elementos(self.table, self.estructura)
                                    self.estructura.clear()
                                    self.pila.pop()
                                elif palabra == '}':
                                    self.eliminar_elementos(self.table, self.funcion)
                                    self.funcion.clear()
                                    self.pila.pop()
                                else:
                                    self.pila.pop()
                            else:
                                self.pila.pop()
                        else:
                            self.pila.append(palabra)
        self.finalizar_programa(self.pila)

    def analizar_expresion(self, expresion):
        """
        Analiza la expresión aritmética o de concatenación y devuelve el resultado y el tipo.
        """
        stack_numeros = []
        stack_operadores = []

        for caracter in expresion:
            if caracter.isdigit() or (caracter[0] == '-' and caracter[1:].isdigit()):
                stack_numeros.append(float(caracter))
            elif caracter in self.matematicos:
                stack_operadores.append(caracter)
            elif not self.buscar(caracter):
                print(f"No existe el caracter")
            else:
                stack_operadores.append(self.obtener_valor(caracter))

            while len(stack_operadores) > 0 and len(stack_numeros) >= 2:
                operador = stack_operadores.pop()
                num2 = stack_numeros.pop()
                num1 = stack_numeros.pop()

                if operador == '+':
                    resultado = num1 + num2
                elif operador == '-':
                    resultado = num1 - num2
                elif operador == '*':
                    resultado = num1 * num2
                elif operador == '/':
                    resultado = num1 / num2 if num2 != 0 else float('inf')

                stack_numeros.append(resultado)

        if len(stack_numeros) == 1 and len(stack_operadores) == 0:
            return stack_numeros[0]
        else:
            print(f"Expresión mal formada")

    def imprimir(self, nombre_variable):
        """
        Busca una variable por nombre en la tabla de simbolos creada.
        Recibe como argumento un string nombre_variable.
        """
        print(f"Valor: {self.obtener_valor(nombre_variable)}")

    def procesar_variables(self, variable):
        if self.pila:
            if self.pila[-1] == '(' or self.pila[-1] == '{':
                self.insertarFuncion(variable)
            elif self.pila[-2] == '{' or self.pila[-1] == '{':
                self.insertar_Estructura_Dentro_Funcion(variable)

    @staticmethod
    def eliminar_elementos(A, B):
        for clave_B, valor_B in B.items():
            if clave_B in A and A[clave_B] == valor_B:
                del A[clave_B]

    @staticmethod
    def finalizar_programa(pila):
        contador_llaves = 0

        for elemento in pila:
            if elemento == '{':
                contador_llaves += 1
            elif elemento == '}':
                contador_llaves -= 1

        # Verifica si hay desequilibrio en la cantidad de llaves abiertas y cerradas
        if contador_llaves > 0:
            print(f"Error: Faltan {contador_llaves} llaves de cerradura '}}'")
        elif contador_llaves < 0:
            print(f"Error: Hay {abs(contador_llaves)} llaves de cerradura '}}' de más")